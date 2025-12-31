from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends, Body, BackgroundTasks, Query
from app.crud.permission import get_user_perm_codes
from app.crud.role import get_user_roles_codes, get_role_by_code
from app.crud.user import get_user_by_username, update_user_info, get_user_by_id, update_user_password, PasswordStatus, \
    send_email_code, SendStatus, get_code_by_email, get_users_page, delete_users, create_user
from app.dependencies import get_current_user
from app.middleware.background_tasks import clean_email_code
from app.schemas.response import SuccessResponse, PaginationResponse, PageData
from app.schemas.user import UserIn, UserUpdate, PasswordUpdate, EmailUpdate, QueryUserPage, UserCreate
from app.utils.str_to_list import str_to_int_list
from app.utils.verification import check_email

router = APIRouter()


# 获取用户信息
@router.get("/me", summary="获取当前用户信息")
async def get_me(current_user=Depends(get_current_user)):
    roles = await get_user_roles_codes(current_user.id)
    perms = await get_user_perm_codes(current_user.id)
    user = {
        "userId": current_user.id,
        "username": current_user.username,
        "nickname": current_user.nickname,
        "avatar": current_user.avatar,
        "email": current_user.email,
        "created_at": current_user.created_at,
        "roles": roles,  # 用户角色,例如：["admin", "user"]
        "perms": perms  # 用户权限,例如：["user:add", "user:delete"]
    }
    return SuccessResponse(code="00000", data=user)


# 通过用户名查询用户信息
@router.get("/userinfo/{username}", response_model=SuccessResponse, summary="通过用户名查询用户信息")
async def get_user(username: str):
    user = get_user_by_username(username)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return SuccessResponse(data={
        "user_id": user.user_id,
        "username": user.username,
        "email": user.email
    })


# 通过用户id查询用户信息
@router.get("/userinfo", response_model=SuccessResponse, summary="通过用户id查询用户信息")
async def root(user_id: int):
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return SuccessResponse(data={
        "user_id": user.user_id,
        "username": user.username,
        "email": user.email
    })


# 更新用户信息
@router.put("/userinfo", response_model=SuccessResponse, summary="更新用户全部信息")
async def update_user(user_id: int, user: UserIn):
    user = update_user_info(user_id, user.username, user.password, user.email)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return SuccessResponse(data={
        "user_id": user.user_id,
        "username": user.username,
        "email": user.email
    })


# 获取个人中心用户信息
@router.get("/profile", response_model=SuccessResponse, summary="获取个人中心用户信息")
async def root(current_user=Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=401, detail="未授权访问")
    roles = await get_user_roles_codes(current_user.user_id)
    role_info = await get_role_by_code(roles[0])
    perms = await get_user_perm_codes(current_user.user_id)
    return SuccessResponse(data={
        "id": current_user.user_id,
        "username": current_user.username,
        "nickname": current_user.nickname,
        "avatar": current_user.avatar,
        "gender": 1,
        "mobile": "",
        "email": current_user.email,
        "deptName": "管理中心",
        "roleNames": role_info.role_desc or role_info.role_name,
        "createTime": current_user.created_at
    })


# 个人中心修改用户信息
@router.put("/profile", summary="个人中心修改用户信息")
async def root(user: UserUpdate = Body(...), current_user=Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=401, detail="未授权访问")
    user.id = current_user.user_id
    new_user = UserUpdate(**user.dict())
    result = await update_user_info(new_user)
    if not result:
        raise HTTPException(status_code=500, detail="修改失败")
    return SuccessResponse()


# 修改密码
@router.put("/password", summary="修改密码")
async def root(password: PasswordUpdate = Body(...), current_user=Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=401, detail="未授权访问")
    result = await update_user_password(password, current_user.user_id)
    if not result:
        raise HTTPException(status_code=500, detail="修改失败")
    elif result == PasswordStatus.success:
        return SuccessResponse()
    elif result == PasswordStatus.samePasswordError:
        raise HTTPException(status_code=500, detail="新密码不能与旧密码相同")
    elif result == PasswordStatus.oldPasswordError:
        raise HTTPException(status_code=500, detail="旧密码错误")
    elif result == PasswordStatus.newPasswordError:
        raise HTTPException(status_code=500, detail="新密码格式错误")
    else:
        raise HTTPException(status_code=500, detail="修改失败")


# 发送邮箱验证码（绑定或更换邮箱）
@router.post("/email/code", summary="发送邮箱验证码（绑定或更换邮箱）")
async def root(email: str, background_tasks: BackgroundTasks, current_user=Depends(get_current_user)):
    background_tasks.add_task(clean_email_code)
    if not current_user:
        raise HTTPException(status_code=401, detail="未授权访问")
    if not check_email(email):
        raise HTTPException(status_code=400, detail="邮箱格式错误")
    if current_user.email == email:
        raise HTTPException(status_code=400, detail="邮箱已绑定")
    result = await send_email_code(email, current_user.user_id)
    if result == SendStatus.exist:
        raise HTTPException(status_code=400, detail="邮箱已存在")
    elif result == SendStatus.error:
        raise HTTPException(status_code=500, detail="发送失败")
    elif result == SendStatus.success:
        return SuccessResponse()
    else:
        raise HTTPException(status_code=500, detail="发送失败")


# 绑定或更换邮箱
@router.put("/email", summary="绑定或更换邮箱")
async def root(email: EmailUpdate = Body(...), current_user=Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=401, detail="未授权访问")
    if not check_email(email.email):
        raise HTTPException(status_code=400, detail="邮箱格式错误")
    if not email.code:
        raise HTTPException(status_code=400, detail="验证码不能为空")
    email_res = get_code_by_email(email.email)
    if not email_res:
        raise HTTPException(status_code=500, detail="修改失败")
    if email_res.code != email.code:
        raise HTTPException(status_code=400, detail="验证码错误")
    if email_res.expire_time < datetime.now():
        raise HTTPException(status_code=400, detail="验证码已过期")
    info = UserUpdate(id=current_user.user_id, email=email.email)
    result = await update_user_info(info)
    if not result:
        raise HTTPException(status_code=500, detail="修改失败")
    else:
        return SuccessResponse()


# 获取用户分页列表
@router.get("/page", summary="获取用户分页列表")
async def root(queryUser: QueryUserPage = Query(...), current_user=Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=401, detail="未授权访问")
    if queryUser.pageSize < 1:
        raise HTTPException(status_code=400, detail="页码不能小于1")
    if queryUser.pageNum < 1:
        raise HTTPException(status_code=400, detail="每页数量不能小于1")
    result = await get_users_page(queryUser)
    if not result:
        raise HTTPException(status_code=500, detail="获取失败")
    else:
        return PaginationResponse(data=PageData(
            total=result[0],
            list=result[1]
        ))


# 新增用户
@router.post("", summary="新增用户")
async def root(user: UserCreate, current_user=Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=401, detail="未授权访问")
    result = await create_user(user)
    if not result:
        raise HTTPException(status_code=500, detail="新增失败")
    else:
        return SuccessResponse()


# 删除用户
@router.delete("/{user_id}", summary="删除用户", description="用户ID列表，逗号分隔，如 1 或 2,3,4")
async def root(user_id: str, current_user=Depends(get_current_user)):
    user_id_list = str_to_int_list(user_id)
    if not current_user:
        raise HTTPException(status_code=401, detail="未授权访问")
    result = await delete_users(user_id_list)
    if not result:
        raise HTTPException(status_code=500, detail="删除失败")
    else:
        return SuccessResponse()
