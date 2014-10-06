#!/bin/bash

if [ $# -ne 3 ]; then
    echo "$0 <strokes> <chord> <output>"
    exit
fi

path=$1
c=$2
out=$3

for f in n.pck r.pck s.pck
do
    file=$c"_"$f
    ./util/updown.py -i $path/$file -o $path/ud.$file
    ./util/plot.py $path/ud.$file
done

convert $path/ud.$c"_"{s,n,r}.pck.png -append $out

