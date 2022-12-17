diz = {(9,8): 1, (89,33):2, (5,9):-2}

print(sorted(diz.keys(), key=lambda k: diz[k]))