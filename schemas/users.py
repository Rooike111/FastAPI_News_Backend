from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class UserRequest(BaseModel):
    username: str
    password: str

class UserInforBase(BaseModel):
    """
    用户信息基础数据模型
    """
    nickname:Optional[str] = Field(None, max_length=50, description="昵称")
    avatar: Optional[str] = Field(None, max_length=255, description="头像url")
    gender: Optional[str] = Field(None, max_length=10, description="新别")
    bio: Optional[str] = Field(None, max_length=500, description="个人简介")


# user_info 对应的类 基础类 —+ Info类(id, 用户名)
class UserInfoResponse(UserInforBase):
    id:int
    username: str

    # 模型类配置
    model_config = ConfigDict(
        from_attributes=True  # 允许从ORM 对象属性取值
    )

#data 数据类型
class UserAuthResponse(BaseModel):
    token: str
    user_info: UserInfoResponse = Field(...,alias="userInfo")

    # 模型类配置
    model_config = ConfigDict(
        populate_by_name=True, # alia/字段名兼容
        from_attributes=True  # 允许从ORM 对象属性取值
    )

# 更新用户信息的模型类
class UserUpdateRequest(BaseModel):
    nickname: Optional[str] = Field(None, max_length=50, description="昵称")
    avatar: Optional[str] = Field(None, max_length=255, description="头像url")
    gender: Optional[str] = Field(None, max_length=10, description="新别")
    bio: Optional[str] = Field(None, max_length=500, description="个人简介")
    phone: Optional[str] = Field(None, max_length=20, description="手机号")

class UserChangePasswordRequest(BaseModel):
    old_password: str = Field(...,alias="oldPassword",description="旧密码")
    new_password: str = Field(...,alias="newPassword",description="新密码",min_length=6)