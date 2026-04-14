# -*- coding: utf-8 -*-
"""
RAG配置文件
"""

import os
from pathlib import Path


class RAGConfig:
    BASE_DIR = Path(__file__).resolve().parent.parent.parent

    DEEPSEEK_API_KEY = "sk-8b9e2719092f4a8bb33dc00b07a5bf6f"
    DEEPSEEK_BASE_URL = "https://api.deepseek.com/v1"
    DEEPSEEK_MODEL = "deepseek-chat"

    ZHIPU_API_KEY = "8a68a0298fe243488bf395a5826df361.N4n6wVvjDR6OQ299"
    ZHIPU_EMBEDDING_MODEL = "embedding-2"

    CHROMA_PERSIST_DIR = str(BASE_DIR / "question" / "rag" / "chroma_db")
    CHROMA_COLLECTION_NAME = "poetry_knowledge"

    EMBEDDING_MODEL = "embedding-2"
    EMBEDDING_DIMENSION = 1024

    NEO4J_URI = "bolt://localhost:7687"
    NEO4J_USER = "neo4j"
    NEO4J_PASSWORD = "12345678"

    RETRIEVAL_TOP_K = 5
    TEMPERATURE = 0.7
    MAX_TOKENS = 2000

    POETRY_DATA_PATH = str(BASE_DIR / "question" / "bot" / "data" / "poetry_data.json")
    POET_DATA_PATH = str(BASE_DIR / "question" / "bot" / "data" / "poet_data.json")

    SYSTEM_PROMPT = """你是一个专业的古诗词助手，名叫"夫子"。你的职责是帮助用户了解和学习中国古诗词。

你的知识来源包括：
1. 知识图谱：包含诗人、朝代、诗歌、生平、著作等结构化信息
2. 文档库：包含诗歌的详细内容和背景知识

请根据检索到的信息，用专业、准确、有文采的语言回答用户的问题。

回答格式要求：
- 不要使用Markdown格式（不要用**、###、-等符号）
- 使用自然的中文标点符号
- 用换行来分隔不同的段落
- 用"一、二、三、"或"1. 2. 3."来列举内容
- 诗歌内容用书名号《》标注
- 人名、朝代等不需要特殊标记

回答内容要求：
- 准确性：确保事实正确，引用准确
- 完整性：提供全面的信息，包括背景知识
- 文学性：使用优美的语言，体现古诗词的韵味
- 友好性：态度亲切，乐于助人
- 简洁性：避免冗余，直接回答问题

如果检索到的信息不足以回答问题，请诚实告知，不要编造内容。

示例回答格式：
李白（701年-762年），字太白，号青莲居士，唐代伟大的浪漫主义诗人，被后人誉为"诗仙"。

他的代表作有：
1. 《静夜思》
2. 《将进酒》
3. 《望庐山瀑布》

李白与杜甫并称为"李杜"，是唐代最杰出的诗人之一。"""

    @classmethod
    def update_config(cls, **kwargs):
        for key, value in kwargs.items():
            if hasattr(cls, key):
                setattr(cls, key, value)
