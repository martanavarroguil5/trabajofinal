import networkx as nx
import matplotlib.pyplot as plt
import json

# Muestra el menú principal que ofrece diferentes opciones para gestionar la red social.
def menu():
    print("\n--- Menú de Red Social ---")
    print("1. Agregar usuario")
    print("2. Eliminar usuario")
    print("3. Agregar conexión entre usuarios")
    print("4. Eliminar conexión entre usuarios")
    print("5. Buscar camino más corto entre dos usuarios")
    print("6. Encontrar comunidades (caminos cerrados o bucles en el grafo)")
    print("7. Sugerir amigos")
    print("8. Mostrar red social")
    print("9. Mostrar centralidades (usuarios más seguidos)")
    print("10. Guardar cambios y salir")
    return input("Seleccione una opción: ")

# Guarda el estado actual del grafo en un archivo JSON para que los cambios sean persistentes.
# Este archivo contendrá los nodos (usuarios) y las conexiones (con pesos).
def guardar_grafo(grafo, archivo="red_social.json"):
    data = {
        "nodes": list(grafo.nodes),
        "edges": [
            {"source": u, "target": v, "weight": grafo[u][v].get("weight", 1)}
            for u, v in grafo.edges
        ],
    }
    with open(archivo, "w") as f:
        json.dump(data, f, indent=4)
    print(f"Cambios guardados en {archivo}.")

# Carga el grafo desde un archivo JSON si existe, para retomar el estado previo.
# Si no encuentra el archivo, inicializa un nuevo grafo vacío con valores predeterminados.
def cargar_grafo(archivo="red_social.json"):
    try:
        with open(archivo, "r") as f:
            data = json.load(f)
        grafo = nx.Graph()
        grafo.add_nodes_from(data["nodes"])
        for edge in data["edges"]:
            grafo.add_edge(edge["source"], edge["target"], weight=edge["weight"])
        print(f"Datos cargados desde {archivo}.")
        return grafo
    except FileNotFoundError:
        print(f"Archivo {archivo} no encontrado. Se inicializará un grafo predeterminado.")
    except json.JSONDecodeError:
        print(f"Error al leer {archivo}: formato JSON inválido. Se inicializará un grafo predeterminado.")
    
    grafo = nx.Graph()
    inicial = [
        ("Alice", "Bob", 2),
        ("Alice", "Charlie", 3),
        ("Bob", "Diana", 1),
        ("Eve", "Frank", 2),
        ("Eve", "Grace", 1),
        ("Grace", "Heidi", 3),
        ("Heidi", "Ivan", 2),
        ("Ivan", "Judy", 1),
        ("Charlie", "Grace", 4),
        ("Diana", "Frank", 3),
    ]
    for u1, u2, peso in inicial:
        grafo.add_edge(u1, u2, weight=peso)
    return grafo

# Añade un nuevo usuario al grafo. Si ya existe, no hace nada.
# Al agregar un usuario, también permite al usuario establecer conexiones iniciales.
def agregar_usuario(grafo):
    usuario = input("Ingrese el nombre del usuario a agregar: ")
    if usuario not in grafo:
        grafo.add_node(usuario)
        print(f"Usuario '{usuario}' añadido a la red.")

        print("Usuarios existentes en la red:")
        for nodo in grafo.nodes:
            print(f"  - {nodo}")

        print("Nota: La prioridad de conexión es de menor número para más fuerte.")
        while True:
            opcion = input("¿Desea agregar una conexión para este usuario? (s/n): ").lower()
            if opcion == "s":
                otro_usuario = input("Ingrese el nombre del usuario para conectar: ")
                if otro_usuario in grafo:
                    try:
                        peso = int(input("Ingrese el peso de la conexión (menor número = más fuerte): "))
                        grafo.add_edge(usuario, otro_usuario, weight=peso)
                        print(f"Conexión añadida entre '{usuario}' y '{otro_usuario}' con peso {peso}.")
                    except ValueError:
                        print("El peso debe ser un número entero.")
                else:
                    print(f"El usuario '{otro_usuario}' no existe en la red.")
            elif opcion == "n":
                break
            else:
                print("Opción no válida. Inténtelo de nuevo.")
    else:
        print(f"El usuario '{usuario}' ya existe.")

# Elimina un usuario del grafo junto con todas sus conexiones.
def eliminar_usuario(grafo):
    usuario = input("Ingrese el nombre del usuario a eliminar: ")
    if usuario in grafo:
        grafo.remove_node(usuario)
        print(f"Usuario '{usuario}' y todas sus conexiones han sido eliminados de la red.")
    else:
        print(f"El usuario '{usuario}' no existe.")

# Crea una conexión entre dos usuarios existentes con un peso (empiezan a seguirse).
# El peso determina la fuerza de la conexión: menor número implica una conexión más fuerte.
def agregar_conexion(grafo):
    print("Usuarios existentes en la red:")
    for nodo in grafo.nodes:
        print(f"  - {nodo}")

    print("Nota: La prioridad de conexión es de menor número para más fuerte.")
    usuario1 = input("Ingrese el primer usuario: ")
    usuario2 = input("Ingrese el segundo usuario: ")
    if usuario1 in grafo and usuario2 in grafo:
        try:
            peso = int(input("Ingrese el peso de la conexión (menor número = más fuerte): "))
            grafo.add_edge(usuario1, usuario2, weight=peso)
            print(f"Conexión añadida entre '{usuario1}' y '{usuario2}' con peso {peso}.")
        except ValueError:
            print("El peso debe ser un número entero.")
    else:
        print("Ambos usuarios deben existir en la red para añadir una conexión.")

