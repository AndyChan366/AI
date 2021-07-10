import nn
import pickle
import os, sys, time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



# 0: continuous,1: nominal,2: categorical/discrete
attrlist = {"surgery": 1,
 "Age": 2,
 "Hospital Number": 1,
 "rectal temperature": 0,
 "pulse": 0,
 "respiratory rate": 0,
 "temperature of extremities": 2,
 "peripheral pulse": 2,
 "mucous membranes": 1,
 "capillary refill time": 2,
 "pain": 1,
 "peristalsis": 2,
 "abdominal distension": 1,
 "nasogastric tube": 1,
 "nasogastric reflux": 2,
 "nasogastric reflux PH": 0,
 "rectal examination": 2,
 "abdomen": 1,
 "packed cell volume": 0,
 "total protein": 0,
 "abdominocentesis appearance": 1,
 "abdomcentesis total protein": 0,
 "outcome": 1,
 "surgical lesion": 1,
 "type of lesion 1": 1,
 "type of lesion 2": 1,
 "type of lesion 3": 1,
 "cp_data": 1} 

train_data = pd.read_csv("horse-colic.data",names=attrlist.keys(),index_col=False,delim_whitespace=True)
test_data = pd.read_csv("horse-colic.test",names=attrlist.keys(),index_col=False,delim_whitespace=True)


def preprocessing(data):
    removelist = ["type of lesion 2", "type of lesion 3","Hospital Number","nasogastric reflux PH","abdomcentesis total protein"]
    attributes = []
    for a in data.columns.values:
        indata = attrlist.get(a,None)
        if indata == None:    # newly append
            attributes.append(a)
        elif indata == 0 and a not in removelist: # continuous
            attributes.append(a)
        else: # discrete, no need to append
            pass
    df = data[attributes]
    return df


def fulldata(data):
    """
    Fill the missing data
    For continuous: fill them with mean values
    For discrete: fill them with the mode values
    """
    for a in data.columns.values:
        if a in ["type of lesion 1", "Hospital Number"]: # remove
            continue
        if data[a].dtype != np.int64:   # missing data
            have_data = data[data[a] != "?"][a]
            if attrlist[a]:   # discrete
                data.loc[data[a] == "?",a] = have_data.value_counts().idxmax() # mode values
                if a != "outcome" and attrlist[a] != 2:
                    # generate one-hot encoding
                    data[a] = pd.Categorical(data[a])
                    dummies = pd.get_dummies(data[a],prefix="{}_category".format(a))
                    data = pd.concat([data,dummies],axis=1)
            else:    # continuous
                data.loc[data[a] == "?",a] = np.mean(have_data.astype(np.float))  # mean values
        elif attrlist[a] == 1:
            # generate one-hot encoding
            data[a] = pd.Categorical(data[a])
            dummies = pd.get_dummies(data[a],prefix="{}_category".format(a))
            data = pd.concat([data,dummies],axis=1)
    return data.astype(np.float)


data = pd.concat([train_data,test_data],axis=0)
data = fulldata(data)
label = data["outcome"].astype(np.float)
train_label, test_label = label[:len(train_data)], label[len(train_data):]
train_label = [[1,0,0] if label == 1 else ([0,1,0] if label == 2 else [0,0,1]) for label in train_label]
# train_data, test_data = data[:len(train_data)], data[len(train_data):]
# train_data = preprocessing(train_data)
# test_data = preprocessing(test_data)
data = preprocessing(data)
train_data, test_data = data[:len(train_data)], data[len(train_data):]
# print(train_data.columns)
# print(len(train_data.columns))


def minibatch(data,label,batchsize=16):
    num_batches = len(data) // batchsize
    for i in range(0,num_batches,batchsize):
        yield data[i:i+batchsize].to_numpy(), np.array(label[i:i+batchsize])

def train(net,max_iter=70000):
    losslist, acclist = [], []
    losses = []
    for i in range(max_iter):
        net.train()
        batches = minibatch(train_data,train_label,16) # generator
        for x, y in batches:
            y_hat = net.forwardpass(x)
            loss = net.MSE(y_hat, y)
            losses.append(loss)
            # net.backpass(y_hat,y)   # disable weight decay
            net.backpass(y_hat,y,0.1) # enable weight decay

        # update learning rate and record parameters
        if (i+1) % 100 == 0:
            avg_loss = np.array(losses).mean()
            losslist.append(avg_loss)
            losses = []
            acc = test(net,test_data,test_label)
            acclist.append(acc)
            if (i+1) % 1000==0:
                net.learning_rate *= 0.99
    return losslist, acclist


def test(net,test_X,test_Y,flag=True,print_flag=False):
    count = 0
    for j, x in test_X.iterrows():
        net.end()
        y_hat = net.forwardpass(x.to_numpy().reshape(1,-1))
        predicted = np.argmax(y_hat) + 1
        y = test_Y[j]
        if print_flag:
            print(y_hat,predicted,y)
        if flag:
            if predicted == y:
                count += 1
        else:
            if [1 if t + 1 == predicted else 0 for t in range(3)] == y:
                count += 1
    return (count / len(test_X))



# print(len(test_data.columns.values))
# print(len(train_data.columns.values))
start_time=time.time()
net = nn.Network(len(test_data.columns.values),8,3,0.01)
losslist, acclist = train(net,70000)
print(acclist[-1])
end_time=time.time()
print("Time:{}s".format(end_time-start_time))
print(net.w_ih)
print("\n")
print(net.w_ho)

# plot
fig = plt.figure()
ax = fig.add_subplot(111)
lns1 = ax.plot(losslist,label="Loss")
ax2 = ax.twinx()
lns2 = ax2.plot(acclist,"-r",label="Accuracy")
lns = lns1 + lns2
labs = [l.get_label() for l in lns]
ax.legend(lns,labs,loc=0)
ax.set_xlabel("Iteration (x100)")
ax.set_ylabel("Loss")
ax2.set_ylabel("Accuracy")
ax2.set_ylim(0,1)
plt.savefig(r"fig/iteration.pdf",format="pdf",dpi=200)
plt.show()


