#-*- coding:utf-8 –*-
import timeit,sys
import datetime
import numpy as np

class Vertex:
    def __init__(self, name, neighbor):
        self.name = name
        self.neighbor = neighbor
        self.store = neighbor

    def recover(self):
        self.neighbor = self.store

class Graph:
    def __init__(self, vertexList):
        self.name = "Never Give Up"
        self.vertexList = vertexList
        self.store = vertexList

    def degree(self, toBeElim):
        return len(self.vertexList[toBeElim].neighbor)

    def newEdge(self, toBeElim):
        neighbors = []
        for ver in self.vertexList:
            if ver == toBeElim:
                neighbors = ver.neighbor
        newEdge = 0
        print(toBeElim.name, ' ', neighbors)
        for verName in neighbors:
            for iver in self.vertexList:
                if verName == iver.name:
                    ver = iver
            for iver in neighbors:
                if (not verName == iver) and (iver not in ver.neighbor):
                    newEdge += 1
        return newEdge / 2

    def remove(self, toBeElim):
        name = toBeElim.name
        neighbors = []
        for ver in self.vertexList:
            if ver == toBeElim:
                neighbors = ver.neighbor
        newEdge = 0
        for verName in neighbors:
            for iver in self.vertexList:
                if verName == iver.name:
                    ver = iver
            for iver in neighbors:
                if (not verName == iver) and (iver not in ver.neighbor):
                    ver.neighbor.append(iver)
                    newEdge += 1
        for ver in self.vertexList:
            if name in ver.neighbor:
                ver.neighbor.remove(name)
        self.vertexList.remove(toBeElim)

    def recover(self):
        self.vertexList = self.store
        # for vertex in self.vertexList:
        #     vertex.recover()


class VariableElimination:
    @staticmethod
    def inference(factorList, queryVariables, orderedListOfHiddenVariables, evidenceList):
        for evidence in evidenceList:
            # Your code here
            # 把evidence全部实例化
            for factor in factorList:
                if evidence in factor.varList:
                    if evidence in factor.varList:
                        if len(factor.varList) > 1:
                            factorList.append(factor.restrict(evidence, evidenceList[evidence]))
                        factorList.remove(factor)

            # Your code end
        width = 0
        for ivariable in orderedListOfHiddenVariables:
            int_s = datetime.datetime.now().microsecond
            # Your code here
            # 变量删除
            toBeEliminate = list(filter(lambda afactor : ivariable in afactor.varList, factorList))
            new_var = toBeEliminate[0]
            for e in toBeEliminate:
                for i in factorList:
                    if i.name == e.name:
                        factorList.remove(i)

                if not 0 == toBeEliminate.index(e):
                    new_var = new_var.multiply(e)

            new_var = new_var.sumout(ivariable)
            factorList.append(new_var)
            for ifactor in factorList:
                nowWidth = len(ifactor.varList)
                if nowWidth > width:
                    width = nowWidth
            int_e = datetime.datetime.now().microsecond
            # print(ivariable, ' -> ',  int_e - int_s)
            # Your code end


        print("RESULT:")
        res = factorList[0]
        for factor in factorList[1:]:
            print(factor.varList)
            res = res.multiply(factor)
        print('Width : ', width)
        total = sum(res.cpt.values())
        res.cpt = {k: v/total for k, v in res.cpt.items()}
        res.printInf()

    @staticmethod
    def printFactors(factorList):
        for factor in factorList:
            factor.printInf()


class Util:
    @staticmethod
    def to_binary(num, len):
        return format(num, '0' + str(len) + 'b')


