import os, sys
import pygame, pygame.event

from Game import *
from Board import *
from Team import *
from Piece import *
from Items import *
from Setup import *

# FULL-TIME USER INTERFACE
# RUNS PASSIVE GAME FUNCTIONS, NEVER STOPS RUNNING
class Interface(object):
#### INITIALIZATION ################################################
    def __init__(self):
        # Initializes pygame libraries
        pygame.init()
        pygame.mixer.init()
        pygame.display.init()

        # Screen Setup
        self.background = pygame.image.load('images//backdrop.jpg')
        self.backgroundRect = self.background.get_rect()
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = self.background.get_size()
        self.size = (self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        self.screen = pygame.display.set_mode(self.size, pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()

        # Mouse Constants
        self.LEFT = 1
        self.MIDDLE = 2
        self.RIGHT = 3

        # Menu bars and button lists (actively updated + actively running)
        self.bars = []
        self.buttons = []

        events = [sys.exit, self.toggle1, self.aid]
        temp = window(self.screen, self.size, events)
        self.tools = temp[0]
        self.dummys = temp[1]

        # Running Game
        self.game = None

        # Active Account
        self.users = []

    # Toggles screen to resizable window
    def toggle1(self):
        self.screen = pygame.display.set_mode(self.size, pygame.RESIZABLE)
        self.tools[1] = Button(self.screen, ('buttons//max_btn1.png','buttons//max_btn2.png'),
                                 (self.SCREEN_WIDTH - 30, 10), self.toggle2, None)
    # Toggles screen to fullscreen display
    def toggle2(self):
        self.screen = pygame.display.set_mode(self.size, pygame.FULLSCREEN)
        self.tools[1] = Button(self.screen, ('buttons//restore_btn1.png','buttons//restore_btn2.png'),
                                 (self.SCREEN_WIDTH - 30, 10), self.toggle1, None)
    # Displays Help Screen (for now just detects use)
    def aid(self):
        print("/:> Requesting /b/lackup")

    def start_game(self, g_type):
        users = []
        for u in self.users:
            users.append(u)
        if(len(users) < 2):
            x = 1
            for i in range(2-len(users)):
                a = Account(0)
                a.alias = "Player " + str(x)
                a.set_name("John Smith")
                a.DOB = "13/32/2012"
                users.append(a)
                x += 1
                
        if(self.game == None):
            if(g_type == "Stratego"):
                self.game = Stratego(self.screen, self.size, users, self.reset)
                events = [self.reset]
                temp = game_bars(self.screen, self.size, events)
                self.bars = temp[0]
                self.bars[0].scroll_LU()
                self.buttons = temp[1]
            elif(g_type == "Checkers"):
                self.game = Checkers(self.screen, self.size, users, self.reset)
                temp = game_bars(self.screen, self.size, [self.reset])
                self.bars = temp[0]
                self.bars[0].scroll_LU()
                self.buttons = temp[1]
            elif(g_type == "Ground_War"):
                self.game = Ground_War(self.screen, self.size, users, self.reset)
                events = [self.reset]
                temp = game_bars(self.screen, self.size, events)
                self.bars = temp[0]
                self.bars[0].scroll_LU()
                self.buttons = temp[1]

    def log_in(self, acc):
        self.users.append(acc)
        #acc.save()
        self.reset()

    def log_out(self, acc):
        self.users.remove(acc)
        self.reset()

    def sign_in(self):
        temp = game_bars(self.screen, self.size, [self.reset])
        self.bars = temp[0]
        self.buttons = temp[1]
        temp = account_set(self.screen, self.size, [self.log_in])
        for t in temp[0]:
            self.bars.append(t)
        for t in temp[1]:
            self.buttons.append(t)

    def edit_acc(self, acc):
        self.bars = []
        self.buttons = []
        temp = account_edit(self.screen, self.size, [self.reset], acc)
        for t in temp[0]:
            self.bars.append(t)
        for t in temp[1]:
            self.buttons.append(t)

    def load_acc(self):
        self.reset()

    def new_acc(self):
        temp = game_bars(self.screen, self.size, [self.reset])
        self.bars = temp[0]
        self.buttons = temp[1]
        temp = account_set(self.screen, self.size, [self.log_in])

    def reset(self):
        self.game = None
        events = [self.start_game, self.sign_in, self.edit_acc]
        temp = main_menu(self.screen, self.size, events, self.users)
        self.bars = temp[0]
        self.buttons = temp[1]


#### EXECUTION ####################################
    def execute(self):

        self.reset()

        # Mouse vars for click detection
        left_click = False
        right_click = False
        middle_click = False

        # Keyboard input
        inkey = None
        shift = False
        back = False
        enter = False

        # Main Loop
        run = True
        while run:
            time_passed = self.clock.tick(50)

            # If window closed (alt-F4 or window button)
            for event in pygame.event.get():
                if(event.type == pygame.QUIT):
                    run = False

                # If mouse click (all buttons)
                if(event.type == pygame.MOUSEBUTTONDOWN):
                    if(event.button == self.LEFT):
                        left_click = True
                    elif(event.button == self.RIGHT):
                        right_click = True
                    elif(event.button == self.MIDDLE):
                        middle_click = True
                # If mouse release (all buttons)                        
                elif(event.type == pygame.MOUSEBUTTONUP):
                    left_click = False
                    middle_click = False
                    right_click = False

                if(event.type == pygame.KEYDOWN):
                    tempkey = event.key
                    if((tempkey == pygame.K_RSHIFT) or (tempkey == pygame.K_LSHIFT)):
                        shift = True
                    elif(tempkey == pygame.K_BACKSPACE):
                        back = True
                    elif(tempkey == pygame.K_RETURN):
                        enter = True
                    elif(tempkey <= 127):
                        inkey = tempkey
                elif(event.type == pygame.KEYUP):
                    tempkey = event.key
                    if((tempkey == pygame.K_RSHIFT) or (tempkey == pygame.K_LSHIFT)):
                        shift = False

            # Update Screen + Button use detect
            mouse_pos = pygame.mouse.get_pos()

            interact = (left_click, right_click, middle_click,
                        inkey, shift, back, enter, mouse_pos, time_passed)

            self.screen.blit(self.background, self.backgroundRect)

            if(self.game != None):
                self.game.update(interact)

            if(self.game != None):
                self.game.blitme()

            for b in self.bars:
                b.update(interact)
                b.blitme()

            for b in self.buttons:
                b.update(interact)
                b.blitme()

            for d in self.dummys:
                d.blitme() 

            for t in self.tools:
                t.update(interact)
                t.blitme()
            
            pygame.display.flip()

            inkey = None
            back = False
            enter = False
            
        sys.exit()
