import os
import sys
import subprocess
from netfilterqueue import NetfilterQueue
import logging
logging.getLogger('scapy.runtime').setLevel(logging.ERROR)
from scapy.all import *
from IPython import embed

def nfprocess(pkt):
    packet = IP(pkt.get_payload())

    if packet.proto is 0x06:
        if packet[TCP].payload.__class__ is scapy.packet.Raw:
            tcp = packet[TCP]
            line = [packet.src, '->', packet.dst, ',',
                    tcp.sport, '->', tcp.dport]
            line = ' '.join(map(str, line))
            print(line)
            #print(packet[TCP].payload.load.decode())

    pkt.accept()

#if __name__ is '__main__':
def main():
    subprocess.call('iptables -t raw -A PREROUTING -j NFQUEUE --queue-num 6 -i eth1'.split(' '))
    subprocess.call('iptables -t raw -A OUTPUT -j NFQUEUE --queue-num 6 -s 192.168.67.10'.split(' '))

    nfqueue = NetfilterQueue()
    nfqueue.bind(6, nfprocess)

    try:
        nfqueue.run()
    except:
        print("Exit.")

    nfqueue.unbind()
    subprocess.call('iptables -t raw -F'.split(' '))

main()
