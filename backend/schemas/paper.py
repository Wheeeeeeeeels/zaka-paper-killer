from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PaperBase(BaseModel):
    title: str
    abstract: Optional[str] = None
    authors: Optional[str] = None
    conference: Optional[str] = None
    year: Optional[int] = None
    doi: Optional[str] = None
    pdf_url: Optional[str] = None
    status: str = "draft"

class PaperCreate(PaperBase):
    pass

class PaperResponse(PaperBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class PaperAnalysisBase(BaseModel):
    keywords: Optional[str] = None
    main_contribution: Optional[str] = None
    methodology: Optional[str] = None
    results: Optional[str] = None
    limitations: Optional[str] = None
    future_work: Optional[str] = None

class PaperAnalysisCreate(PaperAnalysisBase):
    pass

class PaperAnalysisResponse(PaperAnalysisBase):
    id: int
    paper_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True 