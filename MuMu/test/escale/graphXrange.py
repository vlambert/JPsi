import array
import math
import ROOT
n=20
x = array.array('d', range(n) )
y = array.array('d', range(n) )
ex = array.array('d', range(n) )
ey = array.array('d', range(n) )
for i in range(n):
    x[i] = i * 0.1
    y[i] = 10 * math.sin(x[i] + 0.2)
    ex[i] = 0.05
    ey[i] = 1.
gr1 = ROOT.TGraphErrors(n, x, y, ex, ey)
axis = gr1.GetXaxis()
axis.SetLimits(-1., 5.) # along X
gr1.GetHistogram().SetMaximum(20.) # along
gr1.GetHistogram().SetMinimum(-20.) # Y
gr1.Draw("AC*")
