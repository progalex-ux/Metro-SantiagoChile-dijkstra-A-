import customtkinter as ctk
import json
from dijkstra import dijkstra
from Astar import a_estrella

LINEAS = {
    "L1": "#E4222B",  # Rojo
    "L2": "#FFD000",  # Amarillo
    "L3": "#8B5226",  # Café
    "L4": "#002A8F",  # Azul Oscuro
    "L4A": "#008CC5", # Celeste
    "L5": "#00A859",  # Verde
    "L6": "#B065A9"   # Morado
}

class MetroApp(ctk.CTk):
    def __init__(self, grafo, conexiones):
        super().__init__()

        self.grafo = grafo
        self.conexiones = conexiones 
        self.title("Metro Santiago")
        self.geometry("1280x720")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = ctk.CTkFrame(self, width=250, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        estaciones = sorted(list(self.grafo.keys()))

        self.combo_inicio = ctk.CTkComboBox(self.sidebar, values=estaciones, width=200)
        self.combo_inicio.set("Origen")
        self.combo_inicio.pack(pady=10)

        self.combo_destino = ctk.CTkComboBox(self.sidebar, values=estaciones, width=200)
        self.combo_destino.set("Destino")
        self.combo_destino.pack(pady=10)

        self.algo_var = ctk.IntVar(value=1)
        ctk.CTkRadioButton(self.sidebar, text="Dijkstra", variable=self.algo_var, value=1).pack(pady=5)
        ctk.CTkRadioButton(self.sidebar, text="A*", variable=self.algo_var, value=2).pack(pady=5)

        self.btn_calcular = ctk.CTkButton(self.sidebar, text="Calcular", command=self.dibujar)
        self.btn_calcular.pack(pady=20)

        self.txt_info = ctk.CTkTextbox(self.sidebar, width=220, height=200)
        self.txt_info.pack(pady=20, padx=10)

        self.canvas_frame = ctk.CTkFrame(self)
        self.canvas_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        
        self.canvas = ctk.CTkCanvas(self.canvas_frame, bg="#1E2229", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.padding = 50
        self.limites()
        
        self.nodos_ids = {}
        
        self.after(100, self.grafo_base)

    def limites(self):
        lats = [info['coordenadas'][0] for info in self.grafo.values()]
        lons = [info['coordenadas'][1] for info in self.grafo.values()]
        self.min_lat, self.max_lat = min(lats), max(lats)
        self.min_lon, self.max_lon = min(lons), max(lons)

    def normalizar(self, lat, lon):
        width = self.canvas.winfo_width() - (self.padding * 2)
        height = self.canvas.winfo_height() - (self.padding * 2)
        if width <= 0 or height <= 0: return 0, 0
        x = ((lon - self.min_lon) / (self.max_lon - self.min_lon)) * width + self.padding
        y = height - (((lat - self.min_lat) / (self.max_lat - self.min_lat)) * height) + self.padding
        return x, y

    def grafo_base(self):
        self.canvas.delete("all") 
        self.nodos_ids.clear()

        for origen, destino, linea in self.conexiones:
            if origen in self.grafo and destino in self.grafo:
                x1, y1 = self.normalizar(self.grafo[origen]['coordenadas'][0], self.grafo[origen]['coordenadas'][1])
                x2, y2 = self.normalizar(self.grafo[destino]['coordenadas'][0], self.grafo[destino]['coordenadas'][1])
                color = LINEAS.get(linea, "#FFFFFF")
                self.canvas.create_line(x1, y1, x2, y2, fill=color, width=3, tags="base")

        r = 4
        for nodo, info in self.grafo.items():
            x, y = self.normalizar(info['coordenadas'][0], info['coordenadas'][1])
            
            nodo_id = self.canvas.create_oval(
                x - r, y - r, x + r, y + r, 
                fill="#FFFFFF", outline="#000000", width=1, tags=("base", "nodo")
            )
            self.nodos_ids[nodo_id] = nodo

        self.canvas.tag_bind("nodo", "<Enter>", self.mostrar_tooltip)
        self.canvas.tag_bind("nodo", "<Leave>", self.ocultar_tooltip)

        self.canvas.tag_bind("nodo", "<Button-1>", self.asignar_origen)
        self.canvas.tag_bind("nodo", "<Button-3>", self.asignar_destino)

    def asignar_origen(self, event):
        items = self.canvas.find_withtag("current")
        if not items: return
        
        nombre_estacion = self.nodos_ids.get(items[0], "")
        if not nombre_estacion: return
        
        self.combo_inicio.set(nombre_estacion)
        

    def asignar_destino(self, event):
        items = self.canvas.find_withtag("current")
        if not items: return
        
        nombre_estacion = self.nodos_ids.get(items[0], "")
        if not nombre_estacion: return
        
        self.combo_destino.set(nombre_estacion)
        

    def mostrar_tooltip(self, event):
        items = self.canvas.find_withtag("current")
        if not items: return
        item_id = items[0]
        
        nombre_estacion = self.nodos_ids.get(item_id, "")
        if not nombre_estacion: return

        #print(nombre_estacion)
        
        x, y = event.x, event.y 

        texto_id = self.canvas.create_text(
            x + 15, y - 15, 
            text=nombre_estacion, 
            anchor="sw", 
            fill="white", 
            font=("Arial", 11, "bold"), 
            tags="tooltip",
            state="disabled"
        )
        
        bbox = self.canvas.bbox(texto_id)
        if bbox:
            fondo_id = self.canvas.create_rectangle(
                bbox[0]-5, bbox[1]-2, bbox[2]+5, bbox[3]+2, 
                fill="#2b2b2b", 
                outline="#00a8ff", 
                tags="tooltip",
                state="disabled" 
            )
            self.canvas.tag_lower(fondo_id, texto_id)

    def ocultar_tooltip(self, event):
        self.canvas.delete("tooltip")

    def dibujar(self):
        inicio = self.combo_inicio.get()
        destino = self.combo_destino.get()
        if inicio not in self.grafo or destino not in self.grafo: return
        self.canvas.delete("ruta")

        if self.algo_var.get() == 1:
            ruta, costo = dijkstra(self.grafo, inicio, destino)
            eleccion = "Dijkstra"
        else:
            ruta, costo = a_estrella(self.grafo, inicio, destino)
            eleccion = "A*"

        for i in range(len(ruta) - 1):
            lat1, lon1 = self.grafo[ruta[i]]['coordenadas']
            lat2, lon2 = self.grafo[ruta[i+1]]['coordenadas']
            
            x1, y1 = self.normalizar(lat1, lon1)
            x2, y2 = self.normalizar(lat2, lon2)
            
            self.canvas.create_line(x1, y1, x2, y2, fill="#FFFFFF", width=5, tags="ruta")

        r = 7 
        xi, yi = self.normalizar(self.grafo[inicio]['coordenadas'][0], self.grafo[inicio]['coordenadas'][1])
        xf, yf = self.normalizar(self.grafo[destino]['coordenadas'][0], self.grafo[destino]['coordenadas'][1])
        
        self.canvas.create_oval(xi-r, yi-r, xi+r, yi+r, fill="#00ff00", outline="#FFFFFF", width=2, tags="ruta")
        self.canvas.create_oval(xf-r, yf-r, xf+r, yf+r, fill="#ff0000", outline="#FFFFFF", width=2, tags="ruta")

        self.txt_info.delete("0.0", "end")
        self.txt_info.insert("0.0", f"Algoritmo: {eleccion}\nDistancia: {costo/1000:.2f} km\n\nPasos:\n" + " -> ".join(ruta))


def datos():
    with open('Santiago_de_Chile.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    grafo = {}
    conexiones = [] 
    
    for obj in data:
        nombre = obj['station']
        linea = obj['line']
        
        if nombre not in grafo:
            grafo[nombre] = {'coordenadas': (obj['coords']['lat'], obj['coords']['lng']), 'vecinos': {}}
            
        if obj['next']: 
            vecino = obj['next']['station']
            grafo[nombre]['vecinos'][vecino] = obj['next']['distance_in_meters']
            conexiones.append((nombre, vecino, linea))
            
        if obj['previous']: 
            vecino = obj['previous']['station']
            grafo[nombre]['vecinos'][vecino] = obj['previous']['distance_in_meters']
            conexiones.append((nombre, vecino, linea))
            
    return grafo, conexiones

if __name__ == "__main__":
    grafo, conexiones = datos() 
    app = MetroApp(grafo, conexiones)
    app.mainloop()