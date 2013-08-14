from ROOT import *


def fillHisto(histo, value, content, entries):
    '''Fill a given histogram with a given value of given content and entries'''
    weight = float(content) / float(entries)
    for i in range( int(entries) ):
        histo.Fill(value, weight)

hpass = TH1F('hpass', 'hpass', 4, 0.5, 4.5)
value = 1.
for tag in '9_1 90_1 9_9 90_90'.split():
    content, entries = tuple( [float(x) for x in tag.split('_')] )
    fillHisto( hpass, value, content, entries )
    bin = hpass.GetXaxis().FindBin( value )
    print bin, hpass.GetBinContent(bin), hpass.GetEntries()
    value += 1.

htot = TH1F('htot', 'htot', 4, 0.5, 4.5)
value = 1.
for tag in '10_1 100_1 10_10 100_100'.split():
    content, entries = tuple( [float(x) for x in tag.split('_')] )
    fillHisto( htot, value, content, entries )
    bin = htot.GetXaxis().FindBin( value )
    print bin, htot.GetBinContent(bin), htot.GetEntries()
    value += 1.

geff = TGraphAsymmErrors()
geff.BayesDivide( hpass, htot )
geff.Draw('ap')

