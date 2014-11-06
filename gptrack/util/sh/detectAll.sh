#!/bin/bash

if [ $# -ne 1 ]; then
    echo "$0 <strokes dir>"
    exit
fi

path=$(readlink -m $1)

for c in Am E G
do
    for f in n.pck r.pck s.pck
    do
	file=$c"_"$f
	./updown.py -i $path/$file -o $path/ud.$file
	./util/plot.py $path/ud.$file
    done
    
    convert $path/ud.$c"_"{s,n,r}.pck.png -append $path/$c.png

done



