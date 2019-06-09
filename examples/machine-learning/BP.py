from numpy import *

def Sigmoid(X):
    return 1.0/(1+exp(-X))

def Map_A(F, X):
    return array(list(map(F, X)))

def Forward(Input, NN):
    for Layer in NN:
        I, W, B, O, DW, DB = Layer
        I[:] = Input
        O[:] = Map_A(Sigmoid, dot(W, I)+B)
        Input = O
    return Input

def Backward(Error, NN):
    for Layer in NN[::-1]:
        I, W, B, O, DW, DB = Layer
        #Sigmoid_D
        Derivative = O*(ones(O.shape)-O)
        Delta = Error*Derivative
        DW[:] = DW + dot(transpose([Delta]), [I])
        DB[:] = DB + Delta
        Error = dot(Delta, W)
    return Error

def Clear_D(NN, Learning_Rate):
    for Layer in NN:
        I, W, B, O, DW, DB = Layer
        W[:] = W - DW*Learning_Rate
        B[:] = B - DB*Learning_Rate
        DW[:] = zeros(DW.shape)
        DB[:] = zeros(DB.shape)

def BP(NN, IOS, Learning_Rate):
    Total_Distance = 0
    for IO in IOS:
        Input, Output = IO
        O = Forward(Input, NN)
        Error = Output - O
        #Energy
        Distance = dot(Error, Error)/2
        Total_Distance += Distance
        #Energy_D
        Derivative = -Error
        Backward(Derivative, NN)
    Clear_D(NN, Learning_Rate)
    return (O, Error, Distance, Total_Distance)

def W_B(WBS):
    W = []
    B = []
    for WB in WBS:
        W.append(WB[:-1:])
        #B.append(WB[-1::])
        B.append(WB[-1])
    return (array(W), array(B))

def Layer(WB):
    W, B = WB
    OL, IL = W.shape
    #OL = B.shape
    return (zeros(IL), W, B, zeros(OL), zeros([OL, IL]), zeros(OL))

def IOS(IOS):
    IORS = []
    for IO in IOS:
        I, O = IO
        IORS.append( (array(I), array(O)) )
    return IORS
