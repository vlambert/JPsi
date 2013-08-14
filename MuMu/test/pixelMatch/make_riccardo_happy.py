import os
import JPsi.MuMu.pmvplotter as plotter

#for varname in 'r9 r9_zoom sihih sihih_highR9'.split():
for varname in 'sihih sihih_nocorrection r9_zoom r9_zoom_nocorrection'.split():
    for subdet in 'EB EE'.split():
        name = '_'.join([varname, subdet])
        plotter.make_plot(name)
    

    
plotter.canvases.update()


##______________________________________________________________________________
if __name__ == '__main__':
    import user
    
