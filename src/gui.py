import pygame
import sys
import numpy as np
import src.colors as colors

FONT_PATH = './src/font.ttf'
LOGFILE = './log.json'
GREEDY_CONFIG = './greedy.config'
HAMILTON_CONFIG = './hamilton.config'

size = 700
pygame.init()
wdw = pygame.display.set_mode((size,size))
wdw_wt = wdw.get_size()[0] 
wdw_ht = wdw.get_size()[1] 
pygame.display.set_caption("Snake")
font = pygame.font.Font(FONT_PATH, 50)
font1 = pygame.font.Font(FONT_PATH, 80)
font2 = pygame.font.Font(FONT_PATH, 60)
clock = pygame.time.Clock()

buttons = []
input_boxes = []
choice_made = False
done = False
try_again = False
start = False
player_info = "None"
frame_delay = 80 
obstacles = "to_be_setup"
autostart = False
x_blocks = 15 
y_blocks = 16

# draw buttons
def buttons_draw(buttons):
    for b in buttons:
        b.draw()
        b.check_click()

# drop previously used buttons
def clear_buttons(buttons):
    while len(buttons) > 0: 
        buttons.pop(0)

# draw pressed buttons
def pressed_buttons(buttons):
    for b in buttons:
        b.draw()

# draw button in new_game
def draw_new_game(buttons):
    for b in buttons:
        b.draw()
        if b.check_click() == 'no':
            pygame.quit()
            sys.exit()

 # drop previously used buttons
def clear_input_boxes(input_boxes):
    while len(input_boxes) > 0:
        input_boxes.pop(0)

