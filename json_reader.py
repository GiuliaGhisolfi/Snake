import json
import numpy as np

logfiles = ['.\dati_hamilton\log1.json'] # aggiungiamo i log di tutti (relativi a una specifica configurazione, 1 sta per config1)
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
	max_len = iterations[-1,-1] # if == grid_area => win
	print("Execution %d	n_iterations=%d	mean_time=%.6f	total_time=%.6f	max_len=%d"
	%(i+1, len(exec), mean_time, total_time, max_len))
	# media di tutti i tempi, media massimo numero di iterazioni, lunghezza media finale