import numpy as np

R = np.array([
    [-1, -1, -1, -1, 0, -1],
    [-1, -1, -1, 0, -1, 100],
    [-1, -1, -1, 0, -1, -1],
    [-1, 0, 0, -1, 0, -1],
    [0, -1, -1, 0, -1, 100],
    [-1, 0, -1, -1, 0, 100]
])
Q = np.zeros([6,6])  # Q矩阵

goal_state = 5  # 目标状态
gamma = 0.8  # 折扣因子

for i in range(5000):
    state = np.random.randint(R.shape[0])  # 随机选取初始状态
    while True:  
        action = np.random.choice(np.where(R[state] >= 0)[0])  # 随机选取一个可行的动作
        nstate = action      # 执行的动作(就是下一状态)
        validaction = np.where(R[nstate] >= 0)[0]  # 获取当前状态下所有可行的动作

        Q[state, action] = R[state, action] + gamma * np.max([Q[nstate, chooseaction] for chooseaction in validaction])
        if nstate == goal_state:
            break  # 结束
        else:
            state = nstate  # 继续

print('Q矩阵:')
print(Q)


state = 2  # 起始状态
steps = [state]  # 路径
while state != goal_state:
    nstate = Q[state].argmax()
    steps.append(nstate)
    state = nstate

print('状态序列:', steps)
