## 项目概述

1. 设计系统，培养自己能够独立发表icml,iros,iclr，iros，siggraph，mlsys,osdi,aplos的论文
2. 并且能够帮助我成功发表第一篇顶会论文

## 系统架构

### 核心模块

1. **论文选题与创新点发现模块**
   - 文献综述与趋势分析
   - 研究空白点识别
   - 创新点建议生成

2. **论文写作辅助模块**
   - 论文结构优化
   - 写作风格检查
   - 学术语言润色

3. **实验设计与分析模块**
   - 实验方案建议
   - 数据分析工具
   - 结果可视化

4. **投稿策略模块**
   - 会议/期刊匹配
   - 投稿时间规划
   - 审稿意见分析

### 技术栈

- 后端：Python + FastAPI
- 前端：React + TypeScript
- 数据库：PostgreSQL
- 机器学习：PyTorch/TensorFlow
- 自然语言处理：Hugging Face Transformers

### 项目结构

```
zaka-paper-killer/
├── backend/                # 后端服务
│   ├── api/               # API接口
│   ├── models/            # 数据模型
│   ├── services/          # 业务逻辑
│   └── utils/             # 工具函数
├── frontend/              # 前端应用
│   ├── src/              # 源代码
│   ├── components/       # 组件
│   └── pages/            # 页面
├── data/                  # 数据存储
├── docs/                  # 文档
└── tests/                 # 测试
```

## 开发计划

1. 第一阶段：基础架构搭建
   - 项目初始化
   - 数据库设计
   - 基础API开发

2. 第二阶段：核心功能开发
   - 文献分析功能
   - 写作辅助功能
   - 实验分析功能

3. 第三阶段：优化与完善
   - 性能优化
   - 用户体验改进
   - 功能扩展

## 使用说明

### 环境要求

- Python 3.8+
- Node.js 16+
- PostgreSQL 12+

### 安装步骤

1. 克隆项目
```bash
git clone https://github.com/Wheeeeeeeeels/zaka-paper-killer.git
cd zaka-paper-killer
```

2. 安装后端依赖
```bash
cd backend
pip install -r requirements.txt
```

3. 安装前端依赖
```bash
cd frontend
npm install
```

4. 配置环境变量
```bash
# 后端
cp backend/.env.example backend/.env
# 编辑 .env 文件，设置必要的环境变量
```

5. 启动服务
```bash
# 启动后端服务
cd backend
uvicorn main:app --reload

# 启动前端服务
cd frontend
npm run dev
```

### 主要功能使用说明

1. **论文分析**
   - 上传论文PDF或输入论文链接
   - 系统自动分析论文结构和内容
   - 获取创新点建议和修改意见

2. **写作辅助**
   - 使用AI辅助写作
   - 检查学术语言和格式
   - 优化论文结构

3. **实验分析**
   - 上传实验数据
   - 自动生成分析报告
   - 可视化实验结果

4. **投稿策略**
   - 输入论文摘要和关键词
   - 获取合适的会议/期刊推荐
   - 查看投稿时间表

## 贡献指南

### 代码规范

- 遵循 PEP 8 (Python) 和 ESLint (JavaScript/TypeScript) 规范
- 使用有意义的变量名和函数名
- 添加必要的注释和文档字符串

### 提交规范

1. 创建功能分支
```bash
git checkout -b feature/your-feature-name
```

2. 提交更改
```bash
git add .
git commit -m "feat: add new feature"
```

3. 推送到远程
```bash
git push origin feature/your-feature-name
```

4. 创建 Pull Request
   - 描述功能变更
   - 关联相关 Issue
   - 等待代码审查

### 开发流程

1. 创建 Issue 描述需求
2. 分配任务
3. 开发功能
4. 编写测试
5. 提交代码审查
6. 合并到主分支

### 测试要求

- 新功能必须包含单元测试
- 保持测试覆盖率在 80% 以上
- 确保所有测试通过

## 许可证

MIT License