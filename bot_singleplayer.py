import threading
from directions import Directions
from player import Player
from search import *
import copy

import grid
import snake
import food
import obstacles
from grid_problem import *
from bottoni import *

FIRST_IT_C = RED
TO_FOOD_C = ORANGE
DEF_C = BLUE

def delete_cell(grid, del_key):
    grid.pop(del_key, None)
    for key in grid:
        grid[key].pop(del_key, None)

def coordinates2cell(x, y, bsize):
    return "(%d,%d)" % (x/bsize, y/bsize)

# restituisce la posizione della cella targhet rispetto alla cella head
def graphDir_to_gameDir(head_pos, target_pos):
    headPosList = head_pos[1:-1].split(',')
    targetPosList = target_pos[1:-1].split(',')

    if int(targetPosList[0]) < int(headPosList[0]):  # x shift
        ret = Directions.LEFT
    elif int(targetPosList[0]) > int(headPosList[0]):
        ret = Directions.RIGHT
    elif int(targetPosList[1]) < int(headPosList[1]):  # y shift
        ret = Directions.UP
    else:
        ret = Directions.DOWN

    return ret

def build_location(grid):
    locations = {}
    for key in grid:
        sL = key.replace('(', '').replace(')','').split(',')
        locations[key]=(int(sL[0]), int(sL[1]))
    return locations


