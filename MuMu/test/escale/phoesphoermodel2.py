'''
Phton Energy Scale and Photon Energy Resolution (PHOESPHOER) Fit model 2.
Strategy to build a 2D model for the mmMass and mmgMass as functions
of PhoES.

Key formula:
mmgMass^2 = mmMass^2 + (mmgMassPhoEGen^2 - mmMass^2) * phoE/phoEGen (1)

Diffenrence to PHOESPHOER Fit model 1:
Only fit for PhoES.  Repeat the procedure scanning over PhoER. The
assumption that phoE/phoEGen is uncorrelated with both mmMass and mmgMass
is not needed.

Strategy:
1. Build a 2D KEYS PDF of X = mmMass and
   T1 = log(mmgMassPho^2 - mmMass^2) fXT1(x, t1).

## 2. Build a 1D KEYS PDF of T2 = log(phoE/phoEGen) depending on
##    s = phoScale and r = phoRes fT2(t2|s,r). Note that
##    phoERes = 100 * (phoE/phoEGen - 1).
##    Thus a substitution
##    phoERes = 100 * (1 + exp(t2))
##    in the phoEResPdf(phoERes|s,r) can be used.

## 3. Use FFT to convolve fXT1 and fT2 in T1 and T2 to get a 2D PDF
##    of X and T = T1 + T2 fXT(x,t|s,r):
##    fXT(x,t|s,r) = fXT1(x,t) * fT2(t|s,r)
##    Note that X is an additional observable while s and t are parameters.
##    It is important to cache the convolution in t *and* x for efficient
##    likelihood calculation.

## 4. Substitute for T using the key formula T -> T3 = log(mmgMass^2 - mmMass^2)
##    to obtain a density in X and Y = mmgMass fXY(x,y|s,r).
##    fXY(x,y|s,r) = fXT(x,t3(x,y)|s,r).

## Culprit:
## T3 is only well defined for y > x.  Need to make the range of x depend on y.
## Is this possible in roofit?

Jan Veverka, Caltech, 18 January 2012.
'''
   
