from Piece import *

class Strat_Team(object):
    def __init__(self, user):
        self.user = user
        self.color = user.color
        self.troops = []
        self.locked = False
        self.dragged = None
        self.move_made = False
        self.track = None

    def strat_set(self):
        res = True

        if(len(self.troops) < 4):
            res = False
        else:
            for t in self.troops:
                if(t.loc == None):
                    res = False
        return res

    def dormant(self):
        for t in self.troops:
            t.dormant()

    def active(self):
        for t in self.troops:
            t.active()

    def get_amount(self, rank):
        temp = 0
        for t in self.troops:
            if(t.rank == rank):
                temp += 1
        return temp

    def get_piece(self, loc):
        p = None
        for t in self.troops:
            if(loc == t.loc):
                p = t
        return p


    def update(self, interact, board):
        mouse_pos = interact[7]
        click = interact[0]
        if(self.dragged == None):
            for t in self.troops:
                t.update(interact, board)
                if(t.drag):
                    self.dragged = t
                    self.track = t.origin
        else:
            self.dragged.update(interact, board)
            if(self.dragged.drag == False):
                if(self.dragged.loc == None):
                    self.troops.remove(self.dragged)
                elif(self.track != self.dragged.loc):
                    self.move_made = True
                    self.track = None
                self.dragged = None

    def blitme(self, board):
        for t in self.troops:
            t.blitme(board, self.color)
        if((self.dragged != None)and(self.locked == True)):
            self.dragged.disp_locs(board)



###################################################################
class Ground_Team(object):
    def __init__(self, user):
        self.user = user
        self.name = user.alias
        self.color = user.color
        self.troops = []
        self.equipment = []
        self.locked = False
        self.dragged = None
        self.selected = None
        self.move_made = False
        self.track = None
        self.LKBP = None

    def strat_set(self):
        res = True

        if(len(self.troops) < 1):
            res = False
        else:
            for t in self.troops:
                if(t.loc == None):
                    res = False
        return res

    def dormant(self):
        for t in self.troops:
            t.dormant()
        for e in self.equipment:
            e.dormant()

    def active(self):
        for t in self.troops:
            t.active()
        for e in self.equipment:
            e.active()

    def get_amount(self, rank):
        temp = 0
        for t in self.troops:
            if(t.rank == rank):
                temp += 1
        return temp

    def get_piece(self, loc):
        p = None
        for t in self.troops:
            if(loc == t.loc):
                p = t
        return p

    def get_equip(self, loc):
        p = None
        for t in self.equipment:
            if(loc == t.loc):
                p = t
        return p

    def update(self, interact, board):
        mouse_pos = interact[7]
        click = interact[0]
        if(self.dragged == None):
            for t in self.troops:
                t.update(interact, board)
                if(t.drag):
                    self.dragged = t
                    self.selected = t
                    self.track = t.origin
        if(self.dragged == None):
            for e in self.equipment:
                if(e.drag):
                    self.dragged = e
        else:
            self.dragged.update(interact, board)
            if(self.dragged.drag == False):
                if(self.dragged.loc == None):
                    if(isinstance(self.dragged, Ground_Piece)):
                        self.troops.remove(self.dragged)
                    elif(isinstance(self.dragged, Equipment)):
                        self.equipment.remove(self.dragged)
                elif(self.track != self.dragged.loc):
                    self.move_made = True
                    self.track = None
                self.dragged = None

    def blitme(self, board):
        for e in self.equipment:
            e.blitme(board, self.color)
        for t in self.troops:
            t.blitme(board, self.color)
        if((self.selected != None)and(self.locked == True)):
            self.selected.disp_locs(board)



#######################################################################
class Check_Team(object):
    def __init__(self, user):
        self.user = user
        self.color = user.color
        self.troops = []
        self.locked = False
        self.dragged = None
        self.move_made = False
        self.track = None

    def set_check(self, screen, top, enemy):
        for z in range(12):
            y = z / 4
            x = z - (4*y)
            if (top):
                x = (2*x) + (y%2)
                y += 5
            else:
                x = (2*x) + ((y+1)%2)
        self.troops.append(Check_Piece(screen, (x,y), top, self, enemy))

    def dormant(self):
        for t in self.troops:
            t.dormant()

    def active(self):
        for t in self.troops:
            t.active()

    def get_amount(self, rank):
        temp = 0
        for t in self.troops:
            if(t.rank == rank):
                temp += 1
        return temp

    def get_jumpers(self, board):
        jumps = []
        for t in self.troops:
            if(t.jump_av):
                jumps.append(t)
        return jumps

    def get_piece(self, loc):
        p = None
        for t in self.troops:
            if(loc == t.loc):
                p = t
        return p

    def update(self, interact, board):
        mouse_pos = interact[7]
        click = interact[0]
        jump = self.get_jumpers(board)
        if(self.dragged == None):
            for t in self.troops:
                t.update(interact, board, self)
                if(t.drag):
                    self.dragged = t
                    self.track = t.origin
        else:
            if((len(jump) > 0)and(self.dragged not in jump)):
                self.dragged = None
            else:
                self.dragged.update(interact, board, self)
                if(self.dragged.drag == False):
                    if(self.dragged.loc == None):
                        self.troops.remove(self.dragged)
                    elif(self.track != self.dragged.loc):
                        self.move_made = True
                        self.track = None
                    self.dragged = None

    def blitme(self, board):
        for t in self.troops:
            t.blitme(board, self.color)
        if(self.dragged != None):
            self.dragged.disp_locs(board)
