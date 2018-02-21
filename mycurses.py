import curses

class MyCurses:
    listtop      = 0
    stdscr       = curses.initscr()
    max_y, max_x = stdscr.getmaxyx()
    curses.noecho()
    curses.cbreak()
    stdscr.clear()
    def __init__(self):
        self.cur_y, self.cur_x = -1, -1
    @classmethod
    def exit(self):
        self.stdscr.keypad(False)
        curses.nocbreak()
        curses.echo()
        curses.endwin()
    def printlist(self, nfq):
        MyCurses.updatelist(nfq)
        MyCurses.stdscr.refresh()
    @classmethod
    def updatelist(self, nfq):
        y = 0
        for e in nfq.get_pktrange(self.listtop,
                                  self.listtop + self.max_y):
            self.stdscr.addstr(y, 0, e['oneline'])
            y += 1
