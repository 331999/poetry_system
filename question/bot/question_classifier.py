import os
import ahocorasick  # 调用这个库函数，可以网上搜索这个函数库用法
from django.conf import settings


class QuestionClassifier:
    def __init__(self):
        cur_dir = str(settings.BASE_DIR) + '\question' + '\\bot'

        # 　特征词路径
        self.poet_name = os.path.join(cur_dir, 'dict/poet_name.txt')  # 诗人姓名
        self.poet_dynasty = os.path.join(cur_dir, 'dict/poet_dynasty.txt')  # 诗人朝代
        self.poet_info = os.path.join(cur_dir, 'dict/poet_info.txt')  # 诗人生平
        self.poet_work = os.path.join(cur_dir, 'dict/poet_works.txt')  # 诗人著作
        self.poetry_name = os.path.join(cur_dir, 'dict/poetry_name.txt')  # 古诗名
        self.poetry_info = os.path.join(cur_dir, 'dict/poetry_info.txt')  # 古诗内容

        # 加载特征词
        self.poet_name_wds = [i.strip() for i in open(self.poet_name, encoding="utf-8") if i.strip()]
        self.poet_dynasty_wds = [i.strip() for i in open(self.poet_dynasty, encoding="utf-8") if i.strip()]
        self.poet_info_wds = [i.strip() for i in open(self.poet_info, encoding="utf-8") if i.strip()]
        self.poet_work_wds = [i.strip() for i in open(self.poet_work, encoding="utf-8") if i.strip()]
        self.poetry_name_wds = [i.strip() for i in open(self.poetry_name, encoding="utf-8") if i.strip()]
        self.poetry_info_wds = [i.strip() for i in open(self.poetry_info, encoding="utf-8") if i.strip()]

        self.region_words = set(
            self.poet_name_wds + self.poet_dynasty_wds + self.poet_info_wds
            + self.poet_work_wds + self.poetry_name_wds + self.poetry_info_wds
        )

        # 构造领域actree，基于树匹配比关键词分割匹配更高效，ahocorasick是个现成的快速匹配函数
        self.region_tree = self.build_actree(list(self.region_words))  # 调用下面的build_actre函数

        # 构建词典
        self.wdtype_dict = self.build_wdtype_dict()  # 调用下面定义的build_wdtype_dict函数，构造词类型

        # 问句疑问词
        self.poet_name_qwds = ['什么姓名', '叫什么名字', '作者', '谁写的', '诗人']
        self.poet_dynasty_qwds = ['哪个朝代', '什么朝代', '抄代', '哪一代', '哪个朝代', '朝代']
        self.poet_info_qwds = ['生平是什么', '生平', '信息', '生平如何', '出生', '具体信息']
        self.poet_work_qwds = ['什么著名作品', '著作', '经典', '作品', '经典作品', '代表作']
        self.poetry_name_qwds = ['叫什么诗歌名字', '什么古诗名字', '古诗名字是什么', '什么名字', '什么诗', '什么词',
                                 '古诗名', '诗']
        self.poetry_info_qwds = ['内容']

    def build_wdtype_dict(self):
        """构造词对应的类型"""
        wd_dict = dict()
        # 找到用户输入的词是什么范围的
        for wd in self.region_words:
            wd_dict[wd] = []
            if wd in self.poet_name_wds:
                wd_dict[wd].append('poet_name')
            if wd in self.poet_dynasty_wds:
                wd_dict[wd].append('poet_dynasty')
            if wd in self.poet_info_wds:
                wd_dict[wd].append('poet_info')
            if wd in self.poet_work_wds:
                wd_dict[wd].append('poet_work')
            if wd in self.poetry_name_wds:
                wd_dict[wd].append('poetry_name')
            if wd in self.poetry_info_wds:
                wd_dict[wd].append('poetry_info')
        return wd_dict

    def check_medical(self, question):
        """获取到问句中属于节点中的词语"""
        # 定义一个列表储存存在节点中的词语
        region_wds = []
        # ahocorasick库 匹配问题  iter返回一个元组，i的形式如(5, (292, '123'))
        for i in self.region_tree.iter(question):
            wd = i[1][1]  # 匹配到的词
            region_wds.append(wd)
        # stop_wds取重复的短的词，如region_wds=['123','3']，则stop_wds=['3']
        stop_wds = []
        for wd1 in region_wds:
            # print(wd1)
            for wd2 in region_wds:
                if wd1 in wd2 and wd1 != wd2:
                    stop_wds.append(wd1)
        # final_wds获取到长度较长的词
        final_wds = [i for i in region_wds if i not in stop_wds]
        # 来自构造词典，# 获取词和词所对应的实体类型 {'阿尔泰狗娃花': ['study']}
        final_dict = {i: self.wdtype_dict.get(i) for i in final_wds}
        return final_dict

    def build_actree(self, wordlist):
        """创建AC自动机"""
        actree = ahocorasick.Automaton()  # 初始化trie树，ahocorasick 库 ac自动化 自动过滤违禁数据
        for index, word in enumerate(wordlist):
            actree.add_word(word, (index, word))  # 向trie树中添加单词
        actree.make_automaton()  # 将trie树转化为Aho-Corasick自动机
        return actree

    def classify(self, question):
        """分类主函数"""
        data = {}
        # 调用check_medical问句过滤函数
        # medical_dict = {'李白': ['poet_name']}
        medical_dict = self.check_medical(question)
        if not medical_dict:
            return {}
        data['args'] = medical_dict
        # 收集问句当中所涉及到的实体类型
        types = []
        for type_ in medical_dict.values():
            types += type_

        # 自定义
        question_type = 'others'

        question_types = []

        # 建立各联系
        # 诗人-->朝代
        if self.check_words(self.poet_dynasty_qwds, question) and ('poet_name' in types):
            question_type = 'poet_name_dynasty'
            question_types.append(question_type)

        # 诗人-->生平
        if self.check_words(self.poet_info_qwds, question) and ('poet_name' in types):
            question_type = 'poet_name_info'
            question_types.append(question_type)

        # 诗人-->著作
        if self.check_words(self.poet_work_qwds, question) and ('poet_name' in types):
            question_type = 'poet_name_work'
            question_types.append(question_type)

        # 诗人-->古诗名
        if self.check_words(self.poetry_name_qwds, question) and ('poet_name' in types):
            question_type = 'poet_name_poetry'
            question_types.append(question_type)

        # 诗人-->古诗内容
        if self.check_words(self.poetry_name_qwds, question) is not True and ('poet_name' in types) and (
                'poetry_name' in types):
            question_type = 'poet_poetry_info'
            question_types.append(question_type)

        # 朝代--》诗人
        if self.check_words(self.poet_name_qwds, question) and ('poet_dynasty' in types):
            question_type = 'poet_dynast_name'
            question_types.append(question_type)

        # 诗人自关联
        if question_types == [] and ('poet_name' in types) and ('poetry_name' not in types):
            question_type = 'poet_name'
            question_types.append(question_type)

        # 诗句自关联
        if question_types == [] and ('poetry_name' in types) and ('poet_name' not in types):
            question_type = 'poetry_name'
            question_types.append(question_type)

        # 将多个分类结果进行合并处理，组装成一个字典
        data['question_types'] = question_types
        # print(data)
        return data

    def check_words(self, wds, sent):
        for wd in wds:
            if wd in sent:
                return True
        return False


if __name__ == '__main__':
    question = QuestionClassifier()
    question.classify('李白是哪个朝代的')
    question.classify('李白的生平信息')
    question.classify('李白的著名作品有什么')
    question.classify('唐代有哪些诗人')
    question.classify('白居易')
    question.classify('望庐山瀑布')
    question.classify('李白写过什么诗词')
    question.classify('李白的望庐山瀑布')
