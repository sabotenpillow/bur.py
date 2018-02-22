from netfilterqueue import NetfilterQueue
import logging
logging.getLogger('scapy.runtime').setLevel(logging.ERROR)
from scapy.all import *
# import socket

class MyNfq:
    def __init__(self, queue_id):
        self.__nfqueue = NetfilterQueue()
        self.__nfqueue.bind(queue_id, self.__cb)
        self.__pktlist  = []
        self.__only_req = False
        self.__only_res = False
        self.__socket   = socket.fromfd(self.__nfqueue.get_fd(),
                                        socket.AF_UNIX,
                                        socket.SOCK_STREAM)

    def __cb(self, pkt):
        packet = IP(pkt.get_payload())
        if packet.proto is 0x06 and packet.haslayer(Raw):
            is_http = MyNfq.__is_HTTP(packet[TCP].payload.load)
            if ( is_http == 'request' ):
                if ( self.__only_res ):
                    pkt.accept(); return
            elif ( is_http == 'response' ):
                if ( self.__only_req ):
                    pkt.accept(); return
            else: pkt.accept(); return
            tcp = packet[TCP]
            line = [is_http, ':', packet.src, '->', packet.dst,
                    ',', tcp.sport, '->', tcp.dport]
            line = ' '.join(map(str, line))
            self.__pktlist.append(
                {'pkt':pkt, 'oneline':line, })
            # print(line)
        else: pkt.accept()

    def get_fd(self):
        return self.__nfqueue.get_fd()
    def run(self):
        self.__nfqueue.run_socket(self.__socket)
    def unbind(self):
        self.__nfqueue.unbind()

    def get_socket(self):
        return self.__socket
    def set_socket_timeout(self, sec):
        self.__socket.settimeout(sec)

    @staticmethod
    def __is_HTTP(raw):
        if ( re.match('^.+ /.* HTTP/.\..\r\n', raw.decode()) ):
            return 'request'
        elif ( re.match('^HTTP/.\.. .+ .+\r\n', raw.decode()) ):
            return 'response'
        else: return False

    def get_pktnum(self):
        return len(self.__pktlist)

    def get_a_pkt(self, i):
        try:
            return self.__pktlist[i]
        except: pass

    def get_ranged_pkts(self, first, last):
        return self.__pktlist[first:last]

    def accept(self, i):
        self.__pktlist[i]['pkt'].accept()
        self.__del_elem(i)
    def drop(self, i):
        self.__pktlist[i]['pkt'].drop()
        self.__del_elem(i)
    def __del_elem(self, i):
        del(self.__pktlist[i])
