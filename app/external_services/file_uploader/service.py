from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile


class FileUploaderService:
    """上传文件到对象存储服务的类"""

    def upload_file(self, file):
        """上传文件到对象存储服务"""
        pass

    # 从对象存储服务下载文件
    def download_file(self, file_id):
        """从对象存储服务下载文件"""
        pass

    # 删除对象存储服务中的文件
    def delete_file(self, file_id):
        """删除对象存储服务中的文件"""
        pass

    # 获取文件在对象存储服务中的URL
    def get_file_url(self, file_id):
        """获取文件在对象存储服务中的URL"""
        pass


"""使用示例：
# 上传文件到对象存储服务
file = FileUploaderService()
file.upload_file(file)
"""


class LocalFileUploader:
    """
    静态资源本地托管封装
    - 自动生成唯一文件名
    - 校验/过滤
    - 统一返回可访问 URL
    """

    def __init__(self, path: str):
        self.path = Path(path)
        self.path.mkdir(parents=True, exist_ok=True)

    async def upload_file(self, file: UploadFile, allowed_ext=None, max_size=10 * 1024 * 1024):
        """ 上传文件到本地
        :param file: UploadFile 文件对象
        :param allowed_ext: 允许的文件扩展名，默认无限制。可选参数: {"jpg", "png"}
        :param max_size: 最大文件大小，默认10MB
        :return: 文件访问 URL，如: /static/2023/01/01/123.jpg
        """
        # 1.校验
        ext = Path(file.filename).suffix.lower()
        if allowed_ext and ext not in allowed_ext:
            raise ValueError(f"不支持的扩展名：{ext}")
        if file.size > max_size:
            raise ValueError("文件过大")
        # 2.生成唯一文件名
        file_id = str(uuid4().hex)
        file_ext = file.filename.split(".")[-1]
        file_name = f"{file_id}.{file_ext}"
        file_path = self.path / file_name
        # 3.写入磁盘
        with open(file_path, "wb") as buffer:
            buffer.write(file.file.read())
        await file.close()
        # 4.返回结果
        return f"/static/{file_path.relative_to(self.path).as_posix()}"
