import pygame, sys
import colors

# global variable to use in main file
dict_info = {}
X_BLOCKS = 15
Y_BLOCKS = 16
FRAME_DELAY = 1
DEATH_DELAY = 700
OBSTACLES = "to_be_setup"
AUTOSTART = False
SIZE = 700
# general dictonary to use in the bot dictonary creation
dictonary = { 
    "type": ["human", "greedy","hamilton"],
    "color": [colors.ORANGE, colors.BLUE ,colors.GREEN],
    "start_location": "top-left",
} 
#initialize game, window size and font
pygame.init()
window = pygame.display.set_mode((SIZE,SIZE))
pygame.display.set_caption("Snake")
font = pygame.font.SysFont('Arial', 40, True)
clock = pygame.time.Clock()
FONT = pygame.font.Font(None, 32)

""" class that implements buttons in the game interface"""
class Button:

    buttons = []
    choise_made = False
    done = False

    def __init__(self,text,width,height,pos,elevation):
        #Core attributes 
        self.pressed = False
        self.elevation = elevation
        self.dynamic_elecation = elevation
        self.original_y_pos = pos[1]

        # top rectangle 
        self.top_rect = pygame.Rect(pos,(width,height))
        self.top_color = colors.GREEN
        
        # bottom rectangle 
        self.bottom_rect = pygame.Rect(pos,(width,height))
        self.bottom_color = '#458B00'
        #text
        self.text = text
        self.text_surf = font.render(text,True,colors.WHITE)
        self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)
        Button.buttons.append(self)

    def draw(self):
        # elevation logic 
        self.top_rect.y = self.original_y_pos - self.dynamic_elecation
        self.text_rect.center = self.top_rect.center 

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elecation

        pygame.draw.rect(window,self.bottom_color, self.bottom_rect,border_radius = 12)
        pygame.draw.rect(window,self.top_color, self.top_rect,border_radius = 12)
        window.blit(self.text_surf, self.text_rect)

    # draw buttons & retrieve bot dictonary
    def buttons_draw(self):
        global dict_info
        for b in Button.buttons:
            b.draw()
            b.check_click()

    # drop previous used buttons
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

    def check_click(self): # check which button i click, the do the respective action
        global FRAME_DELAY, OBSTACLES, X_BLOCKS, Y_BLOCKS, dict_info
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):# mouse ontop the button
            self.top_color = colors.ORANGE
            if pygame.mouse.get_pressed()[0]: # if i've pressed the mouse it returns true
                #print(pygame.mouse.get_pressed())
                self.dynamic_elecation = 0
                self.pressed = True
                if self.text == 'Human Player': # select the correct dictonary for each player
                    dict_info =  {
                        "type": dictonary["type"][0],
                        "color": dictonary["color"][0],
                        "start_location": dictonary["start_location"]
                    }     
                    Button.choise_made = 'human'
                    FRAME_DELAY = 85
                elif self.text == 'Bot Player':
                    dict_info =  {
                        "type": dictonary["type"][1],
                        "color": dictonary["color"][1],
                        "start_location": dictonary["start_location"]
                    }            
                    Button.choise_made = 'bot' 
                elif self.text == 'Greedy search':             
                    dict_info = {
                        "type": dictonary["type"][1],
                        "color": dictonary["color"][1],
                        "start_location": dictonary["start_location"]
                    }
                    Button.choise_made = 'astar'
                elif self.text == 'Hamilton search':
                    dict_info = {
                        "type": dictonary["type"][2],
                        "color": dictonary["color"][2],
                        "start_location": dictonary["start_location"]
                    }
                    Button.choise_made = 'hamilton'
                elif self.text == "Yes":
                    Button.choise_made = True
                    return "yes"
                elif self.text == "No":
                    Button.choise_made = True
                    return "no"
                elif self.text == "Cross": #select the obstacles configuration
                    OBSTACLES = 0
                elif self.text == "Blocks & walls":
                    OBSTACLES = 1
                elif self.text == "Tunnel":
                    OBSTACLES = 2
                elif self.text == "Spiral":
                    OBSTACLES = 3
                elif self.text == "None":
                    OBSTACLES = "None"
                elif self.text == "Done":
                    Button.done = True
            else:
                #print(pygame.mouse.get_pressed())
                self.dynamic_elecation = self.elevation
                if self.pressed == True:
                    self.pressed = False
                return 0
        else:
            self.dynamic_elecation = self.elevation
            self.top_color = colors.GREEN
            return 0

""" class that implements input box in the game """
class InputBox:

    def __init__(self, x, y, w, h, name,text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = colors.GREEN
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False
        self.name = name

    def handle_event(self, event):
        global X_BLOCKS,Y_BLOCKS
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = colors.ORANGE if self.active else colors.GREEN
        if event.type == pygame.KEYDOWN:
            if self.active:
                for value in [i for i in range(10)]:
                    if event.unicode == str(value):
                        self.text += event.unicode
                        if self.name == "X":
                            X_BLOCKS = int(self.text)
                        elif self.name == "Y":
                            Y_BLOCKS = int(self.text)
                        else: print("error: no such input box")
                #self.text = ''
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)

