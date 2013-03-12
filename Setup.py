import pygame
import shelve
from Items import *
from Account import *
from Piece import *
from random import randint

# Sets Title bar + Buttons
def window(screen, size, events):
    WIDTH = size[0]
    HEIGHT = size[1]
    # Permanent Buttons (close/max/help btns)
    tools = []
    tools.append(Button(screen, ('buttons//close_btn1.png','buttons//close_btn2.png'),
                   (WIDTH - 10, 10), events[0], None)) # Close
    tools.append(Button(screen, ('buttons//restore_btn1.png','buttons//restore_btn2.png'),
                             (WIDTH - 30, 10), events[1], None))
    tools.append(Button(screen, ('buttons//help_btn1.png','buttons//help_btn2.png'),
                             (WIDTH - 50, 10), events[2], None))
    # Dummy Display items (title bar)
    dummys = []
    dummys.append(DummyBlob(screen, 'images//title_bar.png', (WIDTH/2, 10)))

    return (tools, dummys)


# Sets Bars + Buttons for main menu
def main_menu(screen, size, events, users):
    WIDTH = size[0]
    HEIGHT = size[1]
    quit_images = ('buttons//quit1.png', 'buttons//quit2.png')
    enter_images = ('buttons//enter1.png', 'buttons//enter2.png')
    start_images = ('buttons//start1.png', 'buttons//start2.png')
    right_images = ('buttons//right_btn1.png', 'buttons//right_btn2.png')
    left_images = ('buttons//left_btn1.png', 'buttons//left_btn2.png')
    up_images = ('buttons//up_btn1.png', 'buttons//up_btn2.png')
    down_images = ('buttons//down_btn1.png', 'buttons//down_btn2.png')

    bars = []
    buttons = []

    x = 1
    for u in users:
        a = 0
        b = 0
        if((x == 1)or(x == 3)):
            a = 150
        else:
            a = WIDTH - 150

        if(x <= 2):
            b = 95
        else:
            b = 450
        bars.append(Acc_Bar(screen, (a,b), u))
        x+=1

    # SECONDARY BAR
    image = pygame.image.load('images//hor_bar1.png')
    image_w, image_h = image.get_size()
    pos = (WIDTH/2, HEIGHT - image_h/2)

    contents = []
    t_pos = (pos[0] - 200, pos[1] - 80)
    contents.append(Button(screen, start_images, t_pos, events[0], "Stratego"))
    t_pos = (pos[0] + 200, pos[1] - 80)
    contents.append(Button(screen, start_images, t_pos, events[0], "Checkers"))
    t_pos = (pos[0], pos[1] - 80)
    contents.append(Button(screen, start_images, t_pos, events[0], "Ground_War"))

    if(len(users) < 4):
        t_pos = (pos[0], pos[1])
        contents.append(Button(screen, quit_images, t_pos, events[1], None))

    x = 0
    for u in users:
        t_pos = (pos[0] - (300 - (200*x)), pos[1] + 50)
        contents.append(Button(screen, enter_images, t_pos, events[2], u))
        x += 1

    bar = Sidebar(screen, contents, 'images//hor_bar1.png', pos, False)

    down = Button(screen, down_images, (pos[0]+(image_w/2)+10, HEIGHT-5), bar.scroll_RD, None)
    up = Button(screen, up_images, (pos[0]+(image_w/2)+10, HEIGHT-15), bar.scroll_LU, None)

    bars.append(bar)
    buttons.append(down)
    buttons.append(up)

    return (bars,buttons)

