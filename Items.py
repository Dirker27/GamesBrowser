import pygame
from pygame.sprite import Sprite
import string

class Sidebar(Sprite):
    def __init__(self, screen, contents, bckgrd, pos, horizontal):
        self.screen = screen
        self.contents = contents
        self.image = pygame.image.load(bckgrd)
        self.image_w, self.image_h = self.image.get_size()
        self.pos = pos
        self.horizontal = horizontal # True == Horizontal, False == Vertical
        self.direction = 0   # Initial direction (Going on/off first)
        self.speed = 0.1
        self.move = False
        #self.set_contents()

    def scroll_LU(self):
        self.move = True
        self.direction = -1

    def scroll_RD(self):
        self.move = True
        self.direction = 1                

    def set_contents(self):
        TOP = self.pos[1] - (self.image_h/2)
        BOTTOM = self.pos[1] + (self.image_h/2)
        LEFT = self.pos[0] + (self.image_w/2)
        RIGHT = self.pos[0] + (self.image_w/2)
        for i in range(len(self.contents)):
            if(self.layout[i] == "TOP"):
                self.contents[i].pos = (self.pos[0], TOP + (self.contents[i].image_h/2))
            
    def update(self, interact):
        time_passed = interact[8]
        mouse_pos = interact[7]
        click = interact[0]
        # if bar is moving
        if(self.move):
            x_diff = 0
            y_diff = 0

            inner_rect = self.screen.get_rect().inflate(-self.image_w,-self.image_h)
            outer_rect = self.screen.get_rect().inflate(self.image_w, self.image_h)

            if(self.horizontal):
                new_pos = (self.pos[0] + (time_passed * self.speed * self.direction), self.pos[1])
                x_diff = self.pos[0] - new_pos[0]
                if((new_pos[0] < inner_rect.left)and(new_pos[0] > outer_rect.left)):
                    pass
                elif((new_pos[0] > inner_rect.right)and(new_pos[0] < outer_rect.right)):
                    pass
                else:
                    self.move = False
                    new_pos = self.pos
                    x_diff = 0
            else:
                new_pos = (self.pos[0], self.pos[1] + (time_passed * self.speed * self.direction))
                y_diff = self.pos[1] - new_pos[1]
                if((new_pos[1] < inner_rect.top)and(new_pos[1] > outer_rect.top)):
                    pass
                elif((new_pos[1] > inner_rect.bottom)and(new_pos[1] < outer_rect.bottom)):
                    pass
                else:
                    self.move = False
                    new_pos = self.pos
                    y_diff = 0

            self.pos = new_pos
            for c in self.contents:
                c.pos = (c.pos[0] - x_diff, c.pos[1] - y_diff)
                c.update(interact)
        else:
            for c in self.contents:
                c.update(interact)

    def blitme(self):
        draw_pos=self.image.get_rect().move(self.pos[0]-(self.image_w/2),self.pos[1]-(self.image_h/2))
        self.screen.blit(self.image,draw_pos)

        for c in self.contents:
            c.blitme()

class Acc_Bar(Sprite):

    def __init__(self, screen, pos, owner):
        self.screen = screen
        self.pos = pos
        self.owner = owner
        self.font = pygame.font.Font(None, 40)
        self.font2 = pygame.font.Font(None, 60)

    def update(self, interact):
        pass

    def blitme(self):
        back = pygame.Surface((300, 150))
        back.fill(self.owner.color)
        back.set_alpha(90)
        draw_pos = (self.pos[0] - 150, self.pos[1] - 75)
        self.screen.blit(back, draw_pos)

        if(self.owner.alias != None):
            t_pos = (self.pos[0]-145, self.pos[1] - 75)
            if(self.owner.color[0]+self.owner.color[1]+self.owner.color[2] < 25):
                self.screen.blit(self.font2.render(self.owner.alias, True, self.owner.inv_col), t_pos)
            else:
                self.screen.blit(self.font2.render(self.owner.alias, True, (0,0,0)), t_pos)
        t_pos = (self.pos[0]+50, self.pos[1] - 25)
        self.screen.blit(self.font.render(str(self.owner.record), True, (0,0,0)),t_pos)
        t_pos = (self.pos[0]+50, self.pos[1] + 25)
        self.screen.blit(self.font.render(str(self.owner.XP), True, (0,0,0)),t_pos)
        t_pos = (self.pos[0] - 50, self.pos[1] + 25)
        self.owner.dog_tag.display(self.screen, t_pos)  
        


class Button(Sprite):

    def __init__(self, screen, images, pos, event, param):
        self.screen = screen
        self.pos = pos
        self.image_base = pygame.image.load(images[0])
        self.image_hover = pygame.image.load(images[1])
        self.image = self.image_base
        self.image_w, self.image_h = self.image.get_size()
        self.event = event
        self.param = param
        self.clicked = False
        self.ready = False

    def do(self):
        if(self.param == None):
            self.event()
        else:
            self.event(self.param)

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

    def update(self, interact):
        mouse_pos = interact[7]
        click = interact[0]
        if(self.clicked == False):
            if(self.hover(mouse_pos)):
                self.image = self.image_hover
                if(click):
                    if(self.ready):
                        self.clicked = True
                        self.do()
                else:
                    self.ready = True
            else:
                self.image = self.image_base
                self.ready = False
        else:
            if((self.hover(mouse_pos) == False)or(click == False)):
                self.clicked = False

    def blitme(self):
        draw_pos=self.image.get_rect().move(self.pos[0]-(self.image_w/2),self.pos[1]-(self.image_h/2))
        self.screen.blit(self.image, draw_pos)


