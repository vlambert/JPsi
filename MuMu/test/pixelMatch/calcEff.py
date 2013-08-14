from math import *
oplus = lambda x,y: sqrt(x*x + y*y)

## passing probes MC
p, ep = 15997., 169.
## failing probes MC
f, ef = 719., 65.

# ## passing probes data
# p, ep = 432., 25.
# ## failing probes data
# f, ef = 29., 8.7

eff = p/(p+f)
eeff = eff*(1-eff)*oplus(ep/p, ef/f)

print eff, "+/-", eeff