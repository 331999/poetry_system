# -*- coding: utf-8 -*-
"""
混合检索器模块
结合Neo4j知识图谱和向量检索的混合检索策略
"""

from typing import List, Dict, Any
from py2neo import Graph
from .config import RAGConfig
from .vector_store import VectorStore


class HybridRetriever:
    def __init__(self):
        self.graph = Graph(
            RAGConfig.NEO4J_URI,
            auth=(RAGConfig.NEO4J_USER, RAGConfig.NEO4J_PASSWORD)
        )
        self.vector_store = VectorStore()

    def retrieve(self, query: str, top_k: int = None) -> Dict[str, Any]:
        if top_k is None:
            top_k = RAGConfig.RETRIEVAL_TOP_K

        kg_results = self._retrieve_from_kg(query)

        vector_results = self.vector_store.search(query, top_k)

        merged_context = self._merge_results(kg_results, vector_results)

        return merged_context

    def _retrieve_from_kg(self, query: str) -> List[Dict[str, Any]]:
        results = []

        poet_keywords = ['诗人', '作者', '谁写的', '生平', '著作', '代表作']
        dynasty_keywords = ['朝代', '年代', '时期']
        poetry_keywords = ['诗', '词', '内容', '全文', '古诗']

        if any(keyword in query for keyword in poet_keywords):
            poet_results = self._search_poet(query)
            results.extend(poet_results)

        if any(keyword in query for keyword in dynasty_keywords):
            dynasty_results = self._search_dynasty(query)
            results.extend(dynasty_results)

        if any(keyword in query for keyword in poetry_keywords):
            poetry_results = self._search_poetry(query)
            results.extend(poetry_results)

        return results

    def _search_poet(self, query: str) -> List[Dict[str, Any]]:
        results = []
        try:
            cypher = """
            MATCH (p:Poet_name)
            WHERE p.name CONTAINS $keyword OR $keyword CONTAINS p.name
            OPTIONAL MATCH (p)-[r]-(related)
            RETURN p.name as poet_name, 
                   collect(DISTINCT {relation: type(r), node: related.name}) as relations
            LIMIT 5
            """
            keyword = self._extract_keyword(query)
            data = self.graph.run(cypher, keyword=keyword).data()

            for item in data:
                poet_name = item['poet_name']
                relations = item['relations']

                context = f"诗人：{poet_name}\n"
                for rel in relations:
                    context += f"- {rel['relation']}: {rel['node']}\n"

                results.append({
                    'source': '知识图谱',
                    'type': 'poet',
                    'content': context,
                    'metadata': {'poet_name': poet_name}
                })
        except Exception as e:
            print(f"从知识图谱检索诗人信息时出错: {e}")

        return results

    def _search_dynasty(self, query: str) -> List[Dict[str, Any]]:
        results = []
        try:
            cypher = """
            MATCH (d:Poet_dynasty)
            WHERE d.name CONTAINS $keyword OR $keyword CONTAINS d.name
            OPTIONAL MATCH (d)-[r]-(p:Poet_name)
            RETURN d.name as dynasty, collect(DISTINCT p.name) as poets
            LIMIT 5
            """
            keyword = self._extract_keyword(query)
            data = self.graph.run(cypher, keyword=keyword).data()

            for item in data:
                dynasty = item['dynasty']
                poets = item['poets']

                context = f"朝代：{dynasty}\n"
                context += f"代表诗人：{', '.join(poets[:10])}\n"

                results.append({
                    'source': '知识图谱',
                    'type': 'dynasty',
                    'content': context,
                    'metadata': {'dynasty': dynasty}
                })
        except Exception as e:
            print(f"从知识图谱检索朝代信息时出错: {e}")

        return results

    def _search_poetry(self, query: str) -> List[Dict[str, Any]]:
        results = []
        try:
            cypher = """
            MATCH (p:Poetry_name)
            WHERE p.name CONTAINS $keyword OR $keyword CONTAINS p.name
            OPTIONAL MATCH (p)-[r]-(related)
            RETURN p.name as poetry_name,
                   collect(DISTINCT {relation: type(r), node: related.name}) as relations
            LIMIT 5
            """
            keyword = self._extract_keyword(query)
            data = self.graph.run(cypher, keyword=keyword).data()

            for item in data:
                poetry_name = item['poetry_name']
                relations = item['relations']

                context = f"诗歌：{poetry_name}\n"
                for rel in relations:
                    context += f"- {rel['relation']}: {rel['node']}\n"

                results.append({
                    'source': '知识图谱',
                    'type': 'poetry',
                    'content': context,
                    'metadata': {'poetry_name': poetry_name}
                })
        except Exception as e:
            print(f"从知识图谱检索诗歌信息时出错: {e}")

        return results

    def _extract_keyword(self, query: str) -> str:
        keywords = query.replace('的', ' ').replace('了', ' ').replace('吗', ' ')
        keywords = keywords.replace('？', ' ').replace('？', ' ').replace('。', ' ')
        keywords = keywords.replace('有', ' ').replace('什么', ' ').replace('哪些', ' ')
        keywords = keywords.strip()

        words = keywords.split()
        if words:
            return words[0]

        return query

    def _merge_results(
        self,
        kg_results: List[Dict[str, Any]],
        vector_results: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        all_contexts = []

        for result in kg_results:
            all_contexts.append({
                'source': result['source'],
                'type': result['type'],
                'content': result['content'],
                'metadata': result.get('metadata', {})
            })

        for result in vector_results:
            all_contexts.append({
                'source': '向量检索',
                'type': result['metadata'].get('type', 'unknown'),
                'content': result['document'],
                'metadata': result.get('metadata', {}),
                'score': 1 - result.get('distance', 0)
            })

        return {
            'contexts': all_contexts,
            'kg_count': len(kg_results),
            'vector_count': len(vector_results),
            'total_count': len(all_contexts)
        }
