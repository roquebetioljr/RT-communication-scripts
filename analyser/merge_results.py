import sys

out_file = None

transmitted_packets = []
received_packets = []
lost_packets = []
dead_line_misses = []
not_transmitted = []
transmission_delays = []


def get_statistics(filename):
    read_file = open(filename, 'r')
    line = read_file.readline()
    while len(line) != 0:
        print("a\n")
        if line.startswith("Total of transmitted packets"):
            transmitted_packets.append(line[len("Total of transmitted packets; "):(len(line)-2)])
        if line.startswith("Total of received packets"):
            received_packets.append(line[len("Total of received packets; "):(len(line)-2)])
        if line.startswith("Total of lost packets"):
            lost_packets.append(line[len("Total of lost packets; "):(len(line)-2)])
        if line.startswith("Total of deadline missed"):
            dead_line_misses.append(line[len("Total of deadline missed; "):(len(line)-2)])
        if line.startswith("Total of not transmitted packets"):
            not_transmitted.append(line[len("Total of not transmitted packets; "):(len(line) - 2)])
        if line.startswith("Average of transmission delay"):
            transmission_delays.append(line[len("Average of transmission delay;"):(len(line)-2)])
        line = read_file.readline()


def output_statistics(outfile):
    out_file = open(outfile, 'w')

    line = str()
    for aux in transmitted_packets:
        line += '{};'.format(aux)
    line += '\n'
    out_file.write(line)

    line = str()
    for aux in received_packets:
        line += '{};'.format(aux)
    line += '\n'
    out_file.write(line)

    line = str()
    for aux in lost_packets:
        line += '{};'.format(aux)
    line += '\n'
    out_file.write(line)

    line = str()
    for aux in dead_line_misses:
        line += '{};'.format(aux)
    line += '\n'
    out_file.write(line)

    line = str()
    for aux in not_transmitted:
        line += '{};'.format(aux)
    line += '\n'
    out_file.write(line)

    line = str()
    for aux in transmission_delays:
        line += '{};'.format(aux)
    line += '\n'
    out_file.write(line)

    out_file.close()


if __name__ == '__main__':
    if len(sys.argv) < 2 or len(sys.argv) > 18:
        print("ERROR! Invalid input arguments ({}).\n Use $ python merge_results.py <in_files> <out_file>\n".format(len(sys.argv)))
    else:
        count = 1
        while count < len(sys.argv) - 1:
            print("{}\n".format(sys.argv[count]))
            get_statistics(sys.argv[count])
            count += 1

        output_statistics(sys.argv[count])