def account_display(screen, size, events, acc):
    WIDTH = size[0]
    HEIGHT = size[1]
    quit_images = ('buttons//quit1.png', 'buttons//quit2.png')
    start_images = ('buttons//start1.png', 'buttons//start2.png')
    right_images = ('buttons//right_btn1.png', 'buttons//right_btn2.png')
    left_images = ('buttons//left_btn1.png', 'buttons//left_btn2.png')
    up_images = ('buttons//up_btn1.png', 'buttons//up_btn2.png')
    down_images = ('buttons//down_btn1.png', 'buttons//down_btn2.png')

    bars = []
    buttons = []

    # EXIT BAR
    image = pygame.image.load("images//vert_bar1.png")
    image_w, image_h = image.get_size()
    pos = (image_w/2, HEIGHT/2)

    contents = []    
    contents.append(Button(screen, quit_images, pos, events[0], None))

    bar = Sidebar(screen, contents, "images//vert_bar1.png", pos, True)

    right = Button(screen, right_images, (15, pos[1]+(image_h/2)+10), bar.scroll_RD, None)
    left = Button(screen, left_images, (5, pos[1]+(image_h/2)+10), bar.scroll_LU, None)

    bars.append(bar)
    buttons.append(right)
    buttons.append(left)

    return (bars, buttons)

def game_bars(screen, size, events):
    WIDTH = size[0]
    HEIGHT = size[1]
    quit_images = ('buttons//quit1.png', 'buttons//quit2.png')
    start_images = ('buttons//start1.png', 'buttons//start2.png')
    right_images = ('buttons//right_btn1.png', 'buttons//right_btn2.png')
    left_images = ('buttons//left_btn1.png', 'buttons//left_btn2.png')
    up_images = ('buttons//up_btn1.png', 'buttons//up_btn2.png')
    down_images = ('buttons//down_btn1.png', 'buttons//down_btn2.png')

    piece_images = ('images//scout.png', 'images//scout.png')

    bars = []
    buttons = []

    # EXIT BAR
    image = pygame.image.load("images//vert_bar1.png")
    image_w, image_h = image.get_size()
    pos = (image_w/2, HEIGHT/2)

    contents = []    
    contents.append(Button(screen, quit_images, pos, events[0], None))

    bar = Sidebar(screen, contents, "images//vert_bar1.png", pos, True)

    right = Button(screen, right_images, (15, pos[1]+(image_h/2)+10), bar.scroll_RD, None)
    left = Button(screen, left_images, (5, pos[1]+(image_h/2)+10), bar.scroll_LU, None)

    bars.append(bar)
    buttons.append(right)
    buttons.append(left)

    return (bars, buttons)

def set_col(param):
    param[0].blitme()
    param[1].color = param[0].screen.get_at(pygame.mouse.get_pos())
    param[2].set_text(str(param[1].color[0]))
    param[3].set_text(str(param[1].color[1]))
    param[4].set_text(str(param[1].color[2]))

