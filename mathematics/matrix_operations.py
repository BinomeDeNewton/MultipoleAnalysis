import numpy as np
import sympy as sp
from mathematics.signalflow_algorithms.algorithms.mason import mason

def initialize_vectors_and_matrix(size):
    S = sp.Matrix(size, size, lambda i, j: sp.symbols(f'S{i+1}{j+1}'))
    a = sp.Matrix(size, 1, lambda i, j: sp.symbols(f'a{i+1}'))
    b = sp.Matrix(size, 1, lambda i, j: sp.symbols(f'b{i+1}'))
    return S, a, b

def initialize_gammavector(size):
    gamma = sp.Matrix(size, 1, lambda i, j: sp.symbols(f'γ{i+1}'))
    d = sp.Matrix(size, 1, lambda i, j: sp.symbols(f'd_{i+1}'))
    return gamma, d

def verifier_adaptation(S):
    taille = S.shape[0]
    adaptation = {}
    for i in range(taille):
        # Vérifie si S_{ii} est nul.
        adaptation[i+1] = (S[i, i] == 0)
    
    print("ℹ️ Résultat de l'adaptation :")
    for accès, adapté in adaptation.items():
        etat = "adapté" if adapté else "non adapté"
        print(f"Accès {accès} est {etat}.")

def matrice_impedance(S):
    # Définition de la matrice d'impédance
    I = sp.eye(S.shape[0])
    Z = (I + S) * (I - S).inv()
    return Z

def matrice_admittance(S):
    # Définition de la matrice d'admittance
    I = sp.eye(S.shape[0])
    Y = (I - S) * (I + S).inv()
    return Y

def calculer_puissance_dissipee(S, a):
    taille = S.shape[0]
    I = sp.eye(taille)  # Matrice identité
    S_dagger = S.conjugate().transpose()  # Transposée complexe conjuguée de S
    Q_S = I - S_dagger @ S  # Matrice de dissipation
    a_dagger = a.conjugate().transpose()  # Transposée complexe conjuguée de a
    P = 1/2 * a_dagger @ Q_S @ a
    return P[0]  # Retourne l'élément scalaire

def calculer_matrices_formalismes(S,Z,Y):
    taille = S.shape[0]
    I = sp.eye(taille)
    S_dagger = S.conjugate().transpose()
    Q_S = I - S_dagger @ S  # Matrice de dissipation
    
    # Calcul des formalismes
    Q_Z = 1/2 * (Z + Z.conjugate().transpose())
    Q_Y = 1/2 * (Y + Y.conjugate().transpose())
    
    return {'Q_S': Q_S, 'Q_Z': Q_Z, 'Q_Y': Q_Y}

def calculate_and_display_transfer_function(G, input_node, output_node):
    # Calculer la fonction de transfert en utilisant la méthode de Mason
    result = mason(G, input_node, output_node)
    
    # Afficher la fonction de transfert
    print(f"✅ La fonction de transfert du port {input_node.label} au port {output_node.label} est :")
    if result.transfer_function:
        T = result.transfer_function[0][0]
        actual = T.subs(result.transfer_function) \
            .subs(result.numerator) \
            .subs(result.denominator) \
            .subs(result.determinant) \
            .subs(result.paths) \
            .subs(result.loops)
        
        # Afficher la fonction de transfert simplifiée
        sp.pprint(actual, use_unicode=True)
    else:
        print("❌ Aucune fonction de transfert n'a été trouvée.")
