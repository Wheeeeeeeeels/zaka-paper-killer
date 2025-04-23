from sqlalchemy import Boolean, Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..core.database import Base

class Paper(Base):
    __tablename__ = "papers"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    abstract = Column(Text)
    authors = Column(String)
    conference = Column(String)
    year = Column(Integer)
    doi = Column(String, unique=True)
    pdf_url = Column(String)
    status = Column(String)  # draft, submitted, accepted, rejected
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # 关系
    user = relationship("User", back_populates="papers")
    analysis = relationship("PaperAnalysis", back_populates="paper", uselist=False)

class PaperAnalysis(Base):
    __tablename__ = "paper_analyses"

    id = Column(Integer, primary_key=True, index=True)
    paper_id = Column(Integer, ForeignKey("papers.id"))
    keywords = Column(String)
    main_contribution = Column(Text)
    methodology = Column(Text)
    results = Column(Text)
    limitations = Column(Text)
    future_work = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # 关系
    paper = relationship("Paper", back_populates="analysis") 