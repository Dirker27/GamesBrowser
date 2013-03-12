import pygame
from pygame.sprite import Sprite

class Strat_Piece(Sprite):
    def __init__(self, screen, rank, loc, friendly, enemy):
        self.rank = rank    # Integer indicating rank
                            # 0: Bomb
                            # 1: Spy
                            # 2: Scout
                            # 3: Miner
                            # 4: Sergeant
                            # 5: Lieutenant
                            # 6: Captain
                            # 7: Major
                            # 8: Colonel
                            # 9: General
                            # 10: Marshal
                            # 11: Flag
        self.loc = loc
        self.pos = (0,0)
        self.friendly = friendly
        self.enemy = enemy
        self.screen = screen
        self.front_image = None
        self.get_image()
        self.back_image = pygame.image.load('images//strat_back.png')
        self.image = self.front_image
        self.image_w, self.image_h = self.image.get_size()
        self.drag = False
        self.origin = loc

    def hover(self, position):
        if((self.pos[0] - (self.image_w/2) < position[0])and
           (self.pos[0] + (self.image_w/2) > position[0])):
            if((self.pos[1] - (self.image_h/2) < position[1])and
               (self.pos[1] + (self.image_h/2) > position[1])):
                return True
            else:
                return False
        else:
            return False

    def reveal(self):
        self.back_image = self.front_image
        self.active()

    def active(self):
        self.image = self.front_image
        self.image_w, self.image_h = self.image.get_size()

    def dormant(self):
        self.image = self.back_image
        self.image_w, self.image_h = self.image.get_size()

    def get_image(self):
        if(self.rank == 0):
            self.front_image = pygame.image.load('images//bomb.png')
        elif(self.rank == 1):
            self.front_image = pygame.image.load('images//spy.png')
        elif(self.rank == 2):
            self.front_image = pygame.image.load('images//scout.png')
        elif(self.rank == 3):
            self.front_image = pygame.image.load('images//miner.png')
        elif(self.rank == 4):
            self.front_image = pygame.image.load('images//sergeant.png')
        elif(self.rank == 5):
            self.front_image = pygame.image.load('images//lieutenant.png')
        elif(self.rank == 6):
            self.front_image = pygame.image.load('images//captain.png')
        elif(self.rank == 7):
            self.front_image = pygame.image.load('images//major1.png')
        elif(self.rank == 8):
            self.front_image = pygame.image.load('images//colonel.png')
        elif(self.rank == 9):
            self.front_image = pygame.image.load('images//general1.png')
        elif(self.rank == 10):
            self.front_image = pygame.image.load('images//marshal.png')
        elif(self.rank == 11):
            self.front_image = pygame.image.load('images//flag.png')

    def can_move(self):
        res = True
        if(self.friendly.locked):
            if(self.loc != None):
                if((self.rank == 0)or(self.rank == 11)):
                    res = False
        return res

    def is_valid_loc(self, loc, board):
        res = True
        if(self.origin != None):
            if(loc not in self.valid_locs(board)):
                res = False
        return res

    def valid_locs(self, board):
        res = []
        if(self.rank == 2):
            forward = True
            back = True
            left = True
            right = True
            c = 0

            while((forward)or(back)or(left)or(right)):
                if(forward):
                    temp = (self.origin[0], self.origin[1] + c)
                    if((self.friendly.get_piece(temp) == None)and(board.get_space1(temp[0], temp[1]) != None)):
                        res.append(temp)

                        if(self.enemy.get_piece(temp) != None):
                            forward = False
                    else:
                        forward = False
                if(back):
                    temp = (self.origin[0], self.origin[1] - c)
                    if((self.friendly.get_piece(temp) == None)and(board.get_space1(temp[0], temp[1]) != None)):
                        res.append(temp)

                        if(self.enemy.get_piece(temp) != None):
                            back = False
                    else:
                        back = False
                if(left):
                    temp = (self.origin[0] - c, self.origin[1])
                    if((self.friendly.get_piece(temp) == None)and(board.get_space1(temp[0], temp[1]) != None)):
                        res.append(temp)

                        if(self.enemy.get_piece(temp) != None):
                            left = False
                    else:
                        left = False
                if(right):
                    temp = (self.origin[0] + c, self.origin[1])
                    if((self.friendly.get_piece(temp) == None)and(board.get_space1(temp[0], temp[1]) != None)):
                        res.append(temp)

                        if(self.enemy.get_piece(temp) != None):
                            right = False
                    else:
                        right = False
                c+=1
                
        else:
            temp = (self.origin[0] + 1, self.origin[1])
            if((self.friendly.get_piece(temp) == None)and(board.get_space1(temp[0], temp[1]) != None)):
                res.append(temp)
            temp = (self.origin[0] - 1, self.origin[1])
            if((self.friendly.get_piece(temp) == None)and(board.get_space1(temp[0], temp[1]) != None)):
                res.append(temp)
            temp = (self.origin[0], self.origin[1] + 1)
            if((self.friendly.get_piece(temp) == None)and(board.get_space1(temp[0], temp[1]) != None)):
                res.append(temp)
            temp = (self.origin[0], self.origin[1] - 1)
            if((self.friendly.get_piece(temp) == None)and(board.get_space1(temp[0], temp[1]) != None)):
                res.append(temp)
                
        return res

    def disp_locs(self, board):
        if(self.origin != None):
            dark = pygame.Surface((50, 50))
            mark = pygame.Surface((50, 50))
            dark.fill((0, 0, 0))
            mark.fill((250, 0, 0))
            dark.set_alpha(75)
            mark.set_alpha(75)

            valid = self.valid_locs(board)

            for s in board.spaces:
                if(s.loc in valid):
                    if(self.enemy.get_piece(s.loc) != None):
                        draw_pos = (s.pos[0] - 25, s.pos[1] - 25)
                        self.screen.blit(mark, draw_pos)
                else:
                    draw_pos = (s.pos[0] - 25, s.pos[1] - 25)
                    self.screen.blit(dark, draw_pos)

    def update(self, interact, board):
        mouse_pos = interact[7]
        click = interact[0]
        if(self.drag):
            if(click):
                self.pos = mouse_pos
            else:
                self.drag = False
                
                b_loc = board.get_space2(self.pos)
                if(b_loc == None):
                    self.loc = self.origin
                else:
                    if((self.friendly.locked == False)or
                       (self.is_valid_loc(b_loc.loc, board))):
                        self.loc = b_loc.loc
                        self.origin = self.loc
                    else:
                        self.loc = self.origin
        else:
            if(self.hover(mouse_pos)):
                if(click):
                    if(self.can_move()):
                        self.drag = True
                        self.loc = None
                

    def blitme(self, b, color):
        bckgrd = pygame.Surface((self.image_w, self.image_h))
        bckgrd.fill(color)
        bckgrd.set_alpha(75)
        if(self.loc != None):
            spot = b.get_space1(self.loc[0], self.loc[1])
            self.pos = spot.pos

        draw_pos = self.image.get_rect().move(self.pos[0]-(self.image_w/2),
                                              self.pos[1]-(self.image_h/2))
        self.screen.blit(bckgrd, draw_pos)
        self.screen.blit(self.image, draw_pos)

