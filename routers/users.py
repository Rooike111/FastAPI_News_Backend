from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from crud import users
from config.db_config import get_db
from models.users import User
from schemas.users import UserRequest, UserAuthResponse, UserInforBase, UserInfoResponse, UserUpdateRequest, \
    UserChangePasswordRequest
from utils.response import success_response
from utils.auth import get_current_user
router = APIRouter(prefix="/api/user", tags=["user"])

@router.post("/register")
async def register(user_data:UserRequest,db:AsyncSession = Depends(get_db)):
    existing_user = await users.get_user_by_username(db,user_data.username)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="用户已经存在")
    user = await users.create_user(db,user_data)
    token = await users.create_token(db,user_id=user.id)
    response_data = UserAuthResponse(token=token,userInfo=UserInfoResponse.model_validate(user))
    return success_response(message="注册成功",data=response_data)

@router.post("/login")
async def login(user_data:UserRequest,db:AsyncSession = Depends(get_db)):
    # 验证用户是否存在:-> 验证密码 ->生成Token-> 响应结果
    user = await users.authenticate_user(db,user_data.username,user_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="用户名或密码错误")
    token = await users.create_token(db,user_id=user.id)
    response_data = UserAuthResponse(token=token,userInfo=UserInfoResponse.model_validate(user))
    return success_response(message="登录成功了",data=response_data)


#查Token查用户->封装crud -> 功能整合成一个工具函数 ->路由导入使用:采用依赖注入
@router.get("/info")
async def get_user_info(user: User = Depends(get_current_user)):
    return success_response(message="获取用户信息成功",data=UserInfoResponse.model_validate(user))

# 更新用户信息
@router.put("/update")
async def update_user_info(
        user_data: UserUpdateRequest,
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="用户未登录")
    updated_user = await users.update_user(db,user.username,user_data)
    return success_response(message="修改用户信息成功",data=UserInfoResponse.model_validate(updated_user))

@router.put("/password")
async def update_password(
        password_data: UserChangePasswordRequest,
        user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="用户登录已过期")
    res_change_pwd = await users.update_password(db,user,password_data.old_password,password_data.new_password)
    if not res_change_pwd:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="修改密码失败 请稍后再试")
    return success_response(message="修改密码成功")