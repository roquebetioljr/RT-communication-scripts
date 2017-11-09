#!/usr/bin/python

import json
from datetime import datetime
import sys

class PacketAnalyser:

    def __init__(self, wlan_file, eth_file, out_file):
        self.wlan_file = wlan_file
        self.eth_file = eth_file
        self.out_file = out_file
        self.merged_dict = {}
        self.seq_pkts = []

    def analyse_wlan(self):
        print('Analysing Wlan')
        try:
            file = open(self.wlan_file, 'r')
            wlan_content = file.read()
            file.close()
        except:
            print("ERROR! Couldn't open {} file.".format(self.wlan_file))
            return False
        last_time = -1
        wlan_packet_list = json.loads(wlan_content)
        for packet in wlan_packet_list:
            if '_source' in packet and 'layers' in packet['_source'] and \
                            'udp' in packet['_source']['layers']:
                pkt_id = packet['_source']['layers']['ip']['ip.id']
                pkt_id = int(pkt_id, 16)

                curr_timestamp = float(packet['_source']['layers']['frame']['frame.time_epoch'])
                delta = 0
                if last_time != -1:
                    delta = curr_timestamp - last_time
                last_time = curr_timestamp

                # pkt_time = datetime.utcfromtimestamp(curr_timestamp)

                self.merged_dict[pkt_id] = {'transmit_timestamp': curr_timestamp,
                                            'delta_wlan_transmit': delta,
                                            'packet_lost': True}
                self.seq_pkts.append(pkt_id)

        return True

    def analyse_eth(self):
        print('Analysing Eth')
        try:
            file = open(self.eth_file, 'r')
            eth_content = file.read()
            file.close()
        except:
            print("ERROR! Couldn't open {} file.".format(self.eth_file))
            return False
        last_time = -1
        eth_packet_list = json.loads(eth_content)
        for packet in eth_packet_list:
            if '_source' in packet and 'layers' in packet['_source'] and \
                            'udp' in packet['_source']['layers']:
                pkt_id = packet['_source']['layers']['ip']['ip.id']
                pkt_id = int(pkt_id, 16)

                curr_timestamp = float(packet['_source']['layers']['frame']['frame.time_epoch'])
                delta = 0
                if last_time != -1:
                    delta = curr_timestamp - last_time
                last_time = curr_timestamp

                # pkt_time = datetime.utcfromtimestamp(curr_timestamp)
                if pkt_id in self.merged_dict:
                    pkt_delay = curr_timestamp - self.merged_dict[pkt_id]['transmit_timestamp']
                    if pkt_delay >= 0:
                        self.merged_dict[pkt_id]['receive_timestamp'] = curr_timestamp
                        self.merged_dict[pkt_id]['delta_eth_receive'] = delta
                        self.merged_dict[pkt_id]['packet_lost'] = False
                        self.merged_dict[pkt_id]['transmission_delay'] = pkt_delay
                    else:
                        del self.merged_dict[pkt_id] # ignore this packet. Something wrong happend
                        self.seq_pkts.remove(pkt_id)
                else:
                    self.merged_dict[pkt_id] = {'transmit_timestamp': -1, 'delta_wlan_transmit': -1,
                                                'packet_lost': True, 'receive_timestamp': curr_timestamp,
                                                'delta_eth_receive': delta,
                                                'transmission_delay': -1}
                    self.seq_pkts.append(pkt_id)

        return True

    def write_out_file(self):
        print('Creating output file')
        #merged_indexes = self.merged_dict.keys()
        #merged_indexes.sort()
        try:
            file = open(self.out_file, 'w')
        except:
            print("ERROR! Couldn't create/open {} file.".format(self.out_file))
            return False

        packet_lost_counter = 0
        packet_not_transmmited = 0
        last_pkt_id = -1
        packet_received_counter = 0
        sum_transmit_delay = 0
        for pkt_id in self.seq_pkts:
            packet = self.merged_dict[pkt_id]
            is_packet_lost = packet['packet_lost']
            if is_packet_lost:
                packet_lost_counter += 1
                receive_timestamp = ''
                delta_eth_receive = ''
                transmission_delay = ''
            else:
                if last_pkt_id != -1 and pkt_id > last_pkt_id + 1:
                    packet_not_transmmited += (pkt_id - last_pkt_id + 1)
                receive_timestamp = datetime.utcfromtimestamp(packet['receive_timestamp'])
                delta_eth_receive = '{:0,.10f}'.format(packet['delta_eth_receive'])
                transmission_delay = '{:0,.10f}'.format(packet['transmission_delay'])
                sum_transmit_delay += packet['transmission_delay']
                packet_received_counter += 1

            last_pkt_id = pkt_id
            transmit_timestamp = datetime.utcfromtimestamp(packet['transmit_timestamp'])
            delta_wlan_transmit = '{:0,.10f}'.format(packet['delta_wlan_transmit'])



            # id | Packet Lost | transmit timestamp | delta transmit | receive timestamp | delta receive | transmmission delay
            line = '{};{};{};{};{};{};{};\n'.format(pkt_id, is_packet_lost, transmit_timestamp, delta_wlan_transmit,
                                                    receive_timestamp, delta_eth_receive, transmission_delay)
            print(line)
            file.write(line)

        line = 'Total of transmitted packets; {};\n'.format(len(self.seq_pkts))
        print(line)
        file.write(line)

        line = 'Total of received packets; {};\n'.format(packet_received_counter)
        print(line)
        file.write(line)

        line = 'Total of lost packets; {};\n'.format(packet_lost_counter)
        print(line)
        file.write(line)

        line = 'Total of not transmitted packets; {};\n'.format(packet_not_transmmited)
        print(line)
        file.write(line)

        avg_transmit_delay = (sum_transmit_delay/packet_received_counter)

        line = 'Average of transmission delay; {};\n'.format(avg_transmit_delay)
        print(line)
        file.write(line)

        # print(merged_dict)
        file.close()

        return True

    def execute(self):
        if self.analyse_wlan() and self.analyse_eth() and self.write_out_file():
            print("FINISHED. Success!")
        else:
            print("FINISHED. Failed!")


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("ERROR! Invalid input.\n Use $ python packet-analyser.py <wlan_file> <eth_file> <out_file> \n")
    else:
        analyser = PacketAnalyser(str(sys.argv[1]), str(sys.argv[2]), str(sys.argv[3]))
        analyser.execute()