#########################################################################


class Ground_Piece(Sprite):
    def __init__(self, screen, rank, loc, friendly, enemy):
        self.rank = rank    # Integer indicating rank
                            # 0: Bomb
                            # 1: Spy
                            # 2: Scout
                            # 3: Miner
                            # 4: Sergeant
                            # 5: Lieutenant
                            # 6: Captain
                            # 7: Major
                            # 8: Colonel
                            # 9: General
                            # 10: Marshal
                            # 11: Flag
        self.loc = loc
        self.pos = (0,0)
        self.friendly = friendly
        self.enemies = enemy
        self.screen = screen
        self.front_image = None
        self.get_image()
        self.back_image = pygame.image.load('images//strat_back.png')
        self.image = self.front_image
        self.image_w, self.image_h = self.image.get_size()
        self.drag = False
        self.origin = loc
        self.stripped = False

    def hover(self, position):
        if((self.pos[0] - (self.image_w/2) < position[0])and
           (self.pos[0] + (self.image_w/2) > position[0])):
            if((self.pos[1] - (self.image_h/2) < position[1])and
               (self.pos[1] + (self.image_h/2) > position[1])):
                return True
            else:
                return False
        else:
            return False

    def reveal(self):
        self.back_image = self.front_image
        self.active()

    def active(self):
        self.image = self.front_image
        self.image_w, self.image_h = self.image.get_size()

    def dormant(self):
        self.image = self.back_image
        self.image_w, self.image_h = self.image.get_size()

    def get_image(self):
        if(self.rank == 1):
            self.front_image = pygame.image.load('images//assassin.png')
        elif(self.rank == 2):
            self.front_image = pygame.image.load('images//scout.png')
        elif(self.rank == 3):
            self.front_image = pygame.image.load('images//engineer.png')
        elif(self.rank == 4):
            self.front_image = pygame.image.load('images//sergeant.png')
        elif(self.rank == 5):
            self.front_image = pygame.image.load('images//warrant_officer.png')
        elif(self.rank == 6):
            self.front_image = pygame.image.load('images//major.png')
        elif(self.rank == 7):
            self.front_image = pygame.image.load('images//general.png')
        elif(self.rank == 8):
            self.front_image = pygame.image.load('images//commander.png')
        elif(self.rank == 11):
            self.front_image = pygame.image.load('images//flag.png')

    def can_move(self):
        res = True
        if(self.friendly.locked):
            if(self.loc != None):
                if((self.rank == 0)or(self.rank == 11)):
                    res = False
        return res

    def trip(self, loc):
        if(self.friendly.locked):
            x_diff = loc[0] - self.origin[0]
            y_diff = loc[1] - self.origin[1]

            i = 0
            t_loc = self.origin
            while(i < abs(x_diff + y_diff)):
                if(x_diff > y_diff):
                    if(x_diff > 0):
                        t_loc = (t_loc[0] + 1, t_loc[1])
                    else:
                        t_loc = (t_loc[0] - 1, t_loc[1])
                else:
                    if(y_diff > 0):
                        t_loc = (t_loc[0], t_loc[1] + 1)
                    else:
                        t_loc = (t_loc[0], t_loc[1] - 1)

                for e in self.enemies:
                    b = e.get_equip(t_loc)
                    if(b != None):
                        if(b.equip == 0):
                            self.loc = t_loc
                            i = abs(x_diff + y_diff)
                        if(b.equip == 1):                            
                            self.loc = t_loc
                            self.stripped = True
                            i = abs(x_diff + y_diff)
                i += 1

    def is_valid_loc(self, loc, board):
        res = True
        if(self.origin != None):
            if(loc not in self.valid_locs(board)):
                res = False
        return res

    def valid_locs(self, board):
        res = []
        if((self.rank == 2)and(self.stripped == False)):
            forward = True
            back = True
            left = True
            right = True
            c = 0

            while((forward)or(back)or(left)or(right)):
                if(forward):
                    temp = (self.origin[0], self.origin[1] + c)
                    if((self.friendly.get_piece(temp) == None)and(board.get_space1(temp[0], temp[1]) != None)):
                        res.append(temp)

                        for e in self.enemies:
                            if(e.get_piece(temp) != None):
                                forward = False
                    else:
                        forward = False
                if(back):
                    temp = (self.origin[0], self.origin[1] - c)
                    if((self.friendly.get_piece(temp) == None)and(board.get_space1(temp[0], temp[1]) != None)):
                        res.append(temp)

                        for e in self.enemies:
                            if(e.get_piece(temp) != None):
                                back = False
                    else:
                        back = False
                if(left):
                    temp = (self.origin[0] - c, self.origin[1])
                    if((self.friendly.get_piece(temp) == None)and(board.get_space1(temp[0], temp[1]) != None)):
                        res.append(temp)

                        for e in self.enemies:
                            if(e.get_piece(temp) != None):
                                left = False
                    else:
                        left = False
                if(right):
                    temp = (self.origin[0] + c, self.origin[1])
                    if((self.friendly.get_piece(temp) == None)and(board.get_space1(temp[0], temp[1]) != None)):
                        res.append(temp)

                        for e in self.enemies:
                            if(e.get_piece(temp) != None):
                                right = False
                    else:
                        right = False
                c+=1
                
        else:
            temp = (self.origin[0] + 1, self.origin[1])
            if((self.friendly.get_piece(temp) == None)and(board.get_space1(temp[0], temp[1]) != None)):
                res.append(temp)
            temp = (self.origin[0] - 1, self.origin[1])
            if((self.friendly.get_piece(temp) == None)and(board.get_space1(temp[0], temp[1]) != None)):
                res.append(temp)
            temp = (self.origin[0], self.origin[1] + 1)
            if((self.friendly.get_piece(temp) == None)and(board.get_space1(temp[0], temp[1]) != None)):
                res.append(temp)
            temp = (self.origin[0], self.origin[1] - 1)
            if((self.friendly.get_piece(temp) == None)and(board.get_space1(temp[0], temp[1]) != None)):
                res.append(temp)

            if(self.rank == 1):
                temp = (self.origin[0] + 1, self.origin[1] + 1)
                if((self.friendly.get_piece(temp) == None)and(board.get_space1(temp[0], temp[1]) != None)):
                    res.append(temp)
                temp = (self.origin[0] - 1, self.origin[1] - 1)
                if((self.friendly.get_piece(temp) == None)and(board.get_space1(temp[0], temp[1]) != None)):
                    res.append(temp)
                temp = (self.origin[0] - 1, self.origin[1] + 1)
                if((self.friendly.get_piece(temp) == None)and(board.get_space1(temp[0], temp[1]) != None)):
                    res.append(temp)
                temp = (self.origin[0] + 1, self.origin[1] - 1)
                if((self.friendly.get_piece(temp) == None)and(board.get_space1(temp[0], temp[1]) != None)):
                    res.append(temp)              
        return res

    def disp_locs(self, board):
        if(self.origin != None):
            dark = pygame.Surface((50, 50))
            mark = pygame.Surface((50, 50))
            dark.fill((0, 0, 0))
            mark.fill((250, 0, 0))
            dark.set_alpha(75)
            mark.set_alpha(75)

            valid = self.valid_locs(board)

            for s in board.spaces:
                if(s.loc in valid):
                    for e in self.enemies:
                        if(e.get_piece(s.loc) != None):
                            draw_pos = (s.pos[0] - 25, s.pos[1] - 25)
                            self.screen.blit(mark, draw_pos)
                else:
                    draw_pos = (s.pos[0] - 25, s.pos[1] - 25)
                    self.screen.blit(dark, draw_pos)

    def update(self, interact, board):
        mouse_pos = interact[7]
        click = interact[0]
        if(self.drag):
            if(click):
                self.pos = mouse_pos
            else:
                self.drag = False
                
                b_loc = board.get_space2(self.pos)
                if(b_loc == None):
                    self.loc = self.origin
                else:
                    if((self.friendly.locked == False)or
                       (self.is_valid_loc(b_loc.loc, board))):
                        self.loc = b_loc.loc
                        if((self.rank == 2)and(self.stripped == False)):
                            self.trip(b_loc.loc)
                        self.origin = self.loc
                    else:
                        self.loc = self.origin
        else:
            if(self.hover(mouse_pos)):
                if(click):
                    if(self.can_move()):
                        self.drag = True
                        self.loc = None                

    def blitme(self, b, color):
        bckgrd = pygame.Surface((self.image_w, self.image_h))
        bckgrd.fill(color)
        bckgrd.set_alpha(75)
        if(self.loc != None):
            spot = b.get_space1(self.loc[0], self.loc[1])
            self.pos = spot.pos

        draw_pos = self.image.get_rect().move(self.pos[0]-(self.image_w/2),
                                              self.pos[1]-(self.image_h/2))
        self.screen.blit(bckgrd, draw_pos)
        self.screen.blit(self.image, draw_pos)

        

