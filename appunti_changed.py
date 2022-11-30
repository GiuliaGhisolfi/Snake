# if nn_idx in [n1_coll, head] -> do nothing

# if nn_idx in [node, n2_coll] -> nn_idx -= (node_idx - head_idx - 1)

# if nn_idx in [n2, (node - 1)] -> nn_idx = n2_coll_prec - (node_idx - head_idx - 1) + (nn_idx - n2_coll_prec)
                                        # = nn_idx - node_idx + head_idx + 1

# if nn_idx in [head + 1, n1] -> nn_idx = (node - 1)_idx + delta
                # delta = 1 + "distanza tra head + 1 e nn"
                # "distanza tra head + 1 e nn" = nn_idx - (head + 1)_idx
                               # nn_idx = (node - 1)_idx + 1 + nn_idx - (head + 1)_idx
                               #        = node_idx - 1 + 1 + nn_idx - head_idx + 1
                               #        = nn_idx + node_idx - head_idx + 1

# attenzione che devo lavorare con le distanze relative -> negli if devo mettere (% self.grid_area) !!!                               
for nn in self.ham_cycle:
    value = self.ham_cycle[nn]
    
    # nn_idx in [node, n2_coll]
    if value in range(n1_coll_idx, head_idx + 1):
        self.ham_cycle[nn] = (value - node_idx + head_idx + 1) % self.grid_area
    
    # nn_idx in [n2, (node - 1)]
    if value in range(n2_idx, node_idx):
        self.ham_cycle[nn] = (value - node_idx + head_idx + 1) % self.grid_area
        
    # nn_idx in [head + 1, n1]
    if value in range(n2_idx, node_idx):
        self.ham_cycle[nn] = (value + node_idx - head_idx + 1) % self.grid_area
        
        
# stampo chiavi
# rifaccio il diagramma come volevo io

position = np.array( list(self.ham_cycle.values()) )
            position -= head_idx # head in first position
            
            count = 1
            incr1 = 0
            incr2 = 1
            
            while count < n2_coll_pos + 1:
                for i in range(position.size):
                    if count in range(node_pos, n2_coll_pos + 1): # nn_idx in [node, n2_coll]
                        if i == node_pos + count - 1:
                            position[i] = count
                            count += 1
            
            while count < node_pos:
                for i in range(position.size):
                    if count in range(n2_pos, node_pos): # nn_idx in [n2, (node - 1)]
                        if i == n2_pos + incr1:
                            position[i] = count
                            count += 1
                            incr1 +=1
            
            while count < n1_pos + 1:
                for i in range(position.size):
                    if i in range(1, n1_pos + 1): # nn_idx in [head + 1, n1]
                        if i == incr2:
                            position[i] = count
                            count += 1
                            incr2 +=1
            
            idx = 0
            
# nuovo ciclo:
            # head -> node -> (nodi tra node e n2_coll) -> (nodi tra n2 e (node-1)) ->
            # (nodi tra (head+1) e n1) -> (nodi tra n1_coll e (head-1))