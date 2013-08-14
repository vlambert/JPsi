
file=${1:-$(ls -rt *.dat | tail -1)}
sed -i 's/\*//g' $file