# start-game option configuration menu
def snake_interface():
    global OBSTACLES
    button1 = Button('Human Player',300,70,(50,300),5)
    button2 = Button('Bot Player',300,70,(360,300),5)
    # choose human/bot configuratioin
    while not button1.choise_made:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        window.fill('#000000')
        button1.buttons_draw()
        text = font.render('How do you want to play?', True, colors.WHITE)
        window.blit(text, (95, 170))
        pygame.display.update()
        clock.tick(60)
    button2.pressed_buttons()
    pygame.display.update()
    pygame.time.delay(200)
    button1.clear_buttons()

    # choose which bot to use
    button2_1 = Button('Greedy search',310,70,(40,300),5)
    button3_1 = Button('Hamilton search',310,70,(370,300),5)
    while button2_1.choise_made == 'bot': #loop only if have selected bot previously
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        window.fill('#000000')
        button2_1.buttons_draw()
        text = font.render('Which bot do you prefer?', True, colors.WHITE)
        window.blit(text, (105, 170))
        pygame.display.update()
        clock.tick(60)
    if button2_1.choise_made != 'human':
        button3_1.pressed_buttons()
    pygame.display.update()
    pygame.time.delay(200)
    button2_1.clear_buttons()
    #choose obstacles configuration
    button3 = Button('Cross',300,70,(50,250),5)
    button4 = Button('Blocks & walls',300,70,(360,250),5)
    button5 = Button('Tunnel',300,70,(50,350),5)
    button6 = Button('Spiral',300,70,(360,350),5)
    button7 = Button('None',300,70,(185,450),5)

    while OBSTACLES == "to_be_setup":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        window.fill('#000000')
        button3.buttons_draw()
        text = font.render('Which obstacles configuration', True, colors.WHITE)
        text1 = font.render(' do you prefer?',True, colors.WHITE)
        window.blit(text, (70, 120))
        window.blit(text1, (190, 170))
        pygame.display.update()
        clock.tick(60)
    button4.pressed_buttons()
    pygame.display.update()
    pygame.time.delay(200)
    #drop previous used buttons
    button3.clear_buttons()

    # choose grid dimension if no obstacles selected
    input_box1 = InputBox(window.get_size()[0]/10, window.get_size()[1]/3*1.5, 140, 32, "X")
    input_box2 = InputBox(window.get_size()[0]/10*6, window.get_size()[1]/3*1.5, 140, 32, "Y")
    input_boxes = [input_box1, input_box2]
    button7 = Button('Done',300,70,(185,500),5)
    #global done
    while not Button.done and OBSTACLES == "None": #loop only if i've selectd no obstacles
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
        text = font.render('Insert the grid dimensions in', True, colors.WHITE)
        text4 = font.render('the rectangles and press enter.',True,colors.WHITE)
        text1 = font.render('At the end press the button.',True, colors.WHITE)
        window.blit(text, (window.get_size()[0]/12*1.5, window.get_size()[1]/12))
        window.blit(text4, (window.get_size()[0]/12, window.get_size()[1]/12*2))
        window.blit(text1,(window.get_size()[0]/12*1.5, window.get_size()[1]/12*3))
        text2 = font.render('X', True, colors.WHITE)
        text3 = font.render('Y',True, colors.WHITE)
        window.blit(text2, (window.get_size()[0]/10*2.2, window.get_size()[1]/3*1.2))
        window.blit(text3, (window.get_size()[0]/10*7.3, window.get_size()[1]/3*1.2))
        pygame.display.flip()
        clock.tick(30)
    if OBSTACLES == "None":
        button7.pressed_buttons()
    pygame.display.update()
    button7.clear_buttons()

# window that appears in the endgame, it asks if you want to play again at the same game
def new_game():
    button10 = Button('Yes',window.get_size()[0]/4,window.get_size()[1]/10,(window.get_size()[0]/10*2, window.get_size()[1]/2),5)
    button20 = Button('No',window.get_size()[0]/4,window.get_size()[1]/10,(window.get_size()[0]/10*5.5, window.get_size()[1]/2),5)
    Button.choise_made = False
    while not button10.choise_made:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        window.fill('#000000')
        button10.draw_new_game()
        text = font.render('Do you want to play again?', True, colors.WHITE)
        window.blit(text, (window.get_size()[0]/9*1.2, window.get_size()[1]/4))
        pygame.display.update()
        clock.tick(60)
    button20.pressed_buttons()
    pygame.display.update()
    pygame.time.delay(200)
    button10.clear_buttons()

# halt if the grid dimensions are not allowed for hamilton bot
def grid_not_allowed():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            window.fill('#000000')
            text = font.render("Grid dimensions not allowed,", True, colors.WHITE)
            text2 = font.render(" please try again", True,colors.WHITE )
            window.blit(text, (window.get_size()[0]/10, window.get_size()[1]/4))
            window.blit(text2, (window.get_size()[0]/4,window.get_size()[1]/2))
            pygame.display.update()
            clock.tick(60)