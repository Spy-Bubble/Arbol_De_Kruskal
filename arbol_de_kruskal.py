import networkx as nx
import matplotlib.pyplot as plt

class KruskalSimulator:
    def __init__(self, vertices):
        self.V = vertices
        self.edges = [] # Lista de aristas: [peso, u, v]
        
        # Estructuras para Union-Find
        self.parent = list(range(vertices))
        self.rank = [0] * vertices

    def add_edge(self, u, v, w):
        self.edges.append([w, u, v])

    # --- FUNCIONES DE UNION-FIND ---
    def find(self, i):
        """Encuentra la raíz de un nodo con compresión de ruta"""
        if self.parent[i] != i:
            self.parent[i] = self.find(self.parent[i])
        return self.parent[i]

    def union(self, i, j):
        """Une dos subconjuntos (árboles) basándose en el rango"""
        root_i = self.find(i)
        root_j = self.find(j)

        if root_i != root_j:
            if self.rank[root_i] < self.rank[root_j]:
                self.parent[root_i] = root_j
            elif self.rank[root_i] > self.rank[root_j]:
                self.parent[root_j] = root_i
            else:
                self.parent[root_j] = root_i
                self.rank[root_i] += 1
            return True # Unión exitosa (no había ciclo)
        return False # Ya estaban conectados (formaría ciclo)

    # --- VISUALIZACIÓN ---
    def show_results(self, result_edges, mode):
        G = nx.Graph()
        G.add_nodes_from(range(self.V))
        
        # Agregamos TODAS las aristas para el fondo
        for w, u, v in self.edges:
            G.add_edge(u, v, weight=w)

        pos = nx.spring_layout(G, seed=42)
        plt.figure(figsize=(10, 7))

        # Dibujar todo el grafo en gris
        nx.draw_networkx_nodes(G, pos, node_size=700, node_color='lightgreen', edgecolors='black')
        nx.draw_networkx_labels(G, pos, font_size=12, font_weight='bold')
        nx.draw_networkx_edges(G, pos, style='dashed', alpha=0.3, edge_color='gray')
        
        # Dibujar aristas del resultado en Azul (Max) o Rojo (Min)
        mst_style_edges = [(u, v) for w, u, v in result_edges]
        color = 'blue' if mode == 'max' else 'red'
        nx.draw_networkx_edges(G, pos, edgelist=mst_style_edges, width=3, edge_color=color)
        
        # Etiquetas de peso
        labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

        title_mode = "MÁXIMO Coste" if mode == 'max' else "MÍNIMO Coste"
        plt.title(f"Resultado Kruskal: Árbol de {title_mode}", fontsize=15)
        plt.axis('off')
        plt.show()

    # --- ALGORITMO PRINCIPAL ---
    def ejecutar_kruskal(self, mode='min'):
        # Reiniciar Union-Find para cada ejecución
        self.parent = list(range(self.V))
        self.rank = [0] * self.V
        
        result = []
        i = 0 # Índice para aristas ordenadas
        e = 0 # Contador de aristas en el árbol

        # 1. ORDENAR ARISTAS
        # Si es min: ascendente. Si es max: descendente (reverse=True)
        is_reverse = True if mode == 'max' else False
        self.edges = sorted(self.edges, key=lambda item: item[0], reverse=is_reverse)

        print(f"\n--- INICIO KRUSKAL (Modo: {mode.upper()}) ---")
        print(f"Aristas ordenadas por peso: {[(w, u, v) for w, u, v in self.edges]}")

        # Iterar sobre las aristas ordenadas
        for w, u, v in self.edges:
            if e >= self.V - 1: # Ya tenemos V-1 aristas, terminamos
                break
                
            print(f"-> Analizando arista {u}-{v} con peso {w}...")
            
            # 2. VERIFICAR CICLOS (FIND & UNION)
            if self.union(u, v):
                print(f"   [ACEPTADA] No forma ciclo. Se agrega al árbol.")
                result.append([w, u, v])
                e += 1
            else:
                print(f"   [RECHAZADA] Los nodos {u} y {v} ya están conectados. Formaría un ciclo.")

        # Mostrar resultados
        print("\n" + "="*40)
        print(f"RESULTADO FINAL ({mode.upper()})")
        print("="*40)
        total_cost = 0
        for w, u, v in result:
            print(f"{u} -- {v} == {w}")
            total_cost += w
        print(f"Costo Total: {total_cost}")
        
        self.show_results(result, mode)

# --- EJECUCIÓN ---
if __name__ == '__main__': 
    sim = KruskalSimulator(4)
    sim.add_edge(0, 1, 10)
    sim.add_edge(0, 2, 6)
    sim.add_edge(0, 3, 5)
    sim.add_edge(1, 3, 15)
    sim.add_edge(2, 3, 4)

    # EJECUTAR PARA MÍNIMO
    #sim.ejecutar_kruskal(mode='min')
    
    # EJECUTAR PARA MÁXIMO 
    sim.ejecutar_kruskal(mode='max')