def account_set(screen, size, events):
    WIDTH = size[0]
    HEIGHT = size[1]
    quit_images = ('buttons//quit1.png', 'buttons//quit2.png')
    start_images = ('buttons//start1.png', 'buttons//start2.png')
    enter_images = ('buttons//enter1.png', 'buttons//enter2.png')
    right_images = ('buttons//right_btn1.png', 'buttons//right_btn2.png')
    left_images = ('buttons//left_btn1.png', 'buttons//left_btn2.png')
    up_images = ('buttons//up_btn1.png', 'buttons//up_btn2.png')
    down_images = ('buttons//down_btn1.png', 'buttons//down_btn2.png')
    wheel_images = ('buttons//color_wheel2.png', 'buttons//color_wheel2.png')

    bars = []
    buttons = []

    a = Account(randint(1,999))

    # ACCOUNT BAR
    image = pygame.image.load("images//vert_bar1.png")
    image_w, image_h = image.get_size()
    pos = (WIDTH - image_w/2, HEIGHT/2)

    contents = []
    
    t_pos = (pos[0], pos[1] - 200)
    name = Text_Box(screen, (200,20), t_pos, "*Name*", a.set_name)
    name.set_text(a.name)
    
    t_pos = (pos[0], pos[1] - 160)
    alias = Text_Box(screen, (200, 20), t_pos, "*Alias*", a.set_alias)
    alias.set_text(a.alias)

    t_pos = (pos[0], pos[1] - 120)
    serial = Text_Box(screen, (200, 20), t_pos, "d.o.b. (xx/xx/xx)", a.set_DOB)
    serial.set_text(a.DOB)
    #serial.hidden = True

    t_pos = (pos[0]-40, pos[1] - 80)
    col1 = Text_Box(screen, (40, 20), t_pos, "r", a.set_col1)
    col1.set_text(str(a.color[0]))

    t_pos = (pos[0], pos[1] - 80)
    col2 = Text_Box(screen, (40, 20), t_pos, "g", a.set_col2)
    col2.set_text(str(a.color[1]))

    t_pos = (pos[0]+40, pos[1] - 80)
    col3 = Text_Box(screen, (40, 20), t_pos, "b", a.set_col3)
    col3.set_text(str(a.color[2]))

    t_pos = (pos[0], pos[1] + 100)
    wheel = Button(screen, wheel_images, (t_pos), set_col, None)
    wheel.param = (wheel, a, col1, col2, col3)

    square = SmartSquare(screen, pos, (248, 648), a)

    contents.append(square)
    contents.append(name)
    contents.append(alias)
    contents.append(serial)
    contents.append(col1)
    contents.append(col2)
    contents.append(col3)
    contents.append(wheel)
    
    t_pos = (pos[0], pos[1] + 250)
    contents.append(Button(screen, enter_images, t_pos, events[0], a))

    bar = Sidebar(screen, contents, "images//vert_bar1.png", pos, True)

    right = Button(screen, right_images, (WIDTH-5, pos[1]+(image_h/2)+10), bar.scroll_RD, None)
    left = Button(screen, left_images, (WIDTH-15, pos[1]+(image_h/2)+10), bar.scroll_LU, None)

    bars.append(bar)
    buttons.append(right)
    buttons.append(left)

    return (bars, buttons)

def account_edit(screen, size, events, acc):
    WIDTH = size[0]
    HEIGHT = size[1]
    quit_images = ('buttons//quit1.png', 'buttons//quit2.png')
    start_images = ('buttons//start1.png', 'buttons//start2.png')
    enter_images = ('buttons//enter1.png', 'buttons//enter2.png')
    right_images = ('buttons//right_btn1.png', 'buttons//right_btn2.png')
    left_images = ('buttons//left_btn1.png', 'buttons//left_btn2.png')
    up_images = ('buttons//up_btn1.png', 'buttons//up_btn2.png')
    down_images = ('buttons//down_btn1.png', 'buttons//down_btn2.png')
    wheel_images = ('buttons//color_wheel2.png', 'buttons//color_wheel2.png')

    bars = []
    buttons = []

    t_pos = (WIDTH/2, HEIGHT/2)
    bars.append(Acc_Bar(screen, t_pos, acc))

    # ACCOUNT BAR
    image = pygame.image.load("images//vert_bar1.png")
    image_w, image_h = image.get_size()
    pos = (WIDTH - image_w/2, HEIGHT/2)

    contents = []
    
    t_pos = (pos[0], pos[1] - 200)
    name = Text_Box(screen, (200,20), t_pos, "*Name*", acc.set_name)
    name.set_text(acc.name)
    
    t_pos = (pos[0], pos[1] - 160)
    alias = Text_Box(screen, (200, 20), t_pos, "*Alias*", acc.set_alias)
    alias.set_text(acc.alias)

    t_pos = (pos[0], pos[1] - 120)
    serial = Text_Box(screen, (200, 20), t_pos, "d.o.b. (xx/xx/xx)", acc.set_DOB)
    serial.set_text(acc.DOB)
    #serial.hidden = True

    t_pos = (pos[0]-40, pos[1] - 80)
    col1 = Text_Box(screen, (40, 20), t_pos, "r", acc.set_col1)
    col1.set_text(str(acc.color[0]))

    t_pos = (pos[0], pos[1] - 80)
    col2 = Text_Box(screen, (40, 20), t_pos, "g", acc.set_col2)
    col2.set_text(str(acc.color[1]))

    t_pos = (pos[0]+40, pos[1] - 80)
    col3 = Text_Box(screen, (40, 20), t_pos, "b", acc.set_col3)
    col3.set_text(str(acc.color[2]))

    t_pos = (pos[0], pos[1] + 100)
    wheel = Button(screen, wheel_images, (t_pos), set_col, None)
    wheel.param = (wheel, acc, col1, col2, col3)
    
    square = SmartSquare(screen, pos, (248, 648), acc)

    contents.append(square)
    contents.append(name)
    contents.append(alias)
    contents.append(serial)
    contents.append(col1)
    contents.append(col2)
    contents.append(col3)
    contents.append(wheel)
    
    t_pos = (pos[0], pos[1] + 250)
    contents.append(Button(screen, enter_images, t_pos, events[0], None))

    bar = Sidebar(screen, contents, "images//vert_bar1.png", pos, True)

    right = Button(screen, right_images, (WIDTH-5, pos[1]+(image_h/2)+10), bar.scroll_RD, None)
    left = Button(screen, left_images, (WIDTH-15, pos[1]+(image_h/2)+10), bar.scroll_LU, None)

    bars.append(bar)
    buttons.append(right)
    buttons.append(left)

    return (bars, buttons)

