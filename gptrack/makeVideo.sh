#!/bin/bash

tmp=xxxxxxxtmp

if [ $# -ne 4 ]; then
    echo "$0 <video> <seq> <detect> <out>"
    exit 
fi

mkdir $tmp

echo "dumping frame"
./util/dumpVideo.py -v $1 -d $tmp
echo "adding overlay"
./util/overlay.py -d $tmp -s $2 -i $3
echo "coding"
ffmpeg -framerate 100 -i $tmp/%04d.jpg -c:v libx264 -r 30 -pix_fmt yuv420p $4

rm -rf $tmp
