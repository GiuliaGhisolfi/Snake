import pygame
import sys
import src.colors as colors
import numpy as np

FONT_PATH = './src/font.ttf'
LOGFILE = './log.json'
GREEDY_CONFIG = './greedy.config'
HAMILTON_CONFIG = './hamilton.config'
SIZE = 700

# initialize game
pygame.init()
window = pygame.display.set_mode((SIZE,SIZE))
window_width = window.get_size()[0] # TODO: per caso cambia mai?
window_heigth = window.get_size()[1] # TODO: per caso cambia mai?
pygame.display.set_caption("Snake")
font = pygame.font.Font(FONT_PATH, 50)
font1 = pygame.font.Font(FONT_PATH, 80)
font2 = pygame.font.Font(FONT_PATH, 60)
clock = pygame.time.Clock()
FONT = pygame.font.Font(None, 32)

class Button:
    """This class implements a button of the interface."""

    buttons = []
    choise_made = False
    done = False
    try_again = False
    start = False
    player_info = {}
    X_BLOCKS = 15 # TODO: possiamo spostare ciò che concettualmente non è un attributo del bottone come variabile globale? 
                  # eventualmente qualcosa può essere messo anche in game (ci ho messo FRAME_DEALY as esempio)
                  # avevo detto di evitare variabili globali perchè pensavo di fare un'ulteriore classe GameConfig o qualcosa del genere che raccogliesse questi dati
                  # ma se è troppo complicato non importa, pardon 
    Y_BLOCKS = 16
    FRAME_DELAY = 100 # TODO: se 50 a me va a scatti... anche per giocarci forse è troppo veloce?
    OBSTACLES = "to_be_setup"
    AUTOSTART = False

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
        Button.buttons.append(self)

    def draw(self):
        # elevation logic 
        self.top_rect.y = self.original_y_pos - self.dynamic_elevation
        self.text_rect.center = self.top_rect.center 

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elevation

        pygame.draw.rect(window,self.bottom_color, self.bottom_rect,border_radius = 12)
        pygame.draw.rect(window,self.top_color, self.top_rect,border_radius = 12)
        window.blit(self.text_surf, self.text_rect)

    # draw buttons & retrieve bot dictonary
    def buttons_draw(self):
        Button.player_info
        for b in Button.buttons:
            b.draw()
            b.check_click()

    # drop previously used buttons
    def clear_buttons(self):
        while len(Button.buttons) > 0: Button.buttons.pop(0)
    
    # draw pressed buttons
    def pressed_buttons(self):
        for b in Button.buttons:
            b.draw()

    # draw button in new_game
    def draw_new_game(self):
        for b in Button.buttons:
            b.draw()
            if b.check_click() == 'no':
                pygame.quit()
                sys.exit()

    def check_click(self): # check which button has been clicked, then do the respective action
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos): # mouse on top of the button
            self.top_color = colors.RED
            if pygame.mouse.get_pressed()[0]: # true if the mouse has been pressed
                self.dynamic_elevation = 0
                self.pressed = True
                if self.text == 'Play yourself': # select the correct dictonary for each player
                    Button.player_info =  {
                        "type": "human",
                        "color": colors.GREEN, # TODO: questo probabilmente diventerà globale, nel caso possiamo inizializzarlo con color e start_location che rimangono sempre uguali e settare solo type?
                        "start_location": "top-left"
                    }
                    Button.choise_made = 'human'
                    Button.FRAME_DELAY = 100
                elif self.text == 'Watch an AI':
                    Button.player_info =  {
                        "type": "greedy", # TODO: perchè viene messo greedy? immagino la logica del codice richiesa di settarlo con qualche valore, un None funzionerebbe?
                        "color": colors.GREEN,
                        "start_location": "top-left"
                    }
                    Button.choise_made = 'bot'
                elif self.text == 'Greedy':
                    Button.player_info = {
                        "type": "greedy",
                        "color": colors.GREEN,
                        "start_location": "top-left"
                    }
                    Button.choise_made = 'astar' # TODO: questo astar possiamo cambiarlo?
                elif self.text == 'Hamilton':
                    Button.player_info = {
                        "type": "hamilton",
                        "color": colors.GREEN,
                        "start_location": "top-left"
                    }
                    Button.choise_made = 'hamilton'
                elif self.text == "Yes":
                    Button.choise_made = True
                    return "yes"
                elif self.text == "No":
                    Button.choise_made = True
                    return "no"
                elif self.text == "Cross": # select the obstacles configuration
                    Button.OBSTACLES = 0
                elif self.text == "Blocks":
                    Button.OBSTACLES = 1
                elif self.text == "Tunnel":
                    Button.OBSTACLES = 2
                elif self.text == "Spiral":
                    Button.OBSTACLES = 3
                elif self.text == "None":
                    Button.OBSTACLES = "None"
                elif self.text == "Done":
                    Button.done = True
                elif self.text == "Try again":
                    Button.try_again = True
                elif self.text == "Start":
                    Button.start = True
            else:
                self.dynamic_elevation = self.elevation
                if self.pressed == True:
                    self.pressed = False
                return 0
        else:
            self.dynamic_elevation = self.elevation
            self.top_color = colors.GREEN
            return 0

