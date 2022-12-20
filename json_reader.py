import json
import numpy as np

# deve leggere l'area della griglia per capire se ha vinto

# aggiungiamo una lista simile a sotto i log di tutti (relativi a una specifica configurazione, 1 sta per config1)
# di seguito concatena configurazioni diverse giusto per vedere se funziona

logfiles = ['./hamilton_data/log1.json', './hamilton_data/log2.json', './hamilton_data/log3.json',
            './hamilton_data/log4.json', './hamilton_data/log5.json', './hamilton_data/log6.json', 
            './hamilton_data/log7.json', './hamilton_data/log8.json', './hamilton_data/log9.json',
            './hamilton_data/log10.json', './hamilton_data/log1.json']

"""logfiles = ['./greedy_data/log1.json', './greedy_data/log2.json', './greedy_data/log3.json',
            './greedy_data/log4.json', './greedy_data/log5.json', './greedy_data/log6.json', 
            './greedy_data/log7.json']"""
data = []
for file in logfiles:
	f = open(file)
	data += json.load(f)
	f.close()

print("N executions: %d"%len(data))
for i, exec in enumerate(data):
	iterations = np.array(exec)
	mean_time = np.mean(iterations, axis=0)[0]
	total_time = np.sum(iterations, axis=0)[0]
	max_len = iterations[-1, -1] # if == grid_area => win
	print("Execution %d	n_iterations=%d	mean_time=%.6f	total_time=%.6f	max_len=%d"
	%(i+1, len(exec), mean_time, total_time, max_len))
	# media di tutti i tempi, media massimo numero di iterazioni, lunghezza media finale