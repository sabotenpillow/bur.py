import curses
from curses_pad import curses_pad

class MyCurses:
    __listtop        = 0
    __stdscr         = curses.initscr()
    __max_y, __max_x = __stdscr.getmaxyx()
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)
    __stdscr.nodelay(True)
    #__stdscr.keypad(True)
    __stdscr.clear()

    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_RED)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_GREEN)
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_YELLOW)
    curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_BLUE)
    curses.init_pair(6, curses.COLOR_BLACK, curses.COLOR_MAGENTA)
    curses.init_pair(7, curses.COLOR_BLACK, curses.COLOR_CYAN)
    curses.init_pair(8, curses.COLOR_BLACK, curses.COLOR_WHITE)

    def __init__(self):
        self.__cur_y, self.__cur_x = 0, 0

    @classmethod
    def exit(self):
        self.__stdscr.keypad(False)
        curses.nocbreak()
        curses.echo()
        curses.endwin()

    def printlist(self, nfq):
        self.__stdscr.erase()
        MyCurses.updatelist(nfq)
        self.print_curposline(nfq)
        self.move_curpos()
        MyCurses.__stdscr.refresh()

    def print_curposline(self, nfq):
        pktelem = nfq.get_a_pkt(MyCurses.__listtop + self.__cur_y)
        if pktelem is not None:
            self.__stdscr.addstr(self.__cur_y, 0, pktelem['oneline'],
                                 curses.color_pair(4))

    @classmethod
    def updatelist(self, nfq):
        y = 0
        for e in nfq.get_ranged_pkts(self.__listtop,
                                  self.__listtop + self.__max_y):
            self.__stdscr.addstr(y, 0, e['oneline'])
            y += 1

    def move_curpos(self):
        MyCurses.__stdscr.move(self.__cur_y, self.__cur_x)

    def keyinput(self, nfq):
        #k = MyCurses.__stdscr.getkey()
        k = MyCurses.__stdscr.getch()
        if   k == ord('j'): self.__cursor_down(nfq)
        elif k == ord('k'): self.__cursor_up()
        elif k == ord('g'): self.__cur_y = 0
        elif k == ord('G'):
            dest_y = min(nfq.get_pktnum(), MyCurses.__max_y) - 1
            if dest_y >= 0: self.__cur_y = dest_y
        elif k == ord('a'):
            nfq.accept(MyCurses.__listtop + self.__cur_y)
            self.__correct_curline(nfq)
        elif k == ord('d'):
            nfq.drop(MyCurses.__listtop + self.__cur_y)
            self.__correct_curline(nfq)
        elif k == ord('e'):
            i = MyCurses.__listtop + self.__cur_y
            curses.curs_set(1)
            nfq.set_payload( i,
                curses_pad.CursesPad(
                    self.__stdscr, nfq.get_payload(i)
                    ).edit())
            curses.curs_set(0)
        elif k == ord('v'):
            i = MyCurses.__listtop + self.__cur_y
            curses.curs_set(1)
            curses_pad.CursesPad(
                self.__stdscr, nfq.get_rawpkt(i)
                ).edit()
            curses.curs_set(0)
        elif k == ord('Q'):
            return -1
        self.printlist(nfq)

    def __correct_curline(self, nfq):
        pktnum = nfq.get_pktnum()
        if pktnum != 0 and MyCurses.__listtop + self.__cur_y >= pktnum:
            self.__cur_y -= 1

    def __cursor_down(self, nfq):
        cmp_res = MyCurses.__cmp(self.__cur_y, MyCurses.__max_y-1)
        pktnum = nfq.get_pktnum()
        if   cmp_res is 0:
            MyCurses.__inc_listtop(pktnum)
        elif cmp_res is -1 and self.__cur_y < pktnum-1:
            self.__cur_y += 1
    def __cursor_up(self):
        cmp_res = MyCurses.__cmp(self.__cur_y, 0)
        if   cmp_res is 0:
            MyCurses.__dec_listtop()
        elif cmp_res is 1:
            self.__cur_y -= 1
    @classmethod
    def __inc_listtop(self, pktnum):
        if pktnum > self.__listtop + self.__max_y:
            self.__listtop += 1
    @classmethod
    def __dec_listtop(self):
        if self.__listtop > 0:
            self.__listtop -= 1
    @staticmethod
    def __cmp(a,  b):
        if a is b: return 0
        return -1 if a < b else 1
