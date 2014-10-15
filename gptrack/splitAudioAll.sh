#!/bin/bash

if [ $# -ne 3 ]; then
    echo "$0 <video path> <stroke path> <output path>"
    exit
fi

video=$(readlink -m $1)
strokes=$(readlink -m $2)
dest=$(readlink -m $3)

for c in Am_ E_ G_ 
do
    for f in s n r
    do
	asd=$c$f
	file=$video/$asd.mp4
	updown=$strokes/ud.$asd.pck

	echo $video
	./util/splitAudio.py -v $file -i $updown -o $dest
    done
done
