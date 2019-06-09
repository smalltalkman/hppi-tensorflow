import matplotlib.pyplot as plot
from numpy import *

def Sigmoid(X):
    return 1.0/(1+exp(-X))

def Forward(Input, NN, Learning_Rate):
    for Layer in NN:
        I, W, B, O, DW, DB = Layer
        I[:] = Input
        W[:] = W - DW*Learning_Rate
        B[:] = B - DB*Learning_Rate
        O[:] = array(list(map(Sigmoid, dot(W, I)+B)))
        Input = O
    return Input

def Backward(Error, NN):
    for Layer in NN[::-1]:
        I, W, B, O, DW, DB = Layer
        #Sigmoid_D = O*(ones(O.shape)-O)
        Delta = Error*O*(ones(O.shape)-O)
        DW[:] = dot(transpose([Delta]), [I])
        DB[:] = Delta
        Error = dot(Delta, W)
    return Error

def BP(Input, NN, Output, Learning_Rate):
    O = Forward(Input, NN, Learning_Rate)
    Error = Output - O
    #Energy_D = -Error
    Backward(-Error, NN)
    return (O, Error)

Input=array([0.05, 0.10])
NN=[( zeros(2), array([(0.15, 0.20), (0.25, 0.30)]), array([0.35, 0.35]), zeros(2), zeros([2, 2]), zeros(2) ),
    ( zeros(2), array([(0.40, 0.45), (0.50, 0.55)]), array([0.60, 0.60]), zeros(2), zeros([2, 2]), zeros(2) )
    ]
Output=array([0.01, 0.99])

Learning_Rate=1/2

Count=10000

Plot_X = []
Plot_Y = []

for i in range(Count):
    O, Error = BP(Input, NN, Output, Learning_Rate)
    
    Distance = dot(Error, Error)/2

    Plot_X.append(i)
    Plot_Y.append(Distance)

print("O=", O)
print("Error=", Error)

print("Distance=", Distance)

plot.plot(Plot_X, Plot_Y)
plot.show()
