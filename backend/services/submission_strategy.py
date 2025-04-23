from typing import Dict, List
from datetime import datetime, timedelta
import json

class SubmissionStrategyService:
    def __init__(self):
        # 加载会议/期刊信息
        with open('conference_info.json', 'r') as f:
            self.conference_info = json.load(f)
    
    async def match_conference(self, 
                             paper_keywords: List[str],
                             paper_quality: str) -> List[Dict]:
        """
        匹配适合的会议/期刊
        """
        matches = []
        
        for conf in self.conference_info:
            # 计算关键词匹配度
            keyword_overlap = len(set(paper_keywords) & set(conf['keywords']))
            keyword_score = keyword_overlap / len(conf['keywords'])
            
            # 检查质量要求
            quality_match = paper_quality in conf['accepted_quality_levels']
            
            if keyword_score > 0.5 and quality_match:
                matches.append({
                    'conference': conf['name'],
                    'match_score': keyword_score,
                    'next_deadline': conf['next_deadline'],
                    'impact_factor': conf['impact_factor']
                })
        
        return sorted(matches, key=lambda x: x['match_score'], reverse=True)
    
    async def plan_submission_timeline(self, 
                                     conference: str,
                                     current_date: datetime) -> Dict:
        """
        规划投稿时间线
        """
        conf_info = next((c for c in self.conference_info if c['name'] == conference), None)
        if not conf_info:
            return {}
        
        deadline = datetime.strptime(conf_info['next_deadline'], '%Y-%m-%d')
        timeline = {
            'conference': conference,
            'deadline': deadline.strftime('%Y-%m-%d'),
            'milestones': []
        }
        
        # 添加关键时间节点
        milestones = [
            ('初稿完成', -30),
            ('同行评审', -15),
            ('修改完善', -7),
            ('最终提交', 0)
        ]
        
        for milestone, days in milestones:
            date = deadline + timedelta(days=days)
            timeline['milestones'].append({
                'name': milestone,
                'date': date.strftime('%Y-%m-%d'),
                'days_until_deadline': days
            })
        
        return timeline
    
    async def analyze_review_comments(self, comments: List[str]) -> Dict:
        """
        分析审稿意见
        """
        # TODO: 实现审稿意见分析逻辑
        return {
            'major_issues': [],
            'minor_issues': [],
            'suggestions': []
        } 