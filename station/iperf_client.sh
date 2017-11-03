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

sudo tcpdump -i $2 udp port 5100 -vvv -ttt -c 19500 -w wlan_$5.pcap &
sudo tcpdump -i $3 udp port 5100 -vvv -ttt -c 19500 -w eth_$5.pcap &

iperf -s -u -i 1 -f k -p 5100 >> iperf_server_$5.log &

sleep 1
# for RT stations
iperf -c $4 -b 36k -u -i 1 -f l -p 5100 -S 0x06 -k 1000 -l 45 > iperf_$5.log

# for NRT stations
#iperf -c $4 -b 9M -u -i 1 -f l -p 5100 > iperf_$5.log

sleep 5
sudo killall tcpdump
sudo killall iperf
echo "Test $5 finished."

exit 0
