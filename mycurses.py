import curses

class MyCurses:
    __listtop        = 0
    __stdscr         = curses.initscr()
    __max_y, __max_x = __stdscr.getmaxyx()
    curses.noecho()
    curses.cbreak()
    #__stdscr.nodelay(True)
    #__stdscr.keypad(True)
    __stdscr.clear()

    def __init__(self):
        self.__cur_y, self.__cur_x = 0, 0

    @classmethod
    def exit(self):
        self.__stdscr.keypad(False)
        curses.nocbreak()
        curses.echo()
        curses.endwin()

    def printlist(self, nfq):
        MyCurses.updatelist(nfq)
        self.move_curpos()
        #self.print_curposline(nfq)
        MyCurses.__stdscr.refresh()

    #def print_curposline(self, nfq):
    @classmethod
    def updatelist(self, nfq):
        y = 0
        for e in nfq.get_pktrange(self.__listtop,
                                  self.__listtop + self.__max_y):
            self.__stdscr.addstr(y, 0, e['oneline'])
            y += 1

    def move_curpos(self):
        MyCurses.__stdscr.move(self.__cur_y, self.__cur_x)

    def keyinput(self, nfq):
        k = MyCurses.__stdscr.getkey()
        if   k == 'j' : self.__cursor_down(nfq)
        elif k == 'k' : self.__cursor_up()
        elif k == 'g' : self.__cur_y = 0
        elif k == 'G' :
            self.__cur_y = min(nfq.get_pktnum(), MyCurses.__max_y) - 1
        elif k == 'Q' :
            return -1
    # def keyinput(self, nfq):
    #     k = MyCurses.__stdscr.getch()
    #     if   k == ord('j') or k == curses.KEY_DOWN : self.__cursor_down(nfq)
    #     elif k == ord('k') or k == curses.KEY_UP : self.__cursor_up()
    #     elif k == ord('g') : self.__cur_y = 0
    #     elif k == ord('G') :
    #         self.__cur_y = min(nfq.get_pktnum(), MyCurses.max_y) - 1
    #     elif k == ord('Q') :
    #         return -1

    def __cursor_down(self, nfq):
        cmp_res = MyCurses.cmp(self.__cur_y, MyCurses.__max_y-1)
        pktnum = nfq.get_pktnum()
        if   cmp_res is -1 and self.__cur_y < pktnum-1:
            self.__cur_y += 1
        elif cmp_res is 0:
            MyCurses.__inc_listtop(pktnum)
    def __cursor_up(self):
        cmp_res = MyCurses.cmp(self.__cur_y, 0)
        if   cmp_res is 1:
            self.__cur_y -= 1
        if   cmp_res is 0:
            MyCurses.__dec_listtop()
    @classmethod
    def __inc_listtop(self, pktnum):
        if pktnum > self.__listtop + self.__max_y:
            self.__listtop += 1
    @classmethod
    def __dec_listtop(self):
        if self.__listtop > 0:
            self.__listtop -= 1
    @staticmethod
    def cmp(a,  b):
        if a is b: return 0
        return -1 if a < b else 1
