# -*- coding: utf-8 -*-
"""
RAG管道模块
整合检索和生成的完整流程
"""

from typing import List, Dict, Any, Optional
from .config import RAGConfig
from .retriever import HybridRetriever
from .llm import DeepSeekLLM


class RAGPipeline:
    def __init__(self):
        self.retriever = HybridRetriever()
        self.llm = DeepSeekLLM()
        self.conversation_history: List[Dict[str, str]] = []

    def query(
        self,
        question: str,
        use_history: bool = True,
        top_k: int = None
    ) -> Dict[str, Any]:
        retrieval_result = self.retriever.retrieve(question, top_k)

        contexts = retrieval_result['contexts']

        answer = self.llm.generate(
            query=question,
            context=contexts,
            conversation_history=self.conversation_history if use_history else None
        )

        if use_history:
            self.conversation_history.append({"role": "user", "content": question})
            self.conversation_history.append({"role": "assistant", "content": answer})

        return {
            'question': question,
            'answer': answer,
            'contexts': contexts,
            'metadata': {
                'kg_results': retrieval_result['kg_count'],
                'vector_results': retrieval_result['vector_count'],
                'total_results': retrieval_result['total_count']
            }
        }

    def clear_history(self):
        self.conversation_history = []

    def get_history(self) -> List[Dict[str, str]]:
        return self.conversation_history.copy()

    def chat(self, question: str) -> str:
        result = self.query(question, use_history=True)
        return result['answer']

    def query_without_history(self, question: str) -> str:
        result = self.query(question, use_history=False)
        return result['answer']

    def get_context_only(self, question: str) -> List[Dict[str, Any]]:
        retrieval_result = self.retriever.retrieve(question)
        return retrieval_result['contexts']
