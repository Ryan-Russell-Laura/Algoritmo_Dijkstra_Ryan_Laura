import networkx as nx
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

graph = {
    "v1": {"v2":35.64},
    "v2": {"v1":35.64,"v3":50.55,"v7":50.61},
    "v3": {"v2":50.55,"v4":30.34,"v6":40.15},
    "v4": {"v5":40.16},
    "v5": {"v6":30.23},
    "v6": {"v3":40.15,"v9":49.55},
    "v7": {"v2":50.61,"v8":45.49,"v14":53.29},
    "v8": {"v7":45.49,"v9":41.43,"v15":50.6},
    "v9": {"v6":49.55,"v8":41.43,"v10":51.34},
    "v10": {"v9":51.34,"v11":50.26,"v13":84.35,"v17":51.04},
    "v11": {"v10":50.26,"v12":28.49,"v23":45.69},
    "v12": {"v11":28.49},
    "v13": {"v10":84.35},
    "v14": {"v7":53.29,"v15":48.66,"v25":95.28},
    "v15": {"v8":50.6,"v14":48.66,"v16":40.83,"v18":46.73},
    "v16": {"v15":40.83,"v17":48.68,"v19":45.78},
    "v17": {"v10":51.04,"v16":48.68,"v20":48.5},
    "v18": {"v15":46.73,"v19":42.65,"v26":50.25},
    "v19": {"v16":45.78,"v18":42.65,"v20":50.94},
    "v20": {"v17":48.5,"v19":50.94,"v21":50.38,"v27":50.87},
    "v21": {"v20":50.38,"v22":29.65,"v23":44.13},
    "v22": {"v21":29.65,"v24":44.46},
    "v23": {"v11":45.69,"v21":44.13},
    "v24": {"v23":28.85},
    "v25": {"v14":95.28,"v26":52.39,"v29":56.62},
    "v26": {"v18":50.25,"v25":52.39,"v27":87.61,"v30":56.63},
    "v27": {"v20":50.87,"v26":87.61,"v28":82.54,"v31":56.92},
    "v28": {"v27":82.54},
    "v29": {"v25":56.62,"v30":52.44},
    "v30": {"v26":56.63,"v29":52.44,"v31":90.57},
    "v31": {"v27":56.92,"v30":90.57,"v32":82.73},
    "v32": {"v31":82.73},     
}

def algoritmo():
    #Se crea el grafo vacío
    grafo = nx.Graph()
    #Crear la ventana para graficar con su dimension y su nombre
    fig = plt.figure(figsize=(180, 180),num='Grafica con todos los nodos y la ruta corta en color rojo')
    
    #Se agregan los nodos al grafo
    #add_node = agregar nodo
    for nodo in graph:
        grafo.add_node(nodo)
    
    #Se agregan las aristas al grafo
    #add_edge = agregar arista
    for nodo in graph:
        for nodoVecino, distancia in graph[nodo].items():
            grafo.add_edge(nodo, nodoVecino, weight=distancia)

    #Con spring_layout se calcula una posición para cada nodo del grafo, necesario para dibujar la gráfica
    pos = nx.spring_layout(grafo)

    #Se asigna el valor de partida y el valor de destino   
    partida = str(combobox1.get())
    destino = str(combobox2.get())

    # Inicialización de variables
    nodosNoVisitados = graph
    distanciasCortas = {}
    nodosRutaCorta = []
    caminoNodosPrevios = {}

    # Se inicializan todas las distancias como infinito, excepto la distancia de partida que sera 0
    for nodo in nodosNoVisitados:
        distanciasCortas[nodo] = float('inf')
    distanciasCortas[partida] = 0

    # Algoritmo de Dijkstra para encontrar la ruta más corta
    """
    elif de linea 97:
    Si la distancia hacia el nodoMin es mayor que la distancia hacia el nodoActual, 
    entonces se actualiza nodoMin para que apunte al nodo con la distancia más corta.

    nodoMin = Nodo más corto conocido
     
    If de linea 101:
    Si la distancia hacia el nodo vecino (distanciaTentativa) 
    más la distancia actual (distanciasCortas[nodoMin]) 
    es menor que la distancia inf del nodo que sigue, 
    entonces se actualiza la distancia más corta hacia ese nodo vecino 
    y se registra el nodo previo en caminoNodosPrevios[nodo].
    """
    while nodosNoVisitados:
        nodoMin = None
        for nodoActual in nodosNoVisitados:
            if nodoMin is None:
                nodoMin = nodoActual
            elif distanciasCortas[nodoMin] > distanciasCortas[nodoActual]:
                nodoMin = nodoActual     

        for (nodo, distanciaTentativa) in nodosNoVisitados[nodoMin].items():
            if distanciaTentativa + distanciasCortas[nodoMin] < distanciasCortas[nodo]:
                distanciasCortas[nodo] = distanciaTentativa + distanciasCortas[nodoMin]
                caminoNodosPrevios[nodo] = nodoMin                
        nodosNoVisitados.pop(nodoMin)

    # Reconstrucción de la ruta más corta
    # Una vez que se ha encontrado la ruta más corta utilizando Dijkstra, 
    # esta se reconstruye desde el nodo de destino hasta el nodo de partida y se almacena en la lista "nodosRutaCorta".
    nodo = destino
    while nodo != partida:
        try:
            nodosRutaCorta.insert(0, nodo)
            nodo = caminoNodosPrevios[nodo]
        except Exception:
            print('Ruta sin acceso')
            break
    nodosRutaCorta.insert(0, partida)
  

    # Se imprime la distancia más corta y la ruta encontrada
    if distanciasCortas[destino] != float('inf'):
        distancia=str(distanciasCortas[destino])
        ruta=str(nodosRutaCorta)

    print("La distancia más corta es: "+distancia)
    print("La ruta más corta es: "+ruta)

    # Mostrar el resultado en el widget de texto
    texto_resultado1.delete(1.0, tk.END)  # Limpiar el contenido actual del widget
    texto_resultado1.insert(tk.END, distancia)
    texto_resultado2.delete(1.0, tk.END)
    texto_resultado2.insert(tk.END, ruta)
    
    # Creación del grafo que representa la ruta más corta
    rutaAristas = [(nodosRutaCorta[i], nodosRutaCorta[i+1]) for i in range(len(nodosRutaCorta)-1)]
    grafoRutaCorta = nx.Graph()
    grafoRutaCorta.add_edges_from(rutaAristas)

    # Se crea un nuevo grafo llamado "grafoRutaCorta" que representa la ruta más corta encontrada. 
    # Se crean aristas utilizando los nodos de la lista "nodosRutaCorta".

    # Dibujar el grafo de nombre "grafo" con los nodos y aristas
    nx.draw_networkx(grafo, pos, with_labels=True, node_size=250, node_color='lightblue', font_size=6, font_color='blue',font_weight='bold')
    # Dibujar mediante el grafo de nombre "grafoRutaCorta" las aristas y nodos que representan la ruta más corta en color rojo
    nx.draw_networkx_edges(grafoRutaCorta, pos, edgelist=rutaAristas, width=3, edge_color='red')
    # Dibujar las etiquetas de las aristas con los pesos en negrita
    nx.draw_networkx_edge_labels(grafo, pos, edge_labels=nx.get_edge_attributes(grafo, 'weight'),font_size=6,font_weight='bold')
    # Configurar la visualización
    plt.axis('off')
    plt.subplots_adjust(left=0.0, bottom=0.0, right=1, top=1, wspace=0.2, hspace=0.2)
    # Mostrar la gráfica
    plt.show()

