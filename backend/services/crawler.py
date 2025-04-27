import requests
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime
import logging
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ICLRCrawler:
    def __init__(self):
        self.base_url = "https://openreview.net/group?id=ICLR.cc/2024/Conference"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    def get_papers(self):
        try:
            logger.info("开始获取 ICLR 2024 论文数据...")
            response = requests.get(self.base_url, headers=self.headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            papers = []
            paper_elements = soup.find_all('div', class_='note')
            
            for paper in paper_elements:
                try:
                    paper_data = self._parse_paper(paper)
                    if paper_data:
                        papers.append(paper_data)
                        logger.info(f"成功解析论文: {paper_data['title']}")
                except Exception as e:
                    logger.error(f"解析论文时出错: {str(e)}")
                    continue
                
                # 添加延迟以避免请求过快
                time.sleep(0.5)
            
            logger.info(f"成功获取 {len(papers)} 篇论文")
            return papers
        except Exception as e:
            logger.error(f"获取论文数据时出错: {str(e)}")
            return []

    def _parse_paper(self, paper_element):
        try:
            # 获取论文标题
            title_element = paper_element.find('h4', class_='note-content-title')
            if not title_element:
                return None
            title = title_element.text.strip()
            
            # 获取作者
            authors = []
            author_elements = paper_element.find_all('a', class_='note-content-author')
            for author in author_elements:
                authors.append(author.text.strip())
            
            # 获取摘要
            abstract_element = paper_element.find('div', class_='note-content-abstract')
            if not abstract_element:
                return None
            abstract = abstract_element.text.strip()
            
            # 获取标签
            tags = []
            tag_elements = paper_element.find_all('span', class_='note-content-tag')
            for tag in tag_elements:
                tags.append(tag.text.strip())
            
            # 获取track信息
            track_element = paper_element.find('span', class_='note-content-track')
            track = track_element.text.strip() if track_element else "unknown"
            
            # 获取论文ID
            paper_id = paper_element.get('id', '')
            
            # 获取PDF链接
            pdf_element = paper_element.find('a', class_='note-content-pdf')
            pdf_link = pdf_element['href'] if pdf_element else None
            
            # 获取评审意见
            reviews = self._get_reviews(paper_id)
            
            # 分析创新点和研究空白
            innovations, gaps = self._analyze_paper(abstract, reviews)
            
            return {
                "id": paper_id,
                "title": title,
                "authors": authors,
                "abstract": abstract,
                "tags": tags,
                "track": track,
                "pdf_link": pdf_link,
                "innovations": innovations,
                "gaps": gaps,
                "reviews": reviews,
                "similarityScore": 0.8,  # 默认相似度分数
                "experiments": self._generate_experiment_suggestions(abstract, reviews)
            }
        except Exception as e:
            logger.error(f"解析论文元素时出错: {str(e)}")
            return None

    def _get_reviews(self, paper_id):
        try:
            review_url = f"https://openreview.net/forum?id={paper_id}"
            response = requests.get(review_url, headers=self.headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            reviews = []
            review_elements = soup.find_all('div', class_='note-content-review')
            
            for review in review_elements:
                review_text = review.text.strip()
                reviews.append(review_text)
            
            return reviews
        except Exception as e:
            logger.error(f"获取评审意见时出错: {str(e)}")
            return []

    def _analyze_paper(self, abstract, reviews):
        # 使用NLP技术分析论文的创新点和研究空白
        innovations = []
        gaps = []
        
        # 简单的关键词匹配
        innovation_keywords = ["novel", "propose", "introduce", "new", "improve", "better", "innovative", "breakthrough"]
        gap_keywords = ["limitation", "future work", "challenge", "issue", "problem", "drawback", "weakness"]
        
        text = abstract + " " + " ".join(reviews)
        
        # 分析创新点
        for keyword in innovation_keywords:
            if keyword in text.lower():
                # 提取包含关键词的句子
                sentences = re.split(r'[.!?]+', text)
                for sentence in sentences:
                    if keyword in sentence.lower():
                        innovations.append(sentence.strip())
        
        # 分析研究空白
        for keyword in gap_keywords:
            if keyword in text.lower():
                sentences = re.split(r'[.!?]+', text)
                for sentence in sentences:
                    if keyword in sentence.lower():
                        gaps.append(sentence.strip())
        
        return innovations[:3], gaps[:3]  # 返回前3个创新点和研究空白

    def _generate_experiment_suggestions(self, abstract, reviews):
        # 基于论文内容和评审意见生成实验建议
        return {
            "setup": [
                "使用论文中提到的数据集",
                "实现论文中描述的方法",
                "使用相同的评估指标"
            ],
            "metrics": [
                "准确率",
                "计算效率",
                "模型大小"
            ],
            "baselines": [
                "论文中提到的基线方法",
                "相关领域的最新方法",
                "经典方法"
            ]
        }

def main():
    crawler = ICLRCrawler()
    papers = crawler.get_papers()
    
    # 保存到文件
    with open('iclr2025_papers.json', 'w', encoding='utf-8') as f:
        json.dump(papers, f, ensure_ascii=False, indent=2)
    
    logger.info(f"成功爬取并保存 {len(papers)} 篇论文")

if __name__ == "__main__":
    main() 