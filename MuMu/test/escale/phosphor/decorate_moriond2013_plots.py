import commands
import os
import JPsi.MuMu.escale.moriond2013decorator as decorator

decorator.basepath = '/home/veverka/jobs/outputs/Cristian/SunFeb10_2013/'

plots = []
#for name in '''
            #egm_mc_EB_pt25to999_yyv4_highR9_evt1of4
            #egm_mc_EB_pt25to999_yyv4_evt1of4
            #'''.split():
for name in '''
            data_EB_sixie_R9Low_0.94_R9high_999_PtLow_20_PtHigh_999
            mc_EB_sixie_R9Low_0.94_R9high_999_PtLow_20_PtHigh_999            
            '''.split():
    for subdir in '''
                  Zg_2012ABCD_NoHggRegression_newMuCorr_HighR9
                  Zg_2012ABCD_HggRegression_newMuCorr_HighR9
                  '''.split():
        plots.append(decorator.Moriond2013Decorator(name, subdir))
    
for plot in plots:    
    plot.draw()
    outputname = plot.get_short_name()
    for ext in 'eps png root C'.split():
        plot.new_canvas.Print(outputname + '.' + ext)
    command = 'ps2pdf -dEPSCrop ' + outputname + '.eps'
    (exitstatus, outtext) = commands.getstatusoutput(command)
    if  exitstatus != 0:
        raise RuntimeError, '"%s" failed: "%s"!' % (command, outtext)

## Print the scale and resolution fit results
print 'scale (%), resolution (%)'
for plot in plots:
    print "%.2f +/- %.2f,   %.2f +/- %.2f    %s" % (
        plot.workspace.var('phoScale').getVal(),
        plot.workspace.var('phoScale').getError(),
        plot.workspace.var('phoRes').getVal(),
        plot.workspace.var('phoRes').getError(),
        plot.get_short_name(),
        )

## Print the apparent peak positions
print 'Apparent peak positions (GeV), Number of events in the fit'
for plot in plots:
    print "%.3f   %g   %s" % (plot.peak_position, 
                              plot.get_fit_range_num_events(),
                              plot.get_short_name())
