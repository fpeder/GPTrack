#!/bin/bash

tmp=xxxxxxxtmp

if [ $# -ne 4 ]; then
    echo "$0 <video> <detect> <nframe> <out>"
    exit 
fi

mkdir $tmp

video=$1
det=$2
nframe=$3
out=$4

echo "dumping frame"
./util/dumpVideo.py -v $video -d $tmp

echo "adding overlay"
./util/overlay.py -d $tmp -i $det -n $nframe

echo "coding"
ffmpeg -framerate 100 -i $tmp/%04d.jpg -c:v libx264 -r 30 -pix_fmt yuv420p $out

rm -rf $tmp
