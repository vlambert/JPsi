import commands
import JPsi.MuMu.escale.egmdecorator as decorator

#decorator.basepath = '/raid2/veverka/jobs/outputs/eg_paper_dr0p1'
decorator.basepath = '/raid2/veverka/jobs/outputs/eg_paper_jul2012rereco'

plots = []
#for name in '''
            #egm_mc_EB_pt25to999_yyv4_highR9_evt1of4
            #egm_mc_EB_pt25to999_yyv4_evt1of4
            #'''.split():
for name in '''
            egm_mc_EB_pt25to999_yyv4_highR9_evt1of4
            egm_mc_EB_pt25to999_yyv4_evt1of4
            egm_mc_EE_pt25to999_yyv4_evt1of4
            egm_data_EB_pt25to999_yyv4_highR9
            egm_data_EB_pt25to999_yyv4
            egm_data_EE_pt25to999_yyv4
            '''.split():
    if 'mc' in name:
        for i in range(1, 2):
            iname = name.replace('evt1of4', 'evt%dof4' % i)
            plots.append(decorator.EgmDecorator(iname))
    else:
        plots.append(decorator.EgmDecorator(name))
    
for plot in plots:    
    plot.new_canvas.Draw()
    outputname = plot.name.replace('egm', 'egm_phosphor').replace('_yyv3', '')
    for ext in 'eps png C root'.split():
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
        plot.name
        )

## Print the apparent peak positions
print 'Apparent peak positions (GeV), Number events in the fit'
for plot in plots:
    print "%.3f   %g   %s" % (plot.peak_position, 
                              plot.get_fit_range_num_events(),
                              plot.name)
