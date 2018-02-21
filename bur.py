import os
import sys
import subprocess
import threading
from mynfq import MyNfq
# from IPython import embed

def nfqthread(queue_id):
    nfq = MyNfq(queue_id)

    try:
        nfq.nfqueue.run()
    except:
        print("Exit.")

    nfq.nfqueue.unbind()

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

    nfqthr = threading.Thread(target=nfqthread, args=(QUEUE_ID,))
    nfqthr.start()
    nfqthr.join()

    subprocess.call('iptables -t raw -F'.split(' '))

main()
