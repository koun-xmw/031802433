# -*- coding: utf-8 -*-
#分词包
import jieba
import jieba.analyse
# 机器学习包，用于计算两个向量的余弦相似度
from sklearn.metrics.pairwise import cosine_similarity
#用于读取命令行参数
import sys

class CosineSimilarity(object):
    #构造函数，传入两个参数
    def __init__(self, content_x1, content_y2):
        self.s1 = content_x1
        self.s2 = content_y2

    @staticmethod
    def extract_keyword(content):  # 提取关键词
        # 切割
        seg = [i for i in jieba.cut(content, cut_all=True) if i != '']#分词
        # 提取关键词，按照权重返回前topK个关键词
        keywords = jieba.analyse.extract_tags("|".join(seg), topK=topK, withWeight=False)
        return keywords

    @staticmethod
    def one_hot(word_dict, keywords):  # oneHot编码
        cut_code = [0]*len(word_dict) #初始化为0向量
        for word in keywords:
            cut_code[word_dict[word]] += 1#在对应的位置+1
        return cut_code

    def calculate(self):
        # 去除停用词，由于不让调用外部文件，停用词就不去了
        # jieba.analyse.set_stop_words('cn_stopword.txt')
        # 提取关键词
        keywords1 = self.extract_keyword(self.s1)
        keywords2 = self.extract_keyword(self.s2)
        # 两篇文章关键词的并集
        union = set(keywords1).union(set(keywords2))
        # 利用字典构造hash表
        word_dict = {}
        i = 0
        for word in union:
            word_dict[word] = i
            i += 1
        # oneHot编码
        vector1 = self.one_hot(word_dict, keywords1)
        vector2 = self.one_hot(word_dict, keywords2)
        # 余弦相似度计算
        sample = [vector1,vector2]#sample 为2xtopK的矩阵，topK表示向量的维度（关键词的个数），2表示有两篇文章进行比较
        # 除零处理
        try:
            simRate = cosine_similarity(sample)#simRate为ndarray类型，simRate[x][y]表示第x篇文章和第y篇文章的余弦相似度
            return simRate[1][0]                #因此sim为对称矩阵
        except Exception as e:
            print(e)
            return 0.0


# 测试
if __name__ == '__main__':
    #获取由命令行输入的三个参数
    oriPath = sys.argv[1]
    copyPath = sys.argv[2]
    ansPath = sys.argv[3]
    #获取topK
    try:
        with open(oriPath,encoding='UTF-8') as fp:
            ori = fp.read()
            seg = [i for i in jieba.cut(ori, cut_all=True) if i != '']
        topK = int(len(seg) / 9)
    except:
        print("路径错误")
        topK = 0
    #读入两段文本
    try:
        with open(oriPath,encoding='UTF-8') as fp:
            ori = fp.read()
        with open(copyPath,encoding='UTF-8') as fp:
            copy = fp.read()
    except:
        print("路径错误")
    #建立模型
    model = CosineSimilarity(ori,copy)
    #计算结果并保留两位小数
    similarity = round(model.calculate(),2)
    # 输出文本
    try:
        with open(ansPath,"w+",encoding='UTF-8') as fp:
            fp.write(str(similarity))
    except:
        print("路径错误")