##############################################################

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Algoritmo de Dijkstra")

ventana.geometry("1300x580")

# Crear un título encima de los ComboBox
titulo = tk.Label(ventana, text="PROGRAMA QUE DETERMINA LA RUTA MÁS CORTA \n EN EL P.J. LA ESPERANZA DE TACNA")
titulo.pack(anchor=tk.W)

# Crear los ComboBox y definir las opciones
valores = ["v1","v2","v3","v4","v5","v6","v7","v8","v9","v10","v11","v12","v13","v14","v15","v16","v17","v18","v19","v20","v21","v22","v23","v24","v25","v26","v27","v28","v29","v30","v31","v32"]
titulo = tk.Label(ventana, text="Seleccione el vértice de partida:", justify=tk.LEFT)
titulo.pack(anchor=tk.W, padx=10, pady=5)  # Alinea a la izquierda (oeste)
combobox1 = ttk.Combobox(ventana, values=valores)
combobox1.pack(anchor=tk.W, padx=10, pady=5)
titulo = tk.Label(ventana, text="Seleccione el vértice de destino:", justify=tk.LEFT)
titulo.pack(anchor=tk.W, padx=10, pady=5)  # Alinea a la izquierda (oeste)
combobox2 = ttk.Combobox(ventana, values=valores)
combobox2.pack(anchor=tk.W, padx=10, pady=5)

# Crear el botón para graficar y calcular rutas cortas
boton_principal = tk.Button(ventana, text="Graficar y hallar ruta más corta", bg="blue", fg="white",command=algoritmo)
boton_principal.pack(anchor=tk.W,padx=10,pady=10)

# Crear el widget de texto para mostrar el resultado
titulo = tk.Label(ventana, text="La distancia más corta es:")
titulo.pack(anchor=tk.W, padx=10, pady=5)
texto_resultado1 = tk.Text(ventana, height=1, width=25)
texto_resultado1.pack(anchor=tk.W, padx=10, pady=5)
titulo = tk.Label(ventana, text="La ruta más corta es:")
titulo.pack(anchor=tk.W, padx=10, pady=5)
texto_resultado2 = tk.Text(ventana, height=1, width=72)
texto_resultado2.pack(anchor=tk.W, padx=10, pady=5)

aviso = tk.Label(ventana, text="AVISO: Solo puede utilizar una sola vez este programa, gracias...")
aviso.pack(anchor=tk.W, padx=10, pady=5)

ruta_imagen = 'Croquis_Final.jpg'

# Título que deseas agregar
titulo = "CROQUIS DEL P.J. LA ESPERANZA DE TACNA"

# Agregar el título encima de la imagen
titulo_label = tk.Label(ventana, text=titulo, font=("Arial", 16))
titulo_label.place(x=690, y=10)  # Ajusta las coordenadas del título en la ventana

# Crear un widget Label para mostrar la imagen
imagen = Image.open(ruta_imagen)
imagen = imagen.resize((650,500))  # Ajusta el tamaño de la imagen según tus necesidades
imagen_tk = ImageTk.PhotoImage(imagen)
imagen_label = tk.Label(ventana, image=imagen_tk)
imagen_label.image = imagen_tk
imagen_label.place(x=600, y=40)  # Ajusta las coordenadas de la imagen en la ventana

# Ejecutar la ventana principal
ventana.mainloop()







