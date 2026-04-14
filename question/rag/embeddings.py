# -*- coding: utf-8 -*-
"""
向量嵌入模块
使用智谱AI Embedding API生成文本向量
"""

from typing import List
import time
import re
from .config import RAGConfig

try:
    from zhipuai import ZhipuAI
    ZHIPU_AVAILABLE = True
except ImportError:
    ZHIPU_AVAILABLE = False
    print("警告: zhipuai库未安装，请运行: pip install zhipuai")


class EmbeddingEngine:
    def __init__(self):
        if not ZHIPU_AVAILABLE:
            raise ImportError("zhipuai库未安装，请运行: pip install zhipuai")
        
        self.client = ZhipuAI(api_key=RAGConfig.ZHIPU_API_KEY)
        self.model = RAGConfig.EMBEDDING_MODEL
        self.max_text_length = 7500
        self.request_delay = 0.5

    def preprocess_text(self, text: str) -> str:
        if not text or not isinstance(text, str):
            return ""
        
        text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]', '', text)
        
        text = text.strip()
        
        text = re.sub(r'\s+', ' ', text)
        
        if len(text) > self.max_text_length:
            text = text[:self.max_text_length]
        
        return text

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        if not texts:
            return []

        processed_texts = []
        for text in texts:
            processed = self.preprocess_text(text)
            if processed:
                processed_texts.append(processed)
            else:
                processed_texts.append("空文本")

        if not processed_texts:
            return []

        try:
            time.sleep(self.request_delay)
            
            response = self.client.embeddings.create(
                model=self.model,
                input=processed_texts
            )
            embeddings = [item.embedding for item in response.data]
            return embeddings
        except Exception as e:
            error_msg = str(e)
            if "1210" in error_msg:
                print(f"API参数错误，可能是文本格式问题: {error_msg[:200]}")
            elif "rate limit" in error_msg.lower():
                print(f"API调用频率限制，等待后重试: {error_msg[:200]}")
                time.sleep(2)
            else:
                print(f"生成向量嵌入时出错: {error_msg[:200]}")
            return []

    def embed_query(self, query: str) -> List[float]:
        processed_query = self.preprocess_text(query)
        
        if not processed_query:
            return []

        try:
            time.sleep(self.request_delay)
            
            response = self.client.embeddings.create(
                model=self.model,
                input=[processed_query]
            )
            return response.data[0].embedding
        except Exception as e:
            print(f"生成查询向量时出错: {e}")
            return []
