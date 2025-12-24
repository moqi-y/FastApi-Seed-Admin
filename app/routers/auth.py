from fastapi import APIRouter, HTTPException, Depends, Body
from fastapi.security import OAuth2PasswordRequestForm
from app.core.security import hash_password
from app.crud.role_perms import list_role_permissions
from app.crud.user import authenticate_user, get_user_by_username, create_user
from app.crud.user_role import get_user_roles
from app.dependencies import create_token_response, get_current_user
from app.crud.generate_captcha import generate_captcha, verify_captcha, CaptchaStatus
from app.schemas.response import SuccessResponse, ErrorResponse
from app.schemas.user import UserOut, UserCreate, Token

router = APIRouter()


@router.post("/register", response_model=SuccessResponse, summary="注册新用户")
def register(user: UserCreate):
    if get_user_by_username(user.username):
        raise HTTPException(status_code=400, detail="用户名已存在")
    user_obj = create_user(user.username, user.nickname, user.avatar, hash_password(user.password), user.email)
    if user_obj is None:
        raise HTTPException(status_code=500, detail="用户创建失败")
    return SuccessResponse(data={
        "userId": user_obj.user_id,
        "username": user_obj.username,
        "email": user_obj.email,
        "created_at": user_obj.created_at
    })


@router.post("/login", summary="用户登录", response_model=SuccessResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), captchaKey: str = Body(..., embed=True),
                captchaCode: str = Body(..., embed=True)):
    # 验证验证码
    result = await verify_captcha(captchaKey, captchaCode.lower())
    if result == CaptchaStatus.EXPIRED:
        raise HTTPException(status_code=408, detail="验证码已过期")
    elif result == CaptchaStatus.ERROR:
        raise HTTPException(status_code=422, detail="验证码错误")
    elif result == CaptchaStatus.INVALID:
        raise HTTPException(status_code=400, detail="验证码无效")
    # 再验账号
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="用户名或密码错误")
    else:
        token_data = create_token_response(user.username)
        return SuccessResponse(code="00000", data={
            "tokenType": token_data["token_type"],
            "accessToken": token_data["access_token"]
        })


@router.post("/login/swagger", summary="用户登录（仅Swagger使用）", include_in_schema=False,
             response_model=Token)  # 不出现在Swagger文档中
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    return create_token_response(user.username)


@router.delete("/logout", summary="用户登录", response_model=SuccessResponse)
async def logout():
    return SuccessResponse(data={})


# 验证码
@router.get("/captcha", summary="验证码", response_model=SuccessResponse)
async def root():
    result = await generate_captcha()
    return SuccessResponse(data={
        "captchaKey": result["captcha_key"],
        "captchaBase64": result["images_base64"]
    })
