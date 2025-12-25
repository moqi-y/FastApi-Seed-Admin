import time

from fastapi import BackgroundTasks
from sqlmodel import Session, select, delete
from app.crud.database import engine
from app.middleware.logger_config import log_info
from app.models.captcha import Captcha
from datetime import datetime

from app.models.user import Email

session = Session(engine)


async def clean_captcha():
    """
    清理过期的验证码
    """
    now_time = datetime.now()
    await log_info(message="⏳ Cleaning expired Captchas...")
    expired_delete = delete(Captcha).where(Captcha.expire_time < now_time)
    session.exec(expired_delete)
    session.commit()
    await log_info(message="🎉 Cleaning expired Captchas done!")


async def clean_email_code():
    """
    清理过期的邮箱验证码
    """
    now_time = datetime.now()
    await log_info(message="⏳ Cleaning expired Email Codes...")
    expired_delete = delete(Email).where(Email.expire_time < now_time)
    session.exec(expired_delete)
    session.commit()
    await log_info(message="🎉 Cleaning expired Email Codes done!")
