import math

class ColaPrioridad:
    def __init__(self):
        self.heap = []

    def push(self, elemento):
        self.heap.append(elemento)
        self._subir_nodo(len(self.heap) - 1)

    def pop(self):
        if not self.heap:
            return None
        if len(self.heap) == 1:
            return self.heap.pop()
        
        raiz = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._bajar_nodo(0)
        
        return raiz

    def _subir_nodo(self, i):
        padre = (i - 1) // 2
        while i > 0 and self.heap[i][0] < self.heap[padre][0]:
            self.heap[i], self.heap[padre] = self.heap[padre], self.heap[i]
            i = padre
            padre = (i - 1) // 2

    def _bajar_nodo(self, i):
        n = len(self.heap)
        izquierdo = 2 * i + 1
        derecho = 2 * i + 2
        menor = i

        if izquierdo < n and self.heap[izquierdo][0] < self.heap[menor][0]:
            menor = izquierdo
        
        if derecho < n and self.heap[derecho][0] < self.heap[menor][0]:
            menor = derecho

        if menor != i:
            self.heap[i], self.heap[menor] = self.heap[menor], self.heap[i]
            self._bajar_nodo(menor)

    def esta_vacia(self):
        return len(self.heap) == 0


def calcular_heuristica(nodo_actual, nodo_destino, grafo):
    lat1, lon1 = grafo[nodo_actual]['coordenadas']
    lat2, lon2 = grafo[nodo_destino]['coordenadas']
    
    return math.sqrt((lat2 - lat1)**2 + (lon2 - lon1)**2) * 100000 


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