import sys
import phosphormodel5_test9 as fitter

stdout_save = sys.stdout
stderr_save = sys.stderr

def run():
    fitter.outputfile = 'phosphor5_model_and_fit_' + fitter.name + '.root'
    # print 'Redirecting STDOUT and STDERR to %s.log' % fitter.name
    # log_file = file(fitter.name + '.log', 'w')
    # sys.stdout = log_file
    # sys.stderr = log_file
    fitter.main()
    # sys.stdout = stdout_save
    # sys.stderr = stderr_save
    # print 'Restored STDOUT and STDERR.'
## End of run()

def process_monte_carlo(subdet):
    for pt in '10to12 12to15 15to20 20to999'.split():
        for i in range(4):
            fitter.name = 'test{i}_{subdet}_pt{pt}_v13'.format(
                i=i, subdet=subdet, pt=pt
                )
            fitter.fake_data_cut = 'Entry$ % 4 == {i}'.format(i=i)
            run()
## End of process_monte_carlo()

def process_real_data(subdet):
    for pt in '10to12 12to15 15to20 20to999'.split():
        fitter.name = '{subdet}_pt{pt}_v13_v15data'.format(
            subdet=subdet, pt=pt
            )
        run()
## End of process_real_data()

process_real_data('EB')
# process_real_data('EE')

# fitter.name = 'test_EE_highR9_pt30to999_v13'
# fitter.fake_data_cut = 'Entry$ % 4 == 0'
# run()
