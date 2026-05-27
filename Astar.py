import math
from  utils import ColaPrioridad

def calcular_heuristica(nodo_actual, nodo_destino, grafo):
    lat1, lon1 = grafo[nodo_actual]['coordenadas']
    lat2, lon2 = grafo[nodo_destino]['coordenadas']
    
    return math.sqrt((lat2 - lat1)**2 + (lon2 - lon1)**2) * 101800



def a_estrella(grafo, inicio, destino):
    g_score = {nodo: float('infinity') for nodo in grafo}
    g_score[inicio] = 0
    
    f_score = {nodo: float('infinity') for nodo in grafo}
    f_score[inicio] = calcular_heuristica(inicio, destino, grafo)
    
    padres = {nodo: None for nodo in grafo}
    
    cola_prioridad = ColaPrioridad()
    cola_prioridad.push((f_score[inicio], inicio))
    
    while not cola_prioridad.esta_vacia():
        f_score_actual, nodo_actual = cola_prioridad.pop()
        
        if nodo_actual == destino:
            break
            
        for vecino, peso in grafo[nodo_actual]['vecinos'].items():
            temp_g_score = g_score[nodo_actual] + peso
            
            if temp_g_score < g_score[vecino]:
                padres[vecino] = nodo_actual
                g_score[vecino] = temp_g_score
                
                f_score[vecino] = temp_g_score + calcular_heuristica(vecino, destino, grafo)
                
                cola_prioridad.push((f_score[vecino], vecino))
                
    ruta = []
    actual = destino
    while actual is not None:
        ruta.insert(0, actual)
        actual = padres[actual]
        
    return ruta, g_score[destino]