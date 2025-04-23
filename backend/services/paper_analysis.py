from typing import List, Dict, Any
import numpy as np
from transformers import pipeline
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import arxiv
import requests
from bs4 import BeautifulSoup

class PaperAnalysisService:
    def __init__(self):
        # 初始化NLP模型
        self.nlp = spacy.load("en_core_web_sm")
        self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        self.vectorizer = TfidfVectorizer(stop_words='english')
        
    def analyze_paper(self, title: str, abstract: str, keywords: str) -> Dict[str, Any]:
        """分析论文内容"""
        # 提取关键词
        doc = self.nlp(abstract)
        extracted_keywords = [token.text for token in doc if token.pos_ in ['NOUN', 'PROPN']]
        
        # 生成摘要
        summary = self.summarizer(abstract, max_length=130, min_length=30, do_sample=False)[0]['summary_text']
        
        # 分析创新点
        innovation_points = self._analyze_innovation(abstract)
        
        # 查找相关论文
        related_papers = self._find_related_papers(title, abstract)
        
        return {
            "extracted_keywords": extracted_keywords,
            "summary": summary,
            "innovation_points": innovation_points,
            "related_papers": related_papers
        }
    
    def _analyze_innovation(self, text: str) -> List[str]:
        """分析论文创新点"""
        doc = self.nlp(text)
        innovation_points = []
        
        # 提取包含创新性词汇的句子
        innovation_keywords = ['novel', 'propose', 'introduce', 'develop', 'new', 'improve', 'enhance']
        for sent in doc.sents:
            if any(keyword in sent.text.lower() for keyword in innovation_keywords):
                innovation_points.append(sent.text)
        
        return innovation_points
    
    def _find_related_papers(self, title: str, abstract: str) -> List[Dict[str, str]]:
        """查找相关论文"""
        # 使用arXiv API搜索相关论文
        search = arxiv.Search(
            query=title,
            max_results=5,
            sort_by=arxiv.SortCriterion.Relevance
        )
        
        related_papers = []
        for result in search.results():
            related_papers.append({
                "title": result.title,
                "authors": [author.name for author in result.authors],
                "abstract": result.summary,
                "pdf_url": result.pdf_url,
                "published": result.published.strftime("%Y-%m-%d")
            })
        
        return related_papers
    
    def analyze_conference_suitability(self, paper_data: Dict[str, Any], target_conference: str) -> Dict[str, Any]:
        """分析论文与目标会议的匹配度"""
        # 这里可以添加特定会议的匹配规则
        conference_keywords = {
            "ICML": ["machine learning", "deep learning", "neural networks", "optimization"],
            "ICLR": ["deep learning", "representation learning", "neural networks"],
            "NeurIPS": ["neural networks", "machine learning", "artificial intelligence"],
            "CVPR": ["computer vision", "image processing", "deep learning"],
            "ACL": ["natural language processing", "computational linguistics", "text mining"]
        }
        
        # 计算匹配度
        paper_text = f"{paper_data['title']} {paper_data['abstract']} {paper_data['keywords']}"
        conference_text = " ".join(conference_keywords.get(target_conference, []))
        
        if conference_text:
            vectors = self.vectorizer.fit_transform([paper_text, conference_text])
            similarity = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
        else:
            similarity = 0.0
        
        return {
            "conference": target_conference,
            "similarity_score": float(similarity),
            "suggested_conferences": self._suggest_conferences(paper_text)
        }
    
    def _suggest_conferences(self, paper_text: str) -> List[Dict[str, Any]]:
        """推荐合适的会议"""
        conferences = ["ICML", "ICLR", "NeurIPS", "CVPR", "ACL"]
        suggestions = []
        
        for conference in conferences:
            vectors = self.vectorizer.fit_transform([paper_text, " ".join(conference_keywords.get(conference, []))])
            similarity = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
            suggestions.append({
                "conference": conference,
                "similarity_score": float(similarity)
            })
        
        return sorted(suggestions, key=lambda x: x["similarity_score"], reverse=True)

    async def analyze_paper_trends(self, papers: List[Dict]) -> Dict:
        """
        分析论文趋势
        """
        # 提取论文摘要
        abstracts = [paper.get('abstract', '') for paper in papers]
        
        # 使用TF-IDF进行文本分析
        tfidf_matrix = self.vectorizer.fit_transform(abstracts)
        
        # 计算相似度矩阵
        similarity_matrix = cosine_similarity(tfidf_matrix)
        
        # 提取关键词
        feature_names = self.vectorizer.get_feature_names_out()
        
        return {
            'similarity_matrix': similarity_matrix.tolist(),
            'keywords': feature_names.tolist()
        }
    
    async def identify_research_gaps(self, papers: List[Dict]) -> List[Dict]:
        """
        识别研究空白点
        """
        # TODO: 实现研究空白点识别逻辑
        return []
    
    async def generate_innovation_suggestions(self, papers: List[Dict]) -> List[str]:
        """
        生成创新点建议
        """
        # TODO: 实现创新点建议生成逻辑
        return [] 