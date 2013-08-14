## Source: Jan's talk from 18-11-2011
## https://indico.cern.ch/conferenceDisplay.py?confId=163190
data_2011_11_18_confID_163190 = {}

data_2011_11_18_confID_163190['mc'] = {
    ## s, es
    'EB_lowR9' : (
        (-1.223, 0.450),
        (0.066, 0.344),
        (-0.320, 0.254),
        (0.139, 0.005),
        (0.146, 0.291),
        (-0.143, 0.285),
        ),
    'EB_highR9' : (
        (-0.542, 0.514),
        (-0.761, 0.361),
        (-0.034, 0.259),
        (-0.034, 0.244),
        (-0.131, 0.254),
        (-0.944, 0.261),
        ),
    'EE_lowR9' : (
        (-1.244, 0.862),
        (1.363, 0.673),
        (0.371, 0.505),
        (-0.219, 0.492),
        (1.082, 0.497),
        (-0.931, 0.567),
        ),
    'EE_highR9' : (
        (1.805, 1.316),
        (-1.159, 0.993),
        (-0.138, 0.655),
        (-0.080, 0.592),
        (-0.758, 0.610),
        (0.850, 0.631),
        )
    }

## mtranslation_EB_lowR9_PhoEt10-12 -2.5080604299 +/- 0.348105667383
## mtranslation_EB_lowR9_PhoEt12-15 -1.46038807839 +/- 0.33821548875

## mtranslation_EB_lowR9_PhoEt15-20 -1.08715347123 +/- 0.261805483639
## mtranslation_EB_lowR9_PhoEt20-25 -1.82859267866 +/- 0.286845889318
## mtranslation_EB_lowR9_PhoEt25-30 -0.224950167795 +/- 0.311616340384
## mtranslation_EB_lowR9_PhoEt30-100 -0.464286745356 +/- 0.221113558455
## mtranslation_EB_highR9_PhoEt10-12 -1.82247229697 +/- 0.467452395583
## mtranslation_EB_highR9_PhoEt12-15 -1.62164743839 +/- 0.372898064247

## mtranslation_EB_highR9_PhoEt15-20 -0.695131089016 +/- 0.265070688411
## mtranslation_EB_highR9_PhoEt20-25 -0.851408630069 +/- 0.261119638258
## mtranslation_EB_highR9_PhoEt25-30 -0.577964476599 +/- 0.285272731537
## mtranslation_EB_highR9_PhoEt30-100 0.555416196665 +/- 0.254201499407
## mtranslation_EE_lowR9_PhoEt10-12 -0.619660537879 +/- 0.799689199782
## mtranslation_EE_lowR9_PhoEt12-15 -0.801876941465 +/- 0.666776519717

## mtranslation_EE_lowR9_PhoEt15-20 -0.376934499553 +/- 0.48070717283
## mtranslation_EE_lowR9_PhoEt20-25 0.961994091186 +/- 0.554126993965
## mtranslation_EE_lowR9_PhoEt25-30 0.434460125642 +/- 0.58465947042
## mtranslation_EE_lowR9_PhoEt30-100 1.6995274945 +/- 0.538752596725
## mtranslation_EE_highR9_PhoEt10-12 -1.29327703144 +/- 1.19805306536
## mtranslation_EE_highR9_PhoEt12-15 0.72201014105 +/- 0.933928991441


## mtranslation_EE_highR9_PhoEt15-20 0.30435582831 +/- 0.674714838568
## mtranslation_EE_highR9_PhoEt20-25 -0.374032610471 +/- 0.661966535572
## mtranslation_EE_highR9_PhoEt25-30 0.485002742653 +/- 0.656246809777
## mtranslation_EE_highR9_PhoEt30-100 1.99419797713 +/- 0.620317100174

## Turn tuples of tuples into dictionaries of tuples
for src, data in data_2011_11_18_confID_163190.items():
    for cat, tuples in data.items():
        data_2011_11_18_confID_163190[src][cat] = {}
        for i, x in enumerate('sreco esreco'.split()):
            ## Yack.  This looks aweful.
            data_2011_11_18_confID_163190[src][cat][x] = zip(*tuples)[i]
