# utils/http_client.py
"""
httpx 客户端封装
 - 支持异步
 - 支持请求重试
 - 支持自定义 headers
 - 支持自定义请求参数
"""
from __future__ import annotations
import httpx
from typing import Any, Dict, Optional, Union
from fastapi import HTTPException
import asyncio


class Result:
    """轻量级 Result 包装，避免抛异常"""

    def __init__(self, ok: bool, status: int, data: Any = None, msg: str = ""):
        self.ok = ok
        self.status = status
        self.data = data
        self.msg = msg

    def __bool__(self):
        return self.ok


class HttpClient:
    """ httpx 客户端 """
    _client: Optional[httpx.AsyncClient] = None

    # ---------- 内部工具 ----------
    @classmethod
    def client(cls) -> httpx.AsyncClient:
        if cls._client is None:
            cls._client = httpx.AsyncClient(timeout=30.0)
        return cls._client

    @classmethod
    async def close(cls) -> None:
        if cls._client:
            await cls._client.aclose()
            cls._client = None

    @classmethod
    async def _safe_request(
            cls,
            method: str,
            url: str,
            *,
            params: Dict[str, Any] = None,
            json: Dict[str, Any] = None,
            data: Any = None,
            headers: Dict[str, str] = None,
            auto_raise: bool = True,
    ) -> Union[Any, Result]:
        """
        统一错误处理
        :param auto_raise: True → 直接抛 HTTPException；False → 返回 Result
        """
        try:
            c = cls.client()
            r = await c.request(
                method, url, params=params, json=json, data=data, headers=headers
            )
            r.raise_for_status()
            # 对非 JSON 兼容的接口，可改成 r.text
            return r.json() if auto_raise else Result(True, r.status_code, r.json())
        except httpx.HTTPStatusError as e:
            msg = f"[{e.response.status_code}] {e.response.text[:200]}"
            if auto_raise:
                raise HTTPException(status_code=e.response.status_code, detail=msg)
            return Result(False, e.response.status_code, msg=msg)
        except Exception as e:  # 网络超时/解析错误等
            if auto_raise:
                raise HTTPException(status_code=500, detail=str(e))
            return Result(False, 500, msg=str(e))

    # ---------- 对外快捷方法 ----------
    @classmethod
    async def get(
            cls,
            url: str,
            *,
            params: Dict[str, Any] = None,
            headers: Dict[str, str] = None,
            auto_raise: bool = True,
    ):
        """
        GET 请求
        :param url: 请求地址
        :param params: 请求参数
        :param headers: 请求头
        :param auto_raise: 是否自动抛出异常
        :return: Result
        """
        return await cls._safe_request(
            "GET", url, params=params, headers=headers, auto_raise=auto_raise
        )

    @classmethod
    async def post(
            cls,
            url: str,
            *,
            json: Dict[str, Any] = None,
            data: Any = None,
            headers: Dict[str, str] = None,
            auto_raise: bool = True,
    ):
        """
        发送POST请求
        :param url: 请求的URL
        :param json: 请求的JSON数据
        :param data: 请求的表单数据
        :param headers: 请求的头部信息
        :param auto_raise: 是否自动抛出异常
        :return: 返回结果
        """
        return await cls._safe_request(
            "POST", url, json=json, data=data, headers=headers, auto_raise=auto_raise
        )


'''
使用示例：
场景 1：直接抛异常（最简）
data = await HttpClient.get("https://httpbin.org/status/404")
# 如果 4xx/5xx 会自动转成 FastAPI 的 HTTPException 返回给前端

场景 2：不抛异常，业务层自己处理
res = await HttpClient.post("https://httpbin.org/post", json={"a": 1}, auto_raise=False)
if res.ok:
    return {"success": True, "data": res.data}
else:
    # 记录日志或做重试
    logger.error("外部接口异常: %s", res.msg)
    return {"success": False, "msg": res.msg}



# 使用测试
async def foo():
    data = await HttpClient.get("http://t.weather.sojson.com/api/weather/city/101030100")
    # data = await HttpClient.post("http://t.weather.sojson.com/api/weather/city/101030100", json={"city": 101030100}, auto_raise=False)
    print("data:", data)


if __name__ == '__main__':
    asyncio.run(foo())

'''
