'''Provides custom methods to divide ROOT's TPad. Sub-pads are returned
and have be stared to avoid being collected as garbage.  They can then
be accessed using TPad::cd(n).'''

from ROOT import TPad, gPad

#------------------------------------------------------------------------------
def residPullDivide(pad, topMargin = 0.025, bottomMargin = 0.1,
                    leftMargin = 0.2, rightMargin = 0.05):
    ''' Divides the given pad in 3 sub-pads that are on top of each other
    w/o spaces, share the x-axis and the sizes of their plot area
    along y are in the ratio 2:1:1. This is meant to show a fit to data
    on top, residuals in the middle and pulls in the bottom.
    The optional arguments are margins as fractions of the original pad
    and are recomputed and applied to the sub-pads. The three sub-pads
    given on return have to be assign to a variable in order for the pads
    not to be destroyed by python's garbage collector.'''

    y1 = 0.5*(1 - topMargin + bottomMargin)
    y2 = 0.25 * (1 - topMargin + 3*bottomMargin)

    padsav = gPad
    pad.cd()

    name = pad.GetName() + '_1'
    pad1 = TPad(name, name, 0, y1, 1, 1)
    pad1.SetNumber(1)
    pad1.SetTopMargin( topMargin / (1. - y1) )
    pad1.SetBottomMargin(0)
    pad1.SetLeftMargin(leftMargin)
    pad1.SetRightMargin(rightMargin)
    pad1.Draw()

    name = pad.GetName() + '_2'
    pad2 = TPad(name, name, 0, y2, 1, y1)
    pad2.SetNumber(2)
    pad2.SetTopMargin(0)
    pad2.SetBottomMargin(0)
    pad2.SetLeftMargin(leftMargin)
    pad2.SetRightMargin(rightMargin)
    pad2.Draw()

    name = pad.GetName() + '_3'
    pad3 = TPad(name, name, 0, 0, 1, y2)
    pad3.SetNumber(3)
    pad3.SetTopMargin(0)
    pad3.SetBottomMargin(bottomMargin/y2)
    pad3.SetLeftMargin(leftMargin)
    pad3.SetRightMargin(rightMargin)
    pad3.Draw()

    # Clean up and exit
    pad.Modified()
    if padsav:
        padsav.cd()
    return pad1, pad2, pad3
## end of residPullDivide

