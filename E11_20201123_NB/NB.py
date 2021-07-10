import os, sys, time
import pandas as pd
import numpy as np

attrlist = {"age":0, "workclass":1, "fnlwgt":0, "education":1, "education-num":0, "marital-status":1, "occupation":1, "relationship":1, "race":1, "sex":1, "capital-gain":0, "capital-loss":0, "hours-per-week":0, "native-country":1, "salary":0} # 0: continuous, 1: discrete

traindata = pd.read_csv("adult.data",names=attrlist.keys(),index_col=False)
testdata = pd.read_csv("adult.test",names=attrlist.keys(),index_col=False,header=0)

def preprocessing(data):
    attributes = list(attrlist.keys())
    # attributes.remove("fnlwgt")
    # attributes.remove("capital-gain")
    # attributes.remove("capital-loss")
    return data[attributes]

def fulldata(data):
    # 填充缺失数据，方法是选择该列出现最多的数据填入该位置。
    for a in data.columns.values:
        if attrlist[a]:  # 离散
            data.loc[data[a] == " ?", a] = data[a].value_counts().argmax()  # 众数
        else:  # 连续则跳过
            pass
    # if data == testdata:
    #     for b in data.columns.values:
    #         if attrlist[b]:  # 离散
    #             data.loc[data[b] == " ?", b] = data[b].mean() # 众数
    #         else:  # 连续则跳过
    #             pass
    return data

# Data cleaning
traindata = preprocessing(traindata)
testdata = preprocessing(testdata)
traindata = fulldata(traindata)
testdata = fulldata(testdata)

class NB():
    # 贝叶斯分类器实现
    def __init__(self,traindata,attrlist):
        self.traindata = traindata
        self.attrlist = attrlist
        # 计算概率P(x_i|y)
        self.prob = {}
        self.prob[" >50K"] = traindata["salary"].value_counts(normalize=True)[" >50K"]
        self.prob[" <=50K"] = 1 - self.prob[" >50K"]
        self.attributes = traindata.columns.values[traindata.columns.values != "salary"]
        leq = traindata[traindata["salary"] == " <=50K"]
        geq = traindata[traindata["salary"] == " >50K"]
        for a in self.attributes:
            if self.attrlist[a]: # 离散
                numofleq = leq[a].value_counts()
                numofgeq = geq[a].value_counts()
                N = len(traindata[a].unique())
                l = len(leq)
                g = len(geq)
                for xi in traindata[a].unique():
                    # 拉普拉斯平滑处理
                    self.prob[(xi," <=50K")] = (numofleq.get(xi,0) + 1) / (N + l)
                    self.prob[(xi," >50K")] = (numofgeq.get(xi,0) + 1) / (N + g)
            else: # 连续情况则用高斯分布
                muofleq = np.mean(leq[a])
                sigmaofleq = np.var(leq[a])
                self.prob[(a," <=50K")] = lambda x:  np.exp(-(x-muofleq)**2/(2*sigmaofleq)) / np.sqrt(2*np.pi*sigmaofleq)
                muofgeq = np.mean(geq[a])
                sigmaofgeq = np.var(geq[a])
                self.prob[(a," >50K")] = lambda x:   np.exp(-(x-muofgeq)**2/(2*sigmaofgeq)) / np.sqrt(2*np.pi*sigmaofgeq)

    def predict(self,testdata):
        # 预测
        accuracy = 0
        for i, row in testdata.iterrows():
            # 遍历行数据，计算概率P(y|x1,...,xn)
            prod = np.array([self.prob[" <=50K"],self.prob[" >50K"]])
            for a in self.attributes:
                xi = row[a]
                if self.attrlist[a]: # 离散
                    prod[0] *= (self.prob[(xi," <=50K")])
                    prod[1] *= (self.prob[(xi," >50K")])
                else: # 连续
                    prod[0] *= (self.prob[(a," <=50K")](xi))
                    prod[1] *= (self.prob[(a," >50K")](xi))

            # 找到最大概率的那一个
            if prod.argmax() == 0:
                catagory = " <=50K"
            else:
                catagory = " >50K"
            if catagory == row["salary"][:-1]:
                accuracy += 1
            #每统计完1000次输出一下：
            #if i % 1000 == 0:
            #   print("Finish {}/{}".format(i,len(testdata)))

        accuracy /= len(testdata)
        print("Accuracy: {:.2f}%".format(accuracy * 100))
        return accuracy
start = time.time()
nb = NB(traindata,attrlist)
nb.predict(testdata)
end = time.time()
print('Runtime: ' + str(end-start) + 's')