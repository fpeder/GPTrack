#!/bin/bash

if [ $# -ne 2 ]; then 
    echo "$0: <video dir> <rate>"
    exit
fi

for file in $(ls $1/*.mp4)
do
    ffmpeg -i $file -r $2 $(basename $file)
done
