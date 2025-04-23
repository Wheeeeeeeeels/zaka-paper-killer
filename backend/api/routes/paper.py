from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ...models.paper import Paper, Experiment, Submission, Review
from ...core.database import get_db
from ...services.paper_analysis import PaperAnalysisService
from ...services.writing_assistant import WritingAssistantService
from ...services.experiment_analysis import ExperimentAnalysisService
from ...services.submission_strategy import SubmissionStrategyService

router = APIRouter()
paper_service = PaperAnalysisService()
writing_service = WritingAssistantService()
experiment_service = ExperimentAnalysisService()
submission_service = SubmissionStrategyService()

@router.post("/papers/", response_model=Paper)
async def create_paper(paper: dict, db: Session = Depends(get_db)):
    db_paper = Paper(**paper)
    db.add(db_paper)
    db.commit()
    db.refresh(db_paper)
    return db_paper

@router.get("/papers/", response_model=List[Paper])
async def get_papers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    papers = db.query(Paper).offset(skip).limit(limit).all()
    return papers

@router.get("/papers/{paper_id}", response_model=Paper)
async def get_paper(paper_id: int, db: Session = Depends(get_db)):
    paper = db.query(Paper).filter(Paper.id == paper_id).first()
    if paper is None:
        raise HTTPException(status_code=404, detail="Paper not found")
    return paper

@router.post("/papers/{paper_id}/analyze")
async def analyze_paper(paper_id: int, db: Session = Depends(get_db)):
    paper = db.query(Paper).filter(Paper.id == paper_id).first()
    if paper is None:
        raise HTTPException(status_code=404, detail="Paper not found")
    
    analysis = await paper_service.analyze_paper_trends([{
        'title': paper.title,
        'abstract': paper.abstract,
        'keywords': paper.keywords
    }])
    
    return analysis

@router.post("/papers/{paper_id}/optimize")
async def optimize_paper(paper_id: int, db: Session = Depends(get_db)):
    paper = db.query(Paper).filter(Paper.id == paper_id).first()
    if paper is None:
        raise HTTPException(status_code=404, detail="Paper not found")
    
    optimization = await writing_service.optimize_structure(paper.content)
    return optimization

@router.post("/papers/{paper_id}/experiments/analyze")
async def analyze_experiment(paper_id: int, experiment_data: dict, db: Session = Depends(get_db)):
    paper = db.query(Paper).filter(Paper.id == paper_id).first()
    if paper is None:
        raise HTTPException(status_code=404, detail="Paper not found")
    
    analysis = await experiment_service.analyze_experiment_results(experiment_data)
    return analysis

@router.post("/papers/{paper_id}/submission/suggest")
async def suggest_conference(paper_id: int, db: Session = Depends(get_db)):
    paper = db.query(Paper).filter(Paper.id == paper_id).first()
    if paper is None:
        raise HTTPException(status_code=404, detail="Paper not found")
    
    suggestions = await submission_service.match_conference(
        paper.keywords.split(','),
        "high"  # 这里可以根据论文质量动态设置
    )
    return suggestions 