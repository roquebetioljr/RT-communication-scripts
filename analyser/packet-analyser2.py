#!/usr/bin/python


import json
from datetime import datetime
import sys
import pandas as pd

class PacketAnalyser:

    def __init__(self, wlan_file, eth_file, out_file, deadline):
        self.wlan_file = wlan_file
        self.eth_file = eth_file
        self.out_file = out_file
        self.deadline = deadline
        self.merged_dict = {}
        self.seq_pkts = []

        self.wlan_start = 0
        self.eth_start = 0
        self.first_receive_variation = 0

    def analyse_wlan(self):
        print('Analysing Wlan')
        try:
            file = open(self.wlan_file, 'r')
            wlan_content = file.read()
            file.close()
        except:
            print("ERROR! Couldn't open {} file.".format(self.wlan_file))
            return False

        wlan_packet_list = json.loads(wlan_content)
        for packet in wlan_packet_list:
            if '_source' in packet and 'layers' in packet['_source'] and \
                            'udp' in packet['_source']['layers']:
                pkt_id = packet['_source']['layers']['ip']['ip.id']
                pkt_id = int(pkt_id, 16)
                if self.wlan_start == 0:
                    self.wlan_start = float(packet['_source']['layers']['frame']['frame.time_epoch'])

                pkt_time = float(packet['_source']['layers']['frame']['frame.time_relative'])
                pkt_deadline = pkt_time + self.deadline

                self.merged_dict[pkt_id] = {'wlan_time': pkt_time,
                                            'deadline': pkt_deadline,
                                            'eth_time': '',
                                            'delay': '',
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

        eth_packet_list = json.loads(eth_content)
        for packet in eth_packet_list:
            if '_source' in packet and 'layers' in packet['_source'] and \
                            'udp' in packet['_source']['layers']:
                pkt_id = packet['_source']['layers']['ip']['ip.id']
                pkt_id = int(pkt_id, 16)
                if self.eth_start == 0:
                    self.eth_start = float(packet['_source']['layers']['frame']['frame.time_epoch'])
                    self.first_receive_variation = self.eth_start - self.wlan_start

                pkt_time = float(packet['_source']['layers']['frame']['frame.time_relative']) + self.first_receive_variation

                if pkt_id in self.merged_dict:
                    self.merged_dict[pkt_id]['eth_time'] = pkt_time

                    delay = pkt_time - self.merged_dict[pkt_id]['wlan_time']

                    self.merged_dict[pkt_id]['delay'] = delay

                    if pkt_time <= self.merged_dict[pkt_id]['deadline']:
                        self.merged_dict[pkt_id]['packet_lost'] = False
                '''
                else:
                    self.merged_dict[pkt_id] = {'wlan_time': '',
                                                'deadline': '',
                                                'eth_time': pkt_time,
                                                'delay': '',
                                                'packet_lost': True}
                    self.seq_pkts.append(pkt_id)
                '''

        return True

    def write_out_file(self):
        print('Creating output file')
        try:
            file = open(self.out_file, 'w')
        except:
            print("ERROR! Couldn't create/open {} file.".format(self.out_file))
            return False

        packet_lost_cnt = 0
        over_deadline_cnt = 0
        packet_not_transmmited = 0
        last_pkt_id = -1
        packet_received_counter = 0
        transmitted_cnt = 0

        delay_list = []

        for pkt_id in self.seq_pkts:
            packet = self.merged_dict[pkt_id]
            if packet['delay'] < 0:
                continue

            is_packet_lost = packet['packet_lost']
            if is_packet_lost:
                packet_lost_cnt += 1
                if packet['eth_time'] != '' and packet['eth_time'] > packet['deadline']:
                    over_deadline_cnt += 1
            else:
                if last_pkt_id != -1 and pkt_id > last_pkt_id + 1:
                    packet_not_transmmited += (pkt_id - last_pkt_id + 1)

                packet_received_counter += 1
                delay_list.append(packet['delay'])

            last_pkt_id = pkt_id

            transmitted_cnt += 1
            # id | time_transmission | deadline | time_receive | transmmission delay | packet_lost
            line = '{};{};{};{};{};{};\n'.format(pkt_id,
                                                 packet['wlan_time'],
                                                 packet['deadline'],
                                                 packet['eth_time'],
                                                 packet['delay'],
                                                 packet['packet_lost'])
            print(line)
            file.write(line)

        line = 'Total of transmitted packets; {};\n'.format(transmitted_cnt)
        print(line)
        file.write(line)

        line = 'Total of received packets; {};\n'.format(packet_received_counter)
        print(line)
        file.write(line)

        line = 'Total of lost packets; {};\n'.format(packet_lost_cnt)
        print(line)
        file.write(line)

        line = 'Total of deadline missed; {};\n'.format(over_deadline_cnt)
        print(line)
        file.write(line)

        line = 'Total of not transmitted packets; {};\n'.format(packet_not_transmmited)
        print(line)
        file.write(line)

        pkt_series = pd.Series(delay_list)

        avg_transmit_delay = pkt_series.mean()

        line = 'Average of transmission delay; {} ms;\n'.format(avg_transmit_delay * 1000)
        print(line)
        file.write(line)

        line = 'Standard deviation of transmission delay; {} ms;\n'.format(pkt_series.std() * 1000)
        print(line)
        file.write(line)

        #pkt_series = pd.Series(self.jitter_list)

        #line = 'Mean Jitter; {} ms;\n'.format(pkt_series.mean() * 1000)
        #print(line)
        #file.write(line)

        # print(merged_dict)
        file.close()

        return True

    def execute(self):
        if self.analyse_wlan() and self.analyse_eth() and self.write_out_file():
            print("FINISHED. Success!")
        else:
            print("FINISHED. Failed!")


if __name__ == '__main__':
    if len(sys.argv) != 5:
        print("ERROR! Invalid input.\n Use $ python packet-analyser.py <wlan_file> <eth_file> <out_file> <deadline in seconds> \n")
    else:
        analyser = PacketAnalyser(str(sys.argv[1]), str(sys.argv[2]), str(sys.argv[3]), float(sys.argv[4]))
        analyser.execute()
