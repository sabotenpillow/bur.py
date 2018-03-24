bur.py is a tool for capturing, editing or dropping http request/response(s).

## Usage & Options

```
Usage:
    bur.py <interface> [--req | --res] [-s | --src <src>] [-d | --dst <dst>] [-h | --host <host>]
    bur.py -v | --version
    bur.py --help
Options:
    <interface>        Specify interface name
    --req              Capture request only
    --res              Capture response only
    -s --src <dst>     Specify source address
    -d --dst <dst>     Specify destination address
    -h --host <host>   Specify source or destination address
    -v --version       Show version
    --help             Show help
```

### Keymap

#### List mode

| key | desciption |
|:-:|:-:|
| j | down |
| k | up |
| a | accept a request/response |
| d | drop a request/response |
| e | edit a request/response (switch edit mode) |
| Q | quit |

#### Edit mode

| key | desciption |
|:-:|:-:|
| C-n | down |
| C-p | up |
| C-f | right |
| C-b | left |
| C-e | move end of line |
| C-a | move begging of line |
| C-h | delete right char |
| C-d | delete left char |
| C-k | delete and copy right of line |
| C-u | delete and copy left of line |
| C-y | past |
| C-j | add newline |
| C-g | save & exit |

## dependencies

- python3

### python modules

- NetfilterQueue
- scapy
- curses
- docopt

Execute the following command to install the above modules.

```
pip install NetfilterQueue scapy-python3 curses docopt
```

