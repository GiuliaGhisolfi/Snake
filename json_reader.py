import json
import numpy as np

# deve leggere l'area della griglia per capire se ha vinto

# aggiungiamo una lista simile a sotto i log di tutti (relativi a una specifica configurazione, 1 sta per config1)
# di seguito concatena configurazioni diverse giusto per vedere se funziona

# dalla cartella dei file di ogniuno estrapoliamo la configurazione che vogliamo analizzare
# il ciclo for sotto serve per verificare hamilton abbia sempre vinto
# da data creiamo due matrici:
# iterations_time = [ [tempi primo gioco], [secondo], ... ]
# snake_length = [ [lung. primo gioco], [secondo], ... ]


logfiles = ['./hamilton_results/log1.json', './hamilton_results/log2.json', './hamilton_results/log3.json',
            './hamilton_results/log4.json', './hamilton_results/log5.json', './hamilton_results/log6.json',
            './hamilton_results/log7.json', './hamilton_results/log8.json', './hamilton_results/log9.json',
            './hamilton_results/log10.json', './hamilton_results/log1.json']

"""logfiles = ['./greedy_results/log1.json', './greedy_results/log2.json', './greedy_results/log3.json',
            './greedy_results/log4.json', './greedy_results/log5.json', './greedy_results/log6.json', 
            './greedy_results/log7.json']"""
data = []
for file in logfiles:
    f = open(file)
    data += json.load(f)
    f.close()

print("N executions: %d" % len(data))
for i, exec in enumerate(data):
    iterations = np.array(exec)
    mean_time = np.mean(iterations, axis=0)[0]
    total_time = np.sum(iterations, axis=0)[0]
    max_len = iterations[-1, -1]  # if == grid_area => win
    print("Execution %d	n_iterations=%d	mean_time=%.6f	total_time=%.6f	max_len=%d"
          % (i+1, len(exec), mean_time, total_time, max_len))
    # media di tutti i tempi, media massimo numero di iterazioni, lunghezza media finale
    