from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean, JSON, Float
from sqlalchemy.orm import relationship
from core.database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    papers = relationship("Paper", back_populates="author")

class Paper(Base):
    __tablename__ = "papers"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    abstract = Column(Text)
    keywords = Column(String)
    status = Column(String)  # draft, submitted, accepted, rejected
    target_conference = Column(String)
    author_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    author = relationship("User", back_populates="papers")
    reviews = relationship("Review", back_populates="paper")
    analysis = relationship("PaperAnalysis", back_populates="paper", uselist=False)

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    paper_id = Column(Integer, ForeignKey("papers.id"))
    reviewer = Column(String)
    score = Column(Integer)
    comments = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    paper = relationship("Paper", back_populates="reviews")

class PaperAnalysis(Base):
    __tablename__ = "paper_analyses"

    id = Column(Integer, primary_key=True, index=True)
    paper_id = Column(Integer, ForeignKey("papers.id"))
    
    # 基础分析
    keywords = Column(String)
    main_contribution = Column(Text)
    methodology = Column(Text)
    results = Column(Text)
    limitations = Column(Text)
    future_work = Column(Text)
    
    # 引用分析
    total_citations = Column(Integer, default=0)
    citation_types = Column(JSON)  # 存储引用类型统计
    citation_sentences = Column(JSON)  # 存储引用相关句子
    
    # 质量评估
    quality_scores = Column(JSON)  # 存储各项质量得分
    
    # 创新点分析
    innovations = Column(JSON)  # 存储创新点分析结果
    
    # 实验方法分析
    experiments = Column(JSON)  # 存储实验方法分析结果
    
    # 时间戳
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    paper = relationship("Paper", back_populates="analysis") 