def equip_set(screen, size, events):
    WIDTH = size[0]
    HEIGHT = size[1]
    quit_images = ('buttons//quit1.png', 'buttons//quit2.png')
    start_images = ('buttons//start1.png', 'buttons//start2.png')
    enter_images = ('buttons//enter1.png', 'buttons//enter2.png')
    right_images = ('buttons//right_btn1.png', 'buttons//right_btn2.png')
    left_images = ('buttons//left_btn1.png', 'buttons//left_btn2.png')
    up_images = ('buttons//up_btn1.png', 'buttons//up_btn2.png')
    down_images = ('buttons//down_btn1.png', 'buttons//down_btn2.png')

    bomb_images = ('images//strat_back.png', 'images//bomb.png')
    barb_images = ('images//strat_back.png', 'images//barb.png')
    bunk_images = ('images//strat_back.png', 'images//bunker.png')
    tool_images = ('images//strat_back.png', 'images//toolbox.png')

    # PIECE BAR
    image = pygame.image.load("images//hor_bar1.png")
    image_w, image_h = image.get_size()
    pos = (WIDTH/2, HEIGHT - image_h/2)

    contents = []
    t_pos = (pos[0] - 100, pos[1])
    contents.append(Button(screen, bomb_images, t_pos, events[0], 0))
    t_pos = (pos[0] - 50, pos[1])
    contents.append(Button(screen, barb_images, t_pos, events[0], 1))
    t_pos = (pos[0] + 50, pos[1])
    contents.append(Button(screen, bunk_images, t_pos, events[0], 2))
    t_pos = (pos[0] + 100, pos[1])
    contents.append(Button(screen, tool_images, t_pos, events[0], 3))

    bar = Sidebar(screen, contents, "images//hor_bar1.png", pos, True)

    return (bar)

