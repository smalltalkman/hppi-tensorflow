import matplotlib.pyplot as plot
from numpy import *

W = array([0.0, 0.0])
B = array(0.0)

IOS = [(array([3.0, 3.0]), array( 1.0)),
       (array([4.0, 3.0]), array( 1.0)),
       (array([1.0, 1.0]), array(-1.0)),
       (array([5.0, 2.0]), array(-1.0))
       ]

L_R = 1/2

def Perceptron_Step(IOS):
    global W, B
    for IO in IOS:
        I, O = IO
        L = (dot(W, I)+B)*O
        if L<=0:
            W[:] = W+I*O*L_R
            B    = B+  O*L_R
            return True
    return False

def Perceptron(IOS):
    while Perceptron_Step(IOS):
        pass

Perceptron(IOS)

print("W=", W, "B=", B)

def Line_Data(A, B, C, S):
    if A==0 and B==0:
        return ([], [])
    if B==0:
        X = -C/A
        return ([X for _ in S], S)
    K1 = -A/B
    K2 = -C/B
    return (S, [K1*X+K2 for X in S])
    
def Draw_Line(A, B, C, S):
    XS, YS = Line_Data(A, B, C, S)
    plot.plot(XS, YS)

Draw_Line(W[0], W[1], B, range(6))

def Draw_Point(PS, Style):
    for P in PS:
        X, Y = P
        plot.plot(X, Y, Style, label="point")

Draw_Point([I for I, O in IOS if O== 1], 'ro')
Draw_Point([I for I, O in IOS if O==-1], 'bx')

plot.show()
