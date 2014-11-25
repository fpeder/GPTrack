#!/bin/bash

if [ $# -ne 2 ]; then
    echo "$0 <video dir> <dest dir>"
    exit
fi

path=$(readlink -m $1)
dest=$(readlink -m $2)
prog=./handTracker.py

for c in Am0_ E0_ G0_ Am7_ Bm7_ C7_ G7_
do
    for f in s n r
    do
	file=$path/$c$f.mp4
	echo $file
	$prog -i $file -o $dest/$c$f.pck
    done
done
