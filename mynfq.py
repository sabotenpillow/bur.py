from netfilterqueue import NetfilterQueue
import logging
logging.getLogger('scapy.runtime').setLevel(logging.ERROR)
from scapy.all import *

class MyNfq:
    def __init__(self, queue_id):
        self.nfqueue = NetfilterQueue()
        self.nfqueue.bind(queue_id, self.__cb)
        self.pktnum = 0
        self.pktlist = []
        self.only_req = False
        self.only_res = False

    def __cb(self, pkt):
        packet = IP(pkt.get_payload())
        if packet.proto is 0x06 and packet.haslayer(Raw):
            #print(packet[TCP].payload.load.decode())
            #print(packet[TCP].payload.load.__class__)
            is_http = MyNfq.__is_HTTP(packet[TCP].payload.load)
            if ( is_http == 'request' ):
                if ( self.only_res ):
                    pkt.accept(); return
            elif ( is_http == 'response' ):
                if ( self.only_req ):
                    pkt.accept(); return
            else: pkt.accept(); return
            tcp = packet[TCP]
            line = [is_http, ':', packet.src, '->', packet.dst,
                    ',', tcp.sport, '->', tcp.dport]
            line = ' '.join(map(str, line))
            self.pktnum += 1
            self.pktlist.append(
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
