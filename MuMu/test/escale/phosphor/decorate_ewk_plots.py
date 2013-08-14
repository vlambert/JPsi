import commands
import JPsi.MuMu.escale.vgammadecorator as decorator

plots = []

##______________________________________________________________________________
def customize_axis(axis):
    axis.SetTitleFont(62)
    axis.SetLabelFont(62)
    axis.SetTitleSize(0.06)
    axis.SetLabelSize(0.05)
## End of customize_axis


##______________________________________________________________________________
def get_frame_from_canvas(canvas):
    for primitive in list(canvas.GetListOfPrimitives()):
        if primitive.InheritsFrom('TH1'):
            return primitive
    raise RuntimeError, "Didn't find any frame in canvas %s" % canvas.GetName()
## End get_frame_from_canvas(..)


##______________________________________________________________________________
for name in '''
            sge_data_EB_pt15to20_v13
            '''.split():
    plot = decorator.Decorator(name)
    plot.new_canvas.Draw()
    outputname = plot.name.replace('sge', 'PHOSPHOR_Fit').replace('_v13', '')

    frame = get_frame_from_canvas(plot.new_canvas)
    customize_axis(frame.GetXaxis())
    customize_axis(frame.GetYaxis())

    # plot.new_canvas.SetWindowSize(600, 603)
    # plot.new_canvas.Modified()
    # plot.new_canvas.Update()
    
    plot.new_canvas.Print(outputname + '.eps')
    plot.new_canvas.Print(outputname + '.C')
    plot.new_canvas.Print(outputname + '.root')
    plot.new_canvas.Print(outputname + '.png')
    
    command = 'ps2pdf -dEPSCrop ' + outputname + '.eps'
    (exitstatus, outtext) = commands.getstatusoutput(command)
    if  exitstatus != 0:
        raise RuntimeError, '"%s" failed: "%s"!' % (command, outtext)
    
    plots.append(plot)
