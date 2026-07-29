from datetime import datetime

from fastapi import APIRouter, BackgroundTasks, Body, Depends, HTTPException, Query

from app.crud.permission import get_user_perm_codes
from app.crud.role import get_role_by_code, get_user_roles_codes
from app.crud.user import (
    PasswordStatus,
    SendStatus,
    create_user,
    delete_users,
    get_code_by_email,
    get_user_by_id,
    get_user_by_username,
    get_users_page,
    reset_password,
    send_email_code,
    update_user_info,
    update_user_password,
)
from app.crud.user_role import get_user_role_ids
from app.dependencies import get_current_user, require_admin
from app.middleware.background_tasks import clean_email_code
from app.schemas.response import PageData, PaginationResponse, SuccessResponse
from app.schemas.user import EmailUpdate, PasswordUpdate, QueryUserPage, UserCreate, UserUpdate
from app.utils.str_to_list import str_to_int_list
from app.utils.verification import check_email

router = APIRouter()


@router.get("/me", response_model=SuccessResponse, summary="当前登录用户")
async def get_me(current_user=Depends(get_current_user)):
    return SuccessResponse(
        data={
            "userId": current_user.id,
            "username": current_user.username,
            "nickname": current_user.nickname,
            "avatar": current_user.avatar,
            "email": current_user.email,
            "roles": await get_user_roles_codes(current_user.id),
            "perms": await get_user_perm_codes(current_user.id),
        }
    )


@router.get("/profile", response_model=SuccessResponse, summary="个人资料")
async def get_profile(current_user=Depends(get_current_user)):
    role_codes = await get_user_roles_codes(current_user.id)
    role = await get_role_by_code(role_codes[0]) if role_codes else None
    return SuccessResponse(
        data={
            "id": current_user.id,
            "username": current_user.username,
            "nickname": current_user.nickname,
            "avatar": current_user.avatar,
            "gender": current_user.gender,
            "mobile": current_user.mobile,
            "email": current_user.email,
            "roleNames": (role.description or role.name) if role else "",
            "createTime": current_user.created_at,
        }
    )


@router.put("/profile", response_model=SuccessResponse, summary="更新个人资料")
async def update_profile(data: UserUpdate, current_user=Depends(get_current_user)):
    data.id = current_user.id
    if not await update_user_info(data):
        raise HTTPException(status_code=500, detail="更新个人资料失败")
    return SuccessResponse()


@router.put("/password", response_model=SuccessResponse, summary="修改个人密码")
async def change_password(data: PasswordUpdate, current_user=Depends(get_current_user)):
    status = await update_user_password(data, current_user.id)
    messages = {
        PasswordStatus.oldPasswordError: "原密码错误",
        PasswordStatus.newPasswordError: "新密码不能为空",
        PasswordStatus.samePasswordError: "新密码不能与原密码相同",
    }
    if status != PasswordStatus.success:
        raise HTTPException(status_code=400, detail=messages.get(status, "密码修改失败"))
    return SuccessResponse()


@router.post("/email/code", response_model=SuccessResponse, summary="发送邮箱验证码")
async def email_code(email: str, background_tasks: BackgroundTasks, current_user=Depends(get_current_user)):
    if not check_email(email):
        raise HTTPException(status_code=422, detail="邮箱格式不正确")
    background_tasks.add_task(clean_email_code)
    result = await send_email_code(email, current_user.id)
    if result == SendStatus.exist:
        raise HTTPException(status_code=409, detail="验证码仍在有效期内")
    if result != SendStatus.success:
        raise HTTPException(status_code=500, detail="发送验证码失败")
    return SuccessResponse()


@router.put("/email", response_model=SuccessResponse, summary="绑定邮箱")
async def bind_email(data: EmailUpdate, current_user=Depends(get_current_user)):
    record = get_code_by_email(data.email)
    if not record or record.user_id != current_user.id:
        raise HTTPException(status_code=400, detail="验证码无效")
    if record.code != data.code or record.expire_time < datetime.now():
        raise HTTPException(status_code=400, detail="验证码错误或已过期")
    if not await update_user_info(UserUpdate(id=current_user.id, email=data.email)):
        raise HTTPException(status_code=500, detail="邮箱更新失败")
    return SuccessResponse()


@router.get("/page", response_model=PaginationResponse, summary="用户分页")
async def list_users(query: QueryUserPage = Query(...), current_user=Depends(require_admin)):
    if query.pageNum < 1 or not 1 <= query.pageSize <= 100:
        raise HTTPException(status_code=422, detail="分页参数无效")
    total, users = await get_users_page(query)
    return PaginationResponse(data=PageData(total=total, list=users))


@router.post("", response_model=SuccessResponse, summary="新增用户")
async def add_user(data: UserCreate, current_user=Depends(require_admin)):
    user = await create_user(data)
    if not user:
        raise HTTPException(status_code=409, detail="用户名已存在")
    return SuccessResponse(data=user)


@router.get("/userinfo/{username}", response_model=SuccessResponse, summary="用户信息")
async def user_by_name(username: str, current_user=Depends(require_admin)):
    user = get_user_by_username(username)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return SuccessResponse(data={"id": user.id, "username": user.username, "email": user.email})


@router.get("/{user_id}/form", response_model=SuccessResponse, summary="用户详情")
async def user_form(user_id: int, current_user=Depends(require_admin)):
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return SuccessResponse(
        data={
            "id": user.id,
            "username": user.username,
            "nickname": user.nickname,
            "avatar": user.avatar,
            "gender": user.gender,
            "mobile": user.mobile,
            "email": user.email,
            "status": user.status,
            "roleIds": await get_user_role_ids(user_id),
        }
    )


@router.put("/{user_id}", response_model=SuccessResponse, summary="更新用户")
async def edit_user(user_id: int, data: UserUpdate, current_user=Depends(require_admin)):
    data.id = user_id
    if not await update_user_info(data):
        raise HTTPException(status_code=404, detail="用户不存在")
    return SuccessResponse()


@router.put("/{user_id}/password/reset", response_model=SuccessResponse, summary="重置用户密码")
async def reset_user_password(user_id: int, password: str, current_user=Depends(require_admin)):
    if not await reset_password(user_id, password):
        raise HTTPException(status_code=400, detail="重置密码失败")
    return SuccessResponse()


@router.delete("/{user_ids}", response_model=SuccessResponse, summary="删除用户")
async def remove_users(user_ids: str, current_user=Depends(require_admin)):
    if not await delete_users(str_to_int_list(user_ids)):
        raise HTTPException(status_code=409, detail="系统管理员不能删除")
    return SuccessResponse()
