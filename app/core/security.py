from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
import os

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
# 设置JWT的算法
ALGORITHM = "HS256"
# 设置访问令牌的默认缺省过期时间为30分钟
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def verify_password(plain_pwd, hashed_pwd):
    # 验证明文密码和哈希密码是否匹配
    return pwd_context.verify(plain_pwd, hashed_pwd)


# 定义一个函数，用于对密码进行哈希处理
def hash_password(password):
    # 使用pwd_context.hash()方法对密码进行哈希处理
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta = None):
    # 复制传入的字典
    to_encode = data.copy()
    # 获取当前时间,如果expires_delta过期时间为None或未定义，则使用默认的30分钟。
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    # 将过期时间添加到字典中
    to_encode.update({"exp": expire})
    # 使用jwt库对字典进行编码，并返回结果
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
