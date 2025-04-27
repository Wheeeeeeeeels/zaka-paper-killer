from typing import List, Dict, Any
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import pandas as pd
from datetime import datetime, timedelta
import joblib
import os

class PredictionService:
    def __init__(self):
        # 创建模型存储目录
        self.model_dir = "models"
        os.makedirs(self.model_dir, exist_ok=True)
        
        # 初始化模型
        self.trend_model = None
        self.impact_model = None
        self.scaler = StandardScaler()
    
    def predict_trends(self, historical_data: Dict[str, List], prediction_horizon: int = 5) -> Dict[str, List]:
        """
        预测未来趋势
        
        Args:
            historical_data: 历史数据，包含年份、论文数量、引用数量等
            prediction_horizon: 预测时间跨度（年）
            
        Returns:
            预测结果，包含未来几年的趋势预测
        """
        # 准备训练数据
        X = np.array(range(len(historical_data['years']))).reshape(-1, 1)
        y_papers = np.array(historical_data['paper_counts'])
        y_citations = np.array(historical_data['citation_counts'])
        
        # 训练论文数量预测模型
        self.trend_model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.trend_model.fit(X, y_papers)
        
        # 训练引用数量预测模型
        self.impact_model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.impact_model.fit(X, y_citations)
        
        # 生成预测时间点
        last_year = int(historical_data['years'][-1])
        future_years = [str(last_year + i + 1) for i in range(prediction_horizon)]
        X_future = np.array(range(len(historical_data['years']), 
                                 len(historical_data['years']) + prediction_horizon)).reshape(-1, 1)
        
        # 预测论文数量
        paper_predictions = self.trend_model.predict(X_future)
        
        # 预测引用数量
        citation_predictions = self.impact_model.predict(X_future)
        
        # 预测关键词趋势
        keyword_predictions = self._predict_keyword_trends(historical_data['keyword_frequencies'], 
                                                        prediction_horizon)
        
        return {
            'years': future_years,
            'paper_predictions': paper_predictions.tolist(),
            'citation_predictions': citation_predictions.tolist(),
            'keyword_predictions': keyword_predictions
        }
    
    def predict_paper_impact(self, paper_features: Dict[str, Any]) -> Dict[str, float]:
        """
        预测论文影响力
        
        Args:
            paper_features: 论文特征，包含标题、摘要、作者等信息
            
        Returns:
            影响力预测结果
        """
        # 提取特征
        features = self._extract_paper_features(paper_features)
        
        # 标准化特征
        features_scaled = self.scaler.transform([features])
        
        # 预测影响力
        impact_score = self.impact_model.predict(features_scaled)[0]
        
        return {
            'impact_score': float(impact_score),
            'confidence': self._calculate_prediction_confidence(features_scaled)
        }
    
    def _predict_keyword_trends(self, historical_keywords: List[Dict], prediction_horizon: int) -> List[Dict]:
        """预测关键词趋势"""
        # 收集所有关键词
        all_keywords = set()
        for year_keywords in historical_keywords:
            all_keywords.update(year_keywords.keys())
        
        # 为每个关键词创建时间序列
        keyword_trends = {}
        for keyword in all_keywords:
            values = [year_keywords.get(keyword, 0) for year_keywords in historical_keywords]
            if len(values) > 1:  # 只预测有足够历史数据的关键词
                X = np.array(range(len(values))).reshape(-1, 1)
                y = np.array(values)
                
                # 训练模型
                model = LinearRegression()
                model.fit(X, y)
                
                # 预测未来趋势
                X_future = np.array(range(len(values), len(values) + prediction_horizon)).reshape(-1, 1)
                predictions = model.predict(X_future)
                
                keyword_trends[keyword] = predictions.tolist()
        
        return keyword_trends
    
    def _extract_paper_features(self, paper_features: Dict[str, Any]) -> List[float]:
        """提取论文特征"""
        features = []
        
        # 标题长度
        features.append(len(paper_features.get('title', '')))
        
        # 摘要长度
        features.append(len(paper_features.get('abstract', '')))
        
        # 作者数量
        features.append(len(paper_features.get('authors', [])))
        
        # 引用数量
        features.append(paper_features.get('citation_count', 0))
        
        # 关键词数量
        features.append(len(paper_features.get('keywords', [])))
        
        # 方法创新性得分
        features.append(paper_features.get('innovation_score', 0))
        
        # 实验完整性得分
        features.append(paper_features.get('experiment_score', 0))
        
        return features
    
    def _calculate_prediction_confidence(self, features_scaled: np.ndarray) -> float:
        """计算预测置信度"""
        # 使用特征的标准差作为置信度指标
        confidence = 1.0 - np.std(features_scaled)
        return float(max(0.0, min(1.0, confidence)))
    
    def save_models(self):
        """保存模型"""
        if self.trend_model:
            joblib.dump(self.trend_model, os.path.join(self.model_dir, 'trend_model.joblib'))
        if self.impact_model:
            joblib.dump(self.impact_model, os.path.join(self.model_dir, 'impact_model.joblib'))
        joblib.dump(self.scaler, os.path.join(self.model_dir, 'scaler.joblib'))
    
    def load_models(self):
        """加载模型"""
        trend_model_path = os.path.join(self.model_dir, 'trend_model.joblib')
        impact_model_path = os.path.join(self.model_dir, 'impact_model.joblib')
        scaler_path = os.path.join(self.model_dir, 'scaler.joblib')
        
        if os.path.exists(trend_model_path):
            self.trend_model = joblib.load(trend_model_path)
        if os.path.exists(impact_model_path):
            self.impact_model = joblib.load(impact_model_path)
        if os.path.exists(scaler_path):
            self.scaler = joblib.load(scaler_path) 