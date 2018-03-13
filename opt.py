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

VERSION = ''.join(open('version').readline().splitlines())

def optparser():
    args = docopt(__doc__, version=VERSION)
    if not is_valid_ifname(args['<interface>']):
        print('invalid interface name')
        exit(-1)
    return args

def is_valid_ifname(ifname):
    return ifname in os.listdir('/sys/class/net')

if __name__ == '__main__':
    print(optparser())
