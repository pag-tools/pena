#!/bin/bash
OUTPUT_FILE=dimred.csv
INPUT_FILES=(
    data/single/execution-seedA-PW.log
    data/single/execution-seedB-PW.log
)

echo "n,red" > $OUTPUT_FILE

for f in ${INPUT_FILES[@]}; do
    cat $f | grep Reduced \
        | sed "s/.*Input: //" \
        | sed "s/ Reduced: //" >> $OUTPUT_FILE
done;