# asks for the settings of the game
def snake_interface():
    global choice_made, done, player_info, frame_delay, \
            obstacles, autostart, x_blocks, y_blocks
    button1 = Button('Play yourself', 400, 100,((wdw_wt-400)/2,wdw_ht/10*4.5),5)
    buttons.append(button1)
    button2 = Button('Watch an AI', 400, 100,((wdw_wt-400)/2,wdw_ht/10*6.5),5)
    buttons.append(button2)
    # choose human/bot
    while not choice_made:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        wdw.fill('#000000')
        buttons_draw(buttons)
        text = font1.render('SNAKE GAME', True, colors.WHITE)
        wdw.blit(
            text, 
            ((wdw_wt-text.get_width())/2, (wdw_ht-text.get_height())/4)
        )
        pygame.display.update()
        clock.tick(60)
    pressed_buttons(buttons)
    pygame.display.update()
    pygame.time.delay(200)
    clear_buttons(buttons)

    # choose which bot to use
    button2_1 = Button('Greedy',310,70,
                ((wdw_wt/2 - 310)/2,wdw_ht/2),5)
    buttons.append(button2_1)
    button3_1 = Button('Hamilton',310,70,
                (((wdw_wt/2 - 310)/2)+wdw_wt/2,wdw_ht/2),5)
    buttons.append(button3_1)
    while choice_made == 'bot': # loop only if bot has been selected
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        wdw.fill('#000000')
        buttons_draw(buttons)
        text = font2.render('Choose a strategy', True, colors.WHITE)
        wdw.blit(
            text,
            ((wdw_wt-text.get_width())/2, (wdw_ht-text.get_height())/4)
        )
        pygame.display.update()
        clock.tick(60)
    if choice_made != 'human':
        pressed_buttons(buttons)
    pygame.display.update()
    pygame.time.delay(200)
    clear_buttons(buttons)

    # choose an obstacle configuration
    button3 = Button('Cross',300,70,
                ((wdw_wt/2 - 300)/2,wdw_ht/10*4),5)
    buttons.append(button3)
    button4 = Button('Blocks',300,70,
                (((wdw_wt/2 - 300)/2)+wdw_wt/2,wdw_ht/10*4),5)
    buttons.append(button4)
    button5 = Button('Tunnel',300,70,
                ((wdw_wt/2 - 300)/2,wdw_ht/10*6),5)
    buttons.append(button5)
    button6 = Button('Spiral',300,70,
                (((wdw_wt/2 - 300)/2)+wdw_wt/2,wdw_ht/10*6),5)
    buttons.append(button6)
    button7 = Button('None',300,70,
                ((wdw_wt - 300)/2,(wdw_ht/5)*4),5)
    buttons.append(button7)

    while obstacles == "to_be_setup":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        wdw.fill('#000000')
        buttons_draw(buttons)
        text = font2.render('Choose an obstacle', True, colors.WHITE)
        text1 = font2.render('configuration',True, colors.WHITE)
        wdw.blit(
            text,
            ((wdw_wt-text.get_width())/2, (wdw_ht-text.get_height())/6)
        )
        wdw.blit(
            text1,
            ((wdw_wt-text1.get_width())/2, (wdw_ht-text1.get_height())/4)
        )
        pygame.display.update()
        clock.tick(60)
    pressed_buttons(buttons)
    pygame.display.update()
    pygame.time.delay(200)

    # drop buttons proviously pressed
    clear_buttons(buttons)

    # choose grid dimension if obstacles haven't been selected
    input_box1 = InputBox((wdw_wt/2 - 200)/2, wdw_ht/10*6, 10, 52, "X")
    input_boxes.append(input_box1)
    input_box2 = InputBox(((wdw_wt/2 - 200)/2)+wdw_wt/2, wdw_ht/10*6, 10, 52, "Y")
    input_boxes.append(input_box2)
    button7 = Button('Done',300,70,((wdw_wt - 300)/2,(wdw_ht/5)*4),5)
    buttons.append(button7)

    while not done and obstacles == "None": # loop only if obstacles haven't been selected
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            for box in input_boxes:
                box.handle_event(event)
        for box in input_boxes:
            box.update()
        wdw.fill('#000000')
        for box in input_boxes:
            box.draw(wdw)
        buttons_draw(buttons)
        text = font2.render('Insert the grid', True, colors.WHITE)
        text1 = font2.render('dimensions in the',True,colors.WHITE)
        text2 = font2.render('rectangles',True, colors.WHITE)
        wdw.blit(
            text,
            ((wdw_wt-text.get_width())/2, (wdw_ht-text.get_height())/10)
        )
        wdw.blit(
            text1,
            ((wdw_wt-text1.get_width())/2, (wdw_ht-text1.get_height())/10*2)
        )
        wdw.blit(
            text2,
            ((wdw_wt-text2.get_width())/2, (wdw_ht-text2.get_height())/10*3)
        )
        text3 = font.render('X', True, colors.WHITE)
        text4 = font.render('Y',True, colors.WHITE)
        wdw.blit(
            text3,
            ((wdw_wt/2-text3.get_width())/2, (wdw_ht-text3.get_height())/2)
        )
        wdw.blit(
            text4,
            ((wdw_wt/2-text4.get_width())/2+wdw_wt/2, (wdw_ht-text4.get_height())/2)
            )
        pygame.display.flip()
        clock.tick(30)
    if obstacles == "None":
        pressed_buttons(buttons)
    pygame.display.update()
    clear_buttons(buttons)
    clear_input_boxes(input_boxes)
    if player_info=="hamilton":
        if ((x_blocks % 2) != 0 and (y_blocks % 2) != 0) or\
            (x_blocks < 6 or y_blocks < 6):
                grid_not_allowed()
    else:
         if (x_blocks < 6 or y_blocks < 6):
                grid_not_allowed()

    config = None
    if player_info=='greedy':
        config = GREEDY_CONFIG
    if player_info=='hamilton':
        config = HAMILTON_CONFIG
    #return game configuration
    game_config = {
        'grid_size': size,
        'grid_width': x_blocks,
        'grid_height': y_blocks,
        'frame_delay': frame_delay,
        'obstacles': obstacles,
        'autostart': autostart,
        'max_executions': np.inf,
        'player_info': player_info,
        'bot_config': config,
        'log_file': LOGFILE,
        'test_mode': False,
    }

    if player_info=='human':
        button1 = Button('Start',300,70,
                    ((wdw_wt - 300)/2,wdw_ht/10*6),5)
        buttons.append(button1)
        while not start:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                wdw.fill('#000000')
                buttons_draw(buttons)
                text = font2.render("Use the arrow keys", True, colors.WHITE)
                text1 = font2.render("to move the snake",True,colors.WHITE)
                wdw.blit(
                    text,
                    ((wdw_wt-text.get_width())/2, (wdw_ht-text.get_height())/10*2)
                )
                wdw.blit(
                    text1,
                    ((wdw_wt-text1.get_width())/2, (wdw_ht-text1.get_height())/10*3)
                )
                pygame.display.update()
                clock.tick(60)
        clear_buttons(buttons)
    return game_config

