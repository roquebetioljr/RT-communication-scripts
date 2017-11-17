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

for var in "$@"
do
    echo "$var"

    if [ ! -d $var ]; then
        echo "Path $var not found"
        exit 1
    fi

    cd $var

    CNT=0

    while [ $CNT -lt 10 ] ; do
        echo "Analysing test ${CNT}"
        python ~/dev/RT-communication-scripts/analyser/packet-analyser.py wlan_${CNT}.json eth_${CNT}.json test_${CNT}.csv &
        CNT=$((CNT+1))
    done

    wait
    cd ..
done

echo "end"
exit 0
