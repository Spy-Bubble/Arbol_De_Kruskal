"""
═══════════════════════════════════════════════
Red Eléctrica de Fraccionamiento — Algoritmo de Kruskal
Encuentra la red de cableado de MENOR o MAYOR costo
que conecte todas las casas/transformadores.

Modo MIN → Minimizar metros de cable (menor costo de instalación)
Modo MAX → Maximizar capacidad (priorizar cables de mayor capacidad)

Interfaz terminal interactiva · 
═══════════════════════════════════════════════
"""

import os
import sys


# ═══════════════════════════════════════════════
#  COLORES ANSI
# ═══════════════════════════════════════════════

class Color:
    AMARILLO     = "\033[93m"
    AZUL         = "\033[96m"
    AZUL_OSCURO  = "\033[34m"
    VERDE        = "\033[92m"
    ROJO         = "\033[91m"
    MAGENTA      = "\033[95m"
    GRIS         = "\033[90m"
    BLANCO       = "\033[97m"
    NEGRITA      = "\033[1m"
    RESET        = "\033[0m"

def c(texto, *estilos):
    return "".join(estilos) + str(texto) + Color.RESET


# ═══════════════════════════════════════════════
#  UNION-FIND (Estructura de conjuntos disjuntos)
# ═══════════════════════════════════════════════

class UnionFind:
    """
    Estructura Union-Find con compresión de ruta y unión por rango.
    Permite detectar ciclos eficientemente — clave en Kruskal.
    """

    def __init__(self, nodos):
        # Cada nodo es su propio padre al inicio
        self.parent = {n: n for n in nodos}
        self.rank   = {n: 0 for n in nodos}

    def find(self, i):
        """
        Encuentra la raíz del conjunto al que pertenece i.
        Aplica compresión de ruta: aplana el árbol para futuras búsquedas.
        """
        if self.parent[i] != i:
            self.parent[i] = self.find(self.parent[i])  # compresión
        return self.parent[i]

    def union(self, i, j):
        """
        Une los conjuntos de i y j.
        Retorna True si se unieron (no había ciclo),
                False si ya estaban en el mismo conjunto (formaría ciclo).
        """
        raiz_i = self.find(i)
        raiz_j = self.find(j)

        if raiz_i == raiz_j:
            return False  # Ya conectados → ciclo detectado

        # Unión por rango: el árbol más pequeño cuelga del más grande
        if self.rank[raiz_i] < self.rank[raiz_j]:
            self.parent[raiz_i] = raiz_j
        elif self.rank[raiz_i] > self.rank[raiz_j]:
            self.parent[raiz_j] = raiz_i
        else:
            self.parent[raiz_j] = raiz_i
            self.rank[raiz_i] += 1

        return True  # Unión exitosa


# ═══════════════════════════════════════════════
#  ALGORITMO DE KRUSKAL
# ═══════════════════════════════════════════════

def ejecutar_kruskal(nodos, aristas, modo="min"):
    """
    Algoritmo de Kruskal para Árbol de Expansión Mínima o Máxima.

    Parámetros:
        nodos   : list[str]                  → nombres de los puntos
        aristas : list[tuple(u, v, metros)]  → conexiones con costo
        modo    : 'min' | 'max'

    Retorna:
        mst   : list[tuple(u, v, metros)]  → aristas seleccionadas
        total : int                         → costo total
        pasos : list[str]                   → log del proceso
    """

    pasos = []
    uf    = UnionFind(nodos)

    # ── 1. Ordenar aristas ──
    # MIN → ascendente (primero las más baratas)
    # MAX → descendente (primero las de mayor capacidad)
    aristas_ord = sorted(aristas, key=lambda x: x[2], reverse=(modo == "max"))

    etiqueta = "MENOR costo (MIN)" if modo == "min" else "MAYOR capacidad (MAX)"
    pasos.append(f"▶  Modo {etiqueta}")
    pasos.append(f"   Aristas ordenadas ({len(aristas_ord)}):")
    for u, v, m in aristas_ord:
        pasos.append(f"      {u} ↔ {v}  =  {m} m")
    pasos.append("")

    # ── 2. Iterar aristas en orden ──
    mst   = []
    total = 0
    meta  = len(nodos) - 1   # necesitamos exactamente V-1 aristas

    for u, v, metros in aristas_ord:
        if len(mst) >= meta:
            break

        if uf.union(u, v):
            # Aceptada: no forma ciclo
            mst.append((u, v, metros))
            total += metros
            pasos.append(
                f"   ✔  ACEPTADA  {u} ↔ {v}  ({metros} m)  "
                f"— sin ciclo, se añade al árbol"
            )
        else:
            # Rechazada: formaría ciclo
            pasos.append(
                f"   ✘  RECHAZADA {u} ↔ {v}  ({metros} m)  "
                f"— formaría ciclo"
            )

    return mst, total, pasos