class DummyBlob(Sprite):

    def __init__(self, screen, image, pos):
        self.screen = screen
        self.pos = pos
        self.image = pygame.image.load(image)
        self.image_w, self.image_h = self.image.get_size()

    def blitme(self):
        draw_pos=self.image.get_rect().move(self.pos[0]-(self.image_w/2),self.pos[1]-(self.image_h/2))
        self.screen.blit(self.image, draw_pos)

class SmartSquare(Sprite):
    def __init__(self, screen, pos, size, acc):
        self.screen = screen
        self.pos = pos
        self.size = size
        self.acc = acc
        self.surf = pygame.Surface(size)
        self.surf.fill(acc.color)

    def update(self, interact):
        self.surf = pygame.Surface(self.size)
        self.surf.fill(self.acc.color)

    def blitme(self):
        draw_pos = (self.pos[0] - self.size[0]/2, self.pos[1] - self.size[1]/2)
        self.screen.blit(self.surf, draw_pos)


class Text_Box(Sprite):

    def __init__(self, screen, size, pos, prompt, prop):
        pygame.font.init()
        self.screen = screen
        self.size = size
        self.pos = pos
        self.prop = prop
        self.active = False
        self.base_prompt = prompt
        self.active_prompt = prompt.upper()
        self.prompt = self.base_prompt
        self.font = pygame.font.Font(None, 20)
        self.text = []
        self.hidden = False

    def hover(self, position):
        if((self.pos[0] - (self.size[0]/2) < position[0])and
           (self.pos[0] + (self.size[0]/2) > position[0])):
            if((self.pos[1] - (self.size[1]/2) < position[1])and
               (self.pos[1] + (self.size[1]/2) > position[1])):
                return True
            else:
                return False
        else:
            return False

    def get_text(self):
        message = ""
        for t in self.text:
            message += t
        return message

    def set_text(self, message):
        if(message != None):
            self.text = []
            for i in range(len(message)):
                self.text.append(message[i])

    def update(self, interact):
        mouse_pos = interact[7]
        click = interact[0]
        inkey = interact[3]
        shift = interact[4]
        back = interact[5]
        enter = interact[6]

        if(self.active == False):
            self.prompt = self.base_prompt
            if((self.hover(mouse_pos))and(click)):
                self.active = True
        else:
            self.prompt = self.active_prompt
            if(enter):
                self.active = False
                self.prop(self.get_string())
            elif(back):
                self.text = self.text[0:-1]
            elif(inkey != None):
                if((shift)and(inkey >= 97)and(inkey <= 122)):
                    self.text.append(chr(inkey-32))
                else:
                    self.text.append(chr(inkey))

            if((click)and(self.hover(mouse_pos) == False)):
                self.active = False
                self.prop(self.get_string())

    def get_string(self):
        message = ""
        if(self.hidden):
            for i in range(len(self.text)):
                message += "X"
        else:
            message = self.get_text()

        return message

    def blitme(self):
               
        frame = pygame.Surface(self.size)
        frame.fill((250,0,0))
        t_pos = (self.pos[0]-(self.size[0]/2), self.pos[1]-(self.size[1]/2))
        self.screen.blit(frame, t_pos)
        
        box = pygame.Surface((self.size[0]-2, self.size[1]-2))
        box.fill((0,0,0))
        t_pos = (self.pos[0]-(self.size[0]/2)+1, self.pos[1]-(self.size[1]/2)+1)
        self.screen.blit(box, t_pos)

        t_pos = (self.pos[0] - (self.size[0]/2), self.pos[1] - (self.size[1]/2) - 12)
        self.screen.blit(self.font.render(self.prompt, True, (0,0,0)), t_pos)
        
        t_pos = (self.pos[0]-(self.size[0]/2)+3, self.pos[1]-(self.size[1]/2)+3)        
        self.screen.blit(self.font.render(self.get_string(), True, (255,255,255)), t_pos)

class grande_door:
    def __init__(self, screen, size, event):
        enter_images = ('buttons//enter1.png', 'buttons//enter2.png')
        self.width = size[0]
        self.height = size[1]
        self.left = Sidebar(screen, [], 'images//door.png', (-512, self.height/2), True)
        self.right = Sidebar(screen, [], 'images//door.png', (self.width + 512, self.height/2), True)
        self.left.speed = 0.5
        self.right.speed = 0.5
        self.opening = False
        self.closing = False
        self.butt_enable = False
        self.butt = Button(screen, enter_images, (self.width/2, self.height/2), event, None)

    def close(self):
        self.left.scroll_RD()
        self.right.scroll_LU()
        self.closing = True

    def split(self):
        self.left.scroll_LU()
        self.right.scroll_RD()
        self.butt_enable = False
        self.opening = True

    def is_closed(self):
        if((self.left.pos[0] == 0)and(self.right.pos[0] == self.width)):
            return True
        else:
            return False

    def shut(self):
        if((self.left.pos[0] >= 0)and(self.right.pos[0] <= self.width)):
            self.left.move = False
            self.right.move = False
            self.left.pos = (0, self.height/2)
            self.right.pos = (self.width, self.height/2)
            self.butt_enable = True
            self.closing = False

    def jam(self):
        if((self.left.pos[0] <= -512 )and(self.right.pos[0] >= self.width + 512)):
            self.left.move = False
            self.right.move = False
        self.opening = False

    def update(self, interact):
        if(self.closing):
            self.shut()
        elif(self.opening):
            self.jam()
        self.right.update(interact)
        self.left.update(interact)
        if(self.butt_enable):
            self.butt.update(interact)

    def blitme(self):
        self.right.blitme()
        self.left.blitme()
        if(self.butt_enable):
            self.butt.blitme()
        
    


