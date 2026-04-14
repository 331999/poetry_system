# 古诗词智能问答系统

一个基于知识图谱和RAG技术的古诗词智能问答系统，支持多轮对话和混合检索。

## 🌟 系统特性

- **双数据库架构**：MySQL + Neo4j + Chroma
- **混合检索策略**：知识图谱 + 向量检索
- **智能问答**：DeepSeek LLM生成自然语言答案
- **多轮对话**：支持上下文记忆
- **知识图谱**：诗人、朝代、诗歌、生平、著作等结构化知识
- **向量检索**：语义相似度匹配，灵活查询

## 📦 技术栈

- **Web框架**：Django 4.1
- **关系数据库**：MySQL
- **图数据库**：Neo4j
- **向量数据库**：Chroma
- **LLM**：DeepSeek Chat
- **嵌入模型**：OpenAI Embedding

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置数据库

#### MySQL数据库
```bash
python manage.py migrate
python populate_data.py
```

#### Neo4j数据库
```bash
# 安装并启动Neo4j
docker run -d --name neo4j -p 7474:7474 -p 7687:7687 -e NEO4J_AUTH=neo4j/12345678 neo4j:latest

# 构建知识图谱
python build_knowledge_graph.py
```

#### Chroma向量数据库
```bash
python build_vector_store.py
```

### 3. 配置API密钥

编辑 `question/rag/config.py`：

```python
DEEPSEEK_API_KEY = "your-api-key-here"
```

### 4. 启动服务

```bash
python manage.py runserver
```

访问：http://localhost:8000/question/

## 📖 使用指南

### Neo4j知识图谱
详细文档：[NEO4J_GUIDE.md](NEO4J_GUIDE.md)

### RAG系统
详细文档：[RAG_GUIDE.md](RAG_GUIDE.md)

## 🧪 测试

```bash
# 测试RAG系统
python test_rag.py

# 测试数据库
python check_db.py
```

## 📁 项目结构

```
poetry_system/
├── question/                  # 问答模块
│   ├── rag/                  # RAG系统
│   │   ├── config.py        # 配置
│   │   ├── embeddings.py    # 向量嵌入
│   │   ├── vector_store.py  # 向量数据库
│   │   ├── llm.py           # LLM集成
│   │   ├── retriever.py     # 混合检索
│   │   └── rag_pipeline.py  # RAG管道
│   ├── bot/                  # 知识图谱模块
│   │   ├── send_question.py # 问答入口
│   │   ├── question_classifier.py
│   │   ├── question_parse.py
│   │   └── anwser_search.py
│   └── views.py
├── poetry/                    # 诗歌模块
├── users/                     # 用户模块
├── build_knowledge_graph.py   # 构建知识图谱
├── build_vector_store.py      # 构建向量数据库
├── test_rag.py                # RAG测试
├── NEO4J_GUIDE.md             # Neo4j指南
├── RAG_GUIDE.md               # RAG指南
└── requirements.txt           # 依赖列表
```

## 🔧 核心功能

### 1. 知识图谱查询

```python
from question.bot.send_question import ChatBotGraph

bot = ChatBotGraph()
answer = bot.chat_main("李白的朝代是什么？")
```

### 2. RAG智能问答

```python
from question.rag import RAGPipeline

rag = RAGPipeline()
result = rag.query("李白的生平是什么？")
print(result['answer'])
```

### 3. 混合问答

```python
from question.bot.send_question import ChatBotHybrid

bot = ChatBotHybrid(use_rag=True)
answer = bot.chat_main("静夜思表达了什么情感？")
```

## 📊 数据来源

- 诗人数据：`question/bot/data/poet_data.json`
- 诗歌数据：`question/bot/data/poetry_data.json`

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📄 许可证

MIT License

## 🙏 致谢

- Django框架
- Neo4j图数据库
- Chroma向量数据库
- DeepSeek AI
- OpenAI Embedding API
