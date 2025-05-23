from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os
import logging
from services.crawler import ICLRCrawler, CHICrawler
from datetime import datetime

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# 加载论文数据
def load_papers(conference):
    try:
        filename = f'{conference}2025_papers.json'
        if not os.path.exists(filename):
            logger.info(f"论文数据文件不存在，正在爬取数据...")
            if conference == 'iclr':
                crawler = ICLRCrawler()
            else:
                crawler = CHICrawler()
            papers = crawler.get_papers()
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(papers, f, ensure_ascii=False, indent=2)
            return papers
        
        with open(filename, 'r', encoding='utf-8') as f:
            papers = json.load(f)
            logger.info(f"成功加载 {len(papers)} 篇论文")
            return papers
    except Exception as e:
        logger.error(f"加载论文数据时出错: {str(e)}")
        return []

# 保存论文数据
def save_papers(conference, papers):
    try:
        filename = f'{conference}2025_papers.json'
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(papers, f, ensure_ascii=False, indent=2)
        logger.info(f"成功保存 {len(papers)} 篇论文")
    except Exception as e:
        logger.error(f"保存论文数据时出错: {str(e)}")

# 获取所有论文
@app.route('/api/papers/<conference>2025', methods=['GET'])
def get_papers(conference):
    try:
        papers = load_papers(conference)
        return jsonify(papers)
    except Exception as e:
        logger.error(f"获取论文列表时出错: {str(e)}")
        return jsonify({"error": "获取论文列表失败"}), 500

# 获取特定论文
@app.route('/api/papers/<conference>2025/<paper_id>', methods=['GET'])
def get_paper(conference, paper_id):
    try:
        papers = load_papers(conference)
        paper = next((p for p in papers if p['id'] == paper_id), None)
        if paper:
            return jsonify(paper)
        return jsonify({"error": "论文未找到"}), 404
    except Exception as e:
        logger.error(f"获取论文详情时出错: {str(e)}")
        return jsonify({"error": "获取论文详情失败"}), 500

# 搜索论文
@app.route('/api/papers/<conference>2025/search', methods=['GET'])
def search_papers(conference):
    try:
        query = request.args.get('q', '').lower()
        papers = load_papers(conference)
        
        if not query:
            return jsonify(papers)
        
        filtered_papers = []
        for paper in papers:
            if (query in paper['title'].lower() or
                query in paper['abstract'].lower() or
                any(query in tag.lower() for tag in paper['tags'])):
                filtered_papers.append(paper)
        
        return jsonify(filtered_papers)
    except Exception as e:
        logger.error(f"搜索论文时出错: {str(e)}")
        return jsonify({"error": "搜索论文失败"}), 500

# 按主题筛选论文
@app.route('/api/papers/<conference>2025/topic/<topic>', methods=['GET'])
def filter_by_topic(conference, topic):
    try:
        papers = load_papers(conference)
        filtered_papers = [p for p in papers if topic in p['tags']]
        return jsonify(filtered_papers)
    except Exception as e:
        logger.error(f"按主题筛选论文时出错: {str(e)}")
        return jsonify({"error": "筛选论文失败"}), 500

# 按track筛选论文
@app.route('/api/papers/<conference>2025/track/<track>', methods=['GET'])
def filter_by_track(conference, track):
    try:
        papers = load_papers(conference)
        filtered_papers = [p for p in papers if p['track'].lower() == track.lower()]
        return jsonify(filtered_papers)
    except Exception as e:
        logger.error(f"按track筛选论文时出错: {str(e)}")
        return jsonify({"error": "筛选论文失败"}), 500

# 更新论文数据
@app.route('/api/papers/<conference>2025/update', methods=['POST'])
def update_papers(conference):
    try:
        if conference == 'iclr':
            crawler = ICLRCrawler()
        else:
            crawler = CHICrawler()
        papers = crawler.get_papers()
        
        save_papers(conference, papers)
        
        return jsonify({"message": f"成功更新 {len(papers)} 篇论文"})
    except Exception as e:
        logger.error(f"更新论文数据时出错: {str(e)}")
        return jsonify({"error": "更新论文数据失败"}), 500

# 创建新论文
@app.route('/api/papers/<conference>2025/create', methods=['POST'])
def create_paper(conference):
    try:
        data = request.json
        papers = load_papers(conference)
        
        # 生成新的论文ID
        new_id = str(len(papers) + 1)
        
        # 创建新论文对象
        new_paper = {
            "id": new_id,
            "title": data.get('topic', ''),
            "authors": ["Your Name"],  # 这里可以替换为实际的作者信息
            "abstract": data.get('innovations', ''),
            "track": "research",  # 默认设置为research
            "tags": data.get('datasets', []),
            "similarityScore": 0.8,
            "gaps": [],
            "innovations": data.get('innovations', '').split('\n'),
            "experiments": {
                "setup": data.get('datasets', []),
                "metrics": data.get('metrics', []),
                "baselines": []
            },
            "created_at": datetime.now().isoformat()
        }
        
        # 添加到论文列表
        papers.append(new_paper)
        
        # 保存更新后的论文列表
        save_papers(conference, papers)
        
        return jsonify({
            "message": "论文创建成功",
            "paper": new_paper
        })
    except Exception as e:
        logger.error(f"创建论文时出错: {str(e)}")
        return jsonify({"error": "创建论文失败"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=8003) 