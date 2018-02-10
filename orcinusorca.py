import os
import sys
import subprocess
from netfilterqueue import NetfilterQueue
from scapy.all import *
#from IPython import embed

def nfprocess(pkt):
    packet = IP(pkt.get_payload())

    print(packet)
    pkt.accept()

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
