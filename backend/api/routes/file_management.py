from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Dict, Any
from ...core.database import get_db
from ...api.deps import get_current_user
from ...services.file_management import FileManagementService

router = APIRouter()
file_service = FileManagementService()

@router.get("/storage")
async def get_storage_info(
    current_user = Depends(get_current_user)
):
    """获取存储信息"""
    return await file_service.get_storage_info()

@router.get("/files")
async def list_files(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user = Depends(get_current_user)
):
    """列出文件"""
    return await file_service.list_files(page, page_size)

@router.delete("/files/{file_path:path}")
async def delete_file(
    file_path: str,
    current_user = Depends(get_current_user)
):
    """删除文件"""
    success = await file_service.delete_file(file_path)
    if success:
        return {"message": "文件删除成功"}
    raise HTTPException(status_code=500, detail="文件删除失败")

@router.post("/files/move")
async def move_file(
    source_path: str,
    target_path: str,
    current_user = Depends(get_current_user)
):
    """移动文件"""
    success = await file_service.move_file(source_path, target_path)
    if success:
        return {"message": "文件移动成功"}
    raise HTTPException(status_code=500, detail="文件移动失败")

@router.post("/cleanup")
async def cleanup_files(
    days: int = Query(30, ge=1),
    current_user = Depends(get_current_user)
):
    """清理旧文件"""
    count = await file_service.cleanup_old_files(days)
    return {
        "message": f"成功清理 {count} 个文件",
        "cleaned_count": count
    } 