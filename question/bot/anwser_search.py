# -*- coding:utf-8 -*-

from py2neo import Graph


class AnswerSearcher:
    def __init__(self):  # 调用数据库进行查询
        self.g = Graph("bolt://localhost:7687", auth=("neo4j", "12345678"))  # 输入自己修改的用户名，密码
        self.num_limit = 20  # 最多显示字符数量

    def search_main(self, sqls):
        final_answers = []
        for sql_ in sqls:
            question_type = sql_['question_type']  # sql_里面的关键字
            queries = sql_['sql']
            answers = []
            for query in queries:
                ress = self.g.run(query).data()  # 运行图数据库
                answers += ress
            final_answer = self.answer_prettify(question_type, answers)  # 调用回复模板函数
            if final_answer:
                final_answers.append(final_answer)
        return final_answers

    def answer_prettify(self, question_type, answers):
        """根据对应的qustion_type，调用相应的回复模板"""
        final_answer = []
        if not answers:
            return ''
        # 朝代--》诗人
        if question_type == 'poet_dynast_name':
            subject = answers[0]['m.name']
            desc = [i['n.name'] for i in answers]
            final_answer = '{0}有{1}这些诗人'.format(subject, ','.join(list(set(desc))[:self.num_limit]))

        # 诗人--》朝代
        if question_type == 'poet_name_dynasty':
            subject = answers[0]['m.name']
            desc = [i['n.name'] for i in answers]
            final_answer = '{0}属于{1}'.format(subject, ','.join(list(set(desc))[:self.num_limit]))

        # 诗人--》生平
        if question_type == 'poet_name_info':
            subject = answers[0]['m.name']
            desc = [i['n.name'] for i in answers]
            final_answer = '{1}'.format(subject, ','.join(list(set(desc))[:self.num_limit]))

        # 诗人--》古诗名 查询5首
        if question_type == 'poet_name_poetry':
            subject = answers[0]['m.name']
            desc = [i['n.name'] for i in answers]
            final_answer = '{0}有这些诗{1}'.format(subject, ','.join(list(set(desc))[:self.num_limit]))

        # 诗人 --》 古诗内容
        if question_type == 'poet_poetry_info':
            subject = answers[0]['p.name']
            desc = [i['n.name'] for i in answers]
            final_answer = '{0}\n{1}'.format(subject, ','.join(list(set(desc))[:self.num_limit]))

        # 诗人-->著作
        if question_type == 'poet_name_work':
            subject = answers[0]['m.name']
            desc = [i['n.name'] for i in answers]
            final_answer = '{0}著有《{1}》等'.format(subject, '》,《'.join(list(set(desc))[:self.num_limit]))

        # 诗人自查询
        if question_type == 'poet_name':
            poet_name = answers[0]['m.name']
            final_answer = f"你可以这样问我:例如{poet_name}的著作有什么？" \
                           f"{poet_name}的生平信息?{poet_name}写过什么诗歌?"

        # 古诗自查询
        if question_type == 'poetry_name':
            subject = answers[0]['m.name']
            desc = [i['n.name'] for i in answers]
            final_answer = '{0}\n{1}'.format(subject, '\n'.join(list(set(desc))[:self.num_limit]))
        return final_answer


if __name__ == '__main__':
    searcher = AnswerSearcher()

