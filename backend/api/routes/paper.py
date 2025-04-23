from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List
from core.database import get_db
from models.models import Paper
from schemas.paper import PaperCreate, PaperResponse, PaperAnalysisCreate, PaperAnalysisResponse
from api.deps import get_current_user
from services.paper_analysis import PaperAnalysisService
from services.file_service import FileService
from pathlib import Path

router = APIRouter()
paper_service = PaperAnalysisService()
file_service = FileService()

@router.post("/", response_model=PaperResponse)
def create_paper(
    paper: PaperCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    db_paper = Paper(**paper.dict(), user_id=current_user.id)
    db.add(db_paper)
    db.commit()
    db.refresh(db_paper)
    return db_paper

@router.get("/", response_model=List[PaperResponse])
def get_papers(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    papers = db.query(Paper).filter(Paper.user_id == current_user.id).offset(skip).limit(limit).all()
    return papers

@router.get("/{paper_id}", response_model=PaperResponse)
def get_paper(
    paper_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    paper = db.query(Paper).filter(Paper.id == paper_id, Paper.user_id == current_user.id).first()
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found")
    return paper

@router.get("/{paper_id}/file")
async def get_paper_file(
    paper_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    paper = db.query(Paper).filter(Paper.id == paper_id, Paper.user_id == current_user.id).first()
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found")
    
    if not paper.pdf_url:
        raise HTTPException(status_code=404, detail="Paper file not found")
    
    file_path = Path(paper.pdf_url)
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Paper file not found")
    
    return FileResponse(
        path=file_path,
        filename=file_path.name,
        media_type='application/pdf'
    )

@router.post("/{paper_id}/analysis", response_model=PaperAnalysisResponse)
def create_paper_analysis(
    paper_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    paper = db.query(Paper).filter(Paper.id == paper_id, Paper.user_id == current_user.id).first()
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found")
    
    # 分析论文
    analysis_result = paper_service.analyze_paper(paper.__dict__)
    
    # 创建分析记录
    db_analysis = PaperAnalysis(
        paper_id=paper_id,
        **analysis_result
    )
    db.add(db_analysis)
    db.commit()
    db.refresh(db_analysis)
    return db_analysis

@router.get("/{paper_id}/analysis", response_model=PaperAnalysisResponse)
def get_paper_analysis(
    paper_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    paper = db.query(Paper).filter(Paper.id == paper_id, Paper.user_id == current_user.id).first()
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found")
    
    analysis = db.query(PaperAnalysis).filter(PaperAnalysis.paper_id == paper_id).first()
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return analysis

@router.post("/upload")
async def upload_paper(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    try:
        # 保存文件
        file_path = await file_service.save_upload_file(file)
        
        # 提取PDF信息
        pdf_info = await file_service.extract_pdf_info(file_path)
        
        # 创建论文记录
        db_paper = Paper(
            title=pdf_info["title"],
            abstract=pdf_info["abstract"],
            authors=pdf_info["authors"],
            conference=pdf_info["conference"],
            year=pdf_info["year"],
            pdf_url=file_path,
            user_id=current_user.id,
            status="draft"
        )
        db.add(db_paper)
        db.commit()
        db.refresh(db_paper)
        
        return {
            "message": "文件上传成功",
            "paper_id": db_paper.id
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/stats")
def get_paper_stats(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    total = db.query(Paper).filter(Paper.user_id == current_user.id).count()
    draft = db.query(Paper).filter(Paper.user_id == current_user.id, Paper.status == "draft").count()
    submitted = db.query(Paper).filter(Paper.user_id == current_user.id, Paper.status == "submitted").count()
    accepted = db.query(Paper).filter(Paper.user_id == current_user.id, Paper.status == "accepted").count()
    rejected = db.query(Paper).filter(Paper.user_id == current_user.id, Paper.status == "rejected").count()
    
    return {
        "total": total,
        "draft": draft,
        "submitted": submitted,
        "accepted": accepted,
        "rejected": rejected
    }

@router.get("/recent")
def get_recent_papers(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    papers = db.query(Paper).filter(
        Paper.user_id == current_user.id
    ).order_by(Paper.created_at.desc()).limit(5).all()
    
    return papers 