class Node:
    def __init__(self, name, var_list):
        self.name = name
        self.varList = var_list
        self.cpt = {}

    def setCpt(self, cpt):
        self.cpt = cpt

    def printInf(self):
        print("Name = " + self.name)
        print(" vars " + str(self.varList))
        for key in self.cpt:
            print ("   key: " + key + " val : " + str(self.cpt[key]))
        print ("")

    def multiply(self, factor):
        """function that multiplies with another factor"""
        #Your code here

        newList = [var for var in self.varList]
        new_cpt = {}

        # 存储相同变量在两个varList中的位置
        idx1 = []
        idx2 = []

        for var2 in factor.varList:
            if var2 in newList:
                idx1.append(self.varList.index(var2))
                idx2.append(factor.varList.index(var2))
            else:
                newList.append(var2)    # 把factor中有而self中没有的变量存入newList
                                            # 这样newList就包含两个node的全部变量
        # print(idx1,'|',idx2)
        for k1, v1 in self.cpt.items():
            for k2, v2 in factor.cpt.items():   # v1,v2是两个概率
                flag = True                 # 用于判断两个items中相同变量的正负性是否一致
                                            # 一致则说明找到用于相乘的两个变量items
                for i in range(len(idx1)):
                    if k1[idx1[i]] != k2[idx2[i]]:  # 存在同一变量在两边正负性相反的情况
                        flag = False
                        break
                if flag:
                    new_key = k1
                    for i in range(len(k2)):
                        if i in idx2:
                            continue
                        new_key += k2[i]    # 对应newList中的各个变量
                    new_cpt[new_key] = v1 * v2      # 概率相乘

        #Your code end
        new_node = Node("f" + str(newList), newList)
        new_node.setCpt(new_cpt)
        return new_node

    def sumout(self, variable):
        """function that sums out a variable given a factor"""
        #Your code here

        new_var_list = [var for var in self.varList]
        new_var_list.remove(variable)       # 删去需要累加的变量
        new_cpt = {}

        idx = self.varList.index(variable)  # 做累加的变量的位置

        for k, v in self.cpt.items():
            if k[:idx] + k[idx + 1:] not in new_cpt.keys(): # 还没记录的变量组合：创建和赋值
                new_cpt[k[:idx] + k[idx + 1:]] = v
            else:                                           # 已经记录的变量组合：累加
                new_cpt[k[:idx] + k[idx + 1:]] += v

        #Your code end
        new_node = Node("f" + str(new_var_list), new_var_list)
        new_node.setCpt(new_cpt)
        return new_node

    def restrict(self, variable, value):
        """function that restricts a variable to some value in a given factor"""
        # 也就是具体化一个变量
        #Your code here

        new_var_list = [i for i in self.varList]
        new_var_list.remove(variable)           # 删去需要具体化的变量
        new_cpt = {}

        idx = self.varList.index(variable)      # 具体化的变量的位置

        # 例如，现在要将Pr(A,B,C)具体化为Pr(~a,B,C)
        # 则传入参数variable = ‘a’，value = 0
        # 对cpt中一项(["A","B","C"],'011'：0.19)，经过变化后得到(["B","C"],‘11’：0.19)
        for k, v in self.cpt.items():
            if k[idx] == str(value):
                new_cpt[k[:idx] + k[idx + 1:]] = v

        #Your code end
        new_node = Node("f" + str(new_var_list), new_var_list)
        new_node.setCpt(new_cpt)
        return new_node

def chooseElimOrderInMinEdge(preorder, evidence, graph):
    for ie in evidence:
        for vertex in graph.vertexList:
            if vertex.name == trans[ie]:
                graph.remove(vertex)
    aftorder = []
    for i in range(len(preorder)):
        min = 999
        minNode = 'C'
        minVertex = Cv
        for vertex in graph.vertexList:
            # print(vertex.name)
            if vertex.name not in [trans[i] for i in preorder]: continue
            else:
                # print(vertex.name, ' - ', len(vertex.neighbor), vertex.neighbor)
                if len(vertex.neighbor) < min:
                    min = len(vertex.neighbor)
                    minNode = list(trans.keys())[list(trans.values()).index(vertex.name)]
                    minVertex = vertex
        aftorder.append(minNode)
        print(minNode)
        graph.remove(minVertex)
        preorder.remove(minNode)
    return aftorder

def chooseElimOrderInBestFill(preorder, evidence, graph):
    for ie in evidence:
        for vertex in graph.vertexList:
            if vertex.name == trans[ie]:
                graph.remove(vertex)
    aftorder = []
    for i in range(len(preorder)):
        min = 999
        minNode = 'C'
        minVertex = Cv
        for vertex in graph.vertexList:
            if vertex.name not in [trans[i] for i in preorder]: continue
            else:
                if graph.newEdge(vertex) < min:
                    print(vertex.name, ' - ', graph.newEdge(vertex))
                    min = graph.newEdge(vertex)
                    minNode = list(trans.keys())[list(trans.values()).index(vertex.name)]
                    minVertex = vertex
        aftorder.append(minNode)
        print(minNode)
        graph.remove(minVertex)
        preorder.remove(minNode)
    return aftorder