class Equipment(Sprite):
    def __init__(self, screen, loc, equip, friendly, owner):
        self.screen = screen
        self.loc = loc
        self.equip = equip
        self.pos = (0,0)
        self.friendly = friendly
        self.owner = owner
        self.back_image = pygame.image.load('images//strat_back.png')
        self.front_image = None
        self.get_images()
        self.image = self.front_image
        self.image_w, self.image_h = self.image.get_size()
        self.set = False
        self.drag = True

    def get_images(self):
        if(self.equip == 0):
            self.front_image = pygame.image.load('images//bomb.png')
        elif(self.equip == 1):
            self.front_image = pygame.image.load('images//barb.png')
        elif(self.equip == 2):
            self.front_image = pygame.image.load('images//bunker.png')
        elif(self.equip == 3):
            self.front_image = pygame.image.load('images//toolbox.png')

    def hover(self, position):
        if((self.pos[0] - (self.image_w/2) < position[0])and
           (self.pos[0] + (self.image_w/2) > position[0])):
            if((self.pos[1] - (self.image_h/2) < position[1])and
               (self.pos[1] + (self.image_h/2) > position[1])):
                return True
            else:
                return False
        else:
            return False

    def reveal(self):
        self.back_image = self.front_image
        self.active()
        
    def active(self):
        self.image = self.front_image
        self.image_w, self.image_h = self.image.get_size()

    def dormant(self):
        self.image = self.back_image
        self.image_w, self.image_h = self.image.get_size()

    def is_valid_loc(self, loc, board):
        res = True
        if(loc not in self.valid_locs(board)):
            res = False
        return res

    def valid_locs(self, board):
        spots = []

        temp = (self.owner.loc[0] + 1, self.owner.loc[1] + 1)
        if((self.friendly.get_piece(temp) == None)and(board.get_space1(temp[0], temp[1]) != None)
           and(self.friendly.get_equip(temp) == None)):
            spots.append(temp)

        temp = (self.owner.loc[0] - 1, self.owner.loc[1] - 1)
        if((self.friendly.get_piece(temp) == None)and(board.get_space1(temp[0], temp[1]) != None)
           and(self.friendly.get_equip(temp) == None)):
            spots.append(temp)
            
        temp = (self.owner.loc[0] - 1, self.owner.loc[1] + 1)
        if((self.friendly.get_piece(temp) == None)and(board.get_space1(temp[0], temp[1]) != None)
           and(self.friendly.get_equip(temp) == None)):
            spots.append(temp)

        temp = (self.owner.loc[0] + 1, self.owner.loc[1] - 1)
        if((self.friendly.get_piece(temp) == None)and(board.get_space1(temp[0], temp[1]) != None)
           and(self.friendly.get_equip(temp) == None)):
            spots.append(temp)

        if(self.equip != 0):
            for s in spots:
                val = False
                for e in self.owner.enemies:
                    if(e.get_piece(s) != None):
                        val = True
                if(val):
                    spots.remove(s)

        if(self.equip == 3):
            for s in spots:
                val = False
                for e in self.owner.enemies:
                    if(e.get_equip(s) != None):
                        val = True
                if(val == False):
                    spots.remove(s)

        return spots

    def disp_locs(self, board):
        dark = pygame.Surface((50, 50))
        mark = pygame.Surface((50, 50))
        dark.fill((0, 0, 0))
        mark.fill((250, 0, 0))
        dark.set_alpha(75)
        mark.set_alpha(75)

        valid = self.valid_locs(board)

        for s in board.spaces:
            if(s.loc in valid):
                pass
            else:
                draw_pos = (s.pos[0] - 25, s.pos[1] - 25)
                self.screen.blit(dark, draw_pos)        

    def update(self, interact, board):
        if(self.set == False):
            mouse_pos = interact[7]
            click = interact[0]
            if(self.drag):
                if(click):
                    self.pos = mouse_pos
                else:
                    self.drag = False
                    
                    b_loc = board.get_space2(self.pos)
                    if(b_loc == None):
                        pass
                    else:
                        if(b_loc.loc in self.valid_locs(board)):
                            self.loc = b_loc.loc
                        else:
                            pass
            else:
                if(self.hover(mouse_pos)):
                    if(click):
                        self.drag = True
                        self.loc = None

    def blitme(self, b, color):
        bckgrd = pygame.Surface((self.image_w, self.image_h))
        bckgrd.fill(color)
        bckgrd.set_alpha(75)
        if(self.loc != None):
            spot = b.get_space1(self.loc[0], self.loc[1])
            self.pos = spot.pos

        draw_pos = self.image.get_rect().move(self.pos[0]-(self.image_w/2),
                                              self.pos[1]-(self.image_h/2))
        self.screen.blit(bckgrd, draw_pos)
        self.screen.blit(self.image, draw_pos)
        


