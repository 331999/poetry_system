# -*- coding: utf-8 -*-

from .question_classifier import *
from .question_parse import *
from .anwser_search import *


'''问答类'''

class ChatBotGraph:
    def __init__(self):
        self.classifier = QuestionClassifier()  # 调用问题分类子函数，可以链接追踪
        self.parser = QuestionPaser()  # 调用问题解析子函数
        self.searcher = AnswerSearcher()  # 调用问题搜索子函数

    def chat_main(self, sent):
        answer = ''  # 这是初始答案
        res_classify = self.classifier.classify(sent)  # 'sent'是用户的输入内容，利用classify函数先对其进行分类

        if not res_classify:
            return answer  # 没有找到对应分类内容，返回初始答案

        res_sql = self.parser.parser_main(res_classify)  # 调用parser_main对内容进行解析
        final_answers = self.searcher.search_main(res_sql)  # 对内容搜索合适的答案

        if not final_answers:
            return answer  # 如果没有找到合适的最终答案，返回初始答案
        else:
            return '\n'.join(final_answers)  # 连接字符


class ChatBotHybrid:
    def __init__(self, use_rag=True):
        self.kg_bot = ChatBotGraph()
        self.use_rag = use_rag
        self.rag_pipeline = None

        if use_rag:
            try:
                from question.rag import RAGPipeline
                self.rag_pipeline = RAGPipeline()
                print("✓ RAG系统初始化成功")
            except Exception as e:
                print(f"⚠ RAG系统初始化失败: {e}")
                self.use_rag = False

    def chat_main(self, sent):
        if self.use_rag and self.rag_pipeline:
            try:
                result = self.rag_pipeline.query(sent, use_history=False)
                answer = result['answer']

                if result['metadata']['kg_results'] > 0:
                    kg_answer = self.kg_bot.chat_main(sent)
                    if kg_answer:
                        answer = f"{answer}\n\n【知识图谱补充】\n{kg_answer}"

                return answer
            except Exception as e:
                print(f"RAG查询出错: {e}")
                return self.kg_bot.chat_main(sent)
        else:
            return self.kg_bot.chat_main(sent)

    def clear_history(self):
        if self.rag_pipeline:
            self.rag_pipeline.clear_history()


bot = ChatBotHybrid(use_rag=True)
