from netfilterqueue import NetfilterQueue
import logging
logging.getLogger('scapy.runtime').setLevel(logging.ERROR)
from scapy.all import *

class MyNfq:
    def __init__(self, queue_id):
        self.nfqueue = NetfilterQueue()
        self.nfqueue.bind(queue_id, self.__cb)
        self.__pktlist = []
        self.__only_req = False
        self.__only_res = False

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
            print(line)
        else: pkt.accept()

    @staticmethod
    def __is_HTTP(raw):
        if ( re.match('^.+ /.* HTTP/.\..\r\n', raw.decode()) ):
            return 'request'
        elif ( re.match('^HTTP/.\.. .+ .+\r\n', raw.decode()) ):
            return 'response'
        else: return False
