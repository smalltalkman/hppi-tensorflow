import matplotlib.pyplot as plot
from BP import *

W, B = W_B([(0.0, 0.0, 0.0)])

NN=[Layer([W, B])]

IOS=IOS([([3, 3], [1]),
         ([4, 3], [1]),
         ([1, 1], [0])
         ])

Learning_Rate=1/2

Count=40000

Plot_X = []
Plot_Y = []

for i in range(Count):
    O, Error, Distance, Total_Distance = BP(NN, IOS, Learning_Rate)

    Plot_X.append(i)
    Plot_Y.append(Total_Distance)

print("Total_Distance=", Total_Distance)

for IO in IOS:
    Input, Output = IO
    I = Input
    O = Map_A(Sigmoid, dot(W, I)+B)
    print(I, "=>", O, "<=", Output)

plot.plot(Plot_X, Plot_Y)
plot.show()
