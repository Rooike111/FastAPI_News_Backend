import uuid
from datetime import datetime, timedelta

from fastapi import HTTPException
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from models.users import User, UserToken
from schemas.users import UserRequest, UserUpdateRequest
from utils import security
from utils.security import  get_hash_password

# 根据用户名查询数据库
async def get_user_by_username(db:AsyncSession, username:str):
    query = select(User).where(User.username == username)
    result = await db.execute(query)
    return result.scalar_one_or_none()


# 创建用户
async def create_user(db:AsyncSession, user_data:UserRequest):
    # 先进行密码加密处理
    hashed_password = get_hash_password(user_data.password)
    user_data = User(
        username=user_data.username,
        password=hashed_password,
    )
    db.add(user_data)
    await db.commit()
    await db.refresh(user_data)
    return user_data


# 生成Token
async def create_token(db:AsyncSession, user_id:int):
    # 生成Token+ 设置过期时间-> 查询数据库当前用户是否有Token -> 又:更新， 没有:添加
    token = str(uuid.uuid4())
    expires_at = datetime.now() + timedelta(days=7)
    query = select(UserToken).where(User.id == user_id)
    user_token = (await db.execute(query)).scalar_one_or_none()
    if user_token :
        user_token.token = token
        user_token.expires_at = expires_at
    else:
        user_token = UserToken(user_id=user_id, token=token, expires_at=expires_at)
        db.add(user_token)
        await db.commit()

    return token

async def authenticate_user(db:AsyncSession, username:str, password:str):
    user = await get_user_by_username(db, username)
    if not user:
        return None
    if not security.verify_password(password, user.password):
        return None
    return user

# 根据token查询用户
async def get_user_by_token(db:AsyncSession, token:str):
    query = select(UserToken).where(UserToken.token == token)
    result = await db.execute(query)
    db_user_token = result.scalar_one_or_none()

    if not db_user_token or db_user_token.expires_at < datetime.now():
        return None

    query = select(User).where(User.id == db_user_token.user_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()

# 更新用户信息
async def update_user(db:AsyncSession, username:str, user_data:UserUpdateRequest):
    query = update(User).where(User.username==username).values(**user_data.model_dump(
        exclude_unset=True,
        exclude_none=True,
    ))

    result = await db.execute(query)
    await db.commit()

    if result.rowcount == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="用户不存在")
    update_user = await get_user_by_username(db, username)
    return update_user

async def update_password(db:AsyncSession, user:User, old_password:str,new_password:str):
    if not security.verify_password(old_password, user.password):
        return False
    user.password=security.get_hash_password(new_password)
    # 由SQLAlchemy真正接管User 确保可以保存 commit
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return True
