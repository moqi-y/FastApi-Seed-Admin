from fastapi import APIRouter, BackgroundTasks, Depends, Form, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.core.config import get_settings
from app.crud.generate_captcha import CaptchaStatus, generate_captcha, verify_captcha
from app.crud.user import authenticate_user, create_user, get_user_by_username
from app.dependencies import create_token_response
from app.middleware.background_tasks import clean_captcha
from app.schemas.response import SuccessResponse
from app.schemas.user import Token, UserCreate

router = APIRouter()


@router.post("/register", response_model=SuccessResponse, summary="注册用户")
async def register(data: UserCreate):
    if get_user_by_username(data.username):
        raise HTTPException(status_code=409, detail="用户名已存在")
    user = await create_user(data)
    if not user:
        raise HTTPException(status_code=500, detail="用户创建失败")
    return SuccessResponse(data={"id": user.id, "username": user.username})


@router.post("/login", response_model=SuccessResponse, summary="用户登录")
async def login(
    username: str = Form(...),
    password: str = Form(...),
    captchaKey: str | None = Form(None),
    captchaCode: str | None = Form(None),
):
    settings = get_settings()
    if settings.use_captcha:
        status = await verify_captcha(captchaKey or "", (captchaCode or "").lower())
        if status != CaptchaStatus.OK:
            raise HTTPException(status_code=400, detail="验证码错误或已过期")
    user = authenticate_user(username, password)
    if not user:
        raise HTTPException(status_code=401, detail="用户名、密码错误或账号已停用")
    token = create_token_response(user.username)
    return SuccessResponse(
        data={
            "tokenType": token["token_type"],
            "accessToken": token["access_token"],
            "expiresIn": get_settings().jwt_expire_minutes * 60,
        }
    )


@router.post("/login/swagger", response_model=Token, include_in_schema=False)
async def swagger_login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    return create_token_response(user.username)


@router.delete("/logout", response_model=SuccessResponse, summary="退出登录")
async def logout():
    return SuccessResponse(data={})


@router.get("/captcha", response_model=SuccessResponse, summary="获取验证码")
async def captcha(background_tasks: BackgroundTasks):
    background_tasks.add_task(clean_captcha)
    result = await generate_captcha()
    return SuccessResponse(
        data={
            "captchaKey": result["captcha_key"],
            "captchaBase64": result["images_base64"],
            "isShow": get_settings().use_captcha,
        }
    )
