import math
import random
import numpy as np
import pandas as pd
import os
import requests
from matplotlib import pyplot as plt
from tqdm import tqdm
import time


def one_hot(data: np.ndarray) -> np.ndarray:
    y_train = np.zeros((data.size, data.max() + 1))
    rows = np.arange(data.size)
    y_train[rows, data] = 1
    return y_train


def plot(loss_history: list, accuracy_history: list, filename='plot'):

    # function to visualize learning process at stage 4

    n_epochs = len(loss_history)

    plt.figure(figsize=(20, 10))
    plt.subplot(1, 2, 1)
    plt.plot(loss_history)

    plt.xlabel('Epoch number')
    plt.ylabel('Loss')
    plt.xticks(np.arange(0, n_epochs, 4))
    plt.title('Loss on train dataframe from epoch')
    plt.grid()

    plt.subplot(1, 2, 2)
    plt.plot(accuracy_history)

    plt.xlabel('Epoch number')
    plt.ylabel('Accuracy')
    plt.xticks(np.arange(0, n_epochs, 4))
    plt.title('Accuracy on test dataframe from epoch')
    plt.grid()

    plt.savefig(f'{filename}.png')


def scale(X_train, X_test):
    maximus = np.concatenate((X_train, X_test)).max()
    X_train_scaled = X_train / maximus
    X_test_scaled = X_test / maximus
    return X_train_scaled, X_test_scaled


def xavier(n_in, n_out):
    n = n_in*n_out
    d = np.sqrt(6 / (n_in + n_out))
    u = np.random.uniform(-d, d, (n_in, n_out))
    return u


def mse(ypred, ytrue):
    return np.mean((ypred - ytrue)**2)


def mse_der(ypred, ytrue):
    return 2*(ypred - ytrue)


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def sigmoid_der(x):
    return (1 / (1 + np.exp(-x)))*(1-(1 / (1 + np.exp(-x))))


def train(model, alpha, X_train, y_train, batch_size=100):
    n = X_train.shape[0]
    for i in range(0, n, batch_size):
        model.backprop(X_train[i:i + batch_size], y_train[i:i + batch_size], alpha)


def accuracy(model, X_train, y_train):
    model.forward(X_train)
    y_pred = np.argmax(model.forward_step, axis=1)
    y_true = np.argmax(y_train, axis=1)
    model.acc = np.mean(y_pred == y_true)
    model.loss = np.mean((y_pred - y_true)**2)



class OneLayerNeural:
    def __init__(self, n_features, n_classes):
        self.w = xavier(n_features, n_classes)
        self.b = xavier(1, n_classes)
        self.forward_step = None
        self.acc = None
        self.loss = None

    def forward(self, X):
        forward_step = np.dot(X, self.w) + self.b
        self.forward_step = sigmoid(forward_step)

    def backprop(self, X, y, alpha):
        self.forward(X)
        err = mse_der(self.forward_step, y)*sigmoid_der(np.dot(X, self.w)+self.b)
        nabla_w = np.dot(X.T, err)/X.shape[0]
        nabla_b = np.mean(err, axis=0)
        self.w -= alpha*nabla_w
        self.b -= alpha*nabla_b


class TwoLayerNeural:
    def __init__(self, n_features, n_classes):
        hidden_layer_nodes = 64
        self.w = [xavier(n_features, hidden_layer_nodes), xavier(hidden_layer_nodes, n_classes)]
        self.b = [xavier(1, hidden_layer_nodes), xavier(1, n_classes)]
        self.forward_step = None
        self.acc = None
        self.loss = None

    def forward(self, X):
        for i in range(2):
            X = sigmoid(X @ self.w[i] + self.b[i])
        self.forward_step = X

    def backprop(self, X, y, alpha):
        self.forward(X)
        yp = self.forward_step
        n = X.shape[0]
        biases = np.ones((1, n))
        loss_grad_1 = 2 * alpha / n * ((yp - y) * yp * (1 - yp))
        f1_out = sigmoid(np.dot(X, self.w[0]) + self.b[0])
        loss_grad_0 = np.dot(loss_grad_1, self.w[1].T) * f1_out * (1 - f1_out)
        self.w[0] -= np.dot(X.T, loss_grad_0)
        self.w[1] -= np.dot(f1_out.T, loss_grad_1)
        self.b[0] -= np.dot(biases, loss_grad_0)
        self.b[1] -= np.dot(biases, loss_grad_1)


