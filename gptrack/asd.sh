#!/bin/bash

path="data/strokes"

for file in do.pck mi.pck sol.pck lam.pck 
do
    ./util/updown.py -i $path/$file -o $path/ud.$file
    ./util/plot.py $path/ud.$file
done

convert $path/ud.{'do','mi','sol','lam'}.pck.png -append stokes.png
