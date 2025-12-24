from enum import Enum
from random import random

from fastapi import HTTPException

from app.models.captcha import Captcha
from app.schemas.response import ErrorResponse
from app.utils.captcha_image import generate_captcha_image
from datetime import datetime, timedelta

from sqlmodel import Session, select

from app.crud.database import engine

session = Session(engine)


async def generate_captcha():
    # 生成随机Id字符串
    captcha_key = str(random()).replace('.', '')
    images_base64 = generate_captcha_image()
    save_captcha(captcha_key, images_base64["image"], images_base64["code"])
    return {"captcha_key": captcha_key, "images_base64": images_base64["image"]}


# 将验证码插入数据表
def save_captcha(captcha_key, code, result):
    """这里把 uuid、验证码文本、过期时间落库"""
    try:
        # 判断是否存在重复的captcha_key
        captcha = session.query(Captcha).where(Captcha.captcha_key == captcha_key).first()
        if captcha:
            session.delete(captcha)
            session.commit()
            # 生成新的验证码
        new_captcha = Captcha(captcha_key=captcha_key,
                              captcha_base64=code,
                              captcha_value=result,
                              expire_time=datetime.now() + timedelta(minutes=5),
                              create_time=datetime.now())
        session.add(new_captcha)
        session.commit()
        return new_captcha
    except Exception as e:
        print("SQL ERROR: ", e)
        return None
    finally:
        session.close()


# 验证验证码
class CaptchaStatus(int, Enum):
    OK = 0
    EXPIRED = 1
    INVALID = 2
    ERROR = 3


async def verify_captcha(captcha_key, captcha_value):
    try:
        # 查询数据库中是否存在该验证码
        captcha = session.query(Captcha).where(Captcha.captcha_key == captcha_key).first()
        if captcha:
            # 判断验证码是否正确
            if captcha.captcha_value == captcha_value and captcha.expire_time > datetime.now():
                # 验证码正确，删除验证码
                session.delete(captcha)
                session.commit()
                return CaptchaStatus.OK
            elif captcha.captcha_value == captcha_value and captcha.expire_time < datetime.now():
                # 验证码已过期，删除验证码
                session.delete(captcha)
                session.commit()
                return CaptchaStatus.EXPIRED
            else:
                # 验证码错误，删除验证码
                session.delete(captcha)
                session.commit()
                return CaptchaStatus.INVALID
        else:
            return CaptchaStatus.ERROR
    except Exception as e:
        print("verify_captcha() SQL ERROR: ", e)
        return CaptchaStatus.ERROR
    finally:
        session.close()
