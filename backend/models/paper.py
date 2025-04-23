from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base

class Paper(Base):
    __tablename__ = "papers"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    abstract = Column(Text)
    keywords = Column(String(255))
    content = Column(Text)
    status = Column(String(50), default="draft")  # draft, submitted, under_review, accepted, rejected
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    # 关系
    user = relationship("User", back_populates="papers")
    experiments = relationship("Experiment", back_populates="paper")
    submissions = relationship("Submission", back_populates="paper")
    reviews = relationship("Review", back_populates="paper")

class Experiment(Base):
    __tablename__ = "experiments"
    
    id = Column(Integer, primary_key=True, index=True)
    paper_id = Column(Integer, ForeignKey("papers.id"))
    name = Column(String(255))
    description = Column(Text)
    results = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 关系
    paper = relationship("Paper", back_populates="experiments")

class Submission(Base):
    __tablename__ = "submissions"
    
    id = Column(Integer, primary_key=True, index=True)
    paper_id = Column(Integer, ForeignKey("papers.id"))
    conference = Column(String(100))
    submission_date = Column(DateTime)
    status = Column(String(50))  # submitted, under_review, accepted, rejected
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 关系
    paper = relationship("Paper", back_populates="submissions")

class Review(Base):
    __tablename__ = "reviews"
    
    id = Column(Integer, primary_key=True, index=True)
    paper_id = Column(Integer, ForeignKey("papers.id"))
    reviewer = Column(String(100))
    comments = Column(Text)
    score = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 关系
    paper = relationship("Paper", back_populates="reviews") 