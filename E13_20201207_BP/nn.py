import numpy as np

class fullparam(object):

    def __init__(self, in_features, out_features,bias):
        self.in_features = in_features
        self.out_features = out_features
        self.weight = np.random.normal(0,np.sqrt(2/in_features),(out_features,in_features))  # kaiming
        if bias:
            self.bias = np.random.rand(out_features)
        else:
            self.bias = None

    def forward(self, inputs):
        if type(self.bias) != type(None):
            return np.dot(inputs, self.weight.T) + self.bias
        else:
            return np.dot(inputs, self.weight.T)

    def __call__(self,x):
        return self.forward(x)

class Network(object):

    def __init__(self,in_features,hidden_features,out_features,learning_rate=0.01):
        self.w_ih = fullparam(in_features,hidden_features,True)
        self.w_ho = fullparam(hidden_features,out_features,True)
        self.learning_rate = learning_rate
        self.memory = {}  # used for store results
        self.train_flag = True

    def train(self):
        self.train_flag = True

    def end(self):
        self.train_flag = False

    def sigmoid(self,x):
        return 1 / (1 + np.exp(-x))

    def d_sigmoid(self,x):
        return self.sigmoid(x) * (1 - self.sigmoid(x))

    def MSE(self,y_hat,y):
        return (np.linalg.norm(y_hat - y)) * (np.linalg.norm(y_hat - y))   # mean square error

    def forwardpass(self,x):
        # training
        if self.train_flag:
            self.memory["a0"] = np.copy(x)
            x = self.w_ih(x)      # between input and hidden
            self.memory["z1"] = np.copy(x)
            x = self.sigmoid(x)
            self.memory["a1"] = np.copy(x)
            x = self.w_ho(x)     # between hidden and out
            self.memory["z2"] = np.copy(x)
            x = self.sigmoid(x)
        # train end
        else:
            x = self.w_ih(x)
            x = self.sigmoid(x)
            x = self.w_ho(x)
            x = self.sigmoid(x)
        return x

    def backpass(self,y_hat,y,lamb=0):
        batchsize = y.shape[0]
        delta = [0] * 3
        # out layer delta calculate
        delta[2] = (y_hat - y) * self.d_sigmoid(self.memory["z2"])
        # hidden layer delta calculate
        delta[1] = np.dot(delta[2],self.w_ho.weight) * self.d_sigmoid(self.memory["z1"])
        grad_W = [0] * 2
        # N * out_features * hidden_features
        grad_W[1] = np.einsum("ij,ik->ijk",delta[2],self.memory["a1"])
        # N * hidden_features * in_features
        grad_W[0] = np.einsum("ij,ik->ijk",delta[1],self.memory["a0"])
        # every col's mean value
        grad_W[1] = grad_W[1].mean(axis=0)
        grad_W[0] = grad_W[0].mean(axis=0)
        # weight update
        self.w_ho.weight -= self.learning_rate * (grad_W[1] + lamb * self.w_ho.weight / batchsize)
        self.w_ih.weight -= self.learning_rate * (grad_W[0] + lamb * self.w_ih.weight / batchsize)