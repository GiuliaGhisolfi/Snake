def change_cycle(self):
    # considero solo celle del path tra self.head e self.goal
    head_idx = self.ham_cycle[self.head]  # valore della testa nel ciclo ham
    goal_idx = self.ham_cycle[self.goal]
    tail_idx = self.ham_cycle[self.body[0]]

    # head_pos = 0    
    goal_pos = (goal_idx - head_idx) % self.grid_area # distanza relativa goal da head su ham_cycle
    tail_pos = (tail_idx - head_idx) % self.grid_area

    if abs(goal_idx - head_idx) > 3 and goal_pos < tail_pos:
        # cerco di fare dei tagli, else pass:        
        # considero i nodi tra testa e goal
        # se trovo un nodo tra i value di head in grid tale che
        # (goal_idx > self.ham_cycle[nodo] > head_idx + 1)
        # -> considero tutti i nodi t.c index in (head_idx, nodo-idx)
        # ne cerco due : n1, n2 t.c.
        # n1_idx == n2_idx - 1 (successivi rispetto all'indice in ham_cycle) AND
        # che siano collegati in grid con due nodi successivi tra loro in ham_cycle
        # i.e. n1_coll in grid[n1] AND n2_coll in grid[n2] AND
        # n2_coll_idx == n1_coll_idx      
        for node in self.grid[self.head]:
            node_idx = self.ham_cycle[node]
            
            if node_idx > (head_idx + 1) and node_idx < goal_idx:
                node_pos = (node_idx - head_idx) % self.grid_area 
                
                flag = False
                for n1, n2 in self.ham_cycle:
                    n1_idx = self.ham_cycle[n1]
                    n2_idx = self.ham_cycle[n2]  
                    n1_pos = (n1_idx - head_idx) % self.grid_area  
                    n2_pos = (n2_idx - head_idx) % self.grid_area                 
                    if self.ham_cycle[n2] > self.ham_cycle[n1] + 1: 
                        if n1_pos > 0 and n2_pos < node_pos: 
                            flag = True
                            break
                
                if flag:
                    flag = False
                    for node_coll in self.ham_cycle[node]:
                        node_coll_idx = self.ham_cycle[node_coll]
                        node_coll_pos = (node_coll_idx - head_idx) % self.grid_area
                        if node_coll_pos > node_pos and node_coll_pos > n2_pos: 
                            flag = True
                            break                    
                
                if flag:
                    flag = False        
                    for n1_coll, n2_coll in self.ham_cycle:
                        n1_coll_idx = self.ham_cycle[n1_coll]
                        n2_coll_idx = self.ham_cycle[n2_coll]
                        n1_coll_pos = (n1_coll_idx - head_idx) % self.grid_area 
                        n2_coll_pos = (n2_coll_idx - head_idx) % self.grid_area 
                        if ( n2_coll_pos > node_coll_pos ) and ( n1_coll_pos == (n2_coll_pos + 1) ) and \
                            n2_coll in self.grid[n2] and n1_coll in self.grid[n1]:
                                flag = True
                                break
            if flag: break
            
        # cambio ciclo ham:
        self.ham_cycle[node_coll] = node_idx + 1
        delta = (node_coll_idx - node_idx + 1) % self.grid_area
        
        for nn in self.ham_cycle:
            if self.ham_cycle[nn] > (node_idx + 1) and self.ham_cycle[nn] <= n2_coll_idx:
                self.ham_cycle[nn] = self.ham_cycle[nn] + delta
                
        self.ham_cycle[n2] = self.ham_cycle[n2_coll] + 1
        
        start_invers = self.ham_cycle[n2] + delta
        for nn in self.ham_cycle:
            if self.ham_cycle[nn] > (n2_idx + 1) and self.ham_cycle[nn] <= n1_idx:
                i = (n2_idx - self.ham_cycle[nn]) % self.grid_area
                self.ham_cycle[nn] = start_invers + i # pezzo del ciclo in cui cambio il senso di percorrenza  
                              
        # self.ham_cycle[n1_coll] = self.ham_cycle[n1] + 1 -> rimane uguale da qua in poi
