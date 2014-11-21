
#!/bin/bash

if [ $# -ne 2 ]
then
    echo "$0 <video src> <dest>"
    exit
fi

video=$(readlink -m $1)
dest=$(readlink -m $2)

for chord in Am0_ E0_ G0_ C0_ Am7_ C7_ G7_ Bm7_
do
    for speed in s n r
    do
	file="$chord$speed.mp4"
	echo $file
	python chords/dumpData.py -i $video/$file \
	       -d $dest \
	       -f 10 20 30 40 50 60 70 80 90 100 \
	          110 120 130 140 150 160 170 180 190 \
	          200 210 220 230 240 250 260 270 280 290
    done
done
