import pygame
from pygame.sprite import Sprite

from random import randint, choice
import shelve

class Account(object):

    def __init__(self, num):
        self.password = None
        self.IDNUM = num
        self.name = None
        self.alias = None
        self.DOB = None
        self.b_type = None
        self.rank = 0
        self.XP = 0
        self.record = (0,0,0)
        self.image = None
        self.inventory = []
        self.dog_tag = Dog_Tag(self)
        col = (0,250)
        self.color = (randint(0,250), randint(0,250), randint(0,250))
        self.inv_col = (250 - self.color[0], 250 - self.color[1], 250 - self.color[2])

    def set_name(self, name):
        self.name = name
        if(len(self.name) > 0):
            self.dog_tag.name = self.dog_tag.get_name()
            self.dog_tag.serial = self.dog_tag.get_serial()

    def set_alias(self, alias):
        self.alias = alias

    def set_DOB(self, dob):
        self.DOB = dob

    def set_col1(self, col):
        self.color = (int(col), self.color[1], self.color[2])
    def set_col2(self, col):
        self.color = (self.color[0], int(col), self.color[2])
    def set_col3(self, col):
        self.color = (self.color[0], self.color[1], int(col))

    def refresh_tag(self):
        self.dog_tag = Dog_Tag(self)

    def win(self):
        self.record = (self.record[0] + 1, self.record[1], self.record[2])
        self.XP += 50
    def tie(self):
        self.record = (self.record[0], self.record[1] + 1, self.record[2])
        self.XP += 25
    def lose(self):
        self.record = (self.record[0], self.record[1], self.record[2] + 1)

    def save(self):
        acc_data = shelve.open('data//account_data.dat')
        if(self.IDNUM in acc_data.keys()):
            for key in acc_data.keys():
                if(key == self.IDNUM):
                    acc_data[key] = [self]
        else:
            acc_data[self.IDNUM] = [self]

        acc_data.sync()
        acc_data.close()

        
        
class Dog_Tag(Sprite):

    def __init__(self, owner):
        pygame.font.init()
        
        self.OWNER = owner
        self.serial = None
        self.name = None
        self.backdrop = pygame.image.load('images//tag.png')
        self.tag_w, self.tag_h = self.backdrop.get_size()

    def get_serial(self):
        res = str(self.OWNER.IDNUM)

        while(len(res) < 10):
            res += str(randint(0,9))

        res += self.OWNER.name[0].upper()

        x = 1
        while(x < len(self.OWNER.name)):
            if(self.OWNER.name[x-1] == ' '):
                res += self.OWNER.name[x].upper()
            x += 1

        return res
            
    def get_name(self):
        res = self.rank_abbrev() + " "
        res += self.OWNER.name[0].upper() + '.'
        x = 1
        y = x
        while (x < len(self.OWNER.name)):
            if(self.OWNER.name[x] == ' '):
                y = x+1
            x += 1
        
        res += self.OWNER.name[y:len(self.OWNER.name)].upper()
        return res

    def rank_abbrev(self):
        if(self.OWNER.rank == 0):
            res = "PFC"
        else:
            res = "CPL"

        return res

    def display(self, screen, pos):
        font = pygame.font.Font(None, 20)
        
        draw_pos = self.backdrop.get_rect().move(pos[0]-(self.tag_w/2),
                                              pos[1]-(self.tag_h/2))
        screen.blit(self.backdrop, draw_pos)

        x = 0
        if(self.name != None):
            t_pos = ((pos[0]-self.tag_w/2)+35, (pos[1]-self.tag_h/2)+10+(x*15))
            screen.blit(font.render(self.name, True, (0,0,0)), t_pos)
            x+=1
        if(self.serial != None):
            t_pos = ((pos[0]-self.tag_w/2)+35, (pos[1]-self.tag_h/2)+10+(x*15))
            screen.blit(font.render(self.serial, True, (0,0,0)), t_pos)
            x+=1
        if(self.OWNER.DOB != None):
            t_pos = ((pos[0]-self.tag_w/2)+35, (pos[1]-self.tag_h/2)+10+(x*15))
            screen.blit(font.render(self.OWNER.DOB, True, (0,0,0)), t_pos)
            x+=1
        if(self.OWNER.b_type != None):
            t_pos = ((pos[0]-self.tag_w/2)+35, (pos[1]-self.tag_h/2)+10+(x*15))
            screen.blit(font.render(self.OWNER.b_type, True, (0,0,0)), t_pos)
            x+=1
