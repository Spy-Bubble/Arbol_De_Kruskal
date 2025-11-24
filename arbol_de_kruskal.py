class KruskalConsole:
    def __init__(self, vertices):
        self.V = vertices
        self.edges = [] # Lista de aristas: [peso, u, v]
        
        # Estructuras para Union-Find
        self.parent = list(range(vertices))
        self.rank = [0] * vertices

    def add_edge(self, u, v, w):
        """Agrega una arista al grafo: u=origen, v=destino, w=peso"""
        self.edges.append([w, u, v])

    # --- FUNCIONES DE UNION-FIND ---
    def find(self, i):
        """Encuentra la raíz de un nodo con compresión de ruta"""
        if self.parent[i] != i:
            self.parent[i] = self.find(self.parent[i])
        return self.parent[i]

    def union(self, i, j):
        """Une dos subconjuntos. Retorna True si la unión fue exitosa (no había ciclo)"""
        root_i = self.find(i)
        root_j = self.find(j)

        if root_i != root_j:
            # Unir por rango (el árbol más pequeño se une al más grande)
            if self.rank[root_i] < self.rank[root_j]:
                self.parent[root_i] = root_j
            elif self.rank[root_i] > self.rank[root_j]:
                self.parent[root_j] = root_i
            else:
                self.parent[root_j] = root_i
                self.rank[root_i] += 1
            return True # Se unieron correctamente
        return False # Ya estaban conectados (formaría ciclo)

    # --- ALGORITMO PRINCIPAL ---
    def ejecutar_kruskal(self, mode='min'):
        # Reiniciar estructuras para permitir múltiples ejecuciones
        self.parent = list(range(self.V))
        self.rank = [0] * self.V
        
        result = [] # Aquí guardaremos el MST final
        e = 0 # Contador de aristas aceptadas
        
        # 1. ORDENAR ARISTAS
        # Si mode es 'max', ordenamos de mayor a menor (reverse=True)
        is_reverse = True if mode == 'max' else False
        self.edges = sorted(self.edges, key=lambda item: item[0], reverse=is_reverse)

        print(f"\n" + "="*50)
        print(f"INICIO KRUSKAL - Modo: {mode.upper()}")
        print("="*50)
        print(f"1. Ordenando aristas ({'Descendente' if is_reverse else 'Ascendente'})...")
        print(f"   Lista ordenada: {[(w, u, v) for w, u, v in self.edges]}")
        print("-" * 50)

        # 2. ITERAR ARISTAS
        for w, u, v in self.edges:
            # Condición de parada: Si ya tenemos V-1 aristas, el árbol está completo
            if e >= self.V - 1:
                break
                
            print(f"-> Analizando arista {u} -- {v} (Peso: {w})")
            
            root_u = self.find(u)
            root_v = self.find(v)
            
            # Verificamos si forman ciclo
            if self.union(u, v):
                print(f"   [OK] Raíces distintas ({root_u} y {root_v}). No forma ciclo.")
                print(f"   >>> AGREGADA al árbol.")
                result.append([w, u, v])
                e += 1
            else:
                print(f"   [X]  Raíces iguales ({root_u}). Ya están conectados.")
                print(f"   >>> RECHAZADA (Formaría ciclo).")
            print("." * 30)

        # 3. MOSTRAR RESULTADOS
        print("\n" + "="*50)
        print(f"RESULTADO FINAL: Árbol de {mode.upper()} Coste")
        print("="*50)
        print(f"{'Origen':<10} {'Destino':<10} {'Peso':<10}")
        print("-" * 30)
        
        total_cost = 0
        for w, u, v in result:
            print(f"{u:<10} {v:<10} {w:<10}")
            total_cost += w
            
        print("-" * 30)
        print(f"Costo Total: {total_cost}")
        print("="*50 + "\n")

# --- BLOQUE DE EJECUCIÓN ---
if __name__ == '__main__':
    sim = KruskalConsole(4)
    
    # Agregamos las aristas (u, v, peso)
    sim.add_edge(0, 1, 10)
    sim.add_edge(0, 2, 6)
    sim.add_edge(0, 3, 5)
    sim.add_edge(1, 3, 15)
    sim.add_edge(2, 3, 4)

    # Ejecutar para Mínimo Coste
    sim.ejecutar_kruskal(mode='min')
    
    # Ejecutar para Máximo Coste
    sim.ejecutar_kruskal(mode='max')