def chooseElimOrderInRandom(preorder, evidence):
    weight = {}
    aftorder = []
    for i in preorder:
        weight[i] = np.random.rand()
    weight = sorted(weight.items(), key = lambda kv:(kv[1], kv[0]))
    # print(weight)
    for i in weight:
        aftorder.append(i[0])
    # print(aftorder)
    return aftorder

def main():
    global trans
    trans = {'C': 'Cv', 'M': 'Mv', 'S': 'Sv', 'N': 'Nv', 'A': 'Av', 'P': 'Pv', 'D': 'Dv'}
    # create nodes for Bayes Net
    P = Node("P", ["P"])                        # PatientAge
    C = Node("C", ["C"])                        # CTScanResult
    M = Node("M", ["M"])                        # MRIScanResult
    A = Node("A", ["A"])                        # Anticoagulants
    S = Node("S", ["S", "C", "M"])              # StrokeType
    N = Node("N", ["N", "S", "A"])              # Mortality
    D = Node("D", ["D", "S", "P"])              # Disability

    # 建立邻接表
    global Pv                          # PatientAge
    Pv = Vertex('Pv', ['Dv'])
    global Cv                          # CTScanResult
    Cv = Vertex('Cv', ['Sv'])
    global Mv                          # MRIScanResult
    Mv = Vertex('Mv', ['Sv'])
    global Av                          # Anticoagulants
    Av = Vertex('Av', ['Nv'])
    global Sv                           # StrokeType
    Sv = Vertex('Sv', ['Cv', 'Mv', 'Nv', 'Dv'])
    global Nv                           # Mortality
    Nv = Vertex('Nv', ['Sv', 'Av'])
    global Dv                     # Disability
    Dv = Vertex('Dv', ['Sv', 'Pv'])

    G = Graph([Pv, Av, Sv, Cv, Mv, Nv, Dv])

    # Generate cpt for each node
    P.setCpt({'0': 0.1, '1': 0.3, '2': 0.6})
    C.setCpt({'0': 0.7, '1': 0.3})
    M.setCpt({'0': 0.7, '1': 0.3})
    A.setCpt({'0': 0.5, '1': 0.5})
    S.setCpt({'000': 0.8, '001': 0.5, '010': 0.5, '011': 0.0,
              '100': 0.0, '101': 0.4, '110': 0.4, '111': 0.9,
              '200': 0.2, '201': 0.1, '210': 0.1, '211': 0.1})
    N.setCpt({'000': 0.56, '010': 0.58, '020': 0.05, '001': 0.28, '011': 0.99, '021': 0.10,
              '100': 0.44, '110': 0.42, '120': 0.95, '101': 0.72, '111': 0.01, '121': 0.90})
    D.setCpt({'000': 0.80, '010': 0.70, '020': 0.90, '001': 0.60, '011': 0.50, '021': 0.40, '002': 0.30, '012': 0.20, '022': 0.10,
              '100': 0.10, '110': 0.20, '120': 0.05, '101': 0.30, '111': 0.40, '121': 0.30, '102': 0.40, '112': 0.20, '122': 0.10,
              '200': 0.10, '210': 0.10, '220': 0.05, '201': 0.10, '211': 0.10, '221': 0.30, '202': 0.30, '212': 0.60, '222': 0.80})


    # print("p1 = P(Mortality=’True’ & CTScanResult=’Ischemic Stroke’ | PatientAge=’31-65’ )")
    # VariableElimination.inference([P,C,M,A,S,N,D], ['N','C'], ['M','A','S','D'], {'P':1})
    #
    # print("p2 = P(Disability=’Moderate’ & CTScanResult=’Hemmorraghic Stroke’ | PatientAge=’65+’& MRIScanResult=’Hemmorraghic Stroke’)")
    # VariableElimination.inference([P,C,M,A,S,N,D], ['D','C'], ['A','S','N'], {'P':2,'M':1})
    #
    # print("p3 = P(StrokeType=’Hemmorraghic Stroke’ | PatientAge=’65+’ & CTScanResult=’Hemmorraghic Stroke’ & MRIScanResult=’Ischemic Stroke’)")
    # VariableElimination.inference([P,C,M,A,S,N,D], ['S'], ['A','N','D'], {'P':2,'C':1,'M':0})
    #
    # print("p4 = P(Anticoagulants=’Used’ | PatientAge=’31-65’)")
    # order4 = chooseElimOrderInMinEdge(['C', 'M', 'S', 'N', 'D'], ['P'], G)
    # VariableElimination.inference([P,C,M,A,S,N,D], ['A'], order4, {'P':1})
    # # 恢复到处理前的状态
    # Pv = Vertex('Pv', ['Dv'])
    # Cv = Vertex('Cv', ['Sv'])
    # Mv = Vertex('Mv', ['Sv'])
    # Av = Vertex('Av', ['Nv'])
    # Sv = Vertex('Sv', ['Cv', 'Mv', 'Nv', 'Dv'])
    # Nv = Vertex('Nv', ['Sv', 'Av'])
    # Dv = Vertex('Dv', ['Sv', 'Pv'])
    # G = Graph([Pv, Av, Sv, Cv, Mv, Nv, Dv])

    # print("p5 = P(Disability=’Negligible’)")
    # order5 = chooseElimOrderInMinEdge(['C', 'M', 'S', 'N', 'A', 'P'], [], G)
    # VariableElimination.inference([P,C,M,A,S,N,D], ['D'], order5, {})
    # # 恢复到处理前的状态
    # Pv = Vertex('Pv', ['Dv'])
    # Cv = Vertex('Cv', ['Sv'])
    # Mv = Vertex('Mv', ['Sv'])
    # Av = Vertex('Av', ['Nv'])
    # Sv = Vertex('Sv', ['Cv', 'Mv', 'Nv', 'Dv'])
    # Nv = Vertex('Nv', ['Sv', 'Av'])
    # Dv = Vertex('Dv', ['Sv', 'Pv'])
    # G = Graph([Pv, Av, Sv, Cv, Mv, Nv, Dv])

