import matplotlib.pyplot as plot
from BP import *

W1, B1 = W_B([(0.15, 0.20, 0.35), (0.25, 0.30, 0.35)])
W2, B2 = W_B([(0.40, 0.45, 0.60), (0.50, 0.55, 0.60)])

NN=[Layer([W1, B1]), Layer([W2, B2])]

IOS=IOS([([0.05, 0.10], [0.01, 0.99])])

Learning_Rate=1/2

Count=10000

Plot_X = []
Plot_Y = []

for i in range(Count):
    O, Error, Distance, Total_Distance = BP(NN, IOS, Learning_Rate)

    Plot_X.append(i)
    Plot_Y.append(Total_Distance)

print("O=", O)
print("Error=", Error)

print("Distance=", Distance)

plot.plot(Plot_X, Plot_Y)
plot.show()
