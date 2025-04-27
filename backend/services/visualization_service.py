from typing import List, Dict, Any
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
from datetime import datetime
import numpy as np
from collections import Counter
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import json
import os
from .visualization_config import VisualizationConfig

class VisualizationService:
    def __init__(self):
        # 设置中文字体支持
        plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
        plt.rcParams['axes.unicode_minus'] = False
        
        # 创建输出目录
        self.output_dir = "static/visualizations"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def generate_trend_visualizations(self, time_series: Dict[str, List]) -> Dict[str, str]:
        """生成趋势相关的可视化图表"""
        visualizations = {}
        
        # 生成论文数量趋势图
        paper_count_fig = self._create_paper_count_trend(time_series)
        visualizations['paper_count_trend'] = self._save_figure(paper_count_fig, 'paper_count_trend')
        
        # 生成引用趋势图
        citation_fig = self._create_citation_trend(time_series)
        visualizations['citation_trend'] = self._save_figure(citation_fig, 'citation_trend')
        
        # 生成关键词热力图
        keyword_heatmap = self._create_keyword_heatmap(time_series)
        visualizations['keyword_heatmap'] = self._save_figure(keyword_heatmap, 'keyword_heatmap')
        
        return visualizations
    
    def generate_topic_evolution_visualizations(self, topic_evolution: List[Dict]) -> Dict[str, str]:
        """生成主题演化相关的可视化图表"""
        visualizations = {}
        
        # 生成主题演化图
        topic_evolution_fig = self._create_topic_evolution_chart(topic_evolution)
        visualizations['topic_evolution'] = self._save_figure(topic_evolution_fig, 'topic_evolution')
        
        # 生成新兴主题图
        emerging_topics_fig = self._create_emerging_topics_chart(topic_evolution)
        visualizations['emerging_topics'] = self._save_figure(emerging_topics_fig, 'emerging_topics')
        
        return visualizations
    
    def generate_citation_visualizations(self, citation_trends: Dict) -> Dict[str, str]:
        """生成引用相关的可视化图表"""
        visualizations = {}
        
        # 生成引用网络图
        citation_network_fig = self._create_citation_network(citation_trends['citation_networks'])
        visualizations['citation_network'] = self._save_figure(citation_network_fig, 'citation_network')
        
        # 生成引用影响力图
        citation_impact_fig = self._create_citation_impact_chart(citation_trends['citation_impact'])
        visualizations['citation_impact'] = self._save_figure(citation_impact_fig, 'citation_impact')
        
        return visualizations
    
    def generate_methodology_visualizations(self, methodology_evolution: List[Dict]) -> Dict[str, str]:
        """生成方法演化相关的可视化图表"""
        visualizations = {}
        
        # 生成方法演化图
        method_evolution_fig = self._create_method_evolution_chart(methodology_evolution)
        visualizations['method_evolution'] = self._save_figure(method_evolution_fig, 'method_evolution')
        
        # 生成方法改进图
        method_improvements_fig = self._create_method_improvements_chart(methodology_evolution)
        visualizations['method_improvements'] = self._save_figure(method_improvements_fig, 'method_improvements')
        
        return visualizations
    
    def generate_experiment_visualizations(self, experiment_trends: Dict) -> Dict[str, str]:
        """生成实验趋势相关的可视化图表"""
        visualizations = {}
        
        # 生成数据集使用趋势图
        dataset_trend_fig = self._create_dataset_trend_chart(experiment_trends['dataset_usage'])
        visualizations['dataset_trend'] = self._save_figure(dataset_trend_fig, 'dataset_trend')
        
        # 生成评估指标演化图
        metric_evolution_fig = self._create_metric_evolution_chart(experiment_trends['metric_evolution'])
        visualizations['metric_evolution'] = self._save_figure(metric_evolution_fig, 'metric_evolution')
        
        # 生成实验设计趋势图
        design_trend_fig = self._create_design_trend_chart(experiment_trends['experiment_design'])
        visualizations['design_trend'] = self._save_figure(design_trend_fig, 'design_trend')
        
        return visualizations
    
    def _create_paper_count_trend(self, time_series: Dict[str, List]) -> go.Figure:
        """创建论文数量趋势图"""
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=time_series['years'],
            y=time_series['paper_counts'],
            mode='lines+markers',
            name='论文数量'
        ))
        
        # 应用配置
        config = VisualizationConfig.get_trend_chart_config()
        fig = VisualizationConfig.apply_config(fig, config)
        
        return fig
    
    def _create_citation_trend(self, time_series: Dict[str, List]) -> go.Figure:
        """创建引用趋势图"""
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=time_series['years'],
            y=time_series['citation_counts'],
            mode='lines+markers',
            name='引用数量'
        ))
        
        # 应用配置
        config = VisualizationConfig.get_citation_chart_config()
        fig = VisualizationConfig.apply_config(fig, config)
        
        return fig
    
    def _create_keyword_heatmap(self, time_series: Dict[str, List]) -> go.Figure:
        """创建关键词热力图"""
        # 提取所有年份的关键词
        all_keywords = set()
        for year_freq in time_series['keyword_frequencies']:
            all_keywords.update(year_freq.keys())
        
        # 创建热力图数据
        heatmap_data = []
        for year_freq in time_series['keyword_frequencies']:
            row = [year_freq.get(keyword, 0) for keyword in all_keywords]
            heatmap_data.append(row)
        
        fig = go.Figure(data=go.Heatmap(
            z=heatmap_data,
            x=list(all_keywords),
            y=time_series['years']
        ))
        
        # 应用配置
        config = VisualizationConfig.get_keyword_heatmap_config()
        fig = VisualizationConfig.apply_config(fig, config)
        
        return fig
    
    def _create_topic_evolution_chart(self, topic_evolution: List[Dict]) -> go.Figure:
        """创建主题演化图"""
        fig = go.Figure()
        
        # 为每个时期创建一条线
        for period in topic_evolution:
            keywords = list(period['top_keywords'].keys())
            values = list(period['top_keywords'].values())
            
            fig.add_trace(go.Scatter(
                x=keywords,
                y=values,
                mode='lines+markers',
                name=f'时期 {period["period"]}'
            ))
        
        # 应用配置
        config = VisualizationConfig.get_topic_evolution_config()
        fig = VisualizationConfig.apply_config(fig, config)
        
        return fig
    
    def _create_emerging_topics_chart(self, topic_evolution: List[Dict]) -> go.Figure:
        """创建新兴主题图"""
        fig = go.Figure()
        
        # 收集所有新兴主题
        all_emerging_topics = set()
        for period in topic_evolution:
            all_emerging_topics.update(period['emerging_topics'])
        
        # 为每个时期创建柱状图
        for period in topic_evolution:
            emerging_topics = period['emerging_topics']
            values = [1] * len(emerging_topics)
            
            fig.add_trace(go.Bar(
                x=emerging_topics,
                y=values,
                name=f'时期 {period["period"]}'
            ))
        
        # 应用配置
        config = VisualizationConfig.get_topic_evolution_config()
        fig = VisualizationConfig.apply_config(fig, config)
        
        return fig
    
    def _create_citation_network(self, citation_networks: List[Dict]) -> go.Figure:
        """创建引用网络图"""
        # 创建网络图
        G = nx.Graph()
        
        # 添加节点和边
        for network in citation_networks:
            paper = network['paper']
            G.add_node(paper)
            
            for cited_paper in network['cited_papers']:
                G.add_node(cited_paper)
                G.add_edge(paper, cited_paper)
        
        # 使用spring布局
        pos = nx.spring_layout(G)
        
        # 创建图形
        fig = go.Figure()
        
        # 添加边
        edge_x = []
        edge_y = []
        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])
        
        fig.add_trace(go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=0.5),
            hoverinfo='none',
            mode='lines'
        ))
        
        # 添加节点
        node_x = []
        node_y = []
        node_text = []
        for node in G.nodes():
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)
            node_text.append(node)
        
        fig.add_trace(go.Scatter(
            x=node_x, y=node_y,
            mode='markers+text',
            hoverinfo='text',
            text=node_text,
            marker=dict(
                showscale=True,
                colorscale='YlGnBu',
                size=10
            )
        ))
        
        # 应用配置
        config = VisualizationConfig.get_citation_network_config()
        fig = VisualizationConfig.apply_config(fig, config)
        
        return fig
    
    def _create_citation_impact_chart(self, citation_impact: Dict) -> go.Figure:
        """创建引用影响力图"""
        fig = go.Figure(data=[
            go.Bar(
                x=list(citation_impact.keys()),
                y=list(citation_impact.values()),
                text=list(citation_impact.values()),
                textposition='auto'
            )
        ])
        
        # 应用配置
        config = VisualizationConfig.get_citation_chart_config()
        fig = VisualizationConfig.apply_config(fig, config)
        
        return fig
    
    def _create_method_evolution_chart(self, methodology_evolution: List[Dict]) -> go.Figure:
        """创建方法演化图"""
        fig = go.Figure()
        
        # 为每个时期创建一条线
        for period in methodology_evolution:
            methods = [m['method'] for m in period['methods']]
            innovation_scores = [m['innovation_score'] for m in period['methods']]
            
            fig.add_trace(go.Scatter(
                x=methods,
                y=innovation_scores,
                mode='lines+markers',
                name=f'时期 {period["period"]}'
            ))
        
        # 应用配置
        config = VisualizationConfig.get_method_evolution_config()
        fig = VisualizationConfig.apply_config(fig, config)
        
        return fig
    
    def _create_method_improvements_chart(self, methodology_evolution: List[Dict]) -> go.Figure:
        """创建方法改进图"""
        fig = go.Figure()
        
        # 收集所有改进类型
        improvement_types = set()
        for period in methodology_evolution:
            for improvement in period['method_improvements']:
                improvement_types.add(improvement['improvement_type'])
        
        # 为每个时期创建柱状图
        for period in methodology_evolution:
            improvements = period['method_improvements']
            improvement_counts = Counter([imp['improvement_type'] for imp in improvements])
            
            fig.add_trace(go.Bar(
                x=list(improvement_types),
                y=[improvement_counts.get(t, 0) for t in improvement_types],
                name=f'时期 {period["period"]}'
            ))
        
        # 应用配置
        config = VisualizationConfig.get_method_evolution_config()
        fig = VisualizationConfig.apply_config(fig, config)
        
        return fig
    
    def _create_dataset_trend_chart(self, dataset_usage: Dict) -> go.Figure:
        """创建数据集使用趋势图"""
        fig = go.Figure(data=[
            go.Bar(
                x=list(dataset_usage.keys()),
                y=list(dataset_usage.values()),
                text=list(dataset_usage.values()),
                textposition='auto'
            )
        ])
        
        # 应用配置
        config = VisualizationConfig.get_experiment_trend_config()
        fig = VisualizationConfig.apply_config(fig, config)
        
        return fig
    
    def _create_metric_evolution_chart(self, metric_evolution: Dict) -> go.Figure:
        """创建评估指标演化图"""
        fig = go.Figure(data=[
            go.Bar(
                x=list(metric_evolution.keys()),
                y=list(metric_evolution.values()),
                text=list(metric_evolution.values()),
                textposition='auto'
            )
        ])
        
        # 应用配置
        config = VisualizationConfig.get_experiment_trend_config()
        fig = VisualizationConfig.apply_config(fig, config)
        
        return fig
    
    def _create_design_trend_chart(self, design_trends: Dict) -> go.Figure:
        """创建实验设计趋势图"""
        fig = go.Figure(data=[
            go.Bar(
                x=list(design_trends.keys()),
                y=list(design_trends.values()),
                text=list(design_trends.values()),
                textposition='auto'
            )
        ])
        
        # 应用配置
        config = VisualizationConfig.get_experiment_trend_config()
        fig = VisualizationConfig.apply_config(fig, config)
        
        return fig
    
    def _save_figure(self, fig: go.Figure, filename: str) -> str:
        """保存图表并返回文件路径"""
        filepath = os.path.join(self.output_dir, f"{filename}.html")
        fig.write_html(filepath)
        return filepath 