from typing import Dict, List, Any
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns

class ExperimentAnalysisService:
    def __init__(self):
        self.plt = plt
        self.sns = sns
        
    async def analyze_experiment_results(self, data: Dict[str, List[float]]) -> Dict:
        """
        分析实验结果
        """
        analysis_results = {}
        
        for group, values in data.items():
            analysis_results[group] = {
                'mean': np.mean(values),
                'std': np.std(values),
                'median': np.median(values),
                'min': np.min(values),
                'max': np.max(values)
            }
        
        return analysis_results
    
    async def perform_statistical_test(self, 
                                     group1: List[float], 
                                     group2: List[float]) -> Dict:
        """
        执行统计检验
        """
        # 正态性检验
        normality1 = stats.normaltest(group1)
        normality2 = stats.normaltest(group2)
        
        # 方差齐性检验
        variance_test = stats.levene(group1, group2)
        
        # t检验
        t_test = stats.ttest_ind(group1, group2)
        
        return {
            'normality_test': {
                'group1': normality1.pvalue,
                'group2': normality2.pvalue
            },
            'variance_test': variance_test.pvalue,
            't_test': t_test.pvalue
        }
    
    async def generate_visualization(self, 
                                   data: Dict[str, List[float]], 
                                   plot_type: str = 'boxplot') -> str:
        """
        生成数据可视化
        """
        plt.figure(figsize=(10, 6))
        
        if plot_type == 'boxplot':
            self.sns.boxplot(data=[data[group] for group in data.keys()])
            plt.xticks(range(len(data)), data.keys())
        elif plot_type == 'violin':
            self.sns.violinplot(data=[data[group] for group in data.keys()])
            plt.xticks(range(len(data)), data.keys())
        
        plt.title('Experiment Results Visualization')
        plt.ylabel('Values')
        
        # 保存图片
        plt.savefig('experiment_results.png')
        plt.close()
        
        return 'experiment_results.png' 