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


def dijkstra(grafo, inicio, destino):
    distancias = {nodo: float('infinity') for nodo in grafo}
    distancias[inicio] = 0
    
    padres = {nodo: None for nodo in grafo}
    
    cola_prioridad = ColaPrioridad()
    cola_prioridad.push((0, inicio))
    
    while not cola_prioridad.esta_vacia():
        distancia_actual, nodo_actual = cola_prioridad.pop()
        
        if nodo_actual == destino:
            break
            
        if distancia_actual > distancias[nodo_actual]:
            continue
            
        for vecino, peso in grafo[nodo_actual]['vecinos'].items():
            nueva_distancia = distancia_actual + peso
            
            if nueva_distancia < distancias[vecino]:
                distancias[vecino] = nueva_distancia
                padres[vecino] = nodo_actual
                # Insertamos en nuestro Heap para su posterior exploración
                cola_prioridad.push((nueva_distancia, vecino))
                
    ruta = []
    actual = destino
    while actual is not None:
        ruta.insert(0, actual)
        actual = padres[actual]
        
    return ruta, distancias[destino]