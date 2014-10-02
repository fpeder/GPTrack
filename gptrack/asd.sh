#!/bin/bash

path=$1
out=$2

for file in Am_n.pck Am_r.pck Am_s.pck
do
    ./util/updown.py -i $path/$file -o $path/ud.$file
    ./util/plot.py $path/ud.$file
done

convert $path/ud.{'Am_n','Am_r','Am_s'}.pck.png -append $out
