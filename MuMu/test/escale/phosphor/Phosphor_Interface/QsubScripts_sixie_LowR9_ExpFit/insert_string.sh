#!/bin/bash
     
for fl in *.sge; do
    mv $fl $fl.old
    sed '/gawk/a RESULTS=yyv3' $fl.old > $fl.old1
    sed '/RESULTS/a LOGS=yyv3_log' $fl.old1 > $fl
    rm -f $fl.old $fl.old1
done