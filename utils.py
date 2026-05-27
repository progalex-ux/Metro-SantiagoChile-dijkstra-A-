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
