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
""".format(f=__file__).strip()

from docopt import docopt

def optparser():
    args = docopt(__doc__, help=False)
    if args['--help']:
        print(__doc__)
        exit(0)
    if args['--version']:
        print('v0.1')
        exit(0)
    return args

if __name__ == '__main__':
    print(optparser())
