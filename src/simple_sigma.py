#! /usr/bin/env python
# -*- coding: utf-8 -*-
from numpy import exp, array, random, dot

import di


class NeuronLayer():

    def __init__(self, number_of_neurons, number_of_inputs_per_neuron):
        self.synaptic_weights = 2 * \
            random.random((number_of_inputs_per_neuron, number_of_neurons)) - 1


class NeuralNetwork():

    def __init__(self, layer1, layer2):
        self.layer1 = layer1
        self.layer2 = layer2

    # Sigmoid函数，S形曲线
    # 传递输入的加权和，正规化为0-1
    def __sigmoid(self, x):
        return 1 / (1 + exp(-x))

    # Sigmoid函数的导数，Sigmoid曲线的梯度，表示对现有权重的置信程度
    def __sigmoid_derivative(self, x):
        return x * (1 - x)

    # 通过试错训练神经网络，每次微调突触权重
    def train(self, training_set_inputs, training_set_outputs, number_of_training_iterations):
        for iteration in range(number_of_training_iterations):
            # 将整个训练集传递给神经网络
            output_from_layer_1, output_from_layer_2 = self.think(training_set_inputs)

            # 计算第二层的误差
            layer2_error = training_set_outputs - output_from_layer_2
            layer2_delta = layer2_error * self.__sigmoid_derivative(output_from_layer_2)

            # 计算第一层的误差，得到第一层对第二层的影响
            layer1_error = layer2_delta.dot(self.layer2.synaptic_weights.T)
            layer1_delta = layer1_error * self.__sigmoid_derivative(output_from_layer_1)

            # 计算权重调整量
            layer1_adjustment = training_set_inputs.T.dot(layer1_delta)
            layer2_adjustment = output_from_layer_1.T.dot(layer2_delta)

            # 调整权重
            self.layer1.synaptic_weights += layer1_adjustment
            self.layer2.synaptic_weights += layer2_adjustment

    # 神经网络一思考
    def think(self, inputs):
        output_from_layer1 = self.__sigmoid(dot(inputs, self.layer1.synaptic_weights))
        output_from_layer2 = self.__sigmoid(dot(output_from_layer1, self.layer2.synaptic_weights))
        return output_from_layer1, output_from_layer2

    # 输出权重
    def print_weights(self):
        print("    Layer 1 (4 neurons, each with 3 inputs): ")
        print(self.layer1.synaptic_weights)
        print("    Layer 2 (1 neuron, with 4 inputs):")
        print(self.layer2.synaptic_weights)

if __name__ == "__main__":

    # 设定随机数种子
    random.seed(1)

    # 创建第一层 (4神经元, 每个3输入)
    layer1 = NeuronLayer(5, 3)

    # 创建第二层 (单神经元，4输入)
    layer2 = NeuronLayer(1, 5)

    # 组合成神经网络
    neural_network = NeuralNetwork(layer1, layer2)

    print("Stage 1) 随机初始突触权重： ")
    neural_network.print_weights()

    # 训练集，7个样本，均有3输入1输出
    training_set_inputs = array([[2, 3.3, 3.6], [1.2, 5.8, 13], [2.2, 3.2, 3], [
        2.3, 3.3, 2.9], [1.8, 3.2, 4.0], [1.55, 3.9, 5.6], [5.0, 3.9, 1.6],[3.3,3.3,2.1],[2.65,3.3,2.5]])
    training_set_outputs = array([[1, 1, 1, 0, 0, 1, 0, 0,0]]).T

    # mongo = di.Di().getMongoDb()

    # for r in mongo[""][""].find():

    t1 = [] 
    t2 = []
    f = open("copy.csv")
    for line in f:
        rt = line.split(",")
        t1.append([float(rt[1]),float(rt[2]),float(rt[3])])
        if float(rt[7]) == 3.0:
            t2.append(1)
        else:
            t2.append(0)
    # training_set_inputs = array(t1)
    # training_set_outputs = array([t2]).T
    # 用训练集训练神经网络
    # 迭代60000次，每次微调权重值
    neural_network.train(training_set_inputs, training_set_outputs, 100000)

    print("Stage 2) 训练后的新权重值： ")
    neural_network.print_weights()

    # 用新数据测试神经网络
    print("Stage 3) 思考新形势 [0, 0, 1] -> ?: [1,0,0]->? ")
    hidden_state, output = neural_network.think(array([[1.75, 3.5, 4.5]]))
    print(output)
