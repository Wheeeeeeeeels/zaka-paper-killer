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
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re
from collections import Counter
import networkx as nx
from rake_nltk import Rake
from .visualization_service import VisualizationService
from .prediction_service import PredictionService

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
        
        # 初始化RAKE
        self.rake = Rake(
            min_length=1,
            max_length=3,
            include_repeated_phrases=False
        )
        
        # 初始化可视化服务
        self.visualization_service = VisualizationService()
        
        # 初始化预测服务
        self.prediction_service = PredictionService()
        
        # 初始化质量评估指标
        self.quality_metrics = {
            'methodology': ['novel', 'innovative', 'state-of-the-art', 'efficient', 'effective'],
            'experiments': ['comprehensive', 'extensive', 'thorough', 'rigorous', 'systematic'],
            'results': ['significant', 'promising', 'outstanding', 'remarkable', 'excellent'],
            'writing': ['clear', 'concise', 'well-structured', 'well-written', 'readable']
        }
        
        # 初始化创新点关键词
        self.innovation_keywords = {
            'method': ['novel', 'new', 'propose', 'introduce', 'develop'],
            'improvement': ['improve', 'enhance', 'optimize', 'advance', 'better'],
            'application': ['apply', 'utilize', 'employ', 'implement', 'use'],
            'comparison': ['compare', 'outperform', 'surpass', 'exceed', 'better than']
        }
        
        # 初始化实验方法关键词
        self.experiment_keywords = {
            'dataset': ['dataset', 'corpus', 'collection', 'benchmark'],
            'evaluation': ['evaluate', 'measure', 'assess', 'test'],
            'metrics': ['accuracy', 'precision', 'recall', 'F1', 'BLEU'],
            'baseline': ['baseline', 'comparison', 'state-of-the-art', 'SOTA']
        }
        
    def extract_keywords(self, text: str, method: str = 'combined') -> Dict[str, List[str]]:
        """
        使用多种方法提取关键词
        
        Args:
            text: 输入文本
            method: 提取方法 ('tfidf', 'rake', 'textrank', 'combined')
            
        Returns:
            Dict包含不同方法提取的关键词
        """
        keywords = {}
        
        if method in ['tfidf', 'combined']:
            keywords['tfidf'] = self._extract_keywords_tfidf(text)
            
        if method in ['rake', 'combined']:
            keywords['rake'] = self._extract_keywords_rake(text)
            
        if method in ['textrank', 'combined']:
            keywords['textrank'] = self._extract_keywords_textrank(text)
            
        if method == 'combined':
            # 合并所有方法的结果，去除重复
            all_keywords = []
            for method_keywords in keywords.values():
                all_keywords.extend(method_keywords)
            keywords['combined'] = list(set(all_keywords))
            
        return keywords
        
    def _extract_keywords_tfidf(self, text: str) -> List[str]:
        """使用TF-IDF方法提取关键词"""
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
        
        return keywords
        
    def _extract_keywords_rake(self, text: str) -> List[str]:
        """使用RAKE算法提取关键词"""
        self.rake.extract_keywords_from_text(text)
        return [keyword for keyword, score in self.rake.get_ranked_phrases_with_scores()[:10]]
        
    def _extract_keywords_textrank(self, text: str) -> List[str]:
        """使用TextRank算法提取关键词"""
        # 分词
        sentences = sent_tokenize(text)
        words = word_tokenize(text.lower())
        
        # 去除停用词
        stop_words = set(stopwords.words('english'))
        words = [word for word in words if word not in stop_words]
        
        # 构建词图
        word_graph = nx.Graph()
        
        # 添加节点
        for word in set(words):
            word_graph.add_node(word)
            
        # 添加边（基于共现关系）
        window_size = 2
        for i in range(len(words) - window_size + 1):
            window = words[i:i + window_size]
            for j in range(len(window)):
                for k in range(j + 1, len(window)):
                    if window[j] != window[k]:
                        if word_graph.has_edge(window[j], window[k]):
                            word_graph[window[j]][window[k]]['weight'] += 1
                        else:
                            word_graph.add_edge(window[j], window[k], weight=1)
        
        # 计算PageRank
        scores = nx.pagerank(word_graph)
        
        # 获取前10个关键词
        keywords = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:10]
        return [keyword for keyword, score in keywords]

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
        
        # 分析引用
        citations = self._analyze_citations(paper['abstract'])
        
        # 评估论文质量
        quality_score = self._evaluate_paper_quality(paper['abstract'])
        
        # 分析创新点
        innovations = self._analyze_innovations(paper['abstract'])
        
        # 分析实验方法
        experiments = self._analyze_experiments(paper['abstract'])
        
        # 预测论文影响力
        impact_prediction = self.prediction_service.predict_paper_impact({
            'title': paper.get('title', ''),
            'abstract': paper.get('abstract', ''),
            'authors': paper.get('authors', []),
            'citation_count': citations['total_citations'],
            'keywords': keywords['combined'],
            'innovation_score': quality_score['methodology'],
            'experiment_score': quality_score['experiments']
        })
        
        return {
            'keywords': keywords,
            'main_contribution': main_contribution,
            'methodology': methodology,
            'results': results,
            'limitations': limitations,
            'future_work': future_work,
            'citations': citations,
            'quality_score': quality_score,
            'innovations': innovations,
            'experiments': experiments,
            'impact_prediction': impact_prediction
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

    def _analyze_citations(self, text: str) -> Dict[str, Any]:
        """分析论文引用"""
        # 提取引用相关的句子
        citation_patterns = [
            r'\[(\d+)\]',
            r'\([A-Za-z]+ et al\., \d{4}\)',
            r'\([A-Za-z]+ and [A-Za-z]+, \d{4}\)'
        ]
        
        citations = []
        for pattern in citation_patterns:
            citations.extend(re.findall(pattern, text))
        
        # 统计引用数量
        citation_count = len(citations)
        
        # 分析引用类型
        citation_types = {
            'methodology': 0,
            'results': 0,
            'background': 0
        }
        
        sentences = nltk.sent_tokenize(text)
        for sentence in sentences:
            if any(citation in sentence for citation in citations):
                if any(word in sentence.lower() for word in ['method', 'approach', 'algorithm']):
                    citation_types['methodology'] += 1
                elif any(word in sentence.lower() for word in ['result', 'outcome', 'performance']):
                    citation_types['results'] += 1
                else:
                    citation_types['background'] += 1
        
        return {
            'total_citations': citation_count,
            'citation_types': citation_types,
            'citation_sentences': [s for s in sentences if any(citation in s for citation in citations)]
        }

    def _evaluate_paper_quality(self, text: str) -> Dict[str, float]:
        """评估论文质量"""
        scores = {}
        
        # 评估方法论
        methodology_score = self._calculate_metric_score(text, self.quality_metrics['methodology'])
        scores['methodology'] = methodology_score
        
        # 评估实验
        experiment_score = self._calculate_metric_score(text, self.quality_metrics['experiments'])
        scores['experiments'] = experiment_score
        
        # 评估结果
        result_score = self._calculate_metric_score(text, self.quality_metrics['results'])
        scores['results'] = result_score
        
        # 评估写作
        writing_score = self._calculate_metric_score(text, self.quality_metrics['writing'])
        scores['writing'] = writing_score
        
        # 计算总分
        scores['overall'] = sum(scores.values()) / len(scores)
        
        return scores

    def _calculate_metric_score(self, text: str, keywords: List[str]) -> float:
        """计算特定指标得分"""
        text_lower = text.lower()
        keyword_count = sum(1 for keyword in keywords if keyword in text_lower)
        return min(1.0, keyword_count / len(keywords))

    def _analyze_innovations(self, text: str) -> Dict[str, List[str]]:
        """分析论文创新点"""
        innovations = {}
        
        for category, keywords in self.innovation_keywords.items():
            sentences = nltk.sent_tokenize(text)
            innovation_sentences = []
            
            for sentence in sentences:
                if any(keyword in sentence.lower() for keyword in keywords):
                    innovation_sentences.append(sentence)
            
            innovations[category] = innovation_sentences
        
        return innovations

    def _analyze_experiments(self, text: str) -> Dict[str, Any]:
        """分析实验方法"""
        experiments = {}
        
        for category, keywords in self.experiment_keywords.items():
            sentences = nltk.sent_tokenize(text)
            experiment_sentences = []
            
            for sentence in sentences:
                if any(keyword in sentence.lower() for keyword in keywords):
                    experiment_sentences.append(sentence)
            
            experiments[category] = experiment_sentences
        
        # 提取实验数据集
        datasets = re.findall(r'([A-Za-z0-9-]+ dataset)', text)
        experiments['datasets'] = list(set(datasets))
        
        # 提取评估指标
        metrics = re.findall(r'([A-Za-z0-9-]+ score|accuracy|precision|recall|F1)', text)
        experiments['metrics'] = list(set(metrics))
        
        return experiments
    
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
        
        Args:
            papers: 论文列表，每个论文包含标题、摘要、发表时间等信息
            
        Returns:
            包含趋势分析结果的字典
        """
        # 按时间排序
        sorted_papers = sorted(papers, key=lambda x: x.get('published_date', ''))
        
        # 提取时间序列数据
        time_series = self._extract_time_series(sorted_papers)
        
        # 分析主题演化
        topic_evolution = self._analyze_topic_evolution(sorted_papers)
        
        # 分析引用趋势
        citation_trends = self._analyze_citation_trends(sorted_papers)
        
        # 分析方法演化
        methodology_evolution = self._analyze_methodology_evolution(sorted_papers)
        
        # 分析实验趋势
        experiment_trends = self._analyze_experiment_trends(sorted_papers)
        
        # 预测未来趋势
        future_trends = self.prediction_service.predict_trends(time_series)
        
        # 生成可视化图表
        visualizations = {
            'trends': self.visualization_service.generate_trend_visualizations(time_series),
            'topics': self.visualization_service.generate_topic_evolution_visualizations(topic_evolution),
            'citations': self.visualization_service.generate_citation_visualizations(citation_trends),
            'methodology': self.visualization_service.generate_methodology_visualizations(methodology_evolution),
            'experiments': self.visualization_service.generate_experiment_visualizations(experiment_trends)
        }
        
        return {
            'time_series': time_series,
            'topic_evolution': topic_evolution,
            'citation_trends': citation_trends,
            'methodology_evolution': methodology_evolution,
            'experiment_trends': experiment_trends,
            'future_trends': future_trends,
            'visualizations': visualizations
        }
    
    def _extract_time_series(self, papers: List[Dict]) -> Dict[str, List]:
        """提取时间序列数据"""
        # 按年份分组
        yearly_data = {}
        for paper in papers:
            year = paper.get('published_date', '').split('-')[0]
            if year not in yearly_data:
                yearly_data[year] = []
            yearly_data[year].append(paper)
        
        # 计算每年的统计指标
        time_series = {
            'years': [],
            'paper_counts': [],
            'citation_counts': [],
            'keyword_frequencies': []
        }
        
        for year, year_papers in sorted(yearly_data.items()):
            time_series['years'].append(year)
            time_series['paper_counts'].append(len(year_papers))
            
            # 计算引用数
            citations = sum(len(self._analyze_citations(p['abstract'])['citation_sentences']) 
                          for p in year_papers)
            time_series['citation_counts'].append(citations)
            
            # 统计关键词频率
            keywords = []
            for paper in year_papers:
                keywords.extend(self.extract_keywords(paper['abstract'])['combined'])
            keyword_freq = Counter(keywords)
            time_series['keyword_frequencies'].append(dict(keyword_freq.most_common(10)))
        
        return time_series
    
    def _analyze_topic_evolution(self, papers: List[Dict]) -> List[Dict]:
        """分析主题演化"""
        # 按时间段分组
        time_periods = self._split_into_periods(papers, num_periods=3)
        
        topic_evolution = []
        for period, period_papers in time_periods.items():
            # 提取该时期的关键词
            period_keywords = []
            for paper in period_papers:
                period_keywords.extend(self.extract_keywords(paper['abstract'])['combined'])
            
            # 统计关键词频率
            keyword_freq = Counter(period_keywords)
            
            # 分析主题变化
            topic_evolution.append({
                'period': period,
                'top_keywords': dict(keyword_freq.most_common(10)),
                'emerging_topics': self._identify_emerging_topics(period_papers, papers),
                'declining_topics': self._identify_declining_topics(period_papers, papers)
            })
        
        return topic_evolution
    
    def _analyze_citation_trends(self, papers: List[Dict]) -> Dict:
        """分析引用趋势"""
        citation_trends = {
            'highly_cited_papers': [],
            'citation_networks': [],
            'citation_impact': {}
        }
        
        # 识别高引用论文
        for paper in papers:
            citations = self._analyze_citations(paper['abstract'])
            if citations['total_citations'] > 5:  # 设置阈值
                citation_trends['highly_cited_papers'].append({
                    'title': paper.get('title', ''),
                    'citations': citations['total_citations'],
                    'citation_types': citations['citation_types']
                })
        
        # 分析引用网络
        citation_networks = self._build_citation_networks(papers)
        citation_trends['citation_networks'] = citation_networks
        
        # 计算引用影响力
        citation_trends['citation_impact'] = self._calculate_citation_impact(papers)
        
        return citation_trends
    
    def _analyze_methodology_evolution(self, papers: List[Dict]) -> List[Dict]:
        """分析方法演化"""
        methodology_evolution = []
        
        # 按时间段分组
        time_periods = self._split_into_periods(papers, num_periods=3)
        
        for period, period_papers in time_periods.items():
            # 提取该时期的方法
            period_methods = []
            for paper in period_papers:
                period_methods.extend(self._analyze_methodology(paper['abstract']).split('.'))
            
            # 分析方法变化
            methodology_evolution.append({
                'period': period,
                'methods': self._extract_method_features(period_methods),
                'method_improvements': self._identify_method_improvements(period_methods),
                'new_methods': self._identify_new_methods(period_methods, papers)
            })
        
        return methodology_evolution
    
    def _analyze_experiment_trends(self, papers: List[Dict]) -> Dict:
        """分析实验趋势"""
        experiment_trends = {
            'dataset_usage': {},
            'metric_evolution': {},
            'experiment_design': {}
        }
        
        # 分析数据集使用趋势
        for paper in papers:
            experiments = self._analyze_experiments(paper['abstract'])
            for dataset in experiments.get('datasets', []):
                if dataset not in experiment_trends['dataset_usage']:
                    experiment_trends['dataset_usage'][dataset] = 0
                experiment_trends['dataset_usage'][dataset] += 1
        
        # 分析评估指标演化
        for paper in papers:
            experiments = self._analyze_experiments(paper['abstract'])
            for metric in experiments.get('metrics', []):
                if metric not in experiment_trends['metric_evolution']:
                    experiment_trends['metric_evolution'][metric] = 0
                experiment_trends['metric_evolution'][metric] += 1
        
        # 分析实验设计趋势
        experiment_trends['experiment_design'] = self._analyze_experiment_design_trends(papers)
        
        return experiment_trends
    
    def _split_into_periods(self, papers: List[Dict], num_periods: int) -> Dict[str, List[Dict]]:
        """将论文按时间段分组"""
        sorted_papers = sorted(papers, key=lambda x: x.get('published_date', ''))
        period_size = len(sorted_papers) // num_periods
        
        periods = {}
        for i in range(num_periods):
            start_idx = i * period_size
            end_idx = start_idx + period_size if i < num_periods - 1 else len(sorted_papers)
            period_name = f"period_{i+1}"
            periods[period_name] = sorted_papers[start_idx:end_idx]
        
        return periods
    
    def _identify_emerging_topics(self, current_papers: List[Dict], all_papers: List[Dict]) -> List[str]:
        """识别新兴主题"""
        # 提取当前时期的关键词
        current_keywords = set()
        for paper in current_papers:
            current_keywords.update(self.extract_keywords(paper['abstract'])['combined'])
        
        # 提取之前时期的关键词
        previous_keywords = set()
        for paper in all_papers:
            if paper not in current_papers:
                previous_keywords.update(self.extract_keywords(paper['abstract'])['combined'])
        
        # 找出新兴主题
        emerging_topics = current_keywords - previous_keywords
        return list(emerging_topics)
    
    def _identify_declining_topics(self, current_papers: List[Dict], all_papers: List[Dict]) -> List[str]:
        """识别衰退主题"""
        # 提取当前时期的关键词
        current_keywords = set()
        for paper in current_papers:
            current_keywords.update(self.extract_keywords(paper['abstract'])['combined'])
        
        # 提取之前时期的关键词
        previous_keywords = set()
        for paper in all_papers:
            if paper not in current_papers:
                previous_keywords.update(self.extract_keywords(paper['abstract'])['combined'])
        
        # 找出衰退主题
        declining_topics = previous_keywords - current_keywords
        return list(declining_topics)
    
    def _build_citation_networks(self, papers: List[Dict]) -> List[Dict]:
        """构建引用网络"""
        networks = []
        
        for paper in papers:
            citations = self._analyze_citations(paper['abstract'])
            if citations['total_citations'] > 0:
                network = {
                    'paper': paper.get('title', ''),
                    'cited_papers': citations['citation_sentences'],
                    'citation_types': citations['citation_types']
                }
                networks.append(network)
        
        return networks
    
    def _calculate_citation_impact(self, papers: List[Dict]) -> Dict:
        """计算引用影响力"""
        impact = {
            'methodology_citations': 0,
            'result_citations': 0,
            'background_citations': 0,
            'total_citations': 0
        }
        
        for paper in papers:
            citations = self._analyze_citations(paper['abstract'])
            impact['methodology_citations'] += citations['citation_types']['methodology']
            impact['result_citations'] += citations['citation_types']['results']
            impact['background_citations'] += citations['citation_types']['background']
            impact['total_citations'] += citations['total_citations']
        
        return impact
    
    def _extract_method_features(self, methods: List[str]) -> List[Dict]:
        """提取方法特征"""
        features = []
        
        for method in methods:
            # 提取关键词
            keywords = self.extract_keywords(method)['combined']
            
            # 分析方法的创新性
            innovation_score = self._calculate_metric_score(method, self.innovation_keywords['method'])
            
            features.append({
                'method': method,
                'keywords': keywords,
                'innovation_score': innovation_score
            })
        
        return features
    
    def _identify_method_improvements(self, methods: List[str]) -> List[Dict]:
        """识别方法改进"""
        improvements = []
        
        for method in methods:
            # 检查是否包含改进相关的关键词
            if any(keyword in method.lower() for keyword in self.innovation_keywords['improvement']):
                improvements.append({
                    'method': method,
                    'improvement_type': self._classify_improvement_type(method)
                })
        
        return improvements
    
    def _identify_new_methods(self, current_methods: List[str], all_papers: List[Dict]) -> List[str]:
        """识别新方法"""
        # 提取当前时期的方法关键词
        current_keywords = set()
        for method in current_methods:
            current_keywords.update(self.extract_keywords(method)['combined'])
        
        # 提取之前时期的方法关键词
        previous_keywords = set()
        for paper in all_papers:
            if paper not in current_methods:
                previous_methods = self._analyze_methodology(paper['abstract']).split('.')
                for method in previous_methods:
                    previous_keywords.update(self.extract_keywords(method)['combined'])
        
        # 找出新方法
        new_methods = current_keywords - previous_keywords
        return list(new_methods)
    
    def _analyze_experiment_design_trends(self, papers: List[Dict]) -> Dict:
        """分析实验设计趋势"""
        design_trends = {
            'ablation_studies': 0,
            'comparative_analysis': 0,
            'statistical_tests': 0,
            'cross_validation': 0
        }
        
        for paper in papers:
            experiments = self._analyze_experiments(paper['abstract'])
            
            # 统计各种实验设计的出现次数
            if any('ablation' in exp.lower() for exp in experiments.get('experiments', [])):
                design_trends['ablation_studies'] += 1
            
            if any('comparison' in exp.lower() for exp in experiments.get('experiments', [])):
                design_trends['comparative_analysis'] += 1
            
            if any('statistical' in exp.lower() for exp in experiments.get('experiments', [])):
                design_trends['statistical_tests'] += 1
            
            if any('cross validation' in exp.lower() for exp in experiments.get('experiments', [])):
                design_trends['cross_validation'] += 1
        
        return design_trends
    
    def _classify_improvement_type(self, method: str) -> str:
        """分类改进类型"""
        if any(keyword in method.lower() for keyword in ['efficient', 'faster', 'speed']):
            return 'efficiency'
        elif any(keyword in method.lower() for keyword in ['accurate', 'precise', 'better']):
            return 'accuracy'
        elif any(keyword in method.lower() for keyword in ['robust', 'stable', 'reliable']):
            return 'robustness'
        elif any(keyword in method.lower() for keyword in ['scalable', 'large-scale']):
            return 'scalability'
        else:
            return 'general'
    
    async def identify_research_gaps(self, papers: List[Dict]) -> List[Dict]:
        """
        识别研究空白点
        
        Args:
            papers: 论文列表，每个论文包含标题、摘要等信息
            
        Returns:
            研究空白点列表，每个空白点包含描述和相关论文
        """
        research_gaps = []
        
        # 提取所有论文的方法和结果
        methods = []
        results = []
        for paper in papers:
            abstract = paper.get('abstract', '')
            methods.extend(self._analyze_methodology(abstract).split('.'))
            results.extend(self._analyze_results(abstract).split('.'))
            
        # 清理和标准化文本
        methods = [m.strip() for m in methods if m.strip()]
        results = [r.strip() for r in results if r.strip()]
        
        # 构建方法-结果矩阵
        method_vectors = self.vectorizer.fit_transform(methods)
        result_vectors = self.vectorizer.fit_transform(results)
        
        # 计算方法和结果之间的相似度
        similarity_matrix = cosine_similarity(method_vectors, result_vectors)
        
        # 识别潜在的研究空白点
        for i, method in enumerate(methods):
            # 找出与该方法相关性较低的结果领域
            low_similarity_indices = np.where(similarity_matrix[i] < 0.3)[0]
            if len(low_similarity_indices) > 0:
                gap = {
                    'type': 'method_result_gap',
                    'description': f"现有方法'{method}'在以下结果领域可能存在改进空间",
                    'related_areas': [results[j] for j in low_similarity_indices],
                    'potential_directions': self._generate_research_directions(method, [results[j] for j in low_similarity_indices])
                }
                research_gaps.append(gap)
        
        # 分析实验方法的覆盖度
        all_experiments = []
        for paper in papers:
            abstract = paper.get('abstract', '')
            experiments = self._analyze_experiments(abstract)
            all_experiments.extend([exp for sublist in experiments.values() for exp in sublist])
        
        # 识别实验方法的空白点
        experiment_gaps = self._identify_experiment_gaps(all_experiments)
        research_gaps.extend(experiment_gaps)
        
        return research_gaps
    
    def _generate_research_directions(self, method: str, weak_areas: List[str]) -> List[str]:
        """生成研究方向建议"""
        directions = []
        
        # 基于方法和弱点区域生成建议
        for area in weak_areas:
            # 结合方法和领域的关键词
            method_keywords = self.extract_keywords(method)['combined']
            area_keywords = self.extract_keywords(area)['combined']
            
            # 生成改进建议
            suggestions = [
                f"将{method_keywords[0]}方法扩展到{area_keywords[0]}领域",
                f"开发针对{area_keywords[0]}的新型{method_keywords[0]}算法",
                f"结合{method_keywords[0]}和{area_keywords[0]}的优势",
                f"改进{method_keywords[0]}以解决{area_keywords[0]}问题"
            ]
            
            directions.extend(suggestions)
        
        return list(set(directions))  # 去除重复建议
    
    def _identify_experiment_gaps(self, experiments: List[str]) -> List[Dict]:
        """识别实验方法中的空白点"""
        gaps = []
        
        # 常见的实验要素
        essential_elements = {
            'dataset': ['benchmark', 'dataset', 'corpus'],
            'metrics': ['accuracy', 'precision', 'recall', 'F1', 'performance'],
            'baseline': ['baseline', 'comparison', 'state-of-the-art'],
            'ablation': ['ablation', 'component', 'analysis'],
            'statistical': ['significance', 'p-value', 'statistical test']
        }
        
        # 检查每个实验要素的覆盖情况
        for element, keywords in essential_elements.items():
            covered = any(any(keyword in exp.lower() for keyword in keywords) for exp in experiments)
            if not covered:
                gap = {
                    'type': 'experiment_gap',
                    'description': f"实验中缺少{element}相关的分析",
                    'suggestions': self._generate_experiment_suggestions(element)
                }
                gaps.append(gap)
        
        return gaps
    
    def _generate_experiment_suggestions(self, missing_element: str) -> List[str]:
        """生成实验改进建议"""
        suggestions = {
            'dataset': [
                "添加更多标准数据集进行评估",
                "使用跨领域数据集验证方法的泛化性",
                "构建新的针对性数据集"
            ],
            'metrics': [
                "增加多样化的评估指标",
                "添加定性和定量分析",
                "使用领域特定的评估标准"
            ],
            'baseline': [
                "添加最新的基准方法比较",
                "包含经典方法作为对照",
                "进行公平和全面的对比实验"
            ],
            'ablation': [
                "进行组件消融实验",
                "分析各模块的贡献",
                "研究参数敏感性"
            ],
            'statistical': [
                "添加统计显著性测试",
                "报告置信区间",
                "进行稳定性分析"
            ]
        }
        
        return suggestions.get(missing_element, ["完善实验设计和分析"])
    
    async def generate_innovation_suggestions(self, papers: List[Dict]) -> List[Dict]:
        """
        生成创新点建议
        
        Args:
            papers: 论文列表，每个论文包含标题、摘要等信息
            
        Returns:
            创新建议列表，每个建议包含类型、描述和具体建议
        """
        suggestions = []
        
        # 分析现有方法的优缺点
        methods = []
        limitations = []
        for paper in papers:
            abstract = paper.get('abstract', '')
            methods.extend(self._analyze_methodology(abstract).split('.'))
            limitations.extend(self._analyze_limitations(abstract).split('.'))
        
        # 清理文本
        methods = [m.strip() for m in methods if m.strip()]
        limitations = [l.strip() for l in limitations if l.strip()]
        
        # 基于方法生成改进建议
        method_suggestions = self._generate_method_improvements(methods)
        suggestions.extend(method_suggestions)
        
        # 基于局限性生成创新建议
        limitation_suggestions = self._generate_limitation_solutions(limitations)
        suggestions.extend(limitation_suggestions)
        
        # 生成跨领域应用建议
        cross_domain_suggestions = self._generate_cross_domain_applications(methods)
        suggestions.extend(cross_domain_suggestions)
        
        return suggestions
    
    def _generate_method_improvements(self, methods: List[str]) -> List[Dict]:
        """基于现有方法生成改进建议"""
        improvements = []
        
        for method in methods:
            # 提取方法的关键特征
            keywords = self.extract_keywords(method)['combined']
            
            # 生成改进建议
            improvement = {
                'type': 'method_improvement',
                'original_method': method,
                'suggestions': [
                    f"通过深度学习增强{keywords[0]}的性能",
                    f"开发{keywords[0]}的自适应版本",
                    f"设计针对{keywords[0]}的并行优化算法",
                    f"结合多模态信息改进{keywords[0]}"
                ]
            }
            improvements.append(improvement)
        
        return improvements
    
    def _generate_limitation_solutions(self, limitations: List[str]) -> List[Dict]:
        """基于局限性生成解决方案"""
        solutions = []
        
        for limitation in limitations:
            # 提取局限性的关键词
            keywords = self.extract_keywords(limitation)['combined']
            
            # 生成解决方案
            solution = {
                'type': 'limitation_solution',
                'limitation': limitation,
                'suggestions': [
                    f"开发新的算法克服{keywords[0]}问题",
                    f"使用集成学习方法解决{keywords[0]}的局限性",
                    f"引入外部知识来改善{keywords[0]}",
                    f"设计专门的模块处理{keywords[0]}"
                ]
            }
            solutions.append(solution)
        
        return solutions
    
    def _generate_cross_domain_applications(self, methods: List[str]) -> List[Dict]:
        """生成跨领域应用建议"""
        applications = []
        
        # 定义潜在的应用领域
        domains = [
            "计算机视觉",
            "自然语言处理",
            "推荐系统",
            "时间序列分析",
            "图神经网络"
        ]
        
        for method in methods:
            # 提取方法的关键特征
            keywords = self.extract_keywords(method)['combined']
            
            # 生成跨领域应用建议
            application = {
                'type': 'cross_domain_application',
                'original_method': method,
                'suggestions': [
                    f"将{keywords[0]}应用到{domain}领域" for domain in domains
                ]
            }
            applications.append(application)
        
        return applications 