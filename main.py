import sympy as sp
from mathematics.matrix_operations import matrice_impedance, matrice_admittance, calculer_puissance_dissipee, calculer_matrices_formalismes, calculate_and_display_transfer_function, verifier_adaptation, initialize_vectors_and_matrix, initialize_gammavector
from mathematics.signal_processing import est_multipole_sans_pertes, adjust_for_propagation_factors
from graph.graph_initialization import initialize_graph, visualize_graph
from mathematics.signalflow_algorithms.algorithms.johnson import simple_cycles
from mathematics.signalflow_algorithms.algorithms.tarjan import strongly_connected_components
from ui.inputs import ask_for_matrix_size, ask_for_generator_and_load, ask_for_propagation_factors, ask_user_for_input_output, afficher_resultats_latex

def main():
        # Début du script
        size = ask_for_matrix_size()
        S_symbolic, a_symbolic, b_symbolic = initialize_vectors_and_matrix(size)
        Z = matrice_impedance(S_symbolic)
        Y = matrice_admittance(S_symbolic)
    
        print("\nℹ️ Matrice génératrice du multipôle :")
        sp.pprint(S_symbolic, use_unicode=True)
    
        print("\nℹ️ Vecteur d'ondes réfléchies :")
        sp.pprint(b_symbolic, use_unicode=True)
    
        print("\nℹ️ Vecteur d'ondes incidentes :")
        sp.pprint(a_symbolic, use_unicode=True)
    
        print("\nℹ️ Matrice d'impedance :")
        sp.pprint(Z, use_unicode=True)
    
        print("\nℹ️ Matrice d'admittance :")
        sp.pprint(Y, use_unicode=True)
    
        P = calculer_puissance_dissipee(S_symbolic, a_symbolic)
        formalismes = calculer_matrices_formalismes(S_symbolic,Z, Y)
        
        afficher_resultats_latex(P, formalismes['Q_S'], formalismes['Q_Z'], formalismes['Q_Y'])
    
        print()
        if est_multipole_sans_pertes(formalismes):
            print("✅ Le multipôle est sans pertes.")
        else:
            print("⚠️ Le multipôle n'est pas sans pertes.")

        print()
        verifier_adaptation(S_symbolic)
    
        print()
        gen_present, gen_port, load_present, load_port = ask_for_generator_and_load(size)
    
        use_factors, gamma, d = ask_for_propagation_factors(size)
        if use_factors:
            S_symbolic, a_symbolic, b_symbolic = adjust_for_propagation_factors(S_symbolic, a_symbolic, b_symbolic, gamma, d, size)
            Z = matrice_impedance(S_symbolic)
            Y = matrice_admittance(S_symbolic)
            P = calculer_puissance_dissipee(S_symbolic, a_symbolic)
            formalismes = calculer_matrices_formalismes(S_symbolic,Z, Y)
            
            if est_multipole_sans_pertes(formalismes):
                print("✅ Le multipôle est sans pertes.")
            else:
                print("⚠️ Le multipôle n'est pas sans pertes.")

            print()
            verifier_adaptation(S_symbolic) 
            
            #print()
            #afficher_resultats_latex(P, formalismes['Q_S'], formalismes['Q_Z'], formalismes['Q_Y'])
            
        G, node_map = initialize_graph(size, S_symbolic, a_symbolic, b_symbolic, gen_present, gen_port, load_present, load_port)
    
        print("✅ Graphe initialisé. Affichage des noeuds et des branches :")
        for node_id, node in node_map.items():
            # Utilisez la propriété `outgoing` pour obtenir les branches sortantes
            print(f"Noeud: {node_id}, Branches sortantes: {[str(branch) for branch in node.outgoing]}")
            
        print()
        input_index, output_index = ask_user_for_input_output(node_map)
    
        # Après avoir identifié les composantes fortement connexes
        # Assurez-vous que la fonction strongly_connected_components peut accepter votre type personnalisé `Graph`
        components = strongly_connected_components(G)
        print("\nℹ️ Composantes fortement connexes du graphique :")
        for i, comp in enumerate(components, start=1):
            print(f"Composante {i}: {[node.label for node in comp]}")
            
        # Informations supplémentaires pour l'utilisateur
        print("\nInterprétation des Composantes Fortement Connexes :")
        if len(components) > 1:
            print("- Le système contient plusieurs composantes fortement connexes, indiquant des zones distinctes de feedback ou de boucles.")
            print("- Ces zones sont cruciales pour comprendre la dynamique interne du système, car elles peuvent significativement affecter la stabilité et la réponse en fréquence.")
            print("- Examiner ces composantes peut révéler des opportunités pour optimiser ou modifier la conception du système afin d'améliorer ses performances.")
        else:
            print("- Le système forme une unique composante fortement connexe, indiquant que tous les éléments sont interconnectés d'une manière qui permet un feedback potentiel à travers le système entier.")
            print("- Cette configuration nécessite une attention particulière pour assurer la stabilité et la réponse désirée du système.")
            
        print("\nConsidérations de Conception :")
        print("- Les modifications au sein des composantes fortement connexes peuvent être utilisées pour ajuster la réponse du système. Cela peut inclure la modification des gains des branches, l'ajout ou la suppression de connexions.")
        print("- Les analyses de stabilité doivent prendre en compte les boucles de feedback identifiées par les composantes fortement connexes, en particulier dans la conception des systèmes de contrôle ou lors de l'ajustement des paramètres du système.")
    
        # Exécution de l'algorithme de Johnson pour trouver toutes les boucles
        # Assurez-vous que la fonction simple_cycles peut accepter votre type personnalisé `Graph`
        cycles = list(simple_cycles(G))
    
        print("\nAnalyse des Boucles Trouvées :")
        if cycles:
            print(f"- Nombre total de boucles trouvées : {len(cycles)}")
            for i, cycle in enumerate(cycles, 1):
                print(f"  Boucle {i}: Composée des branches {[branch.id for branch in cycle]}")
            print("- Ces boucles représentent des chemins de feedback critiques qui peuvent influencer la stabilité et la performance du système.")
        else:
            print("- Aucune boucle trouvée. Le système pourrait être unidirectionnel sans chemins de feedback internes.")
        
        print()
        calculate_and_display_transfer_function(G, input_index, output_index)
    
        visualize_graph(G, node_map)
    

if __name__ == "__main__":
    main()
    