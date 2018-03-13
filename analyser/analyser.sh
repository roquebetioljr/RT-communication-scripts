#!/usr/bin/env bash

# Check if tshark is installed
if ! hash python > /dev/null 2>&1 ; then
    echo 'python needed'
    exit 1
fi

if [ $# -lt 1 ]; then
    echo "Correct usage. $ analyser.sh <paths/of/results>"
    exit 1
fi

CURR_PWD=${PWD}

for var in "$@"
do
    echo "$var"

    if [ ! -d $var ]; then
        echo "Path $var not found"
        echo "Resuming.."
        continue
    fi

    cd $var

    CNT=0

    while [ $CNT -lt 16 ] ; do
        echo "Analysing test ${CNT}"
# deadlines
# 0.01 for 36kbps
# 0.02 for 16kbps
# 0.05 for 7.2kbps
        python ~/dev/RT-communication-scripts/analyser/packet-analyser2.py wlan_${CNT}.json eth_${CNT}.json test_${CNT}.csv 0.01 &
        CNT=$((CNT+1))
    done

    wait
    python ~/dev/RT-communication-scripts/analyser/merge_results.py test_* merged.csv
    cd ${CURR_PWD}
done

echo "end"
exit 0
