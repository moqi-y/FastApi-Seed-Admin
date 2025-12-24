from datetime import datetime, timedelta

from sqlmodel import SQLModel, Field

"""验证码表"""


class Captcha(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    captcha_key: str = Field(index=True)
    captcha_base64: str = Field()
    captcha_value: str = Field()
    expire_time: datetime = Field(default=datetime.now() + timedelta(minutes=5))  # 验证码过期时间, 默认5分钟
    create_time: datetime = Field(default=datetime.now())