from fastapi import APIRouter, HTTPException, Depends, Body

from app.crud.permission import get_perm_by_id, get_user_perm_codes
from app.crud.role import get_role_by_id, get_user_roles_codes, get_role_by_code
from app.crud.role_perms import list_role_permissions
from app.crud.user import get_user_by_username, update_user_info, get_user_by_id, update_user_password, PasswordStatus
from app.crud.user_role import get_user_roles
from app.dependencies import get_current_user
from app.schemas.response import SuccessResponse
from app.schemas.user import UserOut, UserIn, UserUpdate, PasswordUpdate

router = APIRouter()


# 获取用户信息
@router.get("/me", summary="获取当前用户信息")
async def get_me(current_user=Depends(get_current_user)):
    roles = await get_user_roles_codes(current_user.user_id)
    perms = await get_user_perm_codes(current_user.user_id)
    user = {
        "userId": current_user.user_id,
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
        raise HTTPException(status_code=404, detail="用户不存在")
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
        raise HTTPException(status_code=404, detail="用户不存在")
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
        raise HTTPException(status_code=404, detail="用户不存在")
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
