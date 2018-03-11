import os
import sys
import subprocess
import threading
from mynfq import MyNfq
from mycurses import MyCurses as MyCrs
# from IPython import embed
import time
from opt import optparser

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

class CursesRunner(threading.Thread):
    def __init__(self, crs, nfq):
        super(CursesRunner, self).__init__()
        self.__crs       = crs
        self.__nfq       = nfq
        self.__loop_flag = True
    def run(self):
        while self.__loop_flag:
            self.__crs.printlist(self.__nfq)
            time.sleep(0.05)
    def stop(self):
        self.__loop_flag = False

def main():
    args = optparser()
    QUEUE_ID   = 6
    interface  = args['<interface>']
    subprocess.call((
        'iptables -t raw -A PREROUTING -j NFQUEUE --queue-num '
        +str(QUEUE_ID)+' -i '+interface).split(' '))
    subprocess.call((
        'iptables -t raw -A OUTPUT -j NFQUEUE --queue-num '
        +str(QUEUE_ID)+' -o '+interface).split(' '))

    nfq    = MyNfq(QUEUE_ID, args)
    nfq.set_socket_timeout(1)
    nfqthr = NfqRunner(nfq)
    crs    = MyCrs()
    # crsthr = CursesRunner(crs, nfq)
    nfqthr.start()
    # crsthr.start()

    while True:
        if crs.keyinput(nfq) is -1 : break
        # crs.printlist(nfq)

    nfqthr.stop()
    # crsthr.stop()
    MyCrs.exit()
    print('wait for sub thread finish')
    nfqthr.join()
    # crsthr.join()
    nfq.unbind()
    subprocess.call('iptables -t raw -F'.split(' '))

if __name__ == '__main__':
    main()
