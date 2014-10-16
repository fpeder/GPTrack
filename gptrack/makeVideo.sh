#!/bin/bash

tmp=xxxxxxxtmp

if [ $# -ne 4 ]; then
    echo "$0 <video> <detect> <nframe> <out>"
    exit 
fi

mkdir $tmp

input=$1
det=$2
nframe=$3
out=$4

echo "dumping frame"
./util/dumpVideo.py -v $input -d $tmp

echo "adding overlay"
./util/overlay.py -d $tmp -i $det -n $nframe

echo "coding"
video=video.mp4
ffmpeg -framerate 100 -i $tmp/%04d.jpg -c:v libx264 -r 30 -pix_fmt yuv420p $video

echo "merging audio"
audio=tmp.wav
ffmpeg -i $input -f wav $audio
ffmpeg -i $video -i $audio -c:v copy -c:a aac -strict experimental $out

rm -rf $tmp
rm $video
rm $audio
