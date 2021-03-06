import numpy as np
from scipy.optimize import minimize
from math import sqrt
import pickle
'''
You need to modify the functions except for initializeWeights() 
'''

def initializeWeights(n_in, n_out):
    '''
    initializeWeights return the random weights for Neural Network given the
    number of node in the input layer and output layer

    Input:
    n_in: number of nodes of the input layer
    n_out: number of nodes of the output layer

    Output:
    W: matrix of random initial weights with size (n_out x (n_in + 1))
    '''
    epsilon = sqrt(6) / sqrt(n_in + n_out + 1)
    W = (np.random.rand(n_out, n_in + 1) * 2 * epsilon) - epsilon
    return W


def sigmoid(z):
    '''
    Notice that z can be a scalar, a vector or a matrix
    return the sigmoid of input z (same dimensions as z)
    '''
    # remove the next line and replace it with your code
    return(1.0/(1.0 + np.exp(-1.0 * z)))
    print("In sigmoid")

def nnObjFunction(params, *args):
    '''
    % nnObjFunction computes the value of objective function (cross-entropy
    % with regularization) given the weights and the training data and lambda
    % - regularization hyper-parameter.

    % Input:
    % params: vector of weights of 2 matrices W1 (weights of connections from
    %     input layer to hidden layer) and W2 (weights of connections from
    %     hidden layer to output layer) where all of the weights are contained
    %     in a single vector.
    % n_input: number of nodes in input layer (not including the bias node)
    % n_hidden: number of nodes in hidden layer (not including the bias node)
    % n_class: number of nodes in output layer (number of classes in
    %     classification problem
    % train_data: matrix of training data. Each row of this matrix
    %     represents the feature vector of the corresponding instance 
    % train_label: the vector of true labels of training instances. Each entry
    %     in the vector represents the truee label of its corresponding training instance.
    % lambda: regularization hyper-parameter. This value is used for fixing the
    %     overfitting problem.

    % Output:
    % obj_val: a scalar value representing value of error function
    % obj_grad: a SINGLE vector (not a matrix) of gradient value of error function
    % NOTE: how to compute obj_grad
    % Use backpropagation algorithm to compute the gradient of error function
    % for each weights in weight matrices.
    '''
    # do not remove the next 5 lines
    n_input, n_hidden, n_class, train_data, train_label, lambdaval = args
    # First reshape 'params' vector into 2 matrices of weights W1 and W2

    W1 = params[0:n_hidden * (n_input + 1)].reshape((n_hidden, (n_input + 1)))
    W2 = params[(n_hidden * (n_input + 1)):].reshape((n_class, (n_hidden + 1)))

    # remove the next two lines and replace them with your code 
   
    def oneOfKEncode(y):
    #takes in y and encodes it to calcualte loss.
        y_encoded = np.zeros((y.size, W2.shape[0]))
        y_encoded[np.arange(y.size), y.astype(int)] = 1
        return y_encoded
    
    
    N = train_data.shape[0]
    train_label_encode = oneOfKEncode(train_label)
    #Adding bias to input layer
    b1 = np.ones((train_data.shape[0], 1))
    train_data = np.concatenate((train_data, b1), axis =1)
    
    #Calculate z
    z = sigmoid(np.dot(train_data,W1.T))
    
    #Adding bias to hidden layer
    b2 = np.ones((z.shape[0], 1))
    z = np.concatenate((z, b2), axis =1)
    
    #Calculate output
    output = sigmoid(np.dot(z,W2.T))
    
    #Calculate delta
    delta = output - train_label_encode
    
    #Calculate obj val
    obj_val = np.sum((train_label_encode* np.log(output)) + ((1-train_label_encode)* np.log(1-output)))
    obj_val = (-1/N)*obj_val
    
    reg_val = (lambdaval/ (2*N)) * (np.sum(np.square(W1)) + np.sum(np.square(W2)))
    obj_val = obj_val + reg_val
    
    #Calculate obj grad
    obj_grad1 = np.dot(((1 - z) * z * np.dot(delta, W2)).T, train_data)
    obj_grad1 = np.delete(obj_grad1, n_hidden, axis = 0)
    obj_grad2 = np.dot((delta.T), z)
    
    reg_grad1 = obj_grad1 + lambdaval*W1
    reg_grad2 = obj_grad2 + lambdaval*W2
    

    obj_grad = np.concatenate((reg_grad1.flatten(), reg_grad2.flatten()), 0)
    obj_grad = 1/N * (obj_grad)
    

#     obj_val = 0
#     obj_grad = params 

    return (obj_val,obj_grad)

def nnPredict(W1, W2, data):
    '''
    % nnPredict predicts the label of data given the parameter W1, W2 of Neural
    % Network.

    % Input:
    % W1: matrix of weights for hidden layer units
    % W2: matrix of weights for output layer units
    % data: matrix of data. Each row of this matrix represents the feature vector for the corresponding data instance

    % Output:
    % label: a column vector of predicted labels
    '''
    # remove the next line and replace it with your code
    
    items = data.shape[0]
    
    bias = np.ones((data.shape[0], 1))
    data = np.concatenate((data, bias), axis =1)
    
    hidden = sigmoid(np.dot(data, W1.T))
    
    bias1 = np.ones((hidden.shape[0], 1))
    hidden = np.concatenate((hidden, bias), axis =1)
    
    O = sigmoid(np.dot(hidden, W2.T))
    
    labels = np.argmax(O, axis=1)
        
#     labels = [-1]*items
#     for i in range(items):
#         labels[i] = np.argmax(O[i])
#     labels = np.array(labels)    
    

    return labels

        
        
        
#     labels = np.zeros((data.shape[0],1))

#     return labels
