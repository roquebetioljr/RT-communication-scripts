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

    CNT=0

    while [ $CNT -lt 16 ] ; do
        if [ -f eth_${CNT}.pcap ]; then
            echo "Exporting eth_${CNT}.pcap"
            tshark -r eth_${CNT}.pcap -T json > eth_${CNT}.json &
        else
            echo "File eth_${CNT}.pcap not found. Continuing.."
        fi

        if [ -f wlan_${CNT}.pcap ]; then
            echo "Exporting wlan_${CNT}.pcap"
            tshark -r wlan_${CNT}.pcap -T json > wlan_${CNT}.json &
        else
            echo "File wlan_${CNT}.pcap not found. Continuing.."
        fi
        CNT=$((CNT+1))
    done

    wait
    cd ${CURR_PWD}
done

echo "end"
exit 0
