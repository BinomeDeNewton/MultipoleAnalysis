import sympy as sp

def ask_for_matrix_size():
	size = int(input("➡️ Entrez le nombre de pôles du multipôle: "))
	return size

def ask_for_generator_and_load(size):
	# Demande initiale pour le générateur
	gen_present = input("➡️ Y a-t-il un générateur dans le modèle? (oui/non): ").lower() == 'oui'
	# Initialisation des ports à None
	gen_port, load_port = None, None
	
	if gen_present:
		print("💡 Le générateur est toujours au port 1.")
		gen_port = 0  # Comme l'indexation commence à 0 en Python, mais le port 1 pour l'utilisateur
	else:
		# Gestion de la présence d'une charge sans générateur
		load_present_temp = input("➡️ Y a-t-il une charge dans le modèle? (oui/non): ").lower() == 'oui'
		if load_present_temp:
			print("❌ Erreur: Pour qu'il y ait une charge, il doit y avoir un générateur.")
			add_gen = input("➡️ Souhaitez-vous ajouter un générateur? (oui/non): ").lower() == 'oui'
			if add_gen:
				gen_present = True
				print("💡 Le générateur est ajouté au port 1.")
				gen_port = 0
			else:
				return False, None, False, None
			
	# Si un générateur est présent ou a été ajouté suite à la demande de la charge
	if gen_present:
		load_present = input("➡️ Y a-t-il une charge dans le modèle? (oui/non): ").lower() == 'oui'
		if load_present:
			while True:
				load_port = int(input("➡️ À quel pôle la charge est-elle connectée?: ")) - 1
				if load_port == 0:
					print("❌ Erreur: La charge ne peut pas être connectée au même pôle que le générateur.")
				elif load_port < 0 or load_port >= size:
					print(f"❌ Erreur: Le numéro du pôle doit être compris entre 1 et {size}.")
				else:
					break
	else:
		load_present = False
		
	print()
	print("💡On considérera que la condition de continuité est vérifiée pour la connexion entre deux multipôles")
	print()
	
	return gen_present, gen_port, load_present, load_port

def ask_for_propagation_factors(size):
	use_factors = input("➡️ Voulez-vous prendre en compte les facteurs de propagation pour chaque guide? (oui/non): ").lower() == 'oui'
	if use_factors:
		# Création des symboles pour gamma et d
		gamma = sp.Matrix(size, 1, lambda i, j: sp.symbols(f'gamma_{i+1}'))
		d = sp.Matrix(size, 1, lambda i, j: sp.symbols(f'd_{i+1}'))
		
		print()
		# Information à l'utilisateur sur la création des matrices
		print("ℹ️ Création de la matrice des facteurs de propagation ...")
		sp.pprint(gamma, use_unicode=True)
		
		print()
		print("ℹ️ Création de la matrice des distances de changement de plan de référénce ...")
		sp.pprint(d, use_unicode=True)
		
		return True, gamma, d
	else:
		return False, [], []
	
def ask_user_for_input_output(node_map):
	print("➡️ Veuillez choisir les ports d'entrée et de sortie parmi les nœuds suivants :")
	nodes_list = list(node_map.keys())  # Liste des labels des nœuds
	
	for index, node_label in enumerate(nodes_list, start=1):
		print(f"{index}. {node_label}")
		
	def select_node(prompt):
		while True:
			try:
				index = int(input(prompt)) - 1
				if 0 <= index < len(nodes_list):
					node_label = nodes_list[index]
					return node_map[node_label]  # Retourne l'objet Node directement
				else:
					raise ValueError
			except ValueError:
				print("❌ Entrée invalide. Veuillez choisir un indice valide de la liste.")
	print()			
	input_node = select_node("Indice du port d'entrée : ")
	output_node = select_node("Indice du port de sortie : ")
	
	return input_node, output_node

def afficher_resultats_latex(P, Q_S, Q_Z, Q_Y):
    print("ℹ️ Puissance dissipée :")
    sp.pprint(P, use_unicode=True)
    print("\nℹ️ Matrice de dissipation Q_S :")
    sp.pprint(Q_S, use_unicode=True)
    print("\nℹ️ Formalisme de la matrice d'impédance Q_Z :")
    sp.pprint(Q_Z, use_unicode=True)
    print("\nℹ️ Formalisme de la matrice d'admittance Q_Y :")
    sp.pprint(Q_Y, use_unicode=True)
	