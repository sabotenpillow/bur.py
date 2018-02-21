import curses

class MyCurses:
    listtop      = 0
    stdscr       = curses.initscr()
    max_y, max_x = stdscr.getmaxyx()
    curses.noecho()
    curses.cbreak()
    #stdscr.nodelay(True)
    #stdscr.keypad(True)
    stdscr.clear()

    def __init__(self):
        self.__cur_y, self.__cur_x = 0, 0

    @classmethod
    def exit(self):
        self.stdscr.keypad(False)
        curses.nocbreak()
        curses.echo()
        curses.endwin()

    def printlist(self, nfq):
        MyCurses.updatelist(nfq)
        self.move_curpos()
        #self.print_curposline(nfq)
        MyCurses.stdscr.refresh()

    #def print_curposline(self, nfq):
    @classmethod
    def updatelist(self, nfq):
        y = 0
        for e in nfq.get_pktrange(self.listtop,
                                  self.listtop + self.max_y):
            self.stdscr.addstr(y, 0, e['oneline'])
            y += 1

    def move_curpos(self):
        MyCurses.stdscr.move(self.__cur_y, self.__cur_x)

    def keyinput(self, nfq):
        k = MyCurses.stdscr.getkey()
        if   k == 'j' : self.__cursor_down(nfq)
        elif k == 'k' : self.__cursor_up()
        elif k == 'g' : self.__cur_y = 0
        elif k == 'G' :
            self.__cur_y = min(nfq.get_pktnum(), MyCurses.max_y) - 1
        elif k == 'Q' :
            return -1
    # def keyinput(self, nfq):
    #     k = MyCurses.stdscr.getch()
    #     if   k == ord('j') or k == curses.KEY_DOWN : self.__cursor_down(nfq)
    #     elif k == ord('k') or k == curses.KEY_UP : self.__cursor_up()
    #     elif k == ord('g') : self.__cur_y = 0
    #     elif k == ord('G') :
    #         self.__cur_y = min(nfq.get_pktnum(), MyCurses.max_y) - 1
    #     elif k == ord('Q') :
    #         return -1

    def __cursor_down(self, nfq):
        cmp_res = MyCurses.cmp(self.__cur_y, MyCurses.max_y-1)
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
        if pktnum > self.listtop + self.max_y:
            self.listtop += 1
    @classmethod
    def __dec_listtop(self):
        if self.listtop > 0:
            self.listtop -= 1
    @staticmethod
    def cmp(a,  b):
        if a is b: return 0
        return -1 if a < b else 1
