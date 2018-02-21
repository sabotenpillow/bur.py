import os
import sys
import subprocess
import threading
from mynfq import MyNfq
from mycurses import MyCurses as MyCrs
# from IPython import embed
import time

class NfqRunner(threading.Thread):
    def __init__(self, nfq):
        super(NfqRunner, self).__init__()
        self.__nfq       = nfq
        self.__loop_flag = True
    def run(self):
        while self.__loop_flag:
            try:
                self.__nfq.run()
            except:
                pass
    def stop(self):
        self.__loop_flag = False

#if __name__ is '__main__':
def main():
    QUEUE_ID = 6
    IF       = 'eth1'
    subprocess.call((
        'iptables -t raw -A PREROUTING -j NFQUEUE --queue-num '
        +str(QUEUE_ID)+' -i '+IF).split(' '))
    subprocess.call((
        'iptables -t raw -A OUTPUT -j NFQUEUE --queue-num '
        +str(QUEUE_ID)+' -s 192.168.67.10').split(' '))

    nfq    = MyNfq(QUEUE_ID)
    nfq.set_socket_timeout(1)
    nfqthr = NfqRunner(nfq)
    crs    = MyCrs()
    nfqthr.start()

    for i in range(1, 10):
        time.sleep(1)
        crs.printlist(nfq)

    MyCrs.exit()
    nfqthr.stop()
    print('wait for sub thread finish')
    nfqthr.join()
    nfq.unbind()
    subprocess.call('iptables -t raw -F'.split(' '))

main()
