from typing import Dict, Any
import plotly.graph_objects as go
import plotly.express as px

class VisualizationConfig:
    """可视化配置类，定义图表的样式和交互设置"""
    
    # 颜色方案
    COLORS = {
        'primary': '#1f77b4',
        'secondary': '#ff7f0e',
        'tertiary': '#2ca02c',
        'quaternary': '#d62728',
        'background': '#ffffff',
        'grid': '#e5e5e5',
        'text': '#333333'
    }
    
    # 字体设置
    FONTS = {
        'family': 'Arial, sans-serif',
        'size': 12,
        'color': '#333333'
    }
    
    # 布局设置
    LAYOUT = {
        'template': 'plotly_white',
        'paper_bgcolor': COLORS['background'],
        'plot_bgcolor': COLORS['background'],
        'font': FONTS,
        'margin': dict(t=40, b=20, l=5, r=5),
        'showlegend': True,
        'legend': dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='right',
            x=1
        )
    }
    
    # 交互设置
    INTERACTION = {
        'hovermode': 'closest',
        'hoverlabel': dict(
            bgcolor=COLORS['background'],
            font_size=FONTS['size'],
            font_family=FONTS['family']
        )
    }
    
    @classmethod
    def get_trend_chart_config(cls) -> Dict[str, Any]:
        """获取趋势图配置"""
        return {
            'layout': {
                **cls.LAYOUT,
                'title': dict(
                    text='论文发表趋势',
                    font=dict(size=16, color=cls.COLORS['text'])
                ),
                'xaxis': dict(
                    title='年份',
                    gridcolor=cls.COLORS['grid'],
                    showgrid=True
                ),
                'yaxis': dict(
                    title='论文数量',
                    gridcolor=cls.COLORS['grid'],
                    showgrid=True
                )
            },
            'style': {
                'line': dict(
                    color=cls.COLORS['primary'],
                    width=2
                ),
                'marker': dict(
                    size=8,
                    color=cls.COLORS['primary']
                )
            }
        }
    
    @classmethod
    def get_citation_chart_config(cls) -> Dict[str, Any]:
        """获取引用图配置"""
        return {
            'layout': {
                **cls.LAYOUT,
                'title': dict(
                    text='引用趋势分析',
                    font=dict(size=16, color=cls.COLORS['text'])
                ),
                'xaxis': dict(
                    title='年份',
                    gridcolor=cls.COLORS['grid'],
                    showgrid=True
                ),
                'yaxis': dict(
                    title='引用数量',
                    gridcolor=cls.COLORS['grid'],
                    showgrid=True
                )
            },
            'style': {
                'line': dict(
                    color=cls.COLORS['secondary'],
                    width=2
                ),
                'marker': dict(
                    size=8,
                    color=cls.COLORS['secondary']
                )
            }
        }
    
    @classmethod
    def get_keyword_heatmap_config(cls) -> Dict[str, Any]:
        """获取关键词热力图配置"""
        return {
            'layout': {
                **cls.LAYOUT,
                'title': dict(
                    text='关键词频率热力图',
                    font=dict(size=16, color=cls.COLORS['text'])
                ),
                'xaxis': dict(
                    title='关键词',
                    gridcolor=cls.COLORS['grid'],
                    showgrid=True
                ),
                'yaxis': dict(
                    title='年份',
                    gridcolor=cls.COLORS['grid'],
                    showgrid=True
                )
            },
            'style': {
                'colorscale': 'Viridis',
                'showscale': True,
                'colorbar': dict(
                    title='频率',
                    titleside='right'
                )
            }
        }
    
    @classmethod
    def get_topic_evolution_config(cls) -> Dict[str, Any]:
        """获取主题演化图配置"""
        return {
            'layout': {
                **cls.LAYOUT,
                'title': dict(
                    text='主题演化趋势',
                    font=dict(size=16, color=cls.COLORS['text'])
                ),
                'xaxis': dict(
                    title='关键词',
                    gridcolor=cls.COLORS['grid'],
                    showgrid=True
                ),
                'yaxis': dict(
                    title='频率',
                    gridcolor=cls.COLORS['grid'],
                    showgrid=True
                )
            },
            'style': {
                'line': dict(
                    width=2
                ),
                'marker': dict(
                    size=8
                )
            }
        }
    
    @classmethod
    def get_citation_network_config(cls) -> Dict[str, Any]:
        """获取引用网络图配置"""
        return {
            'layout': {
                **cls.LAYOUT,
                'title': dict(
                    text='引用网络分析',
                    font=dict(size=16, color=cls.COLORS['text'])
                ),
                'showlegend': False,
                'hovermode': 'closest'
            },
            'style': {
                'edge': dict(
                    color=cls.COLORS['grid'],
                    width=0.5
                ),
                'node': dict(
                    colorscale='YlGnBu',
                    size=10,
                    showscale=True,
                    colorbar=dict(
                        title='节点中心度',
                        titleside='right'
                    )
                )
            }
        }
    
    @classmethod
    def get_method_evolution_config(cls) -> Dict[str, Any]:
        """获取方法演化图配置"""
        return {
            'layout': {
                **cls.LAYOUT,
                'title': dict(
                    text='方法创新性演化',
                    font=dict(size=16, color=cls.COLORS['text'])
                ),
                'xaxis': dict(
                    title='方法',
                    gridcolor=cls.COLORS['grid'],
                    showgrid=True
                ),
                'yaxis': dict(
                    title='创新性得分',
                    gridcolor=cls.COLORS['grid'],
                    showgrid=True
                )
            },
            'style': {
                'line': dict(
                    width=2
                ),
                'marker': dict(
                    size=8
                )
            }
        }
    
    @classmethod
    def get_experiment_trend_config(cls) -> Dict[str, Any]:
        """获取实验趋势图配置"""
        return {
            'layout': {
                **cls.LAYOUT,
                'title': dict(
                    text='实验设计趋势',
                    font=dict(size=16, color=cls.COLORS['text'])
                ),
                'xaxis': dict(
                    title='实验类型',
                    gridcolor=cls.COLORS['grid'],
                    showgrid=True
                ),
                'yaxis': dict(
                    title='使用次数',
                    gridcolor=cls.COLORS['grid'],
                    showgrid=True
                )
            },
            'style': {
                'bar': dict(
                    color=cls.COLORS['primary']
                )
            }
        }
    
    @classmethod
    def apply_config(cls, fig: go.Figure, config: Dict[str, Any]) -> go.Figure:
        """应用配置到图表"""
        # 应用布局配置
        fig.update_layout(**config['layout'])
        
        # 应用样式配置
        if 'style' in config:
            for trace in fig.data:
                if 'line' in config['style'] and hasattr(trace, 'line'):
                    trace.line.update(**config['style']['line'])
                if 'marker' in config['style'] and hasattr(trace, 'marker'):
                    trace.marker.update(**config['style']['marker'])
                if 'bar' in config['style'] and hasattr(trace, 'marker'):
                    trace.marker.update(**config['style']['bar'])
        
        return fig 