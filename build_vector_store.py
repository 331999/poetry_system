#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
构建向量数据库脚本
将诗歌和诗人数据索引到Chroma向量数据库
"""

import os
import sys
import django

sys.path.insert(0, os.path.dirname(__file__))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'poetry_system.settings')
django.setup()

from question.rag.vector_store import VectorStore
from question.rag.config import RAGConfig


def build_vector_database():
    print("=" * 60)
    print("开始构建向量数据库")
    print("=" * 60)

    print(f"\n配置信息：")
    print(f"  向量数据库路径: {RAGConfig.CHROMA_PERSIST_DIR}")
    print(f"  集合名称: {RAGConfig.CHROMA_COLLECTION_NAME}")
    print(f"  嵌入模型: {RAGConfig.EMBEDDING_MODEL}")
    print(f"  检索Top-K: {RAGConfig.RETRIEVAL_TOP_K}")

    vector_store = VectorStore()

    print("\n是否清空现有向量数据库？(y/n): ", end="")
    choice = input().strip().lower()
    if choice == 'y':
        vector_store.clear()
        print("✓ 已清空向量数据库")

    print("\n开始索引文档...")
    vector_store.build_index()

    stats = vector_store.get_stats()
    print("\n" + "=" * 60)
    print("向量数据库构建完成！")
    print("=" * 60)
    print(f"\n统计信息：")
    print(f"  总文档数: {stats['total_documents']}")
    print(f"  集合名称: {stats['collection_name']}")


if __name__ == '__main__':
    try:
        build_vector_database()
    except KeyboardInterrupt:
        print("\n\n用户中断操作")
    except Exception as e:
        print(f"\n✗ 构建向量数据库时出错: {e}")
        import traceback
        traceback.print_exc()
