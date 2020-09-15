# -*- coding: utf-8 -*-
import jieba
import jieba.analyse
import unittest
from sklearn.metrics.pairwise import cosine_similarity
class CosineSimilarity(object):
    """
    余弦相似度
    """

    def __init__(self, content_x1, content_y2):
        self.s1 = content_x1
        self.s2 = content_y2
    @staticmethod
    def extract_keyword(content):  # 提取关键词
        # 切割
        seg = [i for i in jieba.cut(content, cut_all=True) if i != '']
        # 提取关键词
        keywords = jieba.analyse.extract_tags("|".join(seg), topK=200, withWeight=False)
        return keywords

    @staticmethod
    def one_hot(word_dict, keywords):  # oneHot编码
        # cut_code = [word_dict[word] for word in keywords]
        cut_code = [0]*len(word_dict)
        for word in keywords:
            cut_code[word_dict[word]] += 1
        return cut_code
    def calculate(self):
        # 提取关键词
        keywords1 = self.extract_keyword(self.s1)
        keywords2 = self.extract_keyword(self.s2)
        # 词的并集
        union = set(keywords1).union(set(keywords2))
        # 编码
        word_dict = {}
        i = 0
        for word in union:
            word_dict[word] = i
            i += 1
        # oneHot编码
        s1_cut_code = self.one_hot(word_dict, keywords1)
        s2_cut_code = self.one_hot(word_dict, keywords2)
        # 余弦相似度计算
        sample = [s1_cut_code, s2_cut_code]
        # 除零处理
        try:
            sim = cosine_similarity(sample)
            return sim[1][0]
        except Exception as e:
            print(e)
            return 0.0

class Test(unittest.TestCase):
    def test1(self):
        "改动0.8的文本"
        with open("E:\学校\大三上\软件工程\第一次编程作业：查重\sim_0.8\orig.txt",encoding="utf-8") as fp:
            ori = fp.read()
        with open("E:\学校\大三上\软件工程\第一次编程作业：查重\sim_0.8\orig_0.8_add.txt",encoding="utf-8") as fp:
            copy = fp.read()
        model = CosineSimilarity(ori,copy)
        ans = model.calculate()
        self.assertEqual(round(ans,2), 0.8)
    def test2(self):
        "相同文本"
        with open("E:\学校\大三上\软件工程\第一次编程作业：查重\sim_0.8\orig.txt",encoding="utf-8") as fp:
            ori = fp.read()
        with open("E:\学校\大三上\软件工程\第一次编程作业：查重\sim_0.8\orig.txt",encoding="utf-8") as fp:
            copy = fp.read()
        model = CosineSimilarity(ori,copy)
        ans = model.calculate()
        self.assertEqual(round(ans,2), 1.0)
    def test3(self):
        "空文本"
        with open("E:\学校\大三上\软件工程\第一次编程作业：查重\sim_0.8\orig.txt",encoding="utf-8") as fp:
            ori = fp.read()
        with open("E:\学校\大三上\软件工程\第一次编程作业：查重\sim_0.8\empty.txt",encoding="utf-8") as fp:
            copy = fp.read()
        model = CosineSimilarity(ori,copy)
        ans = model.calculate()
        self.assertEqual(ans, 0.0)

if __name__ == '__main__':
    unittest.main()
