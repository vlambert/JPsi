#!/bin/bash
     
for fl in *.sge; do
    mv $fl $fl.old
    sed 's/yyv3/sixie/g' $fl.old > $fl
    rm -f $fl.old
done