import pygame

from Piece import *
from Team import *
from Board import *
from Setup import *

from random import choice

class Stratego(object):

    def __init__(self, screen, size, users, end):
        self.screen = screen
        self.size = size
        self.users = users
        self.teamA = Strat_Team(users[0])
        self.teamB = Strat_Team(users[1])
        self.active_team = self.teamA
        self.dormant_team = self.teamB
        self.winner = None
        self.phase = None
        self.width = size[0]
        self.height = size[1]
        self.board = Board(self.screen, (self.width/2, self.height/2), "Stratego")
        self.bars = []
        self.buttons = []
        self.doors = None
        self.end = end

        '''self.teamB.troops.append(Strat_Piece(screen, 11, (9,9)))
        self.teamB.troops.append(Strat_Piece(screen, 0, (8,9)))'''

        self.active_team.active()
        self.dormant_team.dormant()

        self.bars.append(Acc_Bar(self.screen, (self.width - 150, self.height - 75), self.active_team.user))

    def swap_teams(self):
        temp = self.active_team
        self.active_team = self.dormant_team
        self.dormant_team = temp

        self.active_team.active()
        self.dormant_team.dormant()

        self.disp_user()

    def make_piece(self, rank):
        if(self.valid_piece(rank, self.active_team)):
            x = len(self.active_team.troops)
            self.active_team.troops.append(
                Strat_Piece(self.screen, rank, None, self.active_team, self.dormant_team))
            self.active_team.troops[x].drag = True
            self.active_team.troops[x].pos = pygame.mouse.get_pos()

    def disp_user(self):
        x = 1
        num = 1
        for u in self.users:
            if(u == self.active_team.user):
                num = x
            x += 1

        a = 0
        b = 0
        if((num == 2)or(num == 3)):
            a = 150
        else:
            a = self.width - 150

        if((num == 2)or(num == 4)):
            b = 95
        else:
            b = self.height - 75

        self.bars[0] = Acc_Bar(self.screen, (a,b), self.active_team.user)

    def valid_piece(self, rank, team):
        res = True
        if(rank == 0):
            if(team.get_amount(rank) >= 6):
                res = False
        elif(rank == 1):
            if(team.get_amount(rank) >= 1):
                res = False
        elif(rank == 2):
            if(team.get_amount(rank) >= 8):
                res = False
        elif(rank == 3):
            if(team.get_amount(rank) >= 5):
                res = False
        elif(rank == 4):
            if(team.get_amount(rank) >= 1):
                res = False
        elif(rank == 5):
            if(team.get_amount(rank) >= 1):
                res = False
        elif(rank == 6):
            if(team.get_amount(rank) >= 1):
                res = False
        elif(rank == 7):
            if(team.get_amount(rank) >= 4):
                res = False
        elif(rank == 8):
            if(team.get_amount(rank) >= 3):
                res = False
        elif(rank == 9):
            if(team.get_amount(rank) >= 2):
                res = False
        elif(rank == 10):
            if(team.get_amount(rank) >= 1):
                res = False
        elif(rank == 11):
            if(team.get_amount(rank) >= 1):
                res = False
        return res

    def preset(self):
        if(self.active_team == self.teamA):
            num = 0
        else:
            num = 1
        self.active_team.troops = []
        temp = GW_Preset(self.screen, self.active_team, self.dormant_team, num)
        for t in temp:
            self.active_team.troops.append(t)
        self.set_team()

    def win(self, winner):
        for u in self.users:
            if(u == winner):
                u.win()
            else:
                u.lose()
                winner.inventory.append(u.dog_tag)
        self.end()

    def setit(self):
        self.doors.split()
        self.swap_teams()

    def set_team(self):
        if(self.active_team.strat_set()):
            self.active_team.locked = True
            self.swap_teams()
        if((self.active_team.locked)and(self.dormant_team.locked)):
            self.phase += 1
            self.active_team.move_made = False
            self.dormant_team.move_made = False
            self.bars.remove(self.bars[len(self.bars)-1])
            self.buttons = []

    def game_phase(self):
        if(self.phase == None):
            events = [self.make_piece, self.set_team, self.preset]
            temp = S_Piece_set(self.screen, self.size, events)
            for t in temp[0]:
                self.bars.append(t)
            for t in temp[1]:
                self.buttons.append(t)
            self.phase = 0
            self.doors = grande_door(self.screen, self.size, self.setit)
            
        if(self.phase == 0):
            for t in self.teamA.troops:
                if(t.loc != None):
                    if(t.loc[1] > 3):
                        self.teamA.troops.remove(t)
            for t in self.teamB.troops:
                if(t.loc != None):
                    if(t.loc[1] < 6):
                        self.teamB.troops.remove(t)

        if(self.phase == 1):
            if(self.dormant_team.get_amount(11) == 0):
                self.win(self.active_team.user)
            elif(self.active_team.get_amount(11) == 0):
                self.win(self.dormant_team.user)
            elif(self.active_team.move_made):
                self.active_team.move_made = False
                self.doors.close()
                #self.swap_teams()
            
            
                
    def conflict(self):
        for a in self.teamA.troops:
            b = self.teamB.get_piece(a.loc)
            if(b != None):
                a.reveal()
                b.reveal()
                
                victor = None
                if(a.rank > b.rank):
                    t_list = (b, a)
                else:
                    t_list = (a, b)
                
                if((t_list[0].rank == 0)and(t_list[1].rank != 3)):
                    victor = t_list[0]
                elif(t_list[1].rank == 11):
                    victor = t_list[0]
                elif((t_list[0].rank == 1)and(t_list[1].rank == 10)):
                    victor = t_list[0]
                elif(t_list[0].rank != t_list[1].rank):
                    victor = t_list[1]

                if(victor == a):
                    self.teamB.troops.remove(b)
                elif(victor == b):
                    self.teamA.troops.remove(a)
                else:
                    self.teamA.troops.remove(a)
                    self.teamB.troops.remove(b)

    def update(self, interact):
        mouse_pos = interact[7]
        click = interact[0]
        self.board.update(interact)
        self.active_team.update(interact, self.board)
        self.game_phase()
        self.conflict()

        for b in self.buttons:
            b.update(interact)
        for b in self.bars:
            b.update(interact)

        self.doors.update(interact)

    def blitme(self):
        self.board.blitme()
        self.dormant_team.blitme(self.board)
        self.active_team.blitme(self.board)
        
        for b in self.buttons:
            b.blitme()
        for b in self.bars:
            b.blitme()

        if(self.active_team.dragged != None):
            self.active_team.dragged.blitme(self.board, self.active_team.color)

        if((self.doors.right.move)or(self.doors.is_closed())):
            self.doors.blitme()