# 测时间，对于每个样例求其执行1000次的平均时间
    sumrun4 = 0
    for i in range (1000):
        print("p4 = P(Anticoagulants=’Used’ | PatientAges=’31-65’)")
        start4 = timeit.default_timer()
        # order4 = chooseElimOrderInMinEdge(['C', 'M', 'S', 'N', 'D'], ['P'], G)
        # VariableElimination.inference([P, C, M, A, S, N, D], ['A'], order4, {'P': 1})
        VariableElimination.inference([P,C,M,A,S,N,D], ['A'], ['N','S','C','M','D'], {'P':1})
        # 恢复到处理前的状态
        Pv = Vertex('Pv', ['Dv'])
        Cv = Vertex('Cv', ['Sv'])
        Mv = Vertex('Mv', ['Sv'])
        Av = Vertex('Av', ['Nv'])
        Sv = Vertex('Sv', ['Cv', 'Mv', 'Nv', 'Dv'])
        Nv = Vertex('Nv', ['Sv', 'Av'])
        Dv = Vertex('Dv', ['Sv', 'Pv'])
        G = Graph([Pv, Av, Sv, Cv, Mv, Nv, Dv])
        end4 = timeit.default_timer()
        run4 = (end4 - start4) * 1000
        sumrun4 += run4
    print('Average time of p4 : ', sumrun4/1000, ' ms\n')
#
    # sumrun5 = 0
    # for i in range(1000):
    #     print("p5 = P(Disability=’Negligible’)")
    #     start5 = timeit.default_timer()
    #     # order5 = chooseElimOrderInMinEdge['C', 'M', 'S', 'N', 'A', 'P'], [], G)
    #     VariableElimination.inference([P,C,M,A,S,N,D], ['D'], ['A', 'P', 'M', 'N', 'S', 'C'], {})
    #     # VariableElimination.inference([P, C, M, A, S, N, D], ['D'], ['A', 'C', 'P', 'N', 'M', 'S'], {})
    #     # 恢复到处理前的状态
    #     Pv = Vertex('Pv', ['Dv'])
    #     Cv = Vertex('Cv', ['Sv'])
    #     Mv = Vertex('Mv', ['Sv'])
    #     Av = Vertex('Av', ['Nv'])
    #     Sv = Vertex('Sv', ['Cv', 'Mv', 'Nv', 'Dv'])
    #     Nv = Vertex('Nv', ['Sv', 'Av'])
    #     Dv = Vertex('Dv', ['Sv', 'Pv'])
    #     G = Graph([Pv, Av, Sv, Cv, Mv, Nv, Dv])
    #     end5 = timeit.default_timer()
    #     run5 = (end5 - start5) * 1000
    #     sumrun5 += run5
    # print('Average time of p5 : ', sumrun5/1000, ' ms\n')

if __name__ == '__main__':
    main()