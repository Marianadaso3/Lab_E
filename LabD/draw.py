import graphviz

# Importamos el módulo graphviz para generar gráficos

# Dibuja el grafo a partir de sus estados y transiciones
def local_graph(states, init_state, end_states, trans_f, title):
    """
    Función que dibuja un grafo a partir de los estados y las transiciones proporcionados.
    Args:
        states (list): Lista de estados.
        init_state (str): Estado inicial.
        end_states (list): Lista de estados de aceptación.
        trans_f (dict): Diccionario de transiciones.
        title (str): Título del grafo.
    Returns:
        None
    """
    # Se crea un objeto de grafo de Graphviz
    graph = graphviz.Digraph()

    # Se itera sobre los estados y se agregan nodos al grafo con formas diferentes según el tipo de estado
    for state in states:
        if state in end_states and state in init_state:
            # Si el estado es tanto un estado de aceptación como el estado inicial, se le asigna la forma 'doubleoctagon'
            graph.attr('node', shape='doubleoctagon')
            graph.node(state)
        elif state in end_states:
            # Si el estado es un estado de aceptación, se le asigna la forma 'doublecircle'
            graph.attr('node', shape='doublecircle')
            graph.node(state)
        elif state in init_state:
            # Si el estado es el estado inicial, se le asigna la forma 'octagon'
            graph.attr('node', shape='octagon')
            graph.node(state)
        else:
            # Para los demás estados, se les asigna la forma 'circle'
            graph.attr('node', shape='circle')
            graph.node(str(state))

    # Se itera sobre las transiciones y se agregan arcos al grafo con las etiquetas correspondientes
    for trans in trans_f:
        for t in trans_f[trans]:
            # Se agrega un arco en el grafo desde el estado de origen hasta el estado de destino,
            # con la etiqueta correspondiente a la transición
            graph.edge(trans, trans_f[trans][t], t)

    # Se renderiza el grafo en un archivo con el título proporcionado
    graph.render(title, view=False)


# Obtener transiciones del AFD con la finalidad de graficarlo
def trans_func_afd(transitions):
    """
    Función que obtiene las transiciones del AFD a partir de una lista de transiciones.
    Args:
        transitions (list): Lista de transiciones.
    Returns:
        dict: Diccionario de transiciones del AFD.
    """
    trans_f = {}
    # Creamos un diccionario vacío para almacenar las transiciones del AFD

        # Se itera sobre las transiciones y se construye un diccionario con las transiciones del AFD
    for transition in transitions:
        init_state, char, end_state = [*transition]
        # Desempaquetamos la transición en sus componentes: estado inicial, caracter y estado final

        if init_state not in trans_f.keys():
            # Si el estado inicial no está presente como clave en el diccionario de transiciones del AFD,
            # se crea una nueva entrada para ese estado inicial
            trans_f[init_state] = {}

        if char != "\\":
            # Si el caracter de la transición no es "\", se agrega la transición al diccionario de transiciones del AFD
            trans_f[init_state][char] = end_state
        else:
            # Si el caracter de la transición es "\", se agrega una transición con el caracter "/" al diccionario de transiciones del AFD
            trans_f[init_state]["/"] = end_state

    # Retornamos el diccionario de transiciones del AFD
    return trans_f

# Importamos el módulo direct_afd y utils
import direct_afd