def S_Piece_set(screen, size, events):
    WIDTH = size[0]
    HEIGHT = size[1]
    quit_images = ('buttons//quit1.png', 'buttons//quit2.png')
    start_images = ('buttons//start1.png', 'buttons//start2.png')
    enter_images = ('buttons//enter1.png', 'buttons//enter2.png')
    right_images = ('buttons//right_btn1.png', 'buttons//right_btn2.png')
    left_images = ('buttons//left_btn1.png', 'buttons//left_btn2.png')
    up_images = ('buttons//up_btn1.png', 'buttons//up_btn2.png')
    down_images = ('buttons//down_btn1.png', 'buttons//down_btn2.png')

    bomb_images = ('images//strat_back.png', 'images//bomb.png')
    spy_images = ('images//strat_back.png', 'images//spy.png')
    scout_images = ('images//strat_back.png', 'images//scout.png')
    min_images = ('images//strat_back.png', 'images//miner.png')
    serg_images = ('images//strat_back.png', 'images//sergeant.png')
    lie_images = ('images//strat_back.png', 'images//lieutenant.png')
    cap_images = ('images//strat_back.png', 'images//captain.png')
    maj_images = ('images//strat_back.png', 'images//major1.png')
    col_images = ('images//strat_back.png', 'images//colonel.png')
    gen_images = ('images//strat_back.png', 'images//general1.png')
    mar_images = ('images//strat_back.png', 'images//marshal.png')
    flag_images = ('images//strat_back.png', 'images//flag.png')

    bars = []
    buttons = []
    
    # PIECE BAR
    image = pygame.image.load("images//vert_bar1.png")
    image_w, image_h = image.get_size()
    pos = (WIDTH - image_w/2, HEIGHT/2)

    contents = []
    t_pos = (pos[0] - 50, pos[1] - 200)
    contents.append(Button(screen, flag_images, t_pos, events[0], 11))
    t_pos = (pos[0] + 50, pos[1] - 200)
    contents.append(Button(screen, bomb_images, t_pos, events[0], 0))
    t_pos = (pos[0] - 50, pos[1] - 150)
    contents.append(Button(screen, spy_images, t_pos, events[0], 1))
    t_pos = (pos[0] + 50, pos[1] - 150)
    contents.append(Button(screen, scout_images, t_pos, events[0], 2))
    t_pos = (pos[0] - 50, pos[1] - 100)
    contents.append(Button(screen, min_images, t_pos, events[0], 3))
    t_pos = (pos[0] + 50, pos[1] - 100)
    contents.append(Button(screen, serg_images, t_pos, events[0], 4))
    t_pos = (pos[0] - 50, pos[1] - 50)
    contents.append(Button(screen, lie_images, t_pos, events[0], 5))
    t_pos = (pos[0] + 50, pos[1] - 50)
    contents.append(Button(screen, cap_images, t_pos, events[0], 6))
    t_pos = (pos[0] - 50, pos[1])
    contents.append(Button(screen, maj_images, t_pos, events[0], 7))
    t_pos = (pos[0] + 50, pos[1])
    contents.append(Button(screen, col_images, t_pos, events[0], 8))
    t_pos = (pos[0] - 50, pos[1] + 50)
    contents.append(Button(screen, gen_images, t_pos, events[0], 9))
    t_pos = (pos[0] + 50, pos[1] + 50)
    contents.append(Button(screen, mar_images, t_pos, events[0], 10))
    t_pos = (pos[0] - 50, pos[1] + 250)
    contents.append(Button(screen, enter_images, t_pos, events[1], None))
    t_pos = (pos[0]+50, pos[1] + 250)
    contents.append(Button(screen, enter_images, t_pos, events[2], None))


    bar = Sidebar(screen, contents, "images//vert_bar1.png", pos, True)

    right = Button(screen, right_images, (WIDTH-5, pos[1]+(image_h/2)+10), bar.scroll_RD, None)
    left = Button(screen, left_images, (WIDTH-15, pos[1]+(image_h/2)+10), bar.scroll_LU, None)

    bars.append(bar)
    buttons.append(right)
    buttons.append(left)

    #buttons.append(Button(screen, enter_images, (WIDTH/2, HEIGHT-50), events[1], None))

    return (bars, buttons)