# ═══════════════════════════════════════════════
#  UTILIDADES DE TERMINAL
# ═══════════════════════════════════════════════

def limpiar():
    os.system("cls" if os.name == "nt" else "clear")

def sep(ancho=52, color=Color.GRIS):
    print(c("  " + "─" * ancho, color))

def encabezado():
    print(c("╔════════════════════════════════════════════════════╗", Color.AMARILLO))
    print(c("║  ⚡  Red Eléctrica de Fraccionamiento              ║", Color.AMARILLO, Color.NEGRITA))
    print(c("║      Algoritmo de Kruskal · Python                ║", Color.AMARILLO))
    print(c("╚════════════════════════════════════════════════════╝", Color.AMARILLO))
    print()

def pedir_entero(msg, minimo=1):
    while True:
        try:
            v = int(input(msg))
            if v >= minimo:
                return v
            print(c(f"  ⚠  Debe ser ≥ {minimo}", Color.AMARILLO))
        except ValueError:
            print(c("  ⚠  Ingresa un número entero.", Color.AMARILLO))

def pedir_opcion(opciones):
    while True:
        op = input("  Opción: ").strip().lower()
        if op in opciones:
            return op
        print(c("  ⚠  Opción no válida.", Color.AMARILLO))

def listar_puntos(nodos, tipos):
    for nombre in sorted(nodos):
        tipo  = tipos.get(nombre, "casa")
        emoji = "🔌" if tipo == "transformador" else ("🏠" if tipo == "casa" else "🏢")
        print(f"    {emoji}  {c(nombre, Color.BLANCO)}")

def dibujar_arbol(mst, nodos, tipos, total, modo):
    """Dibuja una representación ASCII del árbol resultante."""
    color_linea  = Color.AZUL   if modo == "max" else Color.VERDE
    titulo_modo  = "MÁXIMA CAPACIDAD" if modo == "max" else "MÍNIMO COSTO"
    emoji_modo   = "⚡" if modo == "max" else "💰"

    sep(52, color_linea)
    print(c(f"  {emoji_modo}  ÁRBOL DE {titulo_modo}", color_linea, Color.NEGRITA))
    sep(52, color_linea)
    print()

    # Construir adyacencia del MST para el dibujo
    adyacencia = {n: [] for n in nodos}
    for u, v, m in mst:
        adyacencia[u].append((v, m))
        adyacencia[v].append((u, m))

    # Mostrar lista de cables seleccionados
    unidad = "m de cable" if modo == "min" else "m (capacidad)"
    print(c(f"  Cables seleccionados ({len(mst)}):", Color.BLANCO))
    print()
    for u, v, metros in mst:
        tipo_u = tipos.get(u, "casa")
        tipo_v = tipos.get(v, "casa")
        eu = "🔌" if tipo_u == "transformador" else ("🏠" if tipo_u == "casa" else "🏢")
        ev = "🔌" if tipo_v == "transformador" else ("🏠" if tipo_v == "casa" else "🏢")
        barra = c("━" * 6, color_linea)
        print(f"    {eu} {c(u, Color.BLANCO)}  {barra}  {c(str(metros)+'m', Color.AMARILLO)}  {barra}  {ev} {c(v, Color.BLANCO)}")

    print()
    sep(52, color_linea)
    label = "Total cable usado" if modo == "min" else "Capacidad total cubierta"
    print(
        f"  {c(label+':', Color.BLANCO)}  "
        f"{c(str(total) + ' metros', Color.AMARILLO, Color.NEGRITA)}"
    )
    print()


