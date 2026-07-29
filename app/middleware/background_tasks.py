from datetime import datetime

from sqlmodel import Session, delete

from app.crud.database import engine
from app.middleware.logger_config import log_info
from app.models.captcha import Captcha
from app.models.user import Email


async def clean_captcha():
    with Session(engine) as session:
        session.exec(delete(Captcha).where(Captcha.expire_time < datetime.now()))
        session.commit()
    await log_info("Expired captchas cleaned")


async def clean_email_code():
    with Session(engine) as session:
        session.exec(delete(Email).where(Email.expire_time < datetime.now()))
        session.commit()
    await log_info("Expired email codes cleaned")
