# -*- coding: utf-8 -*-
"""
向量数据库管理模块
使用Chroma存储和检索文档向量
"""

import json
import chromadb
from chromadb.config import Settings
from typing import List, Dict, Any
from pathlib import Path
from .config import RAGConfig
from .embeddings import EmbeddingEngine


class VectorStore:
    def __init__(self):
        self.config = RAGConfig

        Path(self.config.CHROMA_PERSIST_DIR).mkdir(parents=True, exist_ok=True)

        self.client = chromadb.PersistentClient(
            path=self.config.CHROMA_PERSIST_DIR,
            settings=Settings(
                anonymized_telemetry=False
            )
        )

        self.collection = self.client.get_or_create_collection(
            name=self.config.CHROMA_COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"}
        )

        self.embedding_engine = EmbeddingEngine()

    def build_index(self):
        print("开始构建向量索引...")

        documents = []
        metadatas = []
        ids = []

        poetry_data_path = Path(self.config.POETRY_DATA_PATH)
        if poetry_data_path.exists():
            with open(poetry_data_path, 'r', encoding='utf-8') as f:
                for idx, line in enumerate(f):
                    try:
                        poetry = json.loads(line.strip())
                        poet_name = poetry.get('poet_name', '')
                        poetry_name = poetry.get('poetry_name', '')
                        poetry_info = poetry.get('poetry_info', '')
                        poet_dynasty = poetry.get('poet_dynasty', '')

                        content = f"【{poetry_name}】\n作者：{poet_name}（{poet_dynasty}）\n\n{poetry_info}"

                        documents.append(content)
                        metadatas.append({
                            'type': 'poetry',
                            'poet_name': poet_name,
                            'poetry_name': poetry_name,
                            'poet_dynasty': poet_dynasty
                        })
                        ids.append(f"poetry_{idx}")
                    except Exception as e:
                        print(f"处理诗歌数据时出错: {e}")
                        continue

        poet_data_path = Path(self.config.POET_DATA_PATH)
        if poet_data_path.exists():
            with open(poet_data_path, 'r', encoding='utf-8') as f:
                for idx, line in enumerate(f):
                    try:
                        poet = json.loads(line.strip())
                        poet_name = poet.get('poet_name', '')
                        poet_info = poet.get('poet_info', '')
                        poet_works = poet.get('poet_works', [])

                        content = f"【{poet_name}】\n\n生平：{poet_info}\n\n代表作：{', '.join(poet_works) if poet_works else '暂无'}"

                        documents.append(content)
                        metadatas.append({
                            'type': 'poet',
                            'poet_name': poet_name
                        })
                        ids.append(f"poet_{idx}")
                    except Exception as e:
                        print(f"处理诗人数据时出错: {e}")
                        continue

        if not documents:
            print("没有找到文档数据")
            return

        print(f"共加载 {len(documents)} 个文档")

        batch_size = 50
        success_count = 0
        failed_batches = []
        
        for i in range(0, len(documents), batch_size):
            batch_docs = documents[i:i + batch_size]
            batch_metas = metadatas[i:i + batch_size]
            batch_ids = ids[i:i + batch_size]
            batch_num = i // batch_size + 1

            try:
                embeddings = self.embedding_engine.embed_texts(batch_docs)

                if embeddings:
                    if len(embeddings) == len(batch_docs):
                        self.collection.add(
                            documents=batch_docs,
                            embeddings=embeddings,
                            metadatas=batch_metas,
                            ids=batch_ids
                        )
                        success_count += len(batch_docs)
                        print(f"✓ 批次 {batch_num}: 已索引 {success_count}/{len(documents)} 个文档")
                    else:
                        print(f"⚠ 批次 {batch_num}: 嵌入数量不匹配 ({len(embeddings)}/{len(batch_docs)})")
                        failed_batches.append(batch_num)
                else:
                    print(f"⚠ 批次 {batch_num}: 嵌入生成失败")
                    failed_batches.append(batch_num)
            except Exception as e:
                print(f"✗ 批次 {batch_num}: 处理失败 - {str(e)[:100]}")
                failed_batches.append(batch_num)
                continue

        print(f"\n{'='*60}")
        print(f"向量索引构建完成")
        print(f"{'='*60}")
        print(f"成功索引: {success_count}/{len(documents)} 个文档")
        
        if failed_batches:
            print(f"失败批次: {len(failed_batches)} 个 (批次号: {failed_batches[:10]}{'...' if len(failed_batches) > 10 else ''})")
        
        print(f"{'='*60}")

    def search(self, query: str, top_k: int = None) -> List[Dict[str, Any]]:
        if top_k is None:
            top_k = self.config.RETRIEVAL_TOP_K

        query_embedding = self.embedding_engine.embed_query(query)

        if not query_embedding:
            return []

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=['documents', 'metadatas', 'distances']
        )

        formatted_results = []
        if results['documents']:
            for i in range(len(results['documents'][0])):
                formatted_results.append({
                    'document': results['documents'][0][i],
                    'metadata': results['metadatas'][0][i],
                    'distance': results['distances'][0][i]
                })

        return formatted_results

    def clear(self):
        self.client.delete_collection(self.config.CHROMA_COLLECTION_NAME)
        self.collection = self.client.create_collection(
            name=self.config.CHROMA_COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"}
        )
        print("✓ 向量数据库已清空")

    def get_stats(self) -> Dict[str, Any]:
        count = self.collection.count()
        return {
            'total_documents': count,
            'collection_name': self.config.CHROMA_COLLECTION_NAME
        }
