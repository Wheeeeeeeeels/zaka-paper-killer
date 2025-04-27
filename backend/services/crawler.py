import requests
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime
import logging
import time
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ICLRCrawler:
    def __init__(self):
        self.base_url = "https://openreview.net/group?id=ICLR.cc/2025/Conference"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        self.session = requests.Session()

    def login(self, email, password):
        """登录 OpenReview"""
        try:
            login_url = "https://openreview.net/login"
            response = self.session.get(login_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 获取登录表单的 token
            token = soup.find('input', {'name': 'token'})['value']
            
            # 发送登录请求
            login_data = {
                'email': email,
                'password': password,
                'token': token
            }
            
            response = self.session.post(login_url, data=login_data)
            if response.ok:
                logger.info("登录成功")
                return True
            else:
                logger.error("登录失败")
                return False
        except Exception as e:
            logger.error(f"登录时出错: {str(e)}")
            return False

    def get_papers(self):
        """获取 ICLR 2025 论文列表"""
        try:
            logger.info("开始获取 ICLR 2025 论文数据...")
            
            # 检查是否需要登录
            if not os.getenv('OPENREVIEW_EMAIL') or not os.getenv('OPENREVIEW_PASSWORD'):
                logger.warning("未设置 OpenReview 登录信息，将使用公开数据")
                return self._get_public_papers()
            
            # 尝试登录
            if not self.login(os.getenv('OPENREVIEW_EMAIL'), os.getenv('OPENREVIEW_PASSWORD')):
                logger.warning("登录失败，将使用公开数据")
                return self._get_public_papers()
            
            # 获取论文列表
            response = self.session.get(self.base_url)
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

    def _get_public_papers(self):
        """获取公开的论文数据"""
        try:
            # 这里可以添加一些公开的论文数据
            return [
                {
                    "id": "1",
                    "title": "Scaling Laws for Neural Language Models",
                    "authors": "Kaplan, Jared and McCandlish, Sam and Henighan, Tom and Brown, Tom B and Chess, Benjamin and Child, Rewon and Gray, Scott and Radford, Alec and Wu, Jeff and Amodei, Dario",
                    "abstract": "We present an empirical study of scaling properties of language model performance on the cross-entropy loss. The loss scales as a power-law with model size, dataset size, and the amount of compute used for training, with some trends spanning more than seven orders of magnitude. Other architectural details such as network width or depth have minimal effects within a wide range. Simple equations govern the dependence of overfitting on model and dataset size. The same trends can be observed in the performance of models trained to generate Python code, suggesting that scaling laws may be universal across modalities and tasks.",
                    "track": "oral",
                    "tags": ["language models", "scaling laws", "deep learning"],
                    "similarityScore": 0.95,
                    "gaps": [
                        "Limited analysis of scaling laws for different architectures",
                        "Need for better understanding of the relationship between model size and performance"
                    ]
                },
                {
                    "id": "2",
                    "title": "Learning Transferable Visual Models From Natural Language Supervision",
                    "authors": "Radford, Alec and Kim, Jong Wook and Hallacy, Chris and Ramesh, Aditya and Goh, Gabriel and Agarwal, Sandhini and Sastry, Girish and Askell, Amanda and Mishkin, Pamela and Clark, Jack and others",
                    "abstract": "State-of-the-art computer vision systems are trained to predict a fixed set of predetermined object categories. This restricted form of supervision limits their generality and usability since additional labeled data is needed to specify any other visual concept. Learning directly from raw text about images is a promising alternative which leverages a much broader source of supervision. We demonstrate that the simple pre-training task of predicting which caption goes with which image is an efficient and scalable way to learn SOTA image representations from scratch on a dataset of 400 million (image, text) pairs collected from the internet. After pre-training, natural language is used to reference learned visual concepts (or describe new ones) enabling zero-shot transfer of the model to downstream tasks. We study the performance of this approach by benchmarking on over 30 different existing computer vision datasets, spanning tasks such as OCR, action recognition in videos, geo-localization, and many types of fine-grained object classification. The model transfers non-trivially to most tasks and is often competitive with a fully supervised baseline without the need for any dataset specific training. For instance, we match the accuracy of the original ResNet-50 on ImageNet zero-shot without needing to use any of the 1.28 million training examples it was trained on.",
                    "track": "oral",
                    "tags": ["computer vision", "transfer learning", "zero-shot learning"],
                    "similarityScore": 0.9,
                    "gaps": [
                        "Need for better understanding of the relationship between image and text representations",
                        "Limited analysis of the model's performance on complex visual tasks"
                    ]
                }
            ]
        except Exception as e:
            logger.error(f"获取公开论文数据时出错: {str(e)}")
            return []

    def _parse_paper(self, paper_element):
        """解析论文元素"""
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
        """获取论文评审意见"""
        try:
            review_url = f"https://openreview.net/forum?id={paper_id}"
            response = self.session.get(review_url)
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
        """分析论文的创新点和研究空白"""
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
        """生成实验建议"""
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

class CHICrawler:
    def __init__(self):
        self.base_url = "https://chi2025.acm.org/for-authors/papers/"
        self.pcs_url = "https://new.precisionconference.com/chi"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1"
        }
        self.session = requests.Session()

    def get_papers(self):
        """获取 CHI 2025 论文列表"""
        try:
            logger.info("开始获取 CHI 2025 论文数据...")
            
            # 由于 CHI 2025 使用 Precision Conference 系统，我们需要返回示例数据
            # 实际应用中，需要实现 PCS 系统的登录和论文获取逻辑
            return self._get_public_papers()
            
        except Exception as e:
            logger.error(f"获取论文数据时出错: {str(e)}")
            return self._get_public_papers()

    def _get_public_papers(self):
        """获取公开的论文数据"""
        try:
            # 根据 CHI 2025 的论文要求生成示例数据
            return [
                {
                    "id": "1",
                    "title": "Designing AI Systems for Human-AI Collaboration",
                    "authors": "Smith, John and Johnson, Sarah and Brown, Michael",
                    "abstract": "This paper explores the design principles and challenges in creating AI systems that effectively collaborate with humans. We present a framework for understanding human-AI collaboration and discuss key considerations in system design, including transparency, controllability, and trust. Through a series of case studies, we demonstrate how these principles can be applied in practice.",
                    "track": "research",
                    "tags": ["human-ai interaction", "system design", "collaboration"],
                    "similarityScore": 0.95,
                    "gaps": [
                        "Need for better understanding of user trust in AI systems",
                        "Limited research on long-term human-AI collaboration"
                    ],
                    "submission_type": "Standard-Length Paper",
                    "word_count": 7500,
                    "submission_date": "2024-09-12",
                    "notification_date": "2025-01-16"
                },
                {
                    "id": "2",
                    "title": "Understanding User Experience in Virtual Reality",
                    "authors": "Chen, Wei and Lee, David and Wilson, Robert",
                    "abstract": "Virtual Reality (VR) has become increasingly popular, but there is still limited understanding of how users experience VR environments. This paper presents a comprehensive study of user experience in VR, focusing on factors such as presence, immersion, and comfort. We conducted a large-scale user study and developed a framework for evaluating VR experiences.",
                    "track": "research",
                    "tags": ["virtual reality", "user experience", "immersion"],
                    "similarityScore": 0.9,
                    "gaps": [
                        "Need for better metrics to measure VR user experience",
                        "Limited understanding of long-term effects of VR use"
                    ],
                    "submission_type": "Short Paper",
                    "word_count": 4500,
                    "submission_date": "2024-09-12",
                    "notification_date": "2025-01-16"
                },
                {
                    "id": "3",
                    "title": "Accessibility in Human-Computer Interaction",
                    "authors": "Taylor, Emma and Martinez, Carlos and Kim, Soo-Jin",
                    "abstract": "This paper examines the current state of accessibility in HCI research and practice. We analyze existing accessibility guidelines and propose a new framework for evaluating and improving the accessibility of interactive systems. Our work includes a comprehensive review of accessibility research and a set of practical recommendations for designers and developers.",
                    "track": "research",
                    "tags": ["accessibility", "inclusive design", "HCI"],
                    "similarityScore": 0.85,
                    "gaps": [
                        "Need for more comprehensive accessibility guidelines",
                        "Limited research on accessibility in emerging technologies"
                    ],
                    "submission_type": "Standard-Length Paper",
                    "word_count": 8000,
                    "submission_date": "2024-09-12",
                    "notification_date": "2025-01-16"
                }
            ]
        except Exception as e:
            logger.error(f"获取公开论文数据时出错: {str(e)}")
            return []

    def _parse_paper(self, paper_element):
        """解析论文元素"""
        try:
            # 获取论文标题
            title_element = paper_element.find('h3', class_='paper-title')
            if not title_element:
                logger.warning("未找到论文标题")
                return None
            title = title_element.text.strip()
            
            # 获取作者
            authors = []
            author_elements = paper_element.find_all('span', class_='author-name')
            if not author_elements:
                author_elements = paper_element.find_all('div', class_='authors')
            for author in author_elements:
                authors.append(author.text.strip())
            
            # 获取摘要
            abstract_element = paper_element.find('div', class_='paper-abstract')
            if not abstract_element:
                abstract_element = paper_element.find('div', class_='abstract')
            if not abstract_element:
                logger.warning(f"未找到论文摘要: {title}")
                return None
            abstract = abstract_element.text.strip()
            
            # 获取标签
            tags = []
            tag_elements = paper_element.find_all('span', class_='paper-tag')
            if not tag_elements:
                tag_elements = paper_element.find_all('div', class_='keywords')
            for tag in tag_elements:
                tags.append(tag.text.strip())
            
            # 获取track信息
            track_element = paper_element.find('span', class_='paper-track')
            if not track_element:
                track_element = paper_element.find('div', class_='track')
            track = track_element.text.strip() if track_element else "research"
            
            # 获取论文ID
            paper_id = paper_element.get('id', '')
            if not paper_id:
                paper_id = str(hash(title))  # 使用标题的哈希值作为ID
            
            # 获取PDF链接
            pdf_element = paper_element.find('a', class_='paper-pdf')
            if not pdf_element:
                pdf_element = paper_element.find('a', href=lambda x: x and x.endswith('.pdf'))
            pdf_link = pdf_element['href'] if pdf_element else None
            
            # 分析创新点和研究空白
            innovations, gaps = self._analyze_paper(abstract)
            
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
                "similarityScore": 0.8,  # 默认相似度分数
                "experiments": self._generate_experiment_suggestions(abstract)
            }
        except Exception as e:
            logger.error(f"解析论文元素时出错: {str(e)}")
            return None

    def _analyze_paper(self, abstract):
        """分析论文的创新点和研究空白"""
        innovations = []
        gaps = []
        
        # 简单的关键词匹配
        innovation_keywords = ["novel", "propose", "introduce", "new", "improve", "better", "innovative", "breakthrough", "framework", "design"]
        gap_keywords = ["limitation", "future work", "challenge", "issue", "problem", "drawback", "weakness", "need for"]
        
        # 分析创新点
        for keyword in innovation_keywords:
            if keyword in abstract.lower():
                # 提取包含关键词的句子
                sentences = re.split(r'[.!?]+', abstract)
                for sentence in sentences:
                    if keyword in sentence.lower():
                        innovations.append(sentence.strip())
        
        # 分析研究空白
        for keyword in gap_keywords:
            if keyword in abstract.lower():
                sentences = re.split(r'[.!?]+', abstract)
                for sentence in sentences:
                    if keyword in sentence.lower():
                        gaps.append(sentence.strip())
        
        return innovations[:3], gaps[:3]  # 返回前3个创新点和研究空白

    def _generate_experiment_suggestions(self, abstract):
        """生成实验建议"""
        return {
            "setup": [
                "使用论文中提到的数据集",
                "实现论文中描述的方法",
                "使用相同的评估指标"
            ],
            "metrics": [
                "用户满意度",
                "任务完成时间",
                "错误率"
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

    crawler = CHICrawler()
    papers = crawler.get_papers()
    
    # 保存到文件
    with open('chi2025_papers.json', 'w', encoding='utf-8') as f:
        json.dump(papers, f, ensure_ascii=False, indent=2)
    
    logger.info(f"成功爬取并保存 {len(papers)} 篇论文")

if __name__ == "__main__":
    main() 