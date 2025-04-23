import os
import shutil
from typing import Dict, Any, Optional, List, Tuple
from fastapi import UploadFile, HTTPException
import PyPDF2
from pathlib import Path
import re
from datetime import datetime
import asyncio
from concurrent.futures import ThreadPoolExecutor
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
import spacy
import logging
from functools import lru_cache
import time

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FileService:
    def __init__(self):
        self.upload_dir = Path("uploads")
        self.upload_dir.mkdir(exist_ok=True)
        self.max_file_size = 10 * 1024 * 1024  # 10MB
        self.allowed_extensions = {'.pdf'}
        self.executor = ThreadPoolExecutor(max_workers=4)
        
        try:
            # 下载必要的NLTK数据
            nltk.download('punkt', quiet=True)
            nltk.download('stopwords', quiet=True)
            nltk.download('wordnet', quiet=True)
            nltk.download('averaged_perceptron_tagger', quiet=True)
            
            # 加载spaCy模型
            self.nlp = spacy.load("en_core_web_sm")
            
            # 初始化TF-IDF向量化器
            self.vectorizer = TfidfVectorizer(
                max_features=100,
                stop_words='english',
                ngram_range=(1, 3)
            )
        except Exception as e:
            logger.error(f"初始化失败: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="服务初始化失败，请稍后重试"
            )

    async def save_upload_file(self, file: UploadFile) -> str:
        """保存上传的文件"""
        start_time = time.time()
        try:
            # 验证文件大小
            file_size = 0
            chunk_size = 8192
            while chunk := await file.read(chunk_size):
                file_size += len(chunk)
                if file_size > self.max_file_size:
                    raise HTTPException(
                        status_code=400,
                        detail=f"文件大小超过限制（{self.max_file_size/1024/1024}MB）"
                    )
            await file.seek(0)

            # 验证文件扩展名
            file_ext = Path(file.filename).suffix.lower()
            if file_ext not in self.allowed_extensions:
                raise HTTPException(
                    status_code=400,
                    detail=f"不支持的文件类型，仅支持PDF文件"
                )

            # 生成唯一文件名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_filename = f"{timestamp}_{file.filename}"
            file_path = self.upload_dir / safe_filename

            # 保存文件
            with file_path.open("wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            logger.info(f"文件保存成功: {file_path}, 耗时: {time.time() - start_time:.2f}秒")
            return str(file_path)
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"文件保存失败: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"文件保存失败: {str(e)}"
            )

    async def extract_pdf_info(self, file_path: str) -> Dict[str, Any]:
        """从PDF文件中提取信息"""
        start_time = time.time()
        try:
            # 使用线程池执行PDF解析
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                self.executor,
                self._extract_pdf_info_sync,
                file_path
            )
            logger.info(f"PDF解析成功: {file_path}, 耗时: {time.time() - start_time:.2f}秒")
            return result
        except Exception as e:
            logger.error(f"PDF解析失败: {str(e)}")
            raise HTTPException(
                status_code=400,
                detail=f"PDF解析失败: {str(e)}"
            )

    @lru_cache(maxsize=100)
    def _extract_pdf_info_sync(self, file_path: str) -> Dict[str, Any]:
        """同步执行PDF解析（使用缓存）"""
        try:
            with open(file_path, 'rb') as file:
                # 创建PDF阅读器对象
                pdf_reader = PyPDF2.PdfReader(file)
                
                # 获取页数
                num_pages = len(pdf_reader.pages)
                
                # 提取前两页文本
                text = ""
                for i in range(min(2, num_pages)):
                    text += pdf_reader.pages[i].extract_text() + "\n"
                
                # 使用spaCy进行文本分析
                doc = self.nlp(text)
                
                # 提取标题和摘要
                title, abstract = self._extract_title_and_abstract(doc)
                
                # 提取作者信息
                authors = self._extract_authors(doc)
                
                # 提取会议/期刊信息
                conference = self._extract_conference(doc)
                
                # 提取年份
                year = self._extract_year(doc)
                
                # 提取关键词
                keywords = self._extract_keywords(doc)
                
                return {
                    "title": title,
                    "abstract": abstract,
                    "authors": authors,
                    "conference": conference,
                    "year": year,
                    "keywords": keywords,
                    "num_pages": num_pages,
                    "file_path": file_path
                }
        except Exception as e:
            logger.error(f"PDF解析失败: {str(e)}")
            raise

    def _extract_title_and_abstract(self, doc: spacy.tokens.Doc) -> Tuple[str, str]:
        """提取标题和摘要"""
        try:
            sentences = list(doc.sents)
            title = ""
            abstract = ""
            in_abstract = False
            
            for sent in sentences:
                text = sent.text.strip()
                if not text:
                    continue
                
                # 如果还没有找到标题，当前句子就是标题
                if not title:
                    title = text
                    continue
                
                # 检查是否进入摘要部分
                if "abstract" in text.lower():
                    in_abstract = True
                    continue
                
                # 如果在摘要部分，收集摘要内容
                if in_abstract:
                    if len(abstract) > 1000:  # 限制摘要长度
                        break
                    abstract += text + " "
            
            return title, abstract.strip()
        except Exception as e:
            logger.error(f"提取标题和摘要失败: {str(e)}")
            return "", ""

    def _extract_authors(self, doc: spacy.tokens.Doc) -> str:
        """提取作者信息"""
        try:
            authors = []
            found_title = False
            
            for sent in doc.sents:
                text = sent.text.strip()
                if not text:
                    continue
                
                if not found_title:
                    found_title = True
                    continue
                
                if "abstract" in text.lower():
                    break
                
                # 使用spaCy的命名实体识别
                sent_doc = self.nlp(text)
                person_entities = [ent.text for ent in sent_doc.ents if ent.label_ == "PERSON"]
                
                if person_entities:
                    authors.extend(person_entities)
                elif any(keyword in text.lower() for keyword in ['university', 'institute', '@', '.edu']):
                    authors.append(text)
            
            return '; '.join(authors) if authors else ""
        except Exception as e:
            logger.error(f"提取作者信息失败: {str(e)}")
            return ""

    def _extract_conference(self, doc: spacy.tokens.Doc) -> Optional[str]:
        """提取会议/期刊信息"""
        try:
            # 使用spaCy的命名实体识别
            org_entities = [ent.text for ent in doc.ents if ent.label_ == "ORG"]
            
            # 常见的会议/期刊名称模式
            conference_patterns = [
                r'(ICML|ICLR|NeurIPS|CVPR|ACL|SIGGRAPH|OSDI|MLSys|APLOS)\s*\d{4}',
                r'(Conference|Workshop|Symposium|Journal)\s+on\s+[A-Za-z\s]+',
                r'[A-Za-z\s]+(Conference|Workshop|Symposium|Journal)'
            ]
            
            # 首先检查组织实体
            for org in org_entities:
                for pattern in conference_patterns:
                    if re.search(pattern, org, re.IGNORECASE):
                        return org
            
            # 如果没有找到，检查整个文本
            text = doc.text
            for pattern in conference_patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    return match.group(0)
            
            return None
        except Exception as e:
            logger.error(f"提取会议/期刊信息失败: {str(e)}")
            return None

    def _extract_year(self, doc: spacy.tokens.Doc) -> Optional[int]:
        """提取年份信息"""
        try:
            # 使用spaCy的命名实体识别
            date_entities = [ent.text for ent in doc.ents if ent.label_ == "DATE"]
            
            # 首先检查日期实体
            for date in date_entities:
                year_match = re.search(r'\b(19|20)\d{2}\b', date)
                if year_match:
                    return int(year_match.group(0))
            
            # 如果没有找到，检查整个文本
            text = doc.text
            year_match = re.search(r'\b(19|20)\d{2}\b', text)
            if year_match:
                return int(year_match.group(0))
            
            return None
        except Exception as e:
            logger.error(f"提取年份信息失败: {str(e)}")
            return None

    def _extract_keywords(self, doc: spacy.tokens.Doc) -> List[str]:
        """提取关键词"""
        try:
            # 获取文本
            text = doc.text
            
            # 分词和词形还原
            tokens = word_tokenize(text.lower())
            lemmatizer = WordNetLemmatizer()
            tokens = [lemmatizer.lemmatize(token) for token in tokens]
            
            # 去除停用词
            stop_words = set(stopwords.words('english'))
            tokens = [token for token in tokens if token not in stop_words]
            
            # 使用TF-IDF提取关键词
            tfidf_matrix = self.vectorizer.fit_transform([text])
            feature_names = self.vectorizer.get_feature_names_out()
            
            # 获取前10个关键词
            keywords = []
            for i in range(min(10, len(feature_names))):
                keywords.append(feature_names[i])
            
            return keywords
        except Exception as e:
            logger.error(f"提取关键词失败: {str(e)}")
            return []

    async def cleanup_file(self, file_path: str):
        """清理临时文件"""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"文件清理成功: {file_path}")
        except Exception as e:
            logger.error(f"文件清理失败: {str(e)}")
            # 不抛出异常，因为清理失败不影响主要功能

    async def process_multiple_files(self, files: List[UploadFile]) -> List[Dict[str, Any]]:
        """处理多个文件"""
        results = []
        for file in files:
            try:
                file_path = await self.save_upload_file(file)
                pdf_info = await self.extract_pdf_info(file_path)
                results.append({
                    "status": "success",
                    "data": pdf_info
                })
            except Exception as e:
                logger.error(f"处理文件失败: {str(e)}")
                results.append({
                    "status": "error",
                    "error": str(e)
                })
        return results 