def GW_Piece_set(screen, size, events):
    WIDTH = size[0]
    HEIGHT = size[1]
    quit_images = ('buttons//quit1.png', 'buttons//quit2.png')
    start_images = ('buttons//start1.png', 'buttons//start2.png')
    enter_images = ('buttons//enter1.png', 'buttons//enter2.png')
    right_images = ('buttons//right_btn1.png', 'buttons//right_btn2.png')
    left_images = ('buttons//left_btn1.png', 'buttons//left_btn2.png')
    up_images = ('buttons//up_btn1.png', 'buttons//up_btn2.png')
    down_images = ('buttons//down_btn1.png', 'buttons//down_btn2.png')

    ass_images = ('images//strat_back.png', 'images//assassin.png')
    scout_images = ('images//strat_back.png', 'images//scout.png')
    eng_images = ('images//strat_back.png', 'images//engineer.png')
    serg_images = ('images//strat_back.png', 'images//sergeant.png')
    warr_images = ('images//strat_back.png', 'images//warrant_officer.png')
    maj_images = ('images//strat_back.png', 'images//major.png')
    gen_images = ('images//strat_back.png', 'images//general.png')
    comm_images = ('images//strat_back.png', 'images//commander.png')
    flag_images = ('images//strat_back.png', 'images//flag.png')

    bars = []
    buttons = []
    
    # PIECE BAR
    image = pygame.image.load("images//vert_bar1.png")
    image_w, image_h = image.get_size()
    pos = (WIDTH - image_w/2, HEIGHT/2)

    contents = []
    t_pos = (pos[0], pos[1] - 250)
    contents.append(Button(screen, flag_images, t_pos, events[0], 11))
    t_pos = (pos[0], pos[1] - 200)
    contents.append(Button(screen, ass_images, t_pos, events[0], 1))
    t_pos = (pos[0], pos[1] - 150)
    contents.append(Button(screen, scout_images, t_pos, events[0], 2))
    t_pos = (pos[0], pos[1] - 100)
    contents.append(Button(screen, eng_images, t_pos, events[0], 3))
    t_pos = (pos[0], pos[1] - 50)
    contents.append(Button(screen, serg_images, t_pos, events[0], 4))
    t_pos = (pos[0], pos[1])
    contents.append(Button(screen, warr_images, t_pos, events[0], 5))
    t_pos = (pos[0], pos[1] + 50)
    contents.append(Button(screen, maj_images, t_pos, events[0], 6))
    t_pos = (pos[0], pos[1] + 100)
    contents.append(Button(screen, gen_images, t_pos, events[0], 7))
    t_pos = (pos[0], pos[1] + 150)
    contents.append(Button(screen, comm_images, t_pos, events[0], 8))
    t_pos = (pos[0]-50, pos[1] + 250)
    contents.append(Button(screen, enter_images, t_pos, events[1], None))
    t_pos = (pos[0]+50, pos[1] + 250)
    contents.append(Button(screen, enter_images, t_pos, events[2], None))


    bar = Sidebar(screen, contents, "images//vert_bar1.png", pos, True)

    right = Button(screen, right_images, (WIDTH-5, pos[1]+(image_h/2)+10), bar.scroll_RD, None)
    left = Button(screen, left_images, (WIDTH-15, pos[1]+(image_h/2)+10), bar.scroll_LU, None)

    bars.append(bar)
    buttons.append(right)
    buttons.append(left)

    #buttons.append(Button(screen, enter_images, (WIDTH/2, HEIGHT-50), events[1], None))

    return (bars, buttons)

def rot(x, y, num):
    pos = None
    if(num == 0):
        pos = (4 + x, y)
    elif(num == 1):
        pos = (13 - x, 17 - y)
    elif(num == 2):
        pos = (y, 13 - x)
    elif(num == 3):
        pos = (17 - y, 4 + x)

    return pos
        

