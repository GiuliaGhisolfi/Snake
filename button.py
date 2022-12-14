import pygame, sys
import colors

pygame.init()
window = pygame.display.set_mode((700,700))
pygame.display.set_caption("Snake")
font = pygame.font.SysFont('Arial', 40, True)
clock = pygame.time.Clock()

scelta = False
buttons = []
dict_info_single = {}

class Button:
    def __init__(self,text,width,height,pos,elevation):
        #Core attributes 
        self.pressed = False
        self.elevation = elevation
        self.dynamic_elecation = elevation
        self.original_y_pos = pos[1]

        # top rectangle 
        self.top_rect = pygame.Rect(pos,(width,height))
        self.top_color = '#475F77'
        
        # bottom rectangle 
        self.bottom_rect = pygame.Rect(pos,(width,height))
        self.bottom_color = '#354B5E'
        #text
        self.text = text
        self.text_surf = font.render(text,True,'#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center = self.top_rect.center)
        buttons.append(self)

    def draw(self):
        # elevation logic 
        self.top_rect.y = self.original_y_pos - self.dynamic_elecation
        self.text_rect.center = self.top_rect.center 

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elecation

        pygame.draw.rect(window,self.bottom_color, self.bottom_rect,border_radius = 12)
        pygame.draw.rect(window,self.top_color, self.top_rect,border_radius = 12)
        window.blit(self.text_surf, self.text_rect)

    def check_click(self):
        global scelta 
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = '#D74B4B'
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elecation = 0
                self.pressed = True
                if self.text == 'Human Player':
                    info_human =  {
                                "type": "human",  # human - sbot - mbot
                                "color": 'orange',
                                "start_location": "top-left",
                                "keys": {
                                    "up": pygame.K_UP,
                                    "down": pygame.K_DOWN,
                                    "right": pygame.K_RIGHT,
                                    "left": pygame.K_LEFT
                                        } 
                            }       
                    scelta = 'human'
                    return info_human
                elif self.text == 'Bot Player':
                    info_bot =  {
                                "type": "sbot",  # human - sbot - mbot
                                "color": colors.PINK,
                                "start_location": "top-left",
                                "keys": {
                                    "up": pygame.K_UP,
                                    "down": pygame.K_DOWN,
                                    "right": pygame.K_RIGHT,
                                    "left": pygame.K_LEFT
                                        } 
                            }            
                    scelta = 'bot'
                    return info_bot  
                elif self.text == 'A* search':             
                    info_bot = {
                              "type": "sbot",  # human - sbot - mbot
                                "color": colors.BLUE,
                                "start_location": "top-left",
                                "keys": {
                                    "up": pygame.K_UP,
                                    "down": pygame.K_DOWN,
                                    "right": pygame.K_RIGHT,
                                    "left": pygame.K_LEFT
                                        } 
                    }
                    scelta = 'astar'
                    return info_bot
                elif self.text == 'Hamilton search':
                    info_bot = {
                               "type": "sbot",  # human - sbot - mbot
                                "color": colors.GREEN,
                                "start_location": "top-left",
                                "keys": {
                                    "up": pygame.K_UP,
                                    "down": pygame.K_DOWN,
                                    "right": pygame.K_RIGHT,
                                    "left": pygame.K_LEFT
                                        } 
                    }
                    scelta = 'hamilton'
                    return info_bot
                elif self.text == "Yes":
                    scelta = True
                    return 'yes'
                elif self.text == "No":
                    scelta = True
                    return 'no'
            else:
                self.dynamic_elecation = self.elevation
                if self.pressed == True:
                    self.pressed = False
                return 0
        else:
            self.dynamic_elecation = self.elevation
            self.top_color = '#475F77'
            return 0

#disegno i bottoni
def buttons_draw():
    global dict_info_single
    for b in buttons:
        b.draw()
        if b.check_click() != 0 :
            dict_info_single = b.check_click()

def draw_new_game():
    for b in buttons:
        b.draw()
        if b.check_click() == 'no':
            exit()
            
### inizio il gioco come in main ###
#pygame.init()
#window = pygame.display.set_mode((700,700))
#pygame.display.set_caption('Snake')

###
def snake_interface():
    global scelta
    scelta = False
    
    button1 = Button('Human Player',300,70,(50,300),5)
    button2 = Button('Bot Player',300,70,(360,300),5)

    while not scelta:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        window.fill('#000000')
        buttons_draw()
        pygame.display.update()
        clock.tick(60)
    for b in buttons:
        b.draw()
    pygame.display.update()
    pygame.time.delay(200)

    buttons.pop(0)
    buttons.pop(0)

    button3 = Button('A* search',310,70,(40,300),5)
    button4 = Button('Hamilton search',310,70,(370,300),5)

    while scelta == 'bot':
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        window.fill('#000000')
        buttons_draw()
        pygame.display.update()
        clock.tick(60)
    for b in buttons:
        b.draw()
    pygame.display.update()
    buttons.pop(0)
    buttons.pop(0)

def new_game():
    global scelta
    scelta = False
   
    button1 = Button('Yes',300,70,(50,300),5)
    button2 = Button('No',300,70,(360,300),5)

    while not scelta:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        window.fill('#000000')
        draw_new_game()
        text = font.render('Do you want to play again?', True, colors.RANDOM)
        window.blit(text, (95, 170))
        pygame.display.update()
        clock.tick(60)
    for b in buttons:
        b.draw()
    pygame.display.update()
    pygame.time.delay(200)

    buttons.pop(0)
    buttons.pop(0)
