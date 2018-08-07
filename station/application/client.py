import asyncio
import json
import os

reader = None
writer = None
server_state = 'idle'
local_state = 'idle'
curr_test_number = -1
local_port = 5100


async def mount_message(method, params):
    return json.dumps({
        "jsonrpc": "2.0",
        "method": str(method),
        "params": params,
        "id": 1})


async def transmmit(message):

    print('Send: %r' % message)
    writer.write(message.encode())

    data = await reader.read()
    print('Received: %r' % data.decode())

    print('Close the socket')


async def start(test_number):
    cmd = "tcpdump -i wla0 udp port 5100 -vvv -ttt -c 19500 -w wlan_{}.pcap &".format(test_number)
    os.system(cmd)
    cmd = "iperf -c 192.168.1.1 -b 4950 -i 1 -f l -p 5100 > iperf_{}.log".format(test_number)
    os.system(cmd)


async def get_server_status():
    message = await mount_message("status", local_port)
    response = await transmmit(message)
    


async def app(loop):
    reader, writer = asyncio.open_connection('127.0.0.1', 8888, loop=loop)
    while curr_test_number < 11:
        if local_state == 'idle':
            pass
        elif local_state == 'waiting':
            pass
        elif local_state == 'run':
            pass
        elif local_state == 'stopped':
            pass
    writer.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(app(loop))
loop.close()
