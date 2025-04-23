from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ...models.database import get_db
from ...models.models import Paper as DBPaper
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

class PaperBase(BaseModel):
    title: str
    abstract: str
    keywords: str
    target_conference: str
    status: str = "draft"

class PaperCreate(PaperBase):
    pass

class PaperUpdate(PaperBase):
    pass

class PaperResponse(PaperBase):
    id: int
    author_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

@router.post("/papers/", response_model=PaperResponse)
def create_paper(paper: PaperCreate, db: Session = Depends(get_db)):
    # TODO: 从token中获取用户ID，这里暂时使用1
    db_paper = DBPaper(**paper.dict(), author_id=1)
    db.add(db_paper)
    db.commit()
    db.refresh(db_paper)
    return db_paper

@router.get("/papers/", response_model=List[PaperResponse])
def read_papers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # TODO: 根据当前用户ID筛选论文
    papers = db.query(DBPaper).offset(skip).limit(limit).all()
    return papers

@router.get("/papers/{paper_id}", response_model=PaperResponse)
def read_paper(paper_id: int, db: Session = Depends(get_db)):
    paper = db.query(DBPaper).filter(DBPaper.id == paper_id).first()
    if paper is None:
        raise HTTPException(status_code=404, detail="Paper not found")
    return paper

@router.put("/papers/{paper_id}", response_model=PaperResponse)
def update_paper(paper_id: int, paper: PaperUpdate, db: Session = Depends(get_db)):
    db_paper = db.query(DBPaper).filter(DBPaper.id == paper_id).first()
    if db_paper is None:
        raise HTTPException(status_code=404, detail="Paper not found")
    
    # TODO: 检查当前用户是否有权限修改此论文
    
    for key, value in paper.dict().items():
        setattr(db_paper, key, value)
    
    db.commit()
    db.refresh(db_paper)
    return db_paper

@router.delete("/papers/{paper_id}")
def delete_paper(paper_id: int, db: Session = Depends(get_db)):
    db_paper = db.query(DBPaper).filter(DBPaper.id == paper_id).first()
    if db_paper is None:
        raise HTTPException(status_code=404, detail="Paper not found")
    
    # TODO: 检查当前用户是否有权限删除此论文
    
    db.delete(db_paper)
    db.commit()
    return {"message": "Paper deleted successfully"} 