class Check_Piece(Sprite):
    def __init__(self, screen, loc, top, friendly, enemy):
        self.loc = loc
        self.top = top
        self.pos = (0,0)
        self.screen = screen
        self.friendly = friendly
        self.enemy = enemy
        self.king = False
        self.back = False
        self.start_image = pygame.image.load('images//bomb.png')
        self.king_image = pygame.image.load('images//flag.png')
        self.image = self.start_image
        self.image_w, self.image_h = self.image.get_size()
        self.drag = False
        self.origin = loc
        self.jump_av = False

    def hover(self, position):
        if((self.pos[0] - (self.image_w/2) < position[0])and
           (self.pos[0] + (self.image_w/2) > position[0])):
            if((self.pos[1] - (self.image_h/2) < position[1])and
               (self.pos[1] + (self.image_h/2) > position[1])):
                return True
            else:
                return False
        else:
            return False

    def active(self):
        self.back = True

    def dormant(self):
        self.back = False

    def disp_locs(self, board):
        if(self.origin != None):
            dark = pygame.Surface((50, 50))
            mark = pygame.Surface((50, 50))
            dark.fill((0, 0, 0))
            mark.fill((250, 0, 0))
            dark.set_alpha(75)
            mark.set_alpha(75)

            valid = self.valid_moves(board)
            jumps = self.valid_jumps(board)

            for s in board.spaces:
                if(s.loc in valid):
                    pass
                elif(s.loc in jumps):
                    pass
                else:
                    draw_pos = (s.pos[0] - 25, s.pos[1] - 25)
                    self.screen.blit(dark, draw_pos)

    def king_me(self):
        if(self.top):
            if(self.loc[1] == 0):
                self.king = True
                self.image = self.king_image
        else:
            if(self.loc[1] == 7):
                self.king = True
                self.image = self.king_image

    def is_valid_loc(self, loc, board):
        res = True
        if(self.origin != None):
            if(loc not in self.valid_moves(board)):
                res = False
        return res

    def valid_moves(self, board):
        spots = []

        if((self.top == False)or(self.king)):
            temp = (self.origin[0] + 1, self.origin[1] + 1)
            if(board.get_space1(temp[0], temp[1]) != None):
                spots.append(temp)

            temp = (self.origin[0] - 1, self.origin[1] + 1)
            if(board.get_space1(temp[0], temp[1]) != None):
                spots.append(temp)

        if((self.top)or(self.king)):
            temp = (self.origin[0] - 1, self.origin[1] - 1)
            if(board.get_space1(temp[0], temp[1]) != None):
                spots.append(temp)
                
            temp = (self.origin[0] + 1, self.origin[1] - 1)
            if(board.get_space1(temp[0], temp[1]) != None):
                spots.append(temp)

        for s in spots:
            if((self.friendly.get_piece(s)!=None)or(self.enemy.get_piece(s)!=None)):
                spots.remove(s)

        return spots

    def valid_jumps(self, board):
        jumps = []

        if((self.top == False)or(self.king)):
            temp = (self.origin[0] + 1, self.origin[1] + 1)
            if(self.enemy.get_piece(temp) != None):
                jumps.append(temp)

            temp = (self.origin[0] - 1, self.origin[1] + 1)
            if(self.enemy.get_piece(temp) != None):
                jumps.append(temp)

        if((self.top)or(self.king)):
            temp = (self.origin[0] - 1, self.origin[1] - 1)
            if(self.enemy.get_piece(temp) != None):
                jumps.append(temp)
                
            temp = (self.origin[0] + 1, self.origin[1] - 1)
            if(self.enemy.get_piece(temp) != None):
                jumps.append(temp)

        for j in jumps:
            x_diff = self.origin[0] - j[0]
            y_diff = self.origin[1] - j[1]

            temp = (self.origin[0] - (x_diff*2), self.origin[1] - (y_diff*2))
            if((self.friendly.get_piece(temp)!=None)or(self.enemy.get_piece(temp)!=None)
               or(board.get_space1(temp[0], temp[1])==None)):
                jumps.remove(j)

        return(jumps)

    def jump(self, loc):
        x_diff = self.origin[0] - loc[0]
        y_diff = self.origin[1] - loc[1]
        e = self.enemy.get_piece(loc)
        new_pos = (self.origin[0] - (x_diff*2), self.origin[1] - (y_diff*2))

        self.enemy.troops.remove(e)
        self.loc = new_pos
        self.origin = self.loc
                 
    def update(self, interact, board, friendly):
        mouse_pos = interact[7]
        click = interact[0]
        if(self.drag):
            if(click):
                self.pos = mouse_pos
            else:
                self.drag = False
                
                b_loc = board.get_space2(self.pos)
                if(b_loc == None):
                    self.loc = self.origin
                else:
                    if(self.is_valid_loc(b_loc.loc, board)):
                        self.loc = b_loc.loc
                        self.origin = self.loc
                    elif(b_loc.loc in self.valid_jumps(board)):
                        self.jump(b_loc.loc)
                    else:
                        self.loc = self.origin
        else:
            if(self.hover(mouse_pos)):
                if(click):
                    self.drag = True
                    self.loc = None

        if(self.loc!=None):
            self.king_me()
                

    def blitme(self, b, color):
        draw_pos = self.image.get_rect().move(self.pos[0]-(self.image_w/2),
                                              self.pos[1]-(self.image_h/2))
        if(self.back):
            t_pos = (draw_pos[0]+2, draw_pos[1]+2)
            bckgrd = pygame.Surface((self.image_w-4, self.image_h-4))
            bckgrd.fill(color)
            #bckgrd.set_alpha(75)
            self.screen.blit(bckgrd, t_pos)
            
        if(self.loc != None):
            spot = b.get_space1(self.loc[0], self.loc[1])
            self.pos = spot.pos

        self.screen.blit(self.image, draw_pos)