class Ground_War(object):
    def __init__(self, screen, size, users, end):
        self.screen = screen
        self.size = size
        self.winner = None
        self.phase = None
        self.width = size[0]
        self.height = size[1]
        self.board = Board(self.screen, (self.width/2, self.height/2), "Ground_War")
        self.bars = []
        self.buttons = []
        self.board_drag = False
        self.deploy = None
        self.users = users
        self.doors = None
        self.end = end
        

        self.teams = []
        for u in self.users:
            self.teams.append(Ground_Team(u))
        self.active_team = self.teams[0]
        self.dormant_teams = []
        
        for t in self.teams:
            if(t != self.active_team):
                t.dormant()
                self.dormant_teams.append(t)
            t.LKBP = self.board.pos
        self.active_team.active()
        self.bars.append(Acc_Bar(self.screen, (self.width - 150, self.height - 75), self.active_team.user))

    def disp_user(self):
        x = 1
        num = 1
        for u in self.users:
            if(u == self.active_team.user):
                num = x
            x += 1

        a = 0
        b = 0
        if((num == 2)or(num == 3)):
            a = 150
        else:
            a = self.width - 150

        if((num == 2)or(num == 4)):
            b = 95
        else:
            b = self.height - 75

        self.bars[0] = Acc_Bar(self.screen, (a,b), self.active_team.user)      
        
    def swap_teams(self):
        if(self.deploy != None):
            self.deploy = None
            l = len(self.bars)-1
            self.bars.remove(self.bars[l])
        self.active_team.selected = None

        temp = 0
        i = 0
        for t in self.teams:
            if(t == self.active_team):
                temp = i
            i += 1

        if(temp == len(self.teams)-1):
            self.active_team = self.teams[0]
        else:
            self.active_team = self.teams[temp+1]

        self.dormant_teams = []
        for t in self.teams:
            if(t != self.active_team):
                t.dormant()
                self.dormant_teams.append(t)
        self.active_team.active()
        self.board.pos = self.active_team.LKBP

        self.disp_user()
                

    def make_piece(self, rank):
        if(self.valid_piece(rank, self.active_team)):
            x = len(self.active_team.troops)
            self.active_team.troops.append(
                Ground_Piece(self.screen, rank, None, self.active_team, self.dormant_teams))
            self.active_team.troops[x].drag = True
            self.active_team.troops[x].pos = pygame.mouse.get_pos()

    def valid_piece(self, rank, team):
        res = True
        grunt = 0
        for i in range(4):
            grunt += team.get_amount(i + 1)
            
        if(rank == 1):
            if((grunt >= 26) or (team.get_amount(rank) >= 13)):
                res = False
        elif(rank == 2):
            if((grunt >= 26) or (team.get_amount(rank) >= 13)):
                res = False
        elif((grunt >= 26) or (team.get_amount(rank) >= 13)):
            if(team.get_amount(rank) >= 5):
                res = False
        elif((grunt >= 26) or (team.get_amount(rank) >= 13)):
            if(team.get_amount(rank) >= 1):
                res = False
        elif(rank == 5):
            if(team.get_amount(rank) >= 8):
                res = False
        elif(rank == 6):
            if(team.get_amount(rank) >= 2):
                res = False
        elif(rank == 7):
            if(team.get_amount(rank) >= 2):
                res = False
        elif(rank == 8):
            if(team.get_amount(rank) >= 1):
                res = False
        elif(rank == 11):
            if(team.get_amount(rank) >= 1):
                res = False
        return res

    def move_board(self, click, pos):
        if(self.board_drag == False):
            if(self.board.hover(pos)):
                if((click)and(self.active_team.dragged == None)):
                    move = True
                    for s in self.board.spaces:
                        if(s.hover(pos)):
                            move = False
                    if(move):
                        self.board_drag = True                        
        else:
            if(click):
                self.board.pos = pos
                self.active_team.LKBP = pos
                '''x_diff = self.dragged.pos[0] - pos[0]
                y_diff = self.dragged.pos[1] - pos[1]
                self.board.pos = (self.board.pos[0] - x_diff,
                self.board.pos[1] - y_diff)'''
            else:
                self.board_drag = False

    def deploy_equip(self):
        if((self.active_team.locked)and(self.active_team.selected != None)):
            if(self.deploy !=  None):                
                if(self.active_team.selected != self.deploy):
                    self.deploy = None
                    self.bars.remove(self.bars[len(self.bars)-1])

            elif(isinstance(self.active_team.selected, Ground_Piece)):
                if(self.active_team.selected.rank == 3):
                    self.deploy = self.active_team.selected
                    self.bars.append(equip_set(self.screen, self.size, [self.make_equip]))

    def make_equip(self, rank):
        equip = Equipment(self.screen, None, rank, self.active_team, self.active_team.selected)
        self.active_team.equipment.append(equip)
        self.active_team.selected = equip
        self.active_team.dragged = equip

    def preset(self):
        num = 0
        x = 0
        for t in self.teams:
            if(t == self.active_team):
                num = x
            x += 1
        self.active_team.troops = []
        temp = GW_Preset(self.screen, self.active_team, self.dormant_teams, num)
        for t in temp:
            self.active_team.troops.append(t)
        self.set_team()
    
    def set_team(self):
        if(self.active_team.strat_set()):
            self.active_team.locked = True
            self.swap_teams()

        all_set = True
        for t in self.teams:
            if(t.locked == False):
                all_set = False
        if(all_set):
            self.phase += 1
            self.active_team.move_made = False
            for d in self.dormant_teams:
                d.move_made = False
            self.bars.remove(self.bars[len(self.bars)-1])
            self.buttons = []

    def capture(self, win, lose):
        for t in lose.troops:
            win.troops.append(t)
        for e in lose.equipment:
            win.equipment.append(e)
        self.teams.remove(lose)
        self.dormant_teams.remove(lose)
        
    def setit(self):
        self.doors.split()
        self.swap_teams()

    def game_phase(self):
        if(self.phase == None):
            events = [self.make_piece, self.set_team, self.preset]
            temp = GW_Piece_set(self.screen, self.size, events)
            for t in temp[0]:
                self.bars.append(t)
            for t in temp[1]:
                self.buttons.append(t)
            self.phase = 0
            self.doors = grande_door(self.screen, self.size, self.setit)
            
        if(self.phase == 0):
            for t in self.teams[0].troops:
                if(t.loc != None):
                    if(t.loc[1] > 3):
                        self.teams[0].troops.remove(t)
            for t in self.teams[1].troops:
                if(t.loc != None):
                    if(t.loc[1] < 6):
                        self.teams[0].troops.remove(t)

        if(self.phase == 1):
            if(self.active_team.move_made):
                self.active_team.move_made = False
                self.doors.close()
                #self.swap_teams()
                if(len(self.teams) == 1):
                    self.win()
                    self.phase+=1

        if(self.phase == 2):
            self.end()
            
                
    def conflict(self):
        for e in self.active_team.equipment:
            for d in self.dormant_teams:
                b = d.get_equip(e.loc)
                if(b != None):
                    if(e.equip == 3):
                        self.active_team.equipment.remove(e)
                        d.equipment.remove(b)
                    if(e.equip == 0):
                        self.active_team.equipment.remove(e)
                        d.equipment.remove(b)   
     
        for a in self.active_team.troops:
            for d in self.dormant_teams:
                b = d.get_piece(a.loc)
                if(b != None):
                    a.reveal()
                    b.reveal()
                    victor = None

                    if(a.rank > b.rank):
                        e = d.get_equip(b.loc)
                        if((e != None)and(e.equip == 2)):
                            r = b.rank + 3
                            if(a.rank < r):
                                victor = b
                            else:
                                victor = a
                        else:
                            victor = a
                            
                    elif(a.rank < b.rank):
                        if(b.rank == 11):
                            victor = a
                        else:
                            victor = b

                    if(a.rank == 1):
                        if(b.rank > 4):
                            victor = a
                            
                    if(victor == a):
                        d.troops.remove(b)
                        if(b.rank == 11):
                            self.capture(self.active_team, d)
                    elif(victor == b):
                        self.active_team.troops.remove(a)
                    else:
                        self.active_team.troops.remove(a)
                        d.troops.remove(b)

                e = d.get_equip(a.loc)
                if(e != None):
                    a.reveal()
                    e.reveal()
                    if(e.equip == 0):
                        self.active_team.troops.remove(a)
                        d.equipment.remove(e)

    def win(self):
        winner = self.teams[0].user

        for u in self.users:
            if(u == winner):
                u.win()
            else:
                u.lose()
                winner.inventory.append(u.dog_tag)

    def update(self, interact):
        mouse_pos = interact[7]
        click = interact[0]
        right_click = interact[1]
        mid_click = interact[2]

        for b in self.buttons:
            b.update(interact)
        for b in self.bars:
            b.update(interact)

        self.board.update(interact)
        if(self.board_drag == False):
            self.active_team.update(interact, self.board)
            self.conflict()
            self.game_phase()
            self.deploy_equip()
        self.move_board(right_click, mouse_pos)
        self.doors.update(interact)

    def blitme(self):
        self.board.blitme()
        for d in self.dormant_teams:
            d.blitme(self.board)
        self.active_team.blitme(self.board)

        for b in self.buttons:
            b.blitme()
        for b in self.bars:
            b.blitme()            

        if(self.active_team.dragged != None):
            self.active_team.dragged.blitme(self.board, self.active_team.color)

        if((self.doors.right.move)or(self.doors.is_closed())):
            self.doors.blitme()



