import time

from fastapi import BackgroundTasks
from sqlmodel import Session, select, delete
from app.crud.database import engine
from app.middleware.logger_config import log_info
from app.models.captcha import Captcha
from datetime import datetime

session = Session(engine)


async def clean_captcha():
    """
    清理过期的验证码
    """
    now_time = datetime.now()
    await log_info(message="⏳ Cleaning expired captchas...")
    expired_delete = delete(Captcha).where(Captcha.expire_time < now_time)
    session.exec(expired_delete)
    session.commit()
    await log_info(message="🎉 Cleaning expired captchas done!")
