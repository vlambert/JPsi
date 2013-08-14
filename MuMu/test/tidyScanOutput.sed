#!/usr/bin/sed -f
## Usage example:
##+ ./tidyScanOutput.sed -i pixelMatch/pixelMatch_data_Nov4ReReco_v3.dat

# remove all the asteriks `*'
s/\*//g

# comment out all lines that are not data
/^[[:space:]]*[0-9#]/ !s/^/# /

