#!/bin/sh

# Check if tshark is installed
if ! hash tshark > /dev/null 2>&1 ; then
    echo 'tshark needed'
    exit 1
fi

if [ $# != 1 ]; then
    echo "Correct usage. $ pcap_to_json.sh <path/of/results>"
    exit 1
fi

if [ ! -d $1 ]; then
    echo "Path $1 not found"
    exit 1
fi

cd $1

CNT=0

while [ $CNT -lt 10 ] ; do
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

echo "end"
exit 0