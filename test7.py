# -*- coding: utf-8 -*-
import jieba
import os
def inputdata(new_path,my_dict,stop_file,precent):
    #list3用于将训练集和测试集返回
    list3 = []
    list1 = []
    stop_List = []
    # 将各个分类标签对应一些数字，对应关系存储在一个字典中，有新的分类则更新字典
    jieba.load_userdict(my_dict)
    # 导入停用词表
    stop_word = open(stop_file, 'r')
    context_stops = stop_word.readlines()
    # 根据停用词表的特点，将其用“，”分割，并去掉两端无用字符，将停用词放在stop_list列表
    for stopword in str(context_stops).strip('[\'').strip('\']').split(','):
        stop_List.append(stopword)

    #读取文件夹，遍历文件夹中的文件
    path_list = os.listdir(new_path)
    #默认文件夹深度只有一层,如文件夹有多层，遍历文件夹
    for i in path_list:
        #print(len(path_list))
        # list1 = [[],[],[]]

        with open(new_path+'\\'+i,'r', encoding='utf-8') as f:
            linelist = f.readlines()
            tag = str(linelist[0]).strip()[-1:]
            #print(tag)
            #移除列表第一个元素
            linelist.reverse()
            linelist.pop()
            linelist.reverse()

            #将多条新闻分隔开来
            newsList = str(linelist).split('---')
            for newList in newsList:
                #list2 = [str1,str2.....]
                list2 = []
                # 将文本中的空格替换为！，以便将其剔除
                for seq in jieba.cut(newList.strip().replace(' ', '!').replace('\n','!')):
                    if seq not in stop_List and len(seq) != 0 and seq != ',' and seq != r'\\t' and seq !='ufeff0' and seq != 'u3000' and seq != '﻿' and seq != r'\t' and seq != '\\' and seq != '，':
                        list2.append(seq)
                #将每条新闻分词之后所形成的列表存在list1中
                list1.append(list2)
            lens = len(list1)
            if (int(precent) > 50):
                list_tem = list1[:lens * precent // 100]
                for li in list_tem:
                    s1 = ' '.join(li)
                    list3.append(s1 + ':' + tag + '\n')
            else:
                list_tem = list1[lens * (100 - precent) // 100:]
                for li in list_tem:
                    s1 = ' '.join(li)
                    list3.append(s1 + ':' + tag + '\n')
    #若所需数据量大于50，则其为训练集，反之为测试集
    return list3
if __name__ == '__main__':
    #test()
    trainset = inputdata(r"C:\news", r'C:\my_word.txt', r'C:\stop_word.txt', 80)
    with open('C:\\trainset.txt','a+',encoding='utf-8') as tr:
        tr.writelines(trainset)
    testset = inputdata(r"C:\news", r'C:\my_word.txt', r'C:\stop_word.txt', 20)
    with open('C:\\testset.txt','a+',encoding='utf-8') as te:
        te.writelines(testset)
