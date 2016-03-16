#!/bin/bash

TMP=$( mktemp 6gem_XXXXXX )
./gem_future.py $* | tee $TMP || exit -1

#TITLE=$( head -n 4 $TMP | awk '{printf("%s", $0)}' | sed 's/#/\\n/g' )
TITLE=$( head -n 4 $TMP | awk '{printf("%s", $0)}' | sed 's/#/   /g' )

echo $TITLE

gnuplot -persist <<EOF
se ke le
se xla "gem cost"
se yla "stat increase"
se tit "$TITLE"
p "$TMP" eve :::0::0 w step t "attack", "" eve :::1::1 w step t "defense", "" eve :::2::2 w step t "troops"
EOF

rm $TMP
