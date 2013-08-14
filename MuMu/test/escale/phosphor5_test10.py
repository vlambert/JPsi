'''
Photon Energy Scale (PhoES) and Photon Energy Resolution (PHOSPHOR) Fit model 5.

Test config file parsing.
'''

import ConfigParser

config = ConfigParser.RawConfigParser()
config.read('phosphor.cfg')

if __name__ == '__main__':
    import user


