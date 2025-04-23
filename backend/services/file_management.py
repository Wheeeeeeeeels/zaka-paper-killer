import os
import shutil
from typing import List, Dict, Any
from pathlib import Path
from datetime import datetime
from fastapi import HTTPException

class FileManagementService:
    def __init__(self):
        self.upload_dir = Path("uploads")
        self.upload_dir.mkdir(exist_ok=True)
        self.max_storage_size = 1024 * 1024 * 1024  # 1GB
        self.allowed_extensions = {'.pdf'}

    async def get_storage_info(self) -> Dict[str, Any]:
        """获取存储信息"""
        try:
            total_size = 0
            file_count = 0
            for file_path in self.upload_dir.glob('**/*'):
                if file_path.is_file():
                    total_size += file_path.stat().st_size
                    file_count += 1

            return {
                "total_size": total_size,
                "file_count": file_count,
                "max_size": self.max_storage_size,
                "used_percentage": (total_size / self.max_storage_size) * 100
            }
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"获取存储信息失败: {str(e)}"
            )

    async def list_files(self, page: int = 1, page_size: int = 20) -> Dict[str, Any]:
        """列出文件"""
        try:
            files = []
            for file_path in self.upload_dir.glob('*.pdf'):
                if file_path.is_file():
                    stat = file_path.stat()
                    files.append({
                        "name": file_path.name,
                        "size": stat.st_size,
                        "created_at": datetime.fromtimestamp(stat.st_ctime),
                        "modified_at": datetime.fromtimestamp(stat.st_mtime),
                        "path": str(file_path)
                    })

            # 按修改时间排序
            files.sort(key=lambda x: x["modified_at"], reverse=True)

            # 分页
            start = (page - 1) * page_size
            end = start + page_size
            paginated_files = files[start:end]

            return {
                "files": paginated_files,
                "total": len(files),
                "page": page,
                "page_size": page_size
            }
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"列出文件失败: {str(e)}"
            )

    async def delete_file(self, file_path: str) -> bool:
        """删除文件"""
        try:
            path = Path(file_path)
            if not path.exists():
                raise HTTPException(
                    status_code=404,
                    detail="文件不存在"
                )

            if path.suffix.lower() not in self.allowed_extensions:
                raise HTTPException(
                    status_code=400,
                    detail="不支持的文件类型"
                )

            os.remove(path)
            return True
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"删除文件失败: {str(e)}"
            )

    async def move_file(self, source_path: str, target_path: str) -> bool:
        """移动文件"""
        try:
            source = Path(source_path)
            target = Path(target_path)

            if not source.exists():
                raise HTTPException(
                    status_code=404,
                    detail="源文件不存在"
                )

            if target.exists():
                raise HTTPException(
                    status_code=400,
                    detail="目标文件已存在"
                )

            shutil.move(source, target)
            return True
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"移动文件失败: {str(e)}"
            )

    async def cleanup_old_files(self, days: int = 30) -> int:
        """清理旧文件"""
        try:
            count = 0
            current_time = datetime.now()
            for file_path in self.upload_dir.glob('*.pdf'):
                if file_path.is_file():
                    file_time = datetime.fromtimestamp(file_path.stat().st_mtime)
                    if (current_time - file_time).days > days:
                        os.remove(file_path)
                        count += 1
            return count
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"清理文件失败: {str(e)}"
            ) 