class InputBox:
    """This class implements an input box of the interface."""

    def __init__(self, x, y, w, h, name,text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = colors.GREEN
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False
        self.name = name

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # if the user clicked on the input_box rectangle
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable
                self.active = not self.active
            else:
                self.active = False
            # change the current color of the input box
            self.color = colors.WHITE if self.active else colors.GREEN
        if event.type == pygame.KEYDOWN:
            if self.active:
                for value in [i for i in range(10)]:
                    if event.unicode == str(value):
                        self.text += event.unicode
                        if self.name == "X":
                            Button.X_BLOCKS = int(self.text)
                        elif self.name == "Y":
                            Button.Y_BLOCKS = int(self.text)
                        else: print("error: no such input box")
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                # re-render the text
                self.txt_surface = FONT.render(self.text, True, colors.WHITE) # TODO: si può centrare nella casella?

    def update(self):
        # resize the box if the text is too long
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(screen, self.color, self.rect, 2)

def snake_interface():
    """This function handles user input through the GUI."""

    button1 = Button('Play yourself',400,100,((window_width-400)/2,window_heigth/10*4.5),5)
    button2 = Button('Watch an AI',400,100,((window_width-400)/2,window_heigth/10*6.5),5)
    # choose human/bot
    while not button1.choise_made:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        window.fill('#000000')
        button1.buttons_draw()
        text = font1.render('SNAKE GAME', True, colors.WHITE)
        window.blit(text, ((window_width-text.get_width())/2, (window_heigth-text.get_height())/4))
        pygame.display.update()
        clock.tick(60)
    button2.pressed_buttons()
    pygame.display.update()
    pygame.time.delay(200)
    button1.clear_buttons()

    # choose which bot to use
    button2_1 = Button('Greedy',310,70,(((window_width)/2 - 310)/2,(window_heigth)/2),5)
    button3_1 = Button('Hamilton',310,70,((((window_width)/2 - 310)/2)+window_width/2,(window_heigth)/2),5)
    while button2_1.choise_made == 'bot': # loop only if bot has been selected
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        window.fill('#000000')
        button2_1.buttons_draw()
        text = font2.render('Choose a strategy', True, colors.WHITE)
        window.blit(text, ((window_width-text.get_width())/2, (window_heigth-text.get_height())/4))
        pygame.display.update()
        clock.tick(60)
    if button2_1.choise_made != 'human':
        button3_1.pressed_buttons()
    pygame.display.update()
    pygame.time.delay(200)
    button2_1.clear_buttons()

    # choose an obstacle configuration
    button3 = Button('Cross',300,70,(((window_width)/2 - 300)/2,(window_heigth)/10*4),5)
    button4 = Button('Blocks',300,70,((((window_width)/2 - 300)/2)+window_width/2,window_heigth/10*4),5)
    # TODO: button5 e button6 non vengono mai usati?
    button5 = Button('Tunnel',300,70,(((window_width)/2 - 300)/2,window_heigth/10*6),5)
    button6 = Button('Spiral',300,70,((((window_width)/2 - 300)/2)+window_width/2,window_heigth/10*6),5)
    button7 = Button('None',300,70,(((window_width) - 300)/2,(window_heigth/5)*4),5)

    while Button.OBSTACLES == "to_be_setup":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        window.fill('#000000')
        button3.buttons_draw()
        text = font2.render('Choose an obstacle', True, colors.WHITE)
        text1 = font2.render('configuration',True, colors.WHITE)
        window.blit(text, ((window_width-text.get_width())/2, (window_heigth-text.get_height())/6))
        window.blit(text1, ((window_width-text1.get_width())/2, (window_heigth-text1.get_height())/4))
        pygame.display.update()
        clock.tick(60)
    button4.pressed_buttons()
    pygame.display.update()
    pygame.time.delay(200)

    # drop buttons proviously pressed
    button3.clear_buttons()

    # choose grid dimension if obstacles haven't been selected
    input_box1 = InputBox(((window_width)/2 - 200)/2, window_heigth/10*6, 10, 52, "X") # TODO: ho cambiato l'altezza del rettangolo in 52 in tutti gli InputBox, non so se così ho rotto qualcosa
    input_box2 = InputBox((((window_width)/2 - 200)/2)+window_width/2, window_heigth/10*6, 10, 52, "Y")
    input_boxes = [input_box1, input_box2]
    button7 = Button('Done',300,70,(((window_width) - 300)/2,(window_heigth/5)*4),5)

    while not Button.done and Button.OBSTACLES == "None": # loop only if obstacles haven't been selected
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            for box in input_boxes:
                box.handle_event(event)
        for box in input_boxes:
            box.update()
        window.fill('#000000')
        for box in input_boxes:
            box.draw(window)
        button7.buttons_draw()
        text = font2.render('Insert the grid', True, colors.WHITE)
        text1 = font2.render('dimensions in the',True,colors.WHITE)
        text2 = font2.render('rectangles',True, colors.WHITE)
        window.blit(text, ((window_width-text.get_width())/2, (window_heigth-text.get_height())/10))
        window.blit(text1, ((window_width-text1.get_width())/2, (window_heigth-text1.get_height())/10*2))
        window.blit(text2, ((window_width-text2.get_width())/2, (window_heigth-text2.get_height())/10*3))
        text3 = font.render('X', True, colors.WHITE)
        text4 = font.render('Y',True, colors.WHITE)
        window.blit(text3, ((window_width/2-text3.get_width())/2, (window_heigth-text3.get_height())/2))
        window.blit(text4, ((window_width/2-text4.get_width())/2+window_width/2, (window_heigth-text4.get_height())/2))
        pygame.display.flip()
        clock.tick(30)
    if Button.OBSTACLES == "None":
        button7.pressed_buttons()
    pygame.display.update()
    button7.clear_buttons()
    if Button.player_info["type"]=="hamilton":
        if ((Button.X_BLOCKS % 2) != 0 and (Button.Y_BLOCKS % 2) != 0) or\
            (Button.X_BLOCKS < 6 or Button.Y_BLOCKS < 6):
                grid_not_allowed()
    else:
         if (Button.X_BLOCKS < 6 or Button.Y_BLOCKS < 6):
                grid_not_allowed()

    config = None
    if Button.player_info['type']=='greedy':
        config = GREEDY_CONFIG
    if Button.player_info['type']=='hamilton':
        config = HAMILTON_CONFIG

    game_config = {
        'grid_size': SIZE,
        'grid_width': Button.X_BLOCKS,
        'grid_height': Button.Y_BLOCKS,
        'frame_delay': Button.FRAME_DELAY,
        'obstacles': Button.OBSTACLES,
        'autostart': Button.AUTOSTART,
        'max_executions': np.inf,
        'player_info': Button.player_info,
        'bot_config': config,
        'log_file': LOGFILE,
        'test_mode': False,
    }

    if Button.player_info['type']=='human':
        button1 = Button('Start',300,70,(((window_width) - 300)/2,(window_heigth)/10*6),5)
        while not Button.start:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                window.fill('#000000')
                button1.buttons_draw()
                text = font2.render("Use the arrow keys", True, colors.WHITE)
                text1 = font2.render("to move the snake",True,colors.WHITE)
                window.blit(text, ((window_width-text.get_width())/2, (window_heigth-text.get_height())/10*2))
                window.blit(text1, ((window_width-text1.get_width())/2, (window_heigth-text1.get_height())/10*3))
                pygame.display.update()
                clock.tick(60)
        button1.clear_buttons()
    return game_config

# at the end of the game, ask whether to play again
def new_game():
    button10 = Button('Yes',window_width/4,window_heigth/10,(window_width/10*2, window_heigth/2),5)
    button20 = Button('No',window_width/4,window_heigth/10,(window_width/10*5.5, window_heigth/2),5)
    Button.choise_made = False
    while not button10.choise_made:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        window.fill('#000000')
        button10.draw_new_game()
        text = font2.render('Do you want', True, colors.WHITE)
        text1 = font2.render('to play again?', True, colors.WHITE)
        window.blit(text, ((window_width-text.get_width())/2, (window_heigth-text.get_height())/10*2))
        window.blit(text1, ((window_width-text1.get_width())/2, (window_heigth-text1.get_height())/10*3))
        pygame.display.update()
        clock.tick(60)
    button20.pressed_buttons()
    pygame.display.update()
    pygame.time.delay(200)
    button10.clear_buttons()

# halt if the grid dimensions are not allowed for hamilton bot
def grid_not_allowed():
    button1 = Button('Try again',400,70,(((window_width) - 400)/2,(window_heigth)/10*6),5)
    Button.try_again = False
    Button.done = False
    while not Button.try_again:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            window.fill('#000000')
            button1.buttons_draw()
            text = font.render("At least one of the", True, colors.WHITE)
            text1 = font.render("dimensions must be even.",True,colors.WHITE)
            text2 = font.render("The minimum dimension",True,colors.WHITE) 
            text3 = font.render("allowed is 6 x 6.",True,colors.WHITE)
            if Button.player_info["type"] == "hamilton":
                window.blit(text, ((window_width-text.get_width())/2, (window_heigth-text.get_height())/10))
                window.blit(text1, ((window_width-text1.get_width())/2, (window_heigth-text1.get_height())/10*2))
            window.blit(text2, ((window_width-text2.get_width())/2, (window_heigth-text2.get_height())/10*3))
            window.blit(text3, ((window_width-text3.get_width())/2, (window_heigth-text3.get_height())/10*4))
            pygame.display.update()
            clock.tick(60)
    button1.clear_buttons()
    # choose grid dimension obstacles haven't been selected
    input_box1 = InputBox(((window_width)/2 - 200)/2, window_heigth/10*6, 10, 52, "X")
    input_box2 = InputBox((((window_width)/2 - 200)/2)+window_width/2, window_heigth/10*6, 10, 52, "Y")
    input_boxes = [input_box1, input_box2]
    button7 = Button('Done',300,70,(((window_width) - 300)/2,(window_heigth/5)*4),5)
    
    # loop if obstacles haven't been selected
    while not Button.done and Button.OBSTACLES == "None":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            for box in input_boxes:
                box.handle_event(event)
        for box in input_boxes:
            box.update()
        window.fill('#000000')
        for box in input_boxes:
            box.draw(window)
        button7.buttons_draw()
        text = font2.render('Insert the grid', True, colors.WHITE)
        text1 = font2.render('dimensions in the',True,colors.WHITE)
        text2 = font2.render('rectangles',True, colors.WHITE)
        window.blit(text, ((window_width-text.get_width())/2, (window_heigth-text.get_height())/10))
        window.blit(text1, ((window_width-text1.get_width())/2, (window_heigth-text1.get_height())/10*2))
        window.blit(text2, ((window_width-text2.get_width())/2, (window_heigth-text2.get_height())/10*3))
        text3 = font.render('X', True, colors.WHITE)
        text4 = font.render('Y',True, colors.WHITE)
        window.blit(text3, ((window_width/2-text3.get_width())/2, (window_heigth-text3.get_height())/2))
        window.blit(text4, ((window_width/2-text4.get_width())/2+window_width/2, (window_heigth-text4.get_height())/2))
        pygame.display.flip()
        clock.tick(30)
    if Button.OBSTACLES == "None":
        button7.pressed_buttons()
    pygame.display.update()
    button7.clear_buttons()
    if Button.player_info["type"]=="hamilton":
        if ((Button.X_BLOCKS % 2) != 0 and (Button.Y_BLOCKS % 2) != 0) or\
            (Button.X_BLOCKS < 6 or Button.Y_BLOCKS < 6):
                grid_not_allowed()
    else:
         if (Button.X_BLOCKS < 6 or Button.Y_BLOCKS < 6):
                grid_not_allowed()