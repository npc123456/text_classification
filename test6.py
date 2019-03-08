# -*- coding: utf-8 -*-
from sklearn import svm
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import metrics
import warnings
import jieba
import os
import numpy as np

#去除各种警告
def warn_cancel():
    warnings.filterwarnings('ignore')

#将训练数据和测试数据切分为训练集和标签，以及测试集和标签
def splitset(trainset, testset):
    train_words = []
    train_tags = []
    test_words = []
    test_tags = []
    for i in trainset:
        i = i.strip()
        train_words.append(i[:-2])
        #-2为冒号的位置
        train_tags.append(int(i[-1]))
    for i in testset:
        i = i.strip()
        test_words.append(i[:-2])
        test_tags.append(int(i[-1]))
    return train_words, train_tags, test_words, test_tags

#将训练集和测试集中的特征词提取出来，并转为稀疏矩阵
def tfvectorize(train_words, test_words):
    warn_cancel()
    v = TfidfVectorizer()
    train_data = v.fit_transform(train_words)
    #v.get_feature_names(),可获取特征词
    test_data = v.transform(test_words)
    return train_data, test_data

#得到准确率
#test,re
def evaluate(actual, pred):
    warn_cancel()
    m_precision = metrics.precision_score(actual, pred)
    print('precision:{0:.3f}'.format(m_precision))


# 创建svm分类器
def train_clf(train_data, train_tags):
    warn_cancel()
    clf = svm.SVC(C=10.0,cache_size=200, class_weight=None, coef0=0.0,
    decision_function_shape=None, degree=3, gamma='auto', kernel='rbf',
    max_iter=-1, probability=False, random_state=None, shrinking=True,
    tol=0.001, verbose=False)
    clf.fit(train_data, train_tags)
    return clf

if __name__ == '__main__':
    tr = open('trainset.txt',encoding='utf-8').readlines()
    te = open('testset.txt',encoding='utf-8').readlines()
    train_words, train_tags, test_words, test_tags = splitset(tr, te)
    train_data, test_data = tfvectorize(train_words, test_words)
    clf = train_clf(train_data, train_tags)
    re = clf.predict(test_data)
    #re即为预测的测试集的分类
    #print(re)
    evaluate(test_tags, re)