# ═══════════════════════════════════════════════
#  MENÚS
# ═══════════════════════════════════════════════

def menu_agregar_punto(nodos, tipos):
    sep()
    print(c("  ➕  AGREGAR PUNTO ELÉCTRICO", Color.AZUL, Color.NEGRITA))
    sep()
    print(f"  Tipos:  {c('1', Color.AMARILLO)} Transformador (fuente)  "
          f"{c('2', Color.AMARILLO)} Casa  "
          f"{c('3', Color.AMARILLO)} Edificio/Local")
    print()
    t = pedir_opcion({"1", "2", "3"})
    tipo_map = {"1": "transformador", "2": "casa", "3": "edificio"}
    tipo = tipo_map[t]

    nombre = input(c("  Nombre del punto (ej: Casa 5, Transf. A): ", Color.BLANCO)).strip()
    if not nombre:
        print(c("  ⚠  Nombre vacío.", Color.AMARILLO)); return
    if nombre in nodos:
        print(c(f"  ⚠  '{nombre}' ya existe.", Color.AMARILLO)); return

    nodos.append(nombre)
    tipos[nombre] = tipo
    emoji = "🔌" if tipo == "transformador" else ("🏠" if tipo == "casa" else "🏢")
    print(c(f"\n  ✔  {emoji} '{nombre}' agregado como {tipo}.", Color.VERDE))


def menu_agregar_cable(nodos, aristas, tipos):
    sep()
    print(c("  🔧  AGREGAR CABLE (CONEXIÓN)", Color.AZUL, Color.NEGRITA))
    sep()
    if len(nodos) < 2:
        print(c("  ⚠  Necesitas al menos 2 puntos.", Color.AMARILLO)); return

    print(c("  Puntos disponibles:", Color.BLANCO))
    listar_puntos(nodos, tipos)
    print()

    origen  = input(c("  Desde: ", Color.BLANCO)).strip()
    destino = input(c("  Hasta: ", Color.BLANCO)).strip()

    if origen not in nodos:
        print(c(f"  ⚠  '{origen}' no existe.", Color.ROJO)); return
    if destino not in nodos:
        print(c(f"  ⚠  '{destino}' no existe.", Color.ROJO)); return
    if origen == destino:
        print(c("  ⚠  Origen y destino iguales.", Color.AMARILLO)); return
    if any((a == origen and b == destino) or (a == destino and b == origen)
           for a, b, _ in aristas):
        print(c("  ⚠  Ya existe un cable entre esos puntos.", Color.AMARILLO)); return

    metros = pedir_entero(c("  Metros de cable: ", Color.BLANCO), minimo=1)
    aristas.append((origen, destino, metros))
    print(c(f"\n  ✔  Cable añadido: '{origen}' ↔ '{destino}'  ({metros} m)", Color.VERDE))


