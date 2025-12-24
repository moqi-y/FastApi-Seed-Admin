from fastapi import APIRouter, UploadFile, File, HTTPException

from app.external_services.file_uploader.service import LocalFileUploader
from app.schemas.response import SuccessResponse

router = APIRouter()


# 本地上传文件
@router.post("", summary="本地文件上传")
async def root(file: UploadFile = File(...)):
    print("file:", file)
    try:
        file_sever = LocalFileUploader('static')
        file_path = await file_sever.upload_file(file, allowed_ext={".jpg", ".png", ".jpeg"})
        return SuccessResponse(data={
            "file_id": file_path.split('/')[-1],
            "file_name": file.filename,
            "file_size": file.size / 1024 / 1024,
            "size_unit": "M",  # 单位
            "file_type": file.content_type,
            "file_path": file_path
        })
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
