import matplotlib.pyplot as plot
from numpy import *

Input  = array([0.05, 0.10])
Output = array([0.01, 0.99])

W1 = array([(0.15, 0.20), (0.25, 0.30)])
B1 = array([0.35, 0.35])

W2 = array([(0.40, 0.45), (0.50, 0.55)])
B2 = array([0.60, 0.60])

Sigmoid = lambda x: 1.0/(1+exp(-x))
Sigmoid_D = lambda x: Sigmoid(x)*(1-Sigmoid(x))

I1 = Input
I2 = array(list(map(Sigmoid, dot(W1, I1)+B1)))
I3 = array(list(map(Sigmoid, dot(W2, I2)+B2)))

Error = Output - I3
Distance = dot(Error, Error)/2
#print("Distance=", Distance)

Plot_X = [0]
Plot_Y = [Distance]

Learning_Rate = 1/2

for i in range(1, 10000):

    Delta_3 =         (-Error)*I3*(ones(2)-I3)
    Delta_2 = dot(Delta_3, W2)*I2*(ones(2)-I2)

    W2 = W2 - dot(transpose([Delta_3]), [I2])*Learning_Rate
    B2 = B2 - Delta_3*Learning_Rate
    W1 = W1 - dot(transpose([Delta_2]), [I1])*Learning_Rate
    B1 = B1 - Delta_2*Learning_Rate

    I2 = array(list(map(Sigmoid, dot(W1, I1)+B1)))
    I3 = array(list(map(Sigmoid, dot(W2, I2)+B2)))

    Error = Output - I3
    Distance = dot(Error, Error)/2
    #print("Distance=", Distance)

    Plot_X.append(i)
    Plot_Y.append(Distance)

print("W1=", W1)
print("B1=", B1)
print("W2=", W2)
print("B2=", B2)
print("I3=", I3)
print("Error=", Error)
print("Distance=", Distance)

plot.plot(Plot_X, Plot_Y)
plot.show()
