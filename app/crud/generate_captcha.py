from datetime import datetime, timedelta
from enum import IntEnum
from secrets import token_urlsafe

from sqlmodel import Session, select

from app.crud.database import engine
from app.models.captcha import Captcha
from app.utils.captcha_image import generate_captcha_image


class CaptchaStatus(IntEnum):
    OK = 0
    EXPIRED = 1
    INVALID = 2
    ERROR = 3


async def generate_captcha():
    captcha_key = token_urlsafe(24)
    image = generate_captcha_image()
    with Session(engine) as session:
        session.add(
            Captcha(
                captcha_key=captcha_key,
                captcha_base64=image["image"],
                captcha_value=image["code"].lower(),
                expire_time=datetime.now() + timedelta(minutes=5),
            )
        )
        session.commit()
    return {"captcha_key": captcha_key, "images_base64": image["image"]}


async def verify_captcha(captcha_key: str, captcha_value: str) -> CaptchaStatus:
    with Session(engine) as session:
        captcha = session.exec(
            select(Captcha).where(Captcha.captcha_key == captcha_key)
        ).first()
        if not captcha:
            return CaptchaStatus.ERROR
        session.delete(captcha)
        session.commit()
        if captcha.expire_time < datetime.now():
            return CaptchaStatus.EXPIRED
        return CaptchaStatus.OK if captcha.captcha_value == captcha_value.lower() else CaptchaStatus.INVALID
