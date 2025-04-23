from typing import List, Dict, Any
import numpy as np
from transformers import pipeline
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import arxiv
import requests
from bs4 import BeautifulSoup
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

class PaperAnalysisService:
    def __init__(self):
        # 下载必要的NLTK数据
        nltk.download('punkt')
        nltk.download('stopwords')
        nltk.download('wordnet')
        
        # 初始化NLP模型
        self.nlp = spacy.load("en_core_web_sm")
        self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        self.vectorizer = TfidfVectorizer(
            max_features=10,
            stop_words='english',
            ngram_range=(1, 2)
        )
        
    def extract_keywords(self, text: str) -> str:
        """提取文本中的关键词"""
        # 分词
        tokens = word_tokenize(text.lower())
        
        # 去除停用词
        stop_words = set(stopwords.words('english'))
        tokens = [token for token in tokens if token not in stop_words]
        
        # 词形还原
        lemmatizer = WordNetLemmatizer()
        tokens = [lemmatizer.lemmatize(token) for token in tokens]
        
        # 使用TF-IDF提取关键词
        tfidf_matrix = self.vectorizer.fit_transform([text])
        feature_names = self.vectorizer.get_feature_names_out()
        
        # 获取前10个关键词
        keywords = []
        for i in range(min(10, len(feature_names))):
            keywords.append(feature_names[i])
        
        return ', '.join(keywords)

    def analyze_paper(self, paper: Dict[str, Any]) -> Dict[str, str]:
        """分析论文内容"""
        # 提取关键词
        keywords = self.extract_keywords(paper['abstract'])
        
        # 生成摘要
        summary = self.summarizer(paper['abstract'], max_length=130, min_length=30, do_sample=False)
        main_contribution = summary[0]['summary_text']
        
        # 分析方法论
        methodology = self._analyze_methodology(paper['abstract'])
        
        # 分析结果
        results = self._analyze_results(paper['abstract'])
        
        # 分析局限性
        limitations = self._analyze_limitations(paper['abstract'])
        
        # 分析未来工作
        future_work = self._analyze_future_work(paper['abstract'])
        
        return {
            'keywords': keywords,
            'main_contribution': main_contribution,
            'methodology': methodology,
            'results': results,
            'limitations': limitations,
            'future_work': future_work
        }

    def _analyze_methodology(self, text: str) -> str:
        """分析论文的方法论部分"""
        # 这里可以使用更复杂的NLP模型来分析方法论
        # 目前使用简单的规则匹配
        methodology_keywords = ['method', 'approach', 'algorithm', 'technique', 'framework']
        sentences = nltk.sent_tokenize(text)
        methodology_sentences = []
        
        for sentence in sentences:
            if any(keyword in sentence.lower() for keyword in methodology_keywords):
                methodology_sentences.append(sentence)
        
        return ' '.join(methodology_sentences)

    def _analyze_results(self, text: str) -> str:
        """分析论文的结果部分"""
        # 使用规则匹配来识别结果相关的句子
        result_keywords = ['result', 'outcome', 'performance', 'accuracy', 'improvement']
        sentences = nltk.sent_tokenize(text)
        result_sentences = []
        
        for sentence in sentences:
            if any(keyword in sentence.lower() for keyword in result_keywords):
                result_sentences.append(sentence)
        
        return ' '.join(result_sentences)

    def _analyze_limitations(self, text: str) -> str:
        """分析论文的局限性部分"""
        # 使用规则匹配来识别局限性相关的句子
        limitation_keywords = ['limitation', 'constraint', 'drawback', 'weakness', 'challenge']
        sentences = nltk.sent_tokenize(text)
        limitation_sentences = []
        
        for sentence in sentences:
            if any(keyword in sentence.lower() for keyword in limitation_keywords):
                limitation_sentences.append(sentence)
        
        return ' '.join(limitation_sentences)

    def _analyze_future_work(self, text: str) -> str:
        """分析论文的未来工作部分"""
        # 使用规则匹配来识别未来工作相关的句子
        future_keywords = ['future', 'prospect', 'direction', 'potential', 'next step']
        sentences = nltk.sent_tokenize(text)
        future_sentences = []
        
        for sentence in sentences:
            if any(keyword in sentence.lower() for keyword in future_keywords):
                future_sentences.append(sentence)
        
        return ' '.join(future_sentences)
    
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