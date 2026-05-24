import heapq

def dijkstra(grafo, inicio, destino):
    distancias = {nodo: float('infinity') for nodo in grafo}
    distancias[inicio] = 0
    
    padres = {nodo: None for nodo in grafo}
    
    cola_prioridad = [(0, inicio)]
    
    while cola_prioridad:
        distancia_actual, nodo_actual = heapq.heappop(cola_prioridad)
        
        if nodo_actual == destino:
            break
            
        if distancia_actual > distancias[nodo_actual]:
            continue
            
        for vecino, peso in grafo[nodo_actual]['vecinos'].items():
            nueva_distancia = distancia_actual + peso
            
            if nueva_distancia < distancias[vecino]:
                distancias[vecino] = nueva_distancia
                padres[vecino] = nodo_actual
                heapq.heappush(cola_prioridad, (nueva_distancia, vecino))
                
    ruta = []
    actual = destino
    while actual is not None:
        ruta.insert(0, actual)
        actual = padres[actual]
        
    return ruta, distancias[destino]

