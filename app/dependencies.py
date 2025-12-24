import os
from datetime import timedelta
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app.core.security import SECRET_KEY, ALGORITHM, create_access_token
from app.crud.user import get_user_by_username

# 定义一个OAuth2PasswordBearer对象，用于处理OAuth2.0密码模式的认证,用于在线文档的认证
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login/swagger")


# 定义一个异步函数get_current_user，用于获取当前用户
async def get_current_user(token: str = Depends(oauth2_scheme)):
    # 解码token
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # 获取payload中的用户名
        username = payload.get("sub")
        # 如果用户名为空，则抛出认证失败的异常
        if not username:
            raise HTTPException(status_code=401, detail="认证失败")
    # 如果解码失败，则抛出令牌无效的异常
    except JWTError:
        raise HTTPException(status_code=401, detail="令牌无效")
    # 根据用户名获取用户
    user = get_user_by_username(username=username)
    # 如果用户不存在，则抛出用户不存在的异常
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    # 返回用户
    return user


def create_token_response(username: str):
    # 设置access_token的过期时间,从环境变量中获取
    access_token_expires = timedelta(minutes=float(os.getenv("JWT_EXPIRE_MINUTES")))
    # 创建access_token，并设置过期时间为access_token_expires
    access_token = create_access_token(
        data={"sub": username}, expires_delta=access_token_expires
    )
    # 返回包含access_token和token_type的字典
    return {"access_token": access_token, "token_type": "bearer"}