# at the end of the game, ask whether to play again
def new_game():
    global choice_made
    button10 = Button('Yes',wdw.get_size()[0]/4,wdw.get_size()[1]/10,
                (wdw.get_size()[0]/10*2, wdw.get_size()[1]/2),5)
    buttons.append(button10)
    button20 = Button('No',wdw.get_size()[0]/4,wdw.get_size()[1]/10,
                (wdw.get_size()[0]/10*5.5, wdw.get_size()[1]/2),5)
    buttons.append(button20)
    choice_made = False
    while not choice_made:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        wdw.fill('#000000')
        draw_new_game(buttons)
        text = font2.render('Do you want', True, colors.WHITE)
        text1 = font2.render('to play again?', True, colors.WHITE)
        wdw.blit(
            text,
            ((wdw.get_size()[0]-text.get_width())/2, (wdw.get_size()[1]-text.get_height())/10*2)
        )
        wdw.blit(
            text1,
            ((wdw.get_size()[0]-text1.get_width())/2, (wdw.get_size()[1]-text1.get_height())/10*3)
        )
        pygame.display.update()
        clock.tick(60)
    pressed_buttons(buttons)
    pygame.display.update()
    pygame.time.delay(200)
    clear_buttons(buttons)

# halt if the grid dimensions are not allowed for hamilton bot
def grid_not_allowed():
    global done, try_again, player_info, obstacles, x_blocks, y_blocks
    button1 = Button('Try again',400,70,((wdw_wt - 400)/2,wdw_ht/10*6),5)
    buttons.append(button1)
    try_again = False
    done = False
    while not try_again:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            wdw.fill('#000000')
            buttons_draw(buttons)
            text = font.render("At least one of the", True, colors.WHITE)
            text1 = font.render("dimensions must be even.",True,colors.WHITE)
            text2 = font.render("The minimum dimension",True,colors.WHITE) 
            text3 = font.render("allowed is 6 x 6.",True,colors.WHITE)
            if player_info == "hamilton":
                wdw.blit(
                    text,
                    ((wdw_wt-text.get_width())/2, (wdw_ht-text.get_height())/10)
                )
                wdw.blit(
                    text1,
                    ((wdw_wt-text1.get_width())/2, (wdw_ht-text1.get_height())/10*2)
                )
            wdw.blit(
                text2,
                ((wdw_wt-text2.get_width())/2, (wdw_ht-text2.get_height())/10*3)
            )
            wdw.blit(
                text3,
                ((wdw_wt-text3.get_width())/2, (wdw_ht-text3.get_height())/10*4)
            )
            pygame.display.update()
            clock.tick(60)
    clear_buttons(buttons)
    # choose grid dimension obstacles haven't been selected
    input_box1 = InputBox((wdw_wt/2 - 200)/2, wdw_ht/10*6, 10, 52, "X")
    input_boxes.append(input_box1)
    input_box2 = InputBox(((wdw_wt/2 - 200)/2)+wdw_wt/2, wdw_ht/10*6, 10, 52, "Y")
    input_boxes.append(input_box2)
    button7 = Button('Done',300,70,((wdw_wt - 300)/2,(wdw_ht/5)*4),5)
    buttons.append(button7)
    
    # loop if obstacles haven't been selected
    while not done and obstacles == "None":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            for box in input_boxes:
                box.handle_event(event)
        for box in input_boxes:
            box.update()
        wdw.fill('#000000')
        for box in input_boxes:
            box.draw(wdw)
        buttons_draw(buttons)
        text = font2.render('Insert the grid', True, colors.WHITE)
        text1 = font2.render('dimensions in the',True,colors.WHITE)
        text2 = font2.render('rectangles',True, colors.WHITE)
        wdw.blit(
            text, 
            ((wdw_wt-text.get_width())/2, (wdw_ht-text.get_height())/10)
        )
        wdw.blit(
            text1, 
            ((wdw_wt-text1.get_width())/2, (wdw_ht-text1.get_height())/10*2)
        )
        wdw.blit(
            text2,
            ((wdw_wt-text2.get_width())/2, (wdw_ht-text2.get_height())/10*3)
        )
        text3 = font.render('X', True, colors.WHITE)
        text4 = font.render('Y',True, colors.WHITE)
        wdw.blit(
            text3, 
            ((wdw_wt/2-text3.get_width())/2, (wdw_ht-text3.get_height())/2)
        )
        wdw.blit(
            text4, 
            ((wdw_wt/2-text4.get_width())/2+wdw_wt/2, (wdw_ht-text4.get_height())/2)
        )
        pygame.display.flip()
        clock.tick(30)
    if obstacles == "None":
        pressed_buttons(buttons)
    pygame.display.update()
    clear_buttons(buttons)
    clear_input_boxes(input_boxes)
    if player_info=="hamilton":
        if ((x_blocks % 2) != 0 and (y_blocks % 2) != 0) or \
            (x_blocks < 6 or y_blocks < 6):
                grid_not_allowed()
    else:
         if (x_blocks < 6 or y_blocks < 6):
                grid_not_allowed()

