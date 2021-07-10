# coding: utf-8
# In[1]:
import logging

logger = logging.getLogger(__name__)
logger.setLevel(level = logging.INFO)
handler = logging.FileHandler("DT-prepruning.log")
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.info("Depth 5, no shuffle, 0.9 train data")


# In[2]:
import pandas as pd
import numpy as np

attrlist = {"age":0, "workclass":1, "fnlwgt":0, "education":1, "education-num":0, "marital-status":1, "occupation":1, "relationship":1, "race":1, "sex":1, "capital-gain":0, "capital-loss":0, "hours-per-week":0, "native-country":1, "salary":0} # 0: continuous, 1: discrete

traindata = pd.read_csv("../data/adult/adult.data", names=attrlist.keys(), index_col=False)
testdata = pd.read_csv("../data/adult/adult.test",names=attrlist.keys(),index_col=False,header=0)

def preprocessing(data):
    attributes = list(attrlist.keys())
    return data[attributes]

def fulldata(data):
    #填充缺失数据，方法是选择该列出现最多的数据填入该位置。
    for a in attrlist:
        if attrlist[a]: # 离散
            data.loc[data[a] == " ?",a] = data[a].value_counts().argmax() 
        else: # 连续
            pass

# 得到数据集
traindata = preprocessing(traindata)
testdata = preprocessing(testdata)
fulldata(traindata)
fulldata(testdata)

# 9：1分配训练集与观测集
breakpoint = int(0.9 * len(traindata))
# breakpoint = int(len(traindata))
traindata, valdata = traindata[:breakpoint], traindata[breakpoint:]


# In[3]:
def entropy(p):
    #计算熵
    if p.ndim == 1:
        nextp = p[p != 0]
        return -np.sum(nextp * np.log2(nextp))
    else:
        return -np.sum(p * np.log2(p),axis=1)

def information_gain(D,a,discrete_flag=False):
    #计算信息增益
    pk = D["salary"].value_counts(normalize=True).values
    if discrete_flag: # 离散
        perDv = D[a].value_counts(normalize=True).values 
        probDv = np.array([D.loc[D[a] == av]["salary"].value_counts(normalize=True).get(" >50K",0) for av in D[a].unique()])
        hstack = np.column_stack((perDv,probDv))
        hstack = hstack[(hstack[:,1] != 0) & (hstack[:,1] != 1)]
        perDv = hstack[:,0]
        probDv = hstack[:,1]
        probDv_not = 1 - probDv
        return (entropy(pk) - np.sum(perDv * entropy(np.column_stack((probDv,probDv_not)))), a)
    else: # 连续
        newa = sorted(D[a].unique())
        T_a = [(newa[i] + newa[i+1]) / 2 for i in range(len(newa)-1)]
        entmin, tmin = 0x3f3f3f3f, newa[0]
        for t in T_a: 
            perDv = len(D[D[a] < t]) / len(D)
            perDv = np.array([perDv,1-perDv])
            probDv_smaller = D[D[a] < t]["salary"].value_counts(normalize=True).get(" >50K",0)
            probDv_bigger = D[D[a] >= t]["salary"].value_counts(normalize=True).get(" >50K",0)
            probDv = np.array([[probDv_smaller,1-probDv_smaller],[probDv_bigger,1-probDv_bigger]])
            probDv = probDv[(probDv[:,0] != 0) & (probDv[:,1] != 0)]
            if len(probDv) == 0:
                sumup = 0
            else:
                sumup = np.sum(perDv * entropy(probDv))
            if entmin > sumup:
                entmin = sumup
                tmin = t
        return (entropy(pk) - entmin, tmin)


# In[4]:
class Node:

    def __init__(self):
        self.branch = {}

    def setLeaf(self,catagory,cnt=1):
        logger.info("{} - Create leaf: {}".format(cnt,catagory))
        if cnt % 10 == 0:
            print("{} - Create leaf: {}".format(cnt,catagory),flush=True)
        self.label = "Leaf"
        self.catagory = catagory
        
    def setBranch(self,attr,value,node,branch_value=None):
        logger.info("Create branch: {} ({})".format(attr,value))
        self.label = "Branch"
        self.attr = attr
        self.branch[value] = node
        if branch_value != None:
            self.branch_value = branch_value


# In[5]:
import time,sys