def menu_calcular(nodos, aristas, tipos):
    sep()
    print(c("  ⚡  CALCULAR RED ELÉCTRICA ÓPTIMA", Color.AMARILLO, Color.NEGRITA))
    sep()

    if len(nodos) < 2:
        print(c("  ⚠  Necesitas al menos 2 puntos.", Color.AMARILLO)); return
    if len(aristas) < len(nodos) - 1:
        print(c(f"  ⚠  Faltan conexiones. Con {len(nodos)} puntos necesitas al menos "
                f"{len(nodos)-1} cables.", Color.AMARILLO)); return

    print(f"  {c('1', Color.AMARILLO)} 💰 Modo MIN — menor metros de cable (menor costo)")
    print(f"  {c('2', Color.AMARILLO)} ⚡ Modo MAX — mayor capacidad (cables más largos primero)")
    print(f"  {c('3', Color.AMARILLO)} 🔀 Ambos modos (comparar)")
    print()
    op = pedir_opcion({"1", "2", "3"})

    modos = []
    if op == "1": modos = ["min"]
    elif op == "2": modos = ["max"]
    else: modos = ["min", "max"]

    for modo in modos:
        print()
        mst, total, pasos = ejecutar_kruskal(nodos, aristas, modo)

        # ── Log del proceso ──
        color_log = Color.VERDE if modo == "min" else Color.AZUL
        sep(52, color_log)
        etiqueta = "MÍNIMO COSTO" if modo == "min" else "MÁXIMA CAPACIDAD"
        print(c(f"  📋  PROCESO KRUSKAL — {etiqueta}", color_log, Color.NEGRITA))
        sep(52, color_log)
        for paso in pasos:
            if "▶" in paso or "Aristas" in paso:
                print(c("  " + paso, Color.BLANCO))
            elif "✔" in paso:
                print(c("  " + paso, Color.VERDE))
            elif "✘" in paso:
                print(c("  " + paso, Color.ROJO))
            else:
                print(c("  " + paso, Color.GRIS))
        print()

        # ── Resultado visual ──
        if not mst:
            print(c("  ⚠  No se pudo construir el árbol. Revisa las conexiones.", Color.ROJO))
        else:
            dibujar_arbol(mst, nodos, tipos, total, modo)

        if len(modos) > 1 and modo == "min":
            input(c("  → Presiona Enter para ver el modo MAX...", Color.GRIS))
            print()


def menu_ver_red(nodos, aristas, tipos):
    sep()
    print(c("  📡  ESTADO DE LA RED ELÉCTRICA", Color.AZUL, Color.NEGRITA))
    sep()

    if not nodos:
        print(c("  (Red vacía)", Color.GRIS)); return

    # Puntos
    transformadores = [n for n in nodos if tipos.get(n) == "transformador"]
    casas           = [n for n in nodos if tipos.get(n) == "casa"]
    edificios       = [n for n in nodos if tipos.get(n) == "edificio"]

    print(c(f"\n  🔌 Transformadores ({len(transformadores)}):", Color.AMARILLO, Color.NEGRITA))
    for t in sorted(transformadores):
        print(f"    🔌  {c(t, Color.BLANCO)}")

    print(c(f"\n  🏠 Casas ({len(casas)}):", Color.BLANCO, Color.NEGRITA))
    for casa in sorted(casas):
        print(f"    🏠  {c(casa, Color.BLANCO)}")

    if edificios:
        print(c(f"\n  🏢 Edificios/Locales ({len(edificios)}):", Color.BLANCO, Color.NEGRITA))
        for ed in sorted(edificios):
            print(f"    🏢  {c(ed, Color.BLANCO)}")

    # Cables
    print(c(f"\n  🔧 Cables posibles ({len(aristas)}):", Color.AZUL, Color.NEGRITA))
    if aristas:
        for u, v, m in sorted(aristas, key=lambda x: x[2]):
            print(f"    {c(u, Color.BLANCO)} ↔ {c(v, Color.BLANCO)}  "
                  f"{c(str(m)+'m', Color.AMARILLO)}")
    else:
        print(c("    (ninguno)", Color.GRIS))
    print()


# ═══════════════════════════════════════════════
#  EJEMPLO PRECONFIGURADO — Fraccionamiento
# ═══════════════════════════════════════════════