class Button():
    """This class implements a button of the interface."""

    def __init__(self,text,width,height,pos,elevation):
        # core attributes 
        self.pressed = False
        self.elevation = elevation
        self.dynamic_elevation = elevation
        self.original_y_pos = pos[1]

        # top rectangle 
        self.top_rect = pygame.Rect(pos,(width,height))
        self.top_color = colors.GREEN
        
        # bottom rectangle 
        self.bottom_rect = pygame.Rect(pos,(width,height))
        self.bottom_color = colors.DARK_GREEN

        # text
        self.text = text
        self.text_surf = font.render(text,True,colors.WHITE)
        self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)

    def draw(self):
        # elevation logic 
        self.top_rect.y = self.original_y_pos - self.dynamic_elevation
        self.text_rect.center = self.top_rect.center 

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elevation

        pygame.draw.rect(wdw,self.bottom_color, self.bottom_rect,border_radius = 12)
        pygame.draw.rect(wdw,self.top_color, self.top_rect,border_radius = 12)
        wdw.blit(self.text_surf, self.text_rect)

    def check_click(self): # check which button has been clicked, then do the respective action
        global choice_made, done, try_again, start, player_info, frame_delay, obstacles
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos): # mouse on top of the button
            self.top_color = colors.RED
            if pygame.mouse.get_pressed()[0]: # true if the mouse has been pressed
                self.dynamic_elevation = 0
                self.pressed = True
                if self.text == 'Play yourself': # select the correct dictonary for each player
                    player_info = "human"
                    choice_made = 'human'
                    frame_delay = 100
                elif self.text == 'Watch an AI':
                    choice_made = 'bot'
                elif self.text == 'Greedy':
                    player_info = "greedy"
                    choice_made = 'greedy' 
                elif self.text == 'Hamilton':
                    player_info = "hamilton"
                    choice_made = 'hamilton'
                elif self.text == "Yes":
                    choice_made = True
                    return "yes"
                elif self.text == "No":
                    choice_made = True
                    return "no"
                elif self.text == "Cross": # select the obstacles configuration
                    obstacles = 0
                elif self.text == "Blocks":
                    obstacles = 1
                elif self.text == "Tunnel":
                    obstacles = 2
                elif self.text == "Spiral":
                    obstacles = 3
                elif self.text == "None":
                    obstacles = "None"
                elif self.text == "Done":
                    done = True
                elif self.text == "Try again":
                    try_again = True
                elif self.text == "Start":
                    start = True
            else:
                self.dynamic_elevation = self.elevation
                if self.pressed == True:
                    self.pressed = False
                return 0
        else:
            self.dynamic_elevation = self.elevation
            self.top_color = colors.GREEN
            return 0

class InputBox():
    """This class implements an input box of the interface."""

    def __init__(self, x, y, w, h, name, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = colors.GREEN
        self.text = text
        self.txt_surface = font.render(text, True, self.color)
        self.active = False
        self.name = name

    def handle_event(self, event):
        global x_blocks, y_blocks
        if event.type == pygame.MOUSEBUTTONDOWN:
            # if the user clicked on the input_box rectangle
            if self.rect.collidepoint(event.pos):
                # toggle the active variable
                self.active = not self.active
            else:
                self.active = False
            # change the current color of the input box
            self.color = colors.WHITE if self.active else colors.GREEN
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                    if len(self.text) > 0:
                        if self.name == "X":
                            x_blocks = int(self.text)
                        elif self.name == "Y":
                            y_blocks = int(self.text)
                        else: print("error: no such input box")
                for value in [i for i in range(10)]:
                    if event.unicode == str(value):
                        self.text += event.unicode
                        if self.name == "X":
                            x_blocks = int(self.text)
                        elif self.name == "Y":
                            y_blocks = int(self.text)
                        else: print("error: no such input box")
                # re-render the text
                self.txt_surface = font.render(self.text, True, colors.WHITE) 
   
    # resize the box if the text is too long
    def update(self):
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        screen.blit(
            self.txt_surface, 
            (self.rect.x+(self.rect.w-self.txt_surface.get_width())/2 , self.rect.y)
        )
        pygame.draw.rect(screen, self.color, self.rect, 2)