if __name__ == '__main__':

    if not os.path.exists('../Data'):
        os.mkdir('../Data')

    # Download data if it is unavailable.
    if ('fashion-mnist_train.csv' not in os.listdir('../Data') and
            'fashion-mnist_test.csv' not in os.listdir('../Data')):
        print('Train dataset loading.')
        url = "https://www.dropbox.com/s/5vg67ndkth17mvc/fashion-mnist_train.csv?dl=1"
        r = requests.get(url, allow_redirects=True)
        open('../Data/fashion-mnist_train.csv', 'wb').write(r.content)
        print('Loaded.')

        print('Test dataset loading.')
        url = "https://www.dropbox.com/s/9bj5a14unl5os6a/fashion-mnist_test.csv?dl=1"
        r = requests.get(url, allow_redirects=True)
        open('../Data/fashion-mnist_test.csv', 'wb').write(r.content)
        print('Loaded.')

    # Read train, test data.
    raw_train = pd.read_csv('../Data/fashion-mnist_train.csv')
    raw_test = pd.read_csv('../Data/fashion-mnist_test.csv')

    X_train = raw_train[raw_train.columns[1:]].values
    X_test = raw_test[raw_test.columns[1:]].values

    y_train = one_hot(raw_train['label'].values)
    y_test = one_hot(raw_test['label'].values)

    # write your code here

    '''
    #Stage 1/7:
    a, b = scale(X_train, X_test)
    print([a[2, 778], b[0, 774]], end=" ")
    print(xavier(2, 3).flatten().tolist(), end=" ")
    c = [-1, 0, 1, 2]
    print(sigmoid(c))


    #Stage 2/7:
    X_train, X_test = scale(X_train, X_test)
    model = OneLayerNeural(X_train.shape[1], y_train.shape[1])
    model.forward(X_train)
    print(model.forward_step[:2].flatten().tolist())


    #Stage 3/7
    arr1 = np.array([-1, 0, 1, 2])
    arr2 = np.array([4, 3, 2, 1])
    print(mse(arr1, arr2).flatten().tolist(), end=" ")
    print(mse_der(arr1, arr2).flatten().tolist(), end=" ")
    print(sigmoid_der(arr1).flatten().tolist(), end=" ")
    X_train, X_test = scale(X_train, X_test)
    model = OneLayerNeural(X_train.shape[1], y_train.shape[1])
    alpha = 0.1
    model.forward(X_train[:2])
    model.backprop(X_train[:2], y_train[:2], alpha)
    model.forward(X_train[:2])
    print(mse(model.forward_step[:2], y_train[:2]).flatten().tolist())


    #Stage 4/7
    X_train, X_test = scale(X_train, X_test)
    model = OneLayerNeural(X_train.shape[1], y_train.shape[1])
    alpha = 0.5
    accuracy(model, X_train, y_train)
    first_part = model.acc.flatten().tolist()
    acc = []
    loss = []
    for i in tqdm(range(20)):
        train(model, alpha, X_train, y_train)
        accuracy(model, X_test, y_test)
        acc.append(model.acc)
        loss.append(model.loss)
    second_part = np.array(acc).flatten().tolist()
    print(first_part, second_part)
    plot(loss, acc)


    #Stage 5/7
    X_train, X_test = scale(X_train, X_test)
    model = TwoLayerNeural(X_train.shape[1], y_train.shape[1])
    model.forward(X_train[:2])
    print(model.forward_step.flatten().tolist())


    #Stage 6/7
    X_train, X_test = scale(X_train, X_test)
    alpha = 0.1
    model = TwoLayerNeural(X_train.shape[1], y_train.shape[1])
    model.forward(X_train[:2])
    model.backprop(X_train[:2], y_train[:2], alpha)
    model.forward(X_train[:2])
    print(mse(model.forward_step[:2], y_train[:2]).flatten().tolist())
    '''


    #Stage 7/7
    X_train, X_test = scale(X_train, X_test)
    model = TwoLayerNeural(X_train.shape[1], y_train.shape[1])
    alpha = 0.5
    acc = []
    loss = []
    for i in tqdm(range(20)):
        train(model, alpha, X_train, y_train)
        accuracy(model, X_test, y_test)
        acc.append(model.acc)
        loss.append(model.loss)
    print(np.array(acc).flatten().tolist())
    plot(loss, acc)