def GW_Preset(screen, ac_team, do_teams, num):
    roll = []

    #Assassins
    temp = Ground_Piece(screen, 1, rot(0, 1, num), ac_team, do_teams)
    temp.loc = rot(0, 1, num)
    temp.origin = temp.loc
    roll.append(temp)
    temp = Ground_Piece(screen, 1, rot(9, 1, num), ac_team, do_teams)
    temp.loc = rot(9, 1, num)
    temp.origin = temp.loc
    roll.append(temp)

    #Scouts
    temp = Ground_Piece(screen, 2, rot(0, 0, num), ac_team, do_teams)
    temp.loc = rot(0, 0, num)
    temp.origin = temp.loc
    roll.append(temp)
    temp = Ground_Piece(screen, 2, rot(9, 0, num), ac_team, do_teams)
    temp.loc = rot(9, 0, num)
    temp.origin = temp.loc
    roll.append(temp)
    temp = Ground_Piece(screen, 2, rot(3, 1, num), ac_team, do_teams)
    temp.loc = rot(3, 1, num)
    temp.origin = temp.loc
    roll.append(temp)
    temp = Ground_Piece(screen, 2, rot(6, 1, num), ac_team, do_teams)
    temp.loc = rot(6, 1, num)
    temp.origin = temp.loc
    roll.append(temp)
    temp = Ground_Piece(screen, 2, rot(4, 2, num), ac_team, do_teams)
    temp.loc = rot(4, 2, num)
    temp.origin = temp.loc
    roll.append(temp)
    temp = Ground_Piece(screen, 2, rot(5, 2, num), ac_team, do_teams)
    temp.loc = rot(5, 2, num)
    temp.origin = temp.loc
    roll.append(temp)
    temp = Ground_Piece(screen, 2, rot(1, 3, num), ac_team, do_teams)
    temp.loc = rot(1, 3, num)
    temp.origin = temp.loc
    roll.append(temp)
    temp = Ground_Piece(screen, 2, rot(8, 3, num), ac_team, do_teams)
    temp.loc = rot(8, 3, num)
    temp.origin = temp.loc
    roll.append(temp)
    temp = Ground_Piece(screen, 2, rot(4, 3, num), ac_team, do_teams)
    temp.loc = rot(4, 3, num)
    temp.origin = temp.loc
    roll.append(temp)
    temp = Ground_Piece(screen, 2, rot(5, 3, num), ac_team, do_teams)
    temp.loc = rot(5, 3, num)
    temp.origin = temp.loc
    roll.append(temp)

    #Engineers
    temp = Ground_Piece(screen, 3, rot(4, 0, num), ac_team, do_teams)
    temp.loc = rot(4, 0, num)
    temp.origin = temp.loc
    roll.append(temp)
    temp = Ground_Piece(screen, 3, rot(6, 0, num), ac_team, do_teams)
    temp.loc = rot(6, 0, num)
    temp.origin = temp.loc
    roll.append(temp)
    temp = Ground_Piece(screen, 3, rot(1, 1, num), ac_team, do_teams)
    temp.loc = rot(1, 1, num)
    temp.origin = temp.loc
    roll.append(temp)
    temp = Ground_Piece(screen, 3, rot(8, 1, num), ac_team, do_teams)
    temp.loc = rot(8, 1, num)
    temp.origin = temp.loc
    roll.append(temp)
    temp = Ground_Piece(screen, 3, rot(2, 2, num), ac_team, do_teams)
    temp.loc = rot(2, 2, num)
    temp.origin = temp.loc
    roll.append(temp)
    temp = Ground_Piece(screen, 3, rot(7, 2, num), ac_team, do_teams)
    temp.loc = rot(7, 2, num)
    temp.origin = temp.loc
    roll.append(temp)
    temp = Ground_Piece(screen, 3, rot(3, 3, num), ac_team, do_teams)
    temp.loc = rot(3, 3, num)
    temp.origin = temp.loc
    roll.append(temp)
    temp = Ground_Piece(screen, 3, rot(6, 3, num), ac_team, do_teams)
    temp.loc = rot(6, 3, num)
    temp.origin = temp.loc
    roll.append(temp)

    #Sergeants
    temp = Ground_Piece(screen, 4, rot(2, 0, num), ac_team, do_teams)
    temp.loc = rot(2, 0, num)
    temp.origin = temp.loc
    roll.append(temp)
    temp = Ground_Piece(screen, 4, rot(7, 0, num), ac_team, do_teams)
    temp.loc = rot(7, 0, num)
    temp.origin = temp.loc
    roll.append(temp)
    temp = Ground_Piece(screen, 4, rot(0, 3, num), ac_team, do_teams)
    temp.loc = rot(0, 3, num)
    temp.origin = temp.loc
    roll.append(temp)
    temp = Ground_Piece(screen, 4, rot(9, 3, num), ac_team, do_teams)
    temp.loc = rot(9, 3, num)
    temp.origin = temp.loc
    roll.append(temp)
    temp = Ground_Piece(screen, 4, rot(2, 3, num), ac_team, do_teams)
    temp.loc = rot(2, 3, num)
    temp.origin = temp.loc
    roll.append(temp)
    temp = Ground_Piece(screen, 4, rot(7, 3, num), ac_team, do_teams)
    temp.loc = rot(7, 3, num)
    temp.origin = temp.loc
    roll.append(temp)

    #Warrant Officers
    temp = Ground_Piece(screen, 5, rot(1, 0, num), ac_team, do_teams)
    temp.loc = rot(1, 0, num)
    temp.origin = temp.loc
    roll.append(temp)
    temp = Ground_Piece(screen, 5, rot(8, 0, num), ac_team, do_teams)
    temp.loc = rot(8, 0, num)
    temp.origin = temp.loc
    roll.append(temp)
    temp = Ground_Piece(screen, 5, rot(2, 1, num), ac_team, do_teams)
    temp.loc = rot(2, 1, num)
    temp.origin = temp.loc
    roll.append(temp)
    temp = Ground_Piece(screen, 5, rot(7, 1, num), ac_team, do_teams)
    temp.loc = rot(7, 1, num)
    temp.origin = temp.loc
    roll.append(temp)
    temp = Ground_Piece(screen, 5, rot(0, 2, num), ac_team, do_teams)
    temp.loc = rot(0, 2, num)
    temp.origin = temp.loc
    roll.append(temp)
    temp = Ground_Piece(screen, 5, rot(9, 2, num), ac_team, do_teams)
    temp.loc = rot(9, 2, num)
    temp.origin = temp.loc
    roll.append(temp)
    temp = Ground_Piece(screen, 5, rot(3, 2, num), ac_team, do_teams)
    temp.loc = rot(3, 2, num)
    temp.origin = temp.loc
    roll.append(temp)
    temp = Ground_Piece(screen, 5, rot(6, 2, num), ac_team, do_teams)
    temp.loc = rot(6, 2, num)
    temp.origin = temp.loc
    roll.append(temp)

    #Majors
    temp = Ground_Piece(screen, 6, rot(1, 2, num), ac_team, do_teams)
    temp.loc = rot(1, 2, num)
    temp.origin = temp.loc
    roll.append(temp)
    temp = Ground_Piece(screen, 6, rot(8, 2, num), ac_team, do_teams)
    temp.loc = rot(8, 2, num)
    temp.origin = temp.loc
    roll.append(temp)

    #Generals
    temp = Ground_Piece(screen, 7, rot(4, 1, num), ac_team, do_teams)
    temp.loc = rot(4, 1, num)
    temp.origin = temp.loc
    roll.append(temp)
    temp = Ground_Piece(screen, 7, rot(5, 1, num), ac_team, do_teams)
    temp.loc = rot(5, 1, num)
    temp.origin = temp.loc
    roll.append(temp)

    #Commander
    temp = Ground_Piece(screen, 8, rot(3, 0, num), ac_team, do_teams)
    temp.loc = rot(3, 0, num)
    temp.origin = temp.loc
    roll.append(temp)

    #Flag
    temp = Ground_Piece(screen, 11, rot(5, 0, num), ac_team, do_teams)
    temp.loc = rot(5, 0, num)
    temp.origin = temp.loc
    roll.append(temp)
    






    return roll
