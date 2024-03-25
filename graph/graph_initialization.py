import networkx as nx
import matplotlib.pyplot as plt
import sympy as sp
from graph.algorithms.graph import Graph, Branch, Node

def initialize_graph(size, S, a, b, gen_present, gen_port, load_present, load_port):
    my_graph = Graph()
    node_map = {}  # Pour mémoriser les objets Node créés
    
    # Création des noeuds avec des labels
    for i in range(size):
        node_map[f'a_{i+1}'] = Node(graph=my_graph, label=f'a_{i+1}')
        node_map[f'b_{i+1}'] = Node(graph=my_graph, label=f'b_{i+1}')
        
    # Ajout des branches en fonction de la matrice S
    for i in range(size):
        for j in range(size):
            if S[i, j] != 0:
                start_node = node_map[f'a_{j+1}']
                end_node = node_map[f'b_{i+1}']
                Branch(start=start_node, end=end_node, weight=str(S[i, j]))
                
    # Ajout du générateur et de la charge si nécessaire
    if gen_present:
        gamma_S = sp.symbols('Gamma_S')
        node_map['b_s'] = Node(graph=my_graph, label='b_s')
        Branch(start=node_map[f'b_s'], end=node_map[f'a_{gen_port+1}'], weight=1)
        Branch(start=node_map[f'b_{gen_port+1}'], end=node_map[f'a_{gen_port+1}'], weight=gamma_S)
    if load_present:
        gamma_C = sp.symbols('Gamma_C')
        Branch(start=node_map[f'b_{load_port+1}'], end=node_map[f'a_{load_port+1}'], weight=gamma_C)
        
    return my_graph, node_map

def visualize_graph(my_graph, node_map):
    G = nx.DiGraph()
    pos = {}
    labels = {}
    label_positions = {}

    # Initialisation des compteurs de position pour chaque type de noeud
    position_counters = {'a': 0, 'b': 0}
    loop_edges = []
    
    for node_label, node in node_map.items():
        # Formatte le label pour l'affichage LaTeX
        formatted_label = f"${node.label}$"
        G.add_node(formatted_label)
        
        # Détermine si le label contient 'a' ou 'b' et extrait l'indice
        node_type = 'a' if 'a' in node_label else 'b'
        pos[formatted_label] = (1 if node_type == 'a' else 2, -position_counters[node_type])
        # Incrémente le compteur pour le type de noeud
        position_counters[node_type] += 1
        
        for branch in node.outgoing:
            # Formatte le label du nœud de fin pour l'affichage LaTeX
            end_node_label_formatted = f"${branch.end.label}$"
            if formatted_label == end_node_label_formatted:  # Détection d'une boucle
                loop_edges.append((formatted_label, end_node_label_formatted))
            weight_label = f"${sp.latex(sp.sympify(branch.weight))}$"
            edge = (formatted_label, end_node_label_formatted)
            labels[edge] = weight_label
            G.add_edge(*edge, weight=weight_label)
            label_positions[edge] = 0.3 if edge not in label_positions else 0.7
            
    # Dessine le graphe sauf les arêtes en boucle
    edges = G.edges() - set(loop_edges)
    nx.draw_networkx_edges(G, pos, edgelist=edges, width=2, edge_color='k', arrows=True)
    # Dessine spécifiquement les arêtes en boucle avec un style courbé
    nx.draw_networkx_edges(G, pos, edgelist=loop_edges, connectionstyle='arc3,rad=0.7', width=2, edge_color='k')
    nx.draw_networkx_nodes(G, pos, node_color='skyblue', node_size=700)
    nx.draw_networkx_labels(G, pos, font_size=15)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, label_pos=0.3, font_size=12)
    plt.show()