class ID3:
    # ID3算法实现
    def __init__(self,trainset=None,validationset=None,testset=None,attrlist=None):
        self.trainset = trainset
        self.validationset = validationset
        self.testset = testset
        self.attrlist = attrlist

    def TreeGenerate(self,dataset,attributes,depth,cnt_leaves=0,root=None):
        catagory = dataset["salary"].unique()
        node = Node() if root == None else root 
        cnt_leaves += 1

        # 1) All samples in `dataset` belongs to the same catagory
        if len(catagory) == 1:
            node.setLeaf(catagory[0],cnt_leaves)
            return node

        # 2) `attributes` is empty, or the values of `dataset` on `attributes` are the same
        if len(attributes) == 0 or np.array([len(dataset[a].unique()) == 1 for a in attributes]).all() == True:
            node.setLeaf(dataset["salary"].value_counts().argmax(),cnt_leaves)
            return node

        # without partition
        node.setLeaf(dataset["salary"].value_counts().argmax(),cnt_leaves)
        accuracy_without_partition = self.validation()

        # with partition
        # 找带来最大增益的属性
        max_gain = (-0x3f3f3f3f,None)
        for a in attributes:
            gain = information_gain(dataset,a,self.attrlist[a])
            if gain[0] > max_gain[0]:
                aright, max_gain = a, gain
        num_leaves = 0
        if self.attrlist[aright]: # 离散
            num_leaves = len(self.trainset[aright].unique())
            for av in self.trainset[aright].unique(): 
                Dv = dataset[dataset[aright] == av]
                cnt_leaves += 1
                leafnode = Node()
                if len(Dv) == 0:
                    leafnode.setLeaf(dataset["salary"].value_counts().argmax(),cnt_leaves)
                else:
                    leafnode.setLeaf(Dv["salary"].value_counts().argmax(),cnt_leaves)
                node.setBranch(aright,av,leafnode)
        else: # 连续
            num_leaves = 2
            for flag in ["Smaller","Bigger"]:
                Dv = dataset[dataset[aright] < max_gain[1]] if flag == "Smaller" else dataset[dataset[aright] >= max_gain[1]]
                cnt_leaves += 1
                leafnode = Node()
                if len(Dv) == 0:
                    leafnode.setLeaf(dataset["salary"].value_counts().argmax(),cnt_leaves)
                else:
                    leafnode.setLeaf(Dv["salary"].value_counts().argmax(),cnt_leaves)
                node.setBranch(aright,flag,leafnode,branch_value=max_gain[1])
        accuracy_with_partition = self.validation()

        # prepruning
        if depth > 5 and accuracy_without_partition >= accuracy_with_partition:
            cnt_leaves -= num_leaves
            print("Prune at {}: {} (without) >= {} (with)".format(aright,accuracy_without_partition,accuracy_with_partition))
            logger.info("Prune at {}: {} (without) >= {} (with)".format(aright,accuracy_without_partition,accuracy_with_partition))
            node.setLeaf(dataset["salary"].value_counts().argmax())
            return node
        elif depth > 5:
            print(aright,accuracy_without_partition,accuracy_with_partition)

        if self.attrlist[aright]: # 离散
            for av in self.trainset[aright].unique(): 
                Dv = dataset[dataset[aright] == av]
                # 3) `Dv` is empty, which can not be partitioned
                if len(Dv) != 0:
                    node.setBranch(aright,av,self.TreeGenerate(Dv,attributes[attributes != aright],depth+1,cnt_leaves))
        else: # 连续
            for flag in ["Smaller","Bigger"]:
                Dv = dataset[dataset[aright] < max_gain[1]] if flag == "Smaller" else dataset[dataset[aright] >= max_gain[1]]
                if len(Dv) != 0:
                    node.setBranch(aright,flag,self.TreeGenerate(Dv,attributes,depth+1,cnt_leaves),branch_value=max_gain[1])
        return node

    def train(self,trainset=None):
        # 训练
        if trainset != None:
            self.trainset = trainset
        start_time = time.time()
        self.root = Node()
        self.root = self.TreeGenerate(self.trainset,self.trainset.columns.values[self.trainset.columns.values != "salary"],depth=1,root=self.root,cnt_leaves=0)
        logger.info("Time: {:.2f}s".format(time.time()-start_time))
        print("Time: {:.2f}s".format(time.time()-start_time))

    def validation(self,validationset=None):
        # 验证
        if validationset != None:
            self.validationset = validationset
        accuracy = 0
        for i,row in self.validationset.iterrows():
            p = self.root
            while p.label != "Leaf": 
                if self.attrlist[p.attr]: # 离散
                    p = p.branch[row[p.attr]]
                else: # 连续
                    p = p.branch["Smaller"] if row[p.attr] < p.branch_value else p.branch["Bigger"]
            if p.catagory == row["salary"]:
                accuracy += 1
        accuracy /= len(self.validationset)
        return accuracy

    def test(self,testset=None):
        # 测试
        if testset != None:
            self.testset = testset
        accuracy = 0
        for i,row in self.testset.iterrows():
            p = self.root
            while p.label != "Leaf": 
                if self.attrlist[p.attr]: # 离散
                    p = p.branch[row[p.attr]]
                else: # 连续
                    p = p.branch["Smaller"] if row[p.attr] < p.branch_value else p.branch["Bigger"]
            if p.catagory == row["salary"][:-1]: 
                accuracy += 1
        accuracy /= len(self.testset)
        logger.info("Accuracy: {:.2f}%".format(accuracy * 100))
        print("Accuracy: {:.2f}%".format(accuracy * 100))
        return accuracy


# In[6]:
dt = ID3(trainset=traindata,validationset=valdata,testset=testdata,attrlist=attrlist)
dt.train()
dt.test()


