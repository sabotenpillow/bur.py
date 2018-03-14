import sys
__doc__ = """

Usage:
    {f} <interface> [--req | --res] [-s | --src <src>] [-d | --dst <dst>] [-h | --host <host>]
    {f} -v | --version
    {f} --help

Options:
    <interface>        Specify interface name
    --req              Capture request only
    --res              Capture response only
    -s --src <src>     Specify source address
    -d --dst <dst>     Specify destination address
    -h --host <host>   Specify source or destination address
    -v --version       Show version
    --help             Show help
""".format(f=sys.argv[0]).strip()

from docopt import docopt
import os
import socket

VERSION = ''.join(open('version').readline().splitlines())

def optparser():
    args = docopt(__doc__, version=VERSION)
    if not is_valid_ifname(args['<interface>']):
        print('invalid interface name')
        exit(-1)
    if args['--src'] and not is_valid_ip(args['--src']):
        print('invalid source')
        exit(-1)
    if args['--dst'] and not is_valid_ip(args['--dst']):
        print('invalid destination')
        exit(-1)
    if args['--host'] and not is_valid_ip(args['--host']):
        print('invalid host')
        exit(-1)
    return args

def is_valid_ifname(ifname):
    return ifname in os.listdir('/sys/class/net')

def is_valid_ip(addrs):
    for addr in addrs:
        if not ( is_valid_ipv4(addr) or is_valid_ipv6(addr) ): return False
    return True

def is_valid_ipv4(addr):
    try:
        socket.inet_pton(socket.AF_INET, addr)
    except socket.error:
        return False
    return True

def is_valid_ipv6(addr):
    try:
        socket.inet_pton(socket.AF_INET6, addr)
    except socket.error:
        return False
    return True

if __name__ == '__main__':
    print(optparser())
