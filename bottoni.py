import pygame, sys
import copy
#from main import *

scelta = False
buttons = []
dict_info=[]

# colori migliori trovati nel mondo
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 190, 80)
BLUE = (0, 0, 255)
FUXIA = (255, 0, 100)
PINK = (255, 105, 180)

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
                if self.text == 'Single Player':
                    info = [
                        {
                            "type": "sbot",  # human - sbot - mbot
                            "color": PINK,
                            "start_location": "top-left",
                            "keys": {
                                "up": pygame.K_UP,
                                "down": pygame.K_DOWN,
                                "right": pygame.K_RIGHT,
                                "left": pygame.K_LEFT
                                    } 
                        },
                        ]
                   # print(len(dict_info))
                    scelta = 'singleplayer'
                    return info
                else:
                    info = [
                            {   
                                "type": "bot",
                                "color": GREEN,
                                "scelta":"singleplayer",
                                "start_location": "top-left",
                                "keys": {
                                    "up": pygame.K_UP,
                                    "down": pygame.K_DOWN,
                                    "right": pygame.K_RIGHT,
                                    "left": pygame.K_LEFT
                                }
                            },
                            {
                                "type": "bot",
                                "color": BLUE,
                                "start_location": "bottom-right",
                                "keys": {
                                    "up": pygame.K_UP,
                                    "down": pygame.K_DOWN,
                                    "right": pygame.K_RIGHT,
                                    "left": pygame.K_LEFT
                                }
                            }
                        ]
                    scelta = 'multiplayer'
                    return info 
                #probabilmente questo else non serve
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
    for b in buttons:
        b.draw()
        if b.check_click() != 0 :
            for li in b.check_click():
                d2 = copy.deepcopy(li)
                dict_info.append(d2)
            
### inizio il gioco come in main ###
pygame.init()
window = pygame.display.set_mode((700,700))
pygame.display.set_caption('Snake')
clock = pygame.time.Clock()
font = pygame.font.SysFont('Arial', 40, True)
###
#parte da aggiungere
#creo i bottoni che mi servono
button1 = Button('Single Player',300,70,(50,300),5)
button2 = Button('Multiplayer',300,70,(360,300),5)

while not scelta:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    window.fill('#DCDDD8')
    buttons_draw()
    pygame.display.update()
    clock.tick(60)
for b in buttons:
        b.draw()
pygame.display.update()