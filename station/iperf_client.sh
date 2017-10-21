#!/bin/bash


if [ $# != 5 ]; then
    echo "Correct usage. $ iperf_client.sh <path/to/store/results> <wireless interface> <ethernet interface> <ip> <test number>"
    exit 1
fi

if [ ! -d $1 ]; then
   mkdir $1
fi

cd $1

echo "Executing test number $COUNTER"

echo "Su password needed"
sudo echo "Thanks!"

sudo tcpdump -i $2 udp port 5100 -vvv -ttt -c 20 -w wlan_$5.pcap &
sudo tcpdump -i $3 udp port 5100 -vvv -ttt -c 20 -w eth_$5.pcap &

sleep 1
iperf -c $4 -b 27k -u -i 1 -f k -p 5100 -S 0x06 > iperf_$5.log 

sleep 5
sudo killall tcpdump
echo "Test $5 finished."

exit 0
