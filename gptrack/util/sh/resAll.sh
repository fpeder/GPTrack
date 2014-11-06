#!/bin/bash

if [ $# -ne 1 ]
then
  echo "$0 <stroke path>"
  exit
fi

path=$(readlink -m $1)

for d in 100 75 50
do
    ./util/res.py -d $path/$d -f $d
done


