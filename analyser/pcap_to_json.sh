#!/bin/sh

# Check if tshark is installed
if ! hash tshark > /dev/null 2>&1 ; then
    echo 'tshark needed'
    exit 1
fi

if [ $# -lt 1 ]; then
    echo "Correct usage. $ pcap_to_json.sh <paths/of/results>"
    exit 1
fi

CURR_PWD=${PWD}

for var in "$@"
do
    echo "$var"

    if [ ! -d $var ]; then
        echo "Path $var not found"
        echo "Continuing.."
        continue
    fi

    cd $var

    for f in *.pcap; do
        echo "Exporting $f"
        tshark -r $f -T json > $f.json &
    done
    CNT=0

    wait
    cd ${CURR_PWD}
done

echo "end"
exit 0