class Bot_singleplayer(Player):
    # input anche lo snake
    def __init__(self, grid: grid.Grid, snake: snake.Snake, food:food.Food, obstacles:obstacles.Obstacles, debug=False):

        self.grid = grid
        self.locations = build_location(self.grid.grid) #immutabile
        self.debug = debug
        self.obstacles = obstacles
        self.snake = snake
        #self.snake_body = self.snake.get_body()
        
        self.food = food
        #self.prec_food_position = self.food.get_positions() #vuota così che dopo start calcola subito
        
        if len(self.snake.get_body()) < 3:
            print('LUNGHEZZA MINIMA SUPPORTATA: 3')
            exit() #boom

        self.default_path = None
        self.path_to_food = None

        #strategia attuale
        self.chosen_strat = self.mela_cicle_strat
        self.chosen_search = 0 #magari utile

        self.nnto = '' #next node to optimize


    #PER CAMBIATE LA CHIAMATA DU FUNZIONE AD A* O COSE SIMILI CAMBIARE QUESTA FUNZIONE E self.chosen_search
    def graph_search(self, start, goal, graph):
        graph = Graph(graph) 
        graph.locations = self.locations

        if self.chosen_search == 0:
            grid_problem = GridProblem(start, True, goal, graph)
            dummy = astar_search_min_turns(grid_problem)

            if dummy != None:
                return dummy.solution()
            else: return dummy

        else:
            print('Strategia ancora non implementata!!')
            exit()
    
    #TODO: magari attuare questa strategia solo se abbastanza lunghi?
    def optimize_standard_path(self, tg={}):
        #i dizionari sono valutati false se vuoti
        
        #restituisce il numero di archi uscenti che non conducono in nodi occupati o presenti
        #in defaulth path
        def get_neighbors_n(node, true_graph):

            caselle_vicine = true_graph[node]
            tot_n = 0
            #chiavi
            for c in caselle_vicine:
                if not c in self.default_path:
                    tot_n += 1

            return tot_n
        def is_optimizable(node, true_graph):
            return get_neighbors_n(node, true_graph) > 0
        def is_chokepoint(node, true_graph):
            return get_neighbors_n(node, true_graph) == 0
        def get_ham_path(start, goal, graph):
            return None
        
        
        #definiamo tg se non già fatto
        if not tg:
            tg = self.get_true_graph(self.snake.fast_get_body()[:-1])

        if self.nnto == self.snake.fast_get_body()[-1]: #next node to optimize
            if is_optimizable(self.snake.fast_get_body()[-1], tg):
                tg = self.get_true_graph([self.snake.fast_get_body()[-1]], tg)
                #cerchiamo il prossimo choke point
                chokepoint = ''
                for c in self.default_path[:-1]:
                    if is_chokepoint(c, tg):
                        chokepoint = c
                        break
                
                if chokepoint != '':
                    true_g = self.get_true_graph(self.snake.fast_get_body()[:-1])
                    choke_ind = self.default_path.index(chokepoint)
                    to_remove = []
                    if len(self.default_path) > choke_ind + 2:
                        to_remove = self.default_path[choke_ind + 1:-1]
                    true_g = tg = self.get_true_graph(to_remove, true_g)

                    #senza testa
                    patch = get_ham_path(self.snake.fast_get_body()[-1], chokepoint, true_g)
                    self.default_path = patch + self.default_path[choke_ind + 1:]

                    print('Ottimizzato')
            else:
                tg = self.get_true_graph(self.snake.fast_get_body()[-1:], tg) #solo ultima posizione
                #calcoliamo il prossimo nodo che è ottimizzabile
                for node in self.default_path:
                    if is_optimizable(node,tg):
                        #se lo troviamo, lo salviamo e terminiamo
                        self.nnto = node
                        return
                        
                
    '''
    def mela_cicle_strat(self):
        # prima iterazione va fatta sempre ed è safe, non succedono cose strane
        snake_body = self.snake.get_body()

        # posizione mela migliore e testa snake
        goal = self.get_best_food()
        start = snake_body[-1]

        #elimino tutto il corpo tranne la testa del serpente dal grafo
        dummy_g = self.get_true_graph(snake_body[:-1])
        graph = Graph(dummy_g) 
        graph.locations = self.locations
        
        #calcolo percorso migliore tra testa e mela
        grid_problem = GridProblem(start, False, goal, graph)
        computed_path_toFood = astar_search_min_turns(grid_problem).solution() #esiste il primo, per forza
       
        #aggiornando il grafo con la posizione futura
        next_pos = (snake_body + computed_path_toFood)[-len(snake_body) - 1:]
        goal = next_pos[0] #futura coda
        start = next_pos[-1] #futura testa

        #ora calcoliamo dalla mela (mangiata) alla coda, elimino coda e testa dello snake
        dummy_g = self.get_true_graph(next_pos[1:-1])
        graph = Graph(dummy_g) 
        graph.locations = self.locations
        grid_problem = GridProblem(start, False, goal, graph)
        computed_cicle = astar_search_min_turns(grid_problem).solution() #esiste il primo, per forza

        self.default_path = computed_cicle + next_pos[1:] #ciclo privo di rischi
        self.path_to_food = computed_path_toFood #path verso la mela, da percorrere prima di usare default path
        
        #la mossa è stata presa, aggiorniamo
        #calcolo direzione verso la mela
        move = graphDir_to_gameDir(self.snake_body[-1], self.path_to_food[0]) 
        self.path_to_food.pop(0)
        self.lock.acquire()
        self.next_move = move
        self.lock.release()


        skipWait = False
        #ora inizia la parte difficile, qui possono accadere cose strane (strande inesistenti ecc...)
        while not self.termination:   
            if not skipWait:
                self.lock.acquire()
                calcola = True
                try:
                    self.condition.wait() # soltanto per capire quando controllare se default path ancora buono
                    if self.next_move != None: print('QUALCOSA DI STRANO E\' ACCADUTO') #???? non dovrebbe

                    self.snake_body = self.snake.get_body()
                    
                    if len(self.path_to_food) > 0: #non siamo ancora arrivati alla mela
                        move = self.path_to_food.pop(0)
                        self.next_move = graphDir_to_gameDir(self.snake_body[-1], move)
                        calcola = False
                    else: #abbiamo raggiunto il cibo, ora diamo una direzione safe e cerchiamo la prossima strada
                        #TODO dobbiamo forse compattare il serpente già da qui?
                        move = self.default_path.pop(0)
                        self.next_move = graphDir_to_gameDir(self.snake_body[-1], move) # è un ciclo
                        self.default_path.append(move)

                finally: self.lock.release()
            skipWait = False

            if calcola:
                # cerchiamo una strada migliore per il cibo
                self.prec_food_position = self.food.get_positions() # TODO: si può migliorare sto schifo??
                goal = self.get_best_food()
                start = self.snake_body[-1]
                # elimino tutto il corpo tranne la testa dello snake dal grafo 
                graph = Graph(self.get_true_graph(self.snake_body[:-1]))
                graph.locations = self.locations
                #calcolo percorso tra TESTA e nuova MELA
                grid_problem = GridProblem(start, False, goal, graph)
                search_tree = astar_search_min_turns(grid_problem) #esiste il primo, per forza
                if search_tree != None: #trovato il primo
                    computed_path_toFood = search_tree.solution() #path
                    #ora calcoliamo dalla MELA alla CODA
                    # TODO provare a cambiare strategia per schiacciare lo snake su se stesso il più possibile
                    #aggiornando il grafo con la posizione futura
                    next_pos = (self.snake_body + computed_path_toFood)[-len(self.snake_body) - 1:]
                    goal = next_pos[0] #futura coda
                    start = next_pos[-1] #futura testa
                    #mantengo solo i nodi con testa e coda dello snake nel grafo
                    dummy_g = self.get_true_graph(next_pos[1:-1])
                    graph = Graph(dummy_g) 
                    graph.locations = self.locations
                    grid_problem = GridProblem(start, False, goal, graph)
                    search_tree = astar_search_min_turns(grid_problem) #esiste il primo, per forza
                    if search_tree != None: #incredibile !!! trovato anche il secondo, abbiamo finito allora
                        computed_cicle = search_tree.solution()

                        self.default_path = computed_cicle + next_pos[1:] #ciclo privo di rischi
                        self.path_to_food = computed_path_toFood #path verso la mela, da percorrere prima di usare default path
                    else: #non siamo sicuri del persorso futuro, non facciamo nulla
                        continue
                else:
                    continue #male male!! niente strada verso la mela
                

                #se siamo arrivati qui allora, abbiamo 2 percorsi
                self.lock.acquire()
                try:
                    if self.next_move != None: #abbiamo fatto in tempo !!!
                        move = self.path_to_food.pop(0)
                        self.next_move = graphDir_to_gameDir(self.snake_body[-1], move)
                        #TODO: aggiungere un meccanismo di recupero, magari aspettando un giro intero???
                    else: #siamo stati lenti, aiai
                        print('STRADA TROVATA, BOT TROPPO LENTO!!!')
                        move = self.default_path.pop(0)
                        self.next_move = graphDir_to_gameDir(self.snake_body[-1], move) # è un ciclo
                        self.default_path.append(move)

                        skipWait = True
                finally: self.lock.release()
    '''

    #TODO: creare una scelta sensata tra le mele ?????
    def get_best_food(self):
        return self.food.get_positions()[0] #una mela a caso, per ora
    
    def get_true_graph(self, snake_false_body, grid={}):
        if not grid:
            grid = self.grid.grid # da controllare

        #eliminiamo dal grafo le celle occupate da noi
        new_grid = copy.deepcopy(self.grid.grid) #forse ci va messo grid?

        for segment in snake_false_body: #manca la testa
            delete_cell(new_grid, segment)
        for pos in self.obstacles.positions:
            str_pos = "(%d,%d)" % (pos[0], pos[1])
            delete_cell(new_grid, str_pos)
        return new_grid

    def change_color(self):
        if self.debug:
            if len(self.path_to_food) > 0:
                self.snake.color = TO_FOOD_C
            else:
                self.snake.color = DEF_C

    # funzione usata per chiedere la prossima mossa dello snake
    def mela_cicle_strat(self):

        # inizio e basta
        if self.default_path == None and self.path_to_food == None:

            if self.debug:
                self.snake.color = FIRST_IT_C 
            
            snake_body = self.snake.get_body()

            # posizione mela migliore e testa snake
            goal = self.get_best_food()
            start = snake_body[-1]

            #elimino tutto il corpo tranne la testa del serpente dal grafo
            dummy_g = self.get_true_graph(snake_body[:-1])
            computed_path_toFood = self.graph_search(start, goal, dummy_g)
        
            #aggiornando il grafo con la posizione futura
            next_pos = (snake_body + computed_path_toFood)[-len(snake_body) - 1:]
            goal = next_pos[0] #futura coda
            start = next_pos[-1] #futura testa

            #ora calcoliamo dalla mela (mangiata) alla coda, elimino coda e testa dello snake
            dummy_g = self.get_true_graph(next_pos[1:-1])
            computed_cicle = self.graph_search(start, goal, dummy_g)

            self.default_path = computed_cicle + next_pos[1:] #ciclo privo di rischi
            self.nnto = self.default_path[0]
            self.path_to_food = computed_path_toFood #path verso la mela, da percorrere prima di usare default path
            
            #la mossa è stata presa, aggiorniamo
            #calcolo direzione verso la mela
            c = self.path_to_food.pop(0)
            return graphDir_to_gameDir(snake_body[-1], self.path_to_food[0]) 

        snake_body = self.snake.get_body()
        self.change_color()
        
        #ora inizia la parte difficile, qui possono accadere cose strane (strande inesistenti ecc...)       
        if len(self.path_to_food) > 0: #non siamo ancora arrivati alla mela
            move = self.path_to_food.pop(0)
            return graphDir_to_gameDir(snake_body[-1], move)

 
        # posizione mela migliore e testa snake
        goal = self.get_best_food()
        start = snake_body[-1]

        #elimino tutto il corpo tranne la testa del serpente dal grafo
        dummy_g = self.get_true_graph(snake_body[:-1])
        #restituisce il cammino se esiste, più pulito di prima
        computed_path_toFood = self.graph_search(start, goal, dummy_g)

        if computed_path_toFood != None: #trovato il primo
            #uguale a prima con una accortezza di differenza
            next_pos = (snake_body + computed_path_toFood)[-len(snake_body) - 1:]
            goal = next_pos[0] #futura coda
            start = next_pos[-1] #futura testa
            dummy_g = self.get_true_graph(next_pos[1:-1]) #non eliminiamo la coda
            computed_cicle = self.graph_search(start, goal, dummy_g)

            if computed_cicle != None: #incredibile !!! trovato anche il secondo, abbiamo finito allora
                self.default_path = computed_cicle + next_pos[1:] #ciclo privo di rischi
                self.nnto = self.default_path[0]
                self.path_to_food = computed_path_toFood #path verso la mela, da percorrere prima di usare default path

                move = self.path_to_food.pop(0)
                return graphDir_to_gameDir(snake_body[-1], move)

        self.optimize_standard_path()
        move = self.default_path.pop(0)
        ret = graphDir_to_gameDir(snake_body[-1], move) # è un ciclo
        self.default_path.append(move)
        return ret

    def get_next_move(self):
        return self.chosen_strat()
    
