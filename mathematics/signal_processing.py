import numpy as np
import sympy as sp

def est_multipole_sans_pertes(resultats):
    # Extraire les matrices des résultats
    Q_S = resultats['Q_S']
    Q_Z = resultats['Q_Z']
    Q_Y = resultats['Q_Y']
    
    # Fonction pour vérifier si tous les éléments d'une matrice sont nuls
    def est_matrice_nulle(matrice):
        # Obtenez les dimensions de la matrice
        m, n = matrice.shape
        # Parcourez chaque élément de la matrice pour vérifier s'il est nul
        for i in range(m):
            for j in range(n):
                # Si un élément n'est pas exactement zéro, retournez False
                if matrice[i, j] != 0:
                    return False
        # Si tous les éléments sont nuls, retournez True
        return True
    
    # Vérifier chaque matrice pour la condition de multipôle sans pertes
    conditions_sans_pertes = est_matrice_nulle(Q_S) and est_matrice_nulle(Q_Z) and est_matrice_nulle(Q_Y)
    
    return conditions_sans_pertes
    
def adjust_for_propagation_factors(S, a, b, gamma, d, size):
    # Vérifie si gamma et d ne sont pas vides
    if gamma and d:
        # Calcul de la matrice diagonale D avec les facteurs d'atténuation
        D = sp.diag(*[sp.exp(-gamma[i] * d[i]) for i in range(size)])
        # Ajustement de la matrice de scattering S avec les facteurs de propagation
        Sr = D * S * D
        # Ajustement des vecteurs a et b avec les facteurs de propagation
        ar = sp.Matrix(size, 1, lambda i, j: a[i] * sp.exp(gamma[i] * d[i]))
        br = sp.Matrix(size, 1, lambda i, j: b[i] * sp.exp(-gamma[i] * d[i]))
    else:
        # Si les facteurs de propagation ne sont pas pris en compte, retourner les paramètres initiaux
        Sr = S
        ar = a
        br = b
        
    return Sr, ar, br
