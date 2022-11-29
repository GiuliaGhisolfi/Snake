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