def cargar_ejemplo():
    """
    Fraccionamiento 'Las Palmas' con 2 transformadores,
    6 casas y 2 locales comerciales.
    Los metros representan la distancia de cableado entre puntos.
    """
    nodos = []
    tipos = {}
    aristas = []

    def agregar(nombre, tipo):
        nodos.append(nombre)
        tipos[nombre] = tipo

    # Fuentes de energía
    agregar("Transf. Norte",  "transformador")
    agregar("Transf. Sur",    "transformador")

    # Casas
    for i in range(1, 7):
        agregar(f"Casa {i}", "casa")

    # Locales comerciales
    agregar("Local A", "edificio")
    agregar("Local B", "edificio")

    # Cables posibles (metros de distancia entre puntos)
    cables = [
        ("Transf. Norte", "Casa 1",        30),
        ("Transf. Norte", "Casa 2",        45),
        ("Transf. Norte", "Local A",       20),
        ("Transf. Sur",   "Casa 5",        25),
        ("Transf. Sur",   "Casa 6",        35),
        ("Transf. Sur",   "Local B",       18),
        ("Casa 1",        "Casa 2",        15),
        ("Casa 1",        "Local A",       22),
        ("Casa 2",        "Casa 3",        18),
        ("Casa 3",        "Casa 4",        12),
        ("Casa 3",        "Local A",       28),
        ("Casa 4",        "Casa 5",        20),
        ("Casa 4",        "Local B",       32),
        ("Casa 5",        "Casa 6",        14),
        ("Casa 6",        "Local B",       25),
        ("Local A",       "Local B",       50),
        ("Transf. Norte", "Transf. Sur",   60),
    ]
    for u, v, m in cables:
        aristas.append((u, v, m))

    return nodos, aristas, tipos


# ═══════════════════════════════════════════════
#  PROGRAMA PRINCIPAL
# ═══════════════════════════════════════════════

def main():
    nodos   = []
    aristas = []
    tipos   = {}

    limpiar()
    encabezado()

    print(c("  ¿Cargar el fraccionamiento de ejemplo ('Las Palmas')?", Color.BLANCO))
    print(f"  {c('s', Color.AMARILLO)} Sí    {c('n', Color.AMARILLO)} No, empezar vacío")
    print()
    if input("  → ").strip().lower() == "s":
        nodos, aristas, tipos = cargar_ejemplo()
        print(c(f"  ✔  Fraccionamiento cargado: {len(nodos)} puntos, {len(aristas)} cables.", Color.VERDE))

    while True:
        print()
        sep(52, Color.AMARILLO)
        print(c("  MENÚ PRINCIPAL", Color.AMARILLO, Color.NEGRITA))
        sep(52, Color.AMARILLO)
        print(f"  {c('1', Color.AMARILLO)} Agregar punto eléctrico   "
              f"{c(f'({len(nodos)} en red)', Color.GRIS)}")
        print(f"  {c('2', Color.AMARILLO)} Agregar cable (conexión)  "
              f"{c(f'({len(aristas)} cables)', Color.GRIS)}")
        print(f"  {c('3', Color.AMARILLO)} {c('⚡ Calcular red óptima', Color.AMARILLO, Color.NEGRITA)}")
        print(f"  {c('4', Color.AMARILLO)} Ver estado de la red")
        print(f"  {c('0', Color.AMARILLO)} Salir")
        print()

        op = pedir_opcion({"1", "2", "3", "4", "0"})

        if op == "1":
            menu_agregar_punto(nodos, tipos)

        elif op == "2":
            menu_agregar_cable(nodos, aristas, tipos)

        elif op == "3":
            print()
            menu_calcular(nodos, aristas, tipos)
            input(c("\n  Presiona Enter para continuar...", Color.GRIS))

        elif op == "4":
            menu_ver_red(nodos, aristas, tipos)
            input(c("  Presiona Enter para continuar...", Color.GRIS))

        elif op == "0":
            print(c("\n  ⚡  ¡Red apagada! Hasta luego.\n", Color.AMARILLO))
            sys.exit(0)


if __name__ == "__main__":
    main()
