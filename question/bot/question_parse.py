# -*- coding: utf-8 -*-
class QuestionPaser:
    """构建实体节点"""

    def build_entitydict(self, args):
        """
        :param args: 字典
        :return: 字典
        """
        entity_dict = {}
        for arg, types in args.items():
            for type_ in types:
                if type_ not in entity_dict:
                    entity_dict[type_] = [arg]
                else:
                    entity_dict[type_].append(arg)
        return entity_dict

    def parser_main(self, res_classify):
        """
        解析主函数
        :param res_classify:{'args': {'阿尔泰狗娃花': ['study']}, 'question_types': ['study_style']}
        :return: 返回sql查询语句给图谱，可以是多条
        """
        args = res_classify['args']
        entity_dict = self.build_entitydict(args)  # 调用上面的构造实体节点函数
        question_types = res_classify['question_types']  # 需要question_classifier.py完成问题类型的识别
        entity_key = entity_dict.keys()
        sqls = []
        for question_type in question_types:
            sql_ = {}  # 注意与下面sql的区别
            sql_['question_type'] = question_type
            sql = []

            # 诗人--》朝代
            if question_type == 'poet_name_dynasty':
                sql = self.sql_transfer(question_type, entity_dict.get('poet_name'), entity_key)

            # sql_transfer是下面定义的分开处理问题子函数
            # 诗人--》生平
            elif question_type == 'poet_name_info':
                sql = self.sql_transfer(question_type, entity_dict.get('poet_name'), entity_key)

            # 诗人--》诗词名
            elif question_type == 'poet_name_poetry':
                sql = self.sql_transfer(question_type, entity_dict.get('poet_name'), entity_key)

            # 诗人 -- 》 古诗内容
            elif question_type == 'poet_poetry_info':
                sql = self.sql_transfer(question_type, entity_dict.get('poet_name'), entity_dict.get('poetry_name'))

            # 诗人--》著作
            elif question_type == 'poet_name_work':
                sql = self.sql_transfer(question_type, entity_dict.get('poet_name'), entity_key)

            # 朝代--》诗人
            elif question_type == 'poet_dynast_name':
                sql = self.sql_transfer(question_type, entity_dict.get('poet_dynasty'), entity_key)

            # 诗人自查询
            elif question_type == 'poet_name':
                sql = self.sql_transfer(question_type, entity_dict.get('poet_name'), entity_key)

            # 诗词自查询
            elif question_type == 'poetry_name':
                sql = self.sql_transfer(question_type, entity_dict.get('poetry_name'), entity_key)

            # print(question_type, entity_dict, entity_key)
            if sql:
                sql_['sql'] = sql
                sqls.append(sql_)
        # print(sqls)
        return sqls

    '''针对不同的问题，分开进行处理'''

    def sql_transfer(self, question_type, entities, entity_key):
        if not entities:
            return []
        # 查询语句
        sql = []
        # 诗人--》朝代
        if question_type == 'poet_name_dynasty':
            sql = [
                "MATCH (m:Poet_name)-[belong_dynasty]->(n:Poet_dynasty) where m.name = '{0}' return m.name,n.name".format(
                    i)
                for i in entities]

        # 诗人--》生平
        if question_type == 'poet_name_info':
            sql = [
                "MATCH (m:Poet_name)-[poet_info]->(n:Poet_info) where m.name = '{0}' return m.name,n.name".format(i)
                for i in entities]

        # 诗人--》古诗名 查询5首
        if question_type == 'poet_name_poetry':
            sql = [
                "MATCH (m:Poet_name)-[poetry_name]->(n:Poetry_name) where m.name = '{0}' return m.name,n.name LIMIT 5".format(
                    i)
                for i in entities]

        # 诗人--》古诗内容
        if question_type == 'poet_poetry_info':
            sql = [
                f"MATCH (m:Poet_name)-[poetry_name]->(p:Poetry_name)-[poetry_info]->(n:Poetry_info) "
                f"where m.name = '{entities[0]}' and p.name = '{entity_key[0]}'   "
                f"return p.name,n.name"]

        # 诗人-->著作
        if question_type == 'poet_name_work':
            sql = [
                "MATCH (m:Poet_name)-[poet_work]->(n:Poet_work) where m.name = '{0}' return m.name,n.name".format(
                    i)
                for i in entities]

        # 朝代--》诗人 限制查询10个
        if question_type == 'poet_dynast_name':
            sql = [
                "MATCH (m:Poet_dynasty)-[has_poet]->(n:Poet_name) where m.name = '{0}' return m.name,n.name limit 10".format(
                    i)
                for i in entities]

        # 诗人自查询 限制查询10个
        if question_type == 'poet_name':
            sql = [
                "MATCH (m:Poet_name)-[r]-(related_node) where m.name = '{}' RETURN m.name, r.name, related_node.name".format(
                    i) for i in entities]

        # 诗人自查询 限制查询10个
        if question_type == 'poetry_name':
            sql = [
                "MATCH (m:Poetry_name)-[poetry_info]->(n:Poetry_info) where m.name = '{0}' return m.name,n.name".format(
                    i) for
                i in entities]
        return sql


if __name__ == '__main__':
    handler = QuestionPaser()

