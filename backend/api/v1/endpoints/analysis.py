from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any
from ...models.database import get_db
from ...models.models import Paper
from ...services.paper_analysis import PaperAnalysisService
from ...core.security import get_current_active_user
from pydantic import BaseModel

router = APIRouter()
paper_analysis_service = PaperAnalysisService()

class AnalysisRequest(BaseModel):
    paper_id: int

@router.post("/analyze", response_model=Dict[str, Any])
async def analyze_paper(
    request: AnalysisRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    paper = db.query(Paper).filter(Paper.id == request.paper_id).first()
    if not paper:
        raise HTTPException(status_code=404, detail="论文不存在")
    
    if paper.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权访问此论文")
    
    analysis_result = paper_analysis_service.analyze_paper(
        title=paper.title,
        abstract=paper.abstract,
        keywords=paper.keywords
    )
    
    return analysis_result

@router.post("/conference-suitability", response_model=Dict[str, Any])
async def analyze_conference_suitability(
    request: AnalysisRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    paper = db.query(Paper).filter(Paper.id == request.paper_id).first()
    if not paper:
        raise HTTPException(status_code=404, detail="论文不存在")
    
    if paper.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权访问此论文")
    
    paper_data = {
        "title": paper.title,
        "abstract": paper.abstract,
        "keywords": paper.keywords
    }
    
    suitability_result = paper_analysis_service.analyze_conference_suitability(
        paper_data=paper_data,
        target_conference=paper.target_conference
    )
    
    return suitability_result 