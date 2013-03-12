import pygame
from pygame.sprite import Sprite

class Board(object):
    def __init__(self, screen, init_pos, gametype):
        self.screen = screen
        self.pos = init_pos
        self.gametype = gametype

        if(self.gametype == "Stratego"):
            self.WIDTH = 10
            self.HEIGHT = 10
            self.backdrop = pygame.image.load('images//strat_board.png')
            self.backdrop_w, self.backdrop_h = self.backdrop.get_size()
        elif(self.gametype == "Checkers"):
            self.WIDTH = 8
            self.HEIGHT = 8
            self.backdrop = pygame.image.load('images//check_board.png')
            self.backdrop_w, self.backdrop_h = self.backdrop.get_size()
        elif(self.gametype == "Chess"):
            self.WIDTH = 8
            self.HEIGHT = 8
            self.backdrop = pygame.image.load('images//chess_board.png')
            self.backdrop_w, self.backdrop_h = self.backdrop.get_size()
        elif(self.gametype == "Ground_War"):
            self.WIDTH = 18
            self.HEIGHT = 18
            self.backdrop = pygame.image.load('images//ground_board.png')
            self.backdrop_w, self.backdrop_h = self.backdrop.get_size()

        self.spaces = []

        images = ('images//space1.png', 'images//space2.png')
        for x in range(self.WIDTH):
            for y in range(self.HEIGHT):
                valid = True
                if(self.gametype == "Stratego"):
                    if((y == 4)or(y == 5)):
                        if((x == 2)or(x==3)or(x==6)or(x==7)):
                            valid = False
                elif(self.gametype == "Ground_War"):
                    if((y < 4)or(y > 13)):
                        if((x < 4)or(x > 13)):
                            valid = False
                    if((x < 4)or(x > 13)):
                        if((y < 4)or(y > 13)):
                            valid = False
                    if((y == 6)or(y == 7)or(y == 10)or(y == 11)):
                        if((x == 6)or(x==7)or(x==10)or(x==11)):
                            valid = False
                if(valid):
                    self.spaces.append(space(screen, (0,0), x, y, images))

    def get_space1(self, x, y):
        loc = None
        for s in self.spaces:
            if((s.loc[0] == x)and(s.loc[1] == y)):
                loc = s
        return loc

    def get_space2(self, position):
        loc = None
        for s in self.spaces:
            if(s.hover(position)):
                loc = s
        return loc

    def hover(self, position):
        if((self.pos[0] - (self.backdrop_w/2) < position[0])and
           (self.pos[0] + (self.backdrop_w/2) > position[0])):
            if((self.pos[1] - (self.backdrop_h/2) < position[1])and
               (self.pos[1] + (self.backdrop_h/2) > position[1])):
                return True
            else:
                return False
        else:
            return False
        
    def update(self, interact):
        mouse_pos = interact[7]
        click = interact[0]
        for s in self.spaces:
            x_dif = self.WIDTH/2 - s.loc[0]
            y_dif = (self.HEIGHT/2 - s.loc[1]) - 1

            s.pos = (self.pos[0] - (x_dif * s.image_w) + s.image_w/2,
                        self.pos[1] + (y_dif * s.image_h) + s.image_w/2)
            s.update(mouse_pos, click)

    def blitme(self):
        draw_pos = self.backdrop.get_rect().move(self.pos[0]-(self.backdrop_w/2),
                                              self.pos[1]-(self.backdrop_h/2))
        self.screen.blit(self.backdrop, draw_pos)
        
        for s in self.spaces:
            s.blitme()


class space(Sprite):
    def __init__(self, screen, pos, x, y, images):        
        self.screen = screen
        self.pos = pos
        self.loc = (x,y)
        self.image_base = pygame.image.load(images[0])
        self.image_hover = pygame.image.load(images[1])
        self.image = self.image_base
        self.image_w, self.image_h = self.image.get_size()

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

    def update(self, mouse_pos, click):
        if(self.hover(mouse_pos)):
            self.image = self.image_hover
        else:
            self.image = self.image_base        

    def blitme(self):
        draw_pos = self.image.get_rect().move(self.pos[0]-(self.image_w/2),
                                              self.pos[1]-(self.image_h/2))
        self.screen.blit(self.image, draw_pos)
        
