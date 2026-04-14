# -*- coding: utf-8 -*-
"""
DeepSeek LLM集成模块
使用DeepSeek API生成回答
"""

from openai import OpenAI
from typing import List, Dict
from .config import RAGConfig


class DeepSeekLLM:
    def __init__(self):
        self.client = OpenAI(
            api_key=RAGConfig.DEEPSEEK_API_KEY,
            base_url=RAGConfig.DEEPSEEK_BASE_URL
        )
        self.model = RAGConfig.DEEPSEEK_MODEL
        self.temperature = RAGConfig.TEMPERATURE
        self.max_tokens = RAGConfig.MAX_TOKENS
        self.system_prompt = RAGConfig.SYSTEM_PROMPT

    def generate(
        self,
        query: str,
        context: List[Dict[str, str]],
        conversation_history: List[Dict[str, str]] = None
    ) -> str:
        messages = [
            {"role": "system", "content": self.system_prompt}
        ]

        if context:
            context_text = self._format_context(context)
            messages.append({
                "role": "system",
                "content": f"以下是检索到的相关信息：\n\n{context_text}"
            })

        if conversation_history:
            messages.extend(conversation_history)

        messages.append({"role": "user", "content": query})

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"生成回答时出错: {e}")
            return "抱歉，生成回答时出现错误，请稍后再试。"

    def _format_context(self, context: List[Dict[str, str]]) -> str:
        formatted = []
        for idx, item in enumerate(context, 1):
            source = item.get('source', '未知来源')
            content = item.get('content', '')
            formatted.append(f"[{idx}] 来源：{source}\n{content}\n")

        return "\n".join(formatted)

    def chat(
        self,
        query: str,
        context: str = None,
        conversation_history: List[Dict[str, str]] = None
    ) -> str:
        messages = [
            {"role": "system", "content": self.system_prompt}
        ]

        if context:
            messages.append({
                "role": "system",
                "content": f"参考信息：\n{context}"
            })

        if conversation_history:
            messages.extend(conversation_history)

        messages.append({"role": "user", "content": query})

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"对话时出错: {e}")
            return "抱歉，对话时出现错误，请稍后再试。"
