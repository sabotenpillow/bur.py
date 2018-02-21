import os
import sys
import subprocess
from mynfq import MyNfq
# from IPython import embed

#if __name__ is '__main__':
def main():
    QUEUE_ID = 6
    IF = 'eth1'
    subprocess.call((
        'iptables -t raw -A PREROUTING -j NFQUEUE --queue-num '
        +str(QUEUE_ID)+' -i '+IF).split(' '))
    subprocess.call((
        'iptables -t raw -A OUTPUT -j NFQUEUE --queue-num '
        +str(QUEUE_ID)+' -s 192.168.67.10').split(' '))

    nfq = MyNfq(QUEUE_ID)

    try:
        nfq.nfqueue.run()
    except:
        print("Exit.")

    nfq.nfqueue.unbind()
    subprocess.call('iptables -t raw -F'.split(' '))

main()
