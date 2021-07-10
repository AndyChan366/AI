from scipy.stats import multivariate_normal
from sklearn import preprocessing
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

class GMM():
    def __init__(self, K, max_iter=500, error=1e-7):
        self.K = K                # 假设由K个GMM组成
        self.max_iter = max_iter  # 最大迭代次数
        self.error = error     # 收敛误差
        self.samples = 0      # 样本数
        self.features = 0    # 特征数
        self.alpha = []     # 权重
        self.mu = []       # 均值
        self.sigma = []   # 标准差

    def para(self, data):  # 相关参数
        np.random.seed(7)
        self.mu = np.array(np.random.rand(self.K, self.features))
        self.sigma = np.array([np.eye(self.features) / self.features] * self.K)
        self.alpha = np.array([1.0 / self.K] * self.K)
        # return self.mu,self.sigma,self.alpha
        # print("initial alpha:\n{}\n".format(self.alpha))
        # print("initial mu:\n{}\n".format(self.mu))
        # print("initial sigma:\n{}\n".format(self.sigma))
        # print(self.alpha.shape, self.mu.shape, self.sigma.shape)

    def gauss(self, Y, mu, sigma):  # 多元高斯分布(假设非奇异)
        return multivariate_normal(mean=mu, cov=sigma).pdf(Y)

    def preprocess(self, data):  # 数据预处理
        self.samples = data.shape[0]
        self.features = data.shape[1]
        pre = preprocessing.MinMaxScaler()
        return pre.fit_transform(data)

    def fit(self, data):  # 拟合数据
        data = self.preprocess(data)
        self.para(data)
        weighted_probs = np.zeros((self.samples, self.K))
        for i in range(self.max_iter):
            prev_weighted_probs = weighted_probs
            weighted_probs = self.ESTEP(data)
            change = np.linalg.norm(weighted_probs - prev_weighted_probs)
            if change < self.error:
                break
            self.MSTEP(data, weighted_probs)
        return weighted_probs.argmax(axis=1)

    def ESTEP(self, data):  # E-STEP
        probs = np.zeros((self.samples, self.K))
        for i in range(self.K):
            probs[:, i] = self.gauss(data, self.mu[i, :], self.sigma[i, :, :])
        weighted_probs = np.zeros(probs.shape)
        for i in range(self.K):
            weighted_probs[:, i] = self.alpha[i] * probs[:, i]
        for i in range(self.samples):
            weighted_probs[i, :] /= np.sum(weighted_probs[i, :])
        return weighted_probs

    def MSTEP(self, data, weighted_probs):  # M-STEP
        for i in range(self.K):
            sum_probs_i = np.sum(weighted_probs[:, i])
            self.mu[i, :] = np.sum(np.multiply(data, np.mat(weighted_probs[:, i]).T), axis=0) / sum_probs_i
            self.sigma[i, :, :] = (data - self.mu[i, :]).T * np.multiply((data - self.mu[i, :]),
                                                                         np.mat(weighted_probs[:, i]).T) / sum_probs_i
            self.alpha[i] = sum_probs_i / data.shape[0]

        # return self.alpha,self.mu,self.sigma
        # a=np.append[self.alpha]
        # print("alpha:\n{}\n".format(self.alpha))
        # print("mu:\n{}\n".format(self.mu))
        # print("sigma:\n{}\n".format(self.sigma))


    # def predict_prob(self, data):  # 预测概率矩阵
    #     return self.ESTEP(data)

    def predict(self, data):  # 输出类别
        return self.ESTEP(data).argmax(axis=1)

    def acc(self,getresult,result):
        if len(getresult) != len(result):
            raise ValueError("Dimension don't match!")
        correct = 0
        for i in range(len(getresult)):
            if getresult[i] == result[i]:
                correct += 1
        return correct/len(getresult)


f = open('iris.txt')
data_list = f.readlines()	    # 读出的是str类型
dataset = []
for data in data_list:
    data1 = data.strip('\n')	# 去掉换行符
    data2 = data1.split(',')	# 按,挑选数据
    dataset.append(data2)	    # 把这一行的结果作为元素加入列表dataset

dataset = np.array(dataset)
dataset = dataset.astype(float)

result = np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,\
                1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,\
                2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2])
# 可视化
# mpl.rcParams['font.sans-serif'] = [u'simHei']
# mpl.rcParams['axes.unicode_minus'] = False
# plt.scatter(dataset[:,0],dataset[:,1],c = result)
# plt.title("Iris种类与前两个属性图")
# plt.show()
# plt.scatter(dataset[:,2],dataset[:,3],c = result)
# plt.title("Iris种类与后两个属性图")
# plt.show()

gmm = GMM(3)

getresult = gmm.fit(dataset)


# print("convergence alpha:\n{}\n".format(gmm.alpha))
# print("convergence mu:\n{}\n".format(gmm.mu))
# print("convergence sigma:\n{}\n".format(gmm.sigma))
mpl.rcParams['font.sans-serif'] = [u'simHei']
mpl.rcParams['axes.unicode_minus'] = False
# plt.scatter(dataset[:,0],dataset[:,1],c = getresult)
# plt.title("GMM预测结果与前两个属性关系图")
# plt.show()
plt.scatter(dataset[:,2],dataset[:,3],c = getresult)
plt.title("GMM预测结果与后两个属性关系图")
plt.show()
print("Predict Result:\n{}\n".format(getresult))
print("True result:\n{}\n".format(result))
print("Accuracy:\n{}".format(gmm.acc(getresult,result)))