class Checkers(object):
    def __init__(self, screen, size, users, end):
        self.screen = screen
        self.size = size
        self.users = users
        self.teamA = Check_Team(users[0])
        self.teamB = Check_Team(users[1])
        self.active_team = self.teamA
        self.dormant_team = self.teamB
        self.active_team.set_check(self.screen, False, self.dormant_team)
        self.dormant_team.set_check(self.screen, True, self.active_team)
        self.active_team.active()
        self.dormant_team.dormant()
        self.winner = None
        self.phase = None
        self.width = size[0]
        self.height = size[1]
        self.board = Board(self.screen, (self.width/2, self.height/2), "Checkers")
        self.bars = []
        self.buttons = []
        self.end = end

        self.bars.append(Acc_Bar(self.screen, (self.width - 150, self.height - 75), self.active_team.user))

    def swap_teams(self):
        temp = self.active_team
        self.active_team = self.dormant_team
        self.dormant_team = temp

        self.active_team.active()
        self.dormant_team.dormant()

        self.disp_user()

    def disp_user(self):
        x = 1
        num = 1
        for u in self.users:
            if(u == self.active_team.user):
                num = x
            x += 1

        a = 0
        b = 0
        if((num == 2)or(num == 3)):
            a = 150
        else:
            a = self.width - 150

        if((num == 2)or(num == 4)):
            b = 95
        else:
            b = self.height - 75

        self.bars[0] = Acc_Bar(self.screen, (a,b), self.active_team.user)

    def win(self, winner):
        for u in self.users:
            if(u == winner):
                u.win()
            else:
                u.lose()
                winner.inventory.append(u.dog_tag)
        self.end()

    def update(self, interact):
        mouse_pos = interact[7]
        click = interact[0]
        self.board.update(interact)
        self.active_team.update(interact, self.board)
        if(self.active_team.move_made):
            self.active_team.move_made = False
            self.swap_teams()

        for b in self.buttons:
            b.update(interact)
        for b in self.bars:
            b.update(interact)

        if(len(self.active_team.troops) == 0):
            self.win(self.dormant_team.user)
        elif(len(self.dormant_team.troops) == 0):
            self.win(self.active_team.user)

    def blitme(self):
        self.board.blitme()
        self.dormant_team.blitme(self.board)
        
        for b in self.buttons:
            b.blitme()
        for b in self.bars:
            b.blitme()

        self.active_team.blitme(self.board)