# Elimina una conexión específica entre dos usuarios del grafo.(se dejan de seguir)
def eliminar_conexion(grafo):
    usuario1 = input("Ingrese el primer usuario: ")
    usuario2 = input("Ingrese el segundo usuario: ")
    if grafo.has_edge(usuario1, usuario2):
        grafo.remove_edge(usuario1, usuario2)
        print(f"Conexión eliminada entre '{usuario1}' y '{usuario2}'.")
    else:
        print(f"No existe conexión entre '{usuario1}' y '{usuario2}'.")

# Busca el camino más corto entre dos usuarios en la red social, basado en los pesos.
# Utiliza el algoritmo de Dijkstra para optimizar la búsqueda.
def buscar_camino_mas_corto(grafo):
    inicio = input("Ingrese el usuario de inicio: ")
    fin = input("Ingrese el usuario de destino: ")
    try:
        camino = nx.shortest_path(grafo, source=inicio, target=fin, weight='weight')
        print(f"Camino más corto entre '{inicio}' y '{fin}': {camino}")
    except nx.NetworkXNoPath:
        print(f"No hay camino entre '{inicio}' y '{fin}'.")
    except nx.NodeNotFound as e:
        print(e)

# Encuentra y lista los caminos cerrados o bucles dentro del grafo (que serían las comunidades de la red social).
# Un bucle se define como un recorrido que comienza y termina en el mismo nodo.
def encontrar_comunidades(grafo):
    print("Buscando bucles en el grafo:")
    ciclos = list(nx.cycle_basis(grafo))
    if ciclos:
        for idx, ciclo in enumerate(ciclos):
            print(f"  Bucle {idx + 1}: {ciclo}")
    else:
        print("No se encontraron bucles en el grafo.")

# Sugiere posibles amigos basándose en amigos en común (aristas).
# Esto permite identificar conexiones que no existen pero que serían lógicas.
def sugerir_amigos(grafo):
    usuario = input("Ingrese el nombre del usuario para sugerir amigos: ")
    if usuario not in grafo:
        print(f"El usuario '{usuario}' no existe.")
        return

    sugerencias = {}
    for amigo in grafo.neighbors(usuario):
        for amigo_de_amigo in grafo.neighbors(amigo):
            if amigo_de_amigo != usuario and amigo_de_amigo not in grafo.neighbors(usuario):
                sugerencias[amigo_de_amigo] = sugerencias.get(amigo_de_amigo, 0) + 1

    sugerencias_ordenadas = sorted(sugerencias.items(), key=lambda x: -x[1])
    print(f"Sugerencias de amigos para '{usuario}']:")
    for sugerencia, peso in sugerencias_ordenadas:
        print(f"  {sugerencia} (amigos en común: {peso})")

# Dibuja el grafo representando la red social, mostrando los usuarios y las conexiones.
# Esto sirve para visualizar la red social y asi comprobar los resultados obtenidos.
def mostrar_red_social(grafo):
    pos = nx.spring_layout(grafo)
    labels = nx.get_edge_attributes(grafo, 'weight')
    nx.draw(grafo, pos, with_labels=True, node_color="skyblue", font_weight="bold")
    nx.draw_networkx_edge_labels(grafo, pos, edge_labels=labels)
    plt.show()

# Calcula y muestra cuáles usuarios son más importantes según el grado de ponderación.
# Esto mide cuántas conexiones y tiene un usuario (teniendo en cuenta el peso) en relación al resto de la red.
def mostrar_centralidades(grafo):
    centralidades = nx.degree_centrality(grafo)
    ordenadas = sorted(centralidades.items(), key=lambda x: -x[1])
    print("Usuarios más seguidos en la red:")
    for usuario, centralidad in ordenadas:
        print(f"  {usuario}: Centralidad = {centralidad:.2f}")


# Función principal que gestiona el flujo del programa interactivo.
# Aquí se manejan las opciones seleccionadas por el usuario y se actualiza el grafo según dichas acciones.
# Crea un grafo inicial con usuarios y conexiones predefinidas para mostrar un ejemplo inicial.
def main():
    grafo = cargar_grafo()

    while True:
        opcion = menu()
        if opcion == "1":
            agregar_usuario(grafo)
        elif opcion == "2":
            eliminar_usuario(grafo)
        elif opcion == "3":
            agregar_conexion(grafo)
        elif opcion == "4":
            eliminar_conexion(grafo)
        elif opcion == "5":
            buscar_camino_mas_corto(grafo)
        elif opcion == "6":
            encontrar_comunidades(grafo)
        elif opcion == "7":
            sugerir_amigos(grafo)
        elif opcion == "8":
            mostrar_red_social(grafo)
        elif opcion == "9":
            mostrar_centralidades(grafo)
        elif opcion == "10":
            guardar_grafo(grafo)
            print("Saliendo del programa. ¡Hasta luego!")
            break
        else:
            print("Opción no válida. Inténtalo de nuevo.")

if __name__ == "__main__":
    main()
