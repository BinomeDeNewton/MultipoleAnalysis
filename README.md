### README en Français

# Analyse de Multipôle et Visualisation de Graphique

Ce projet vise à analyser un multipôle pour obtenir sa fonction de transfert, en utilisant l'étude du graphe de fluence. L'objectif principal est de fournir un moyen efficace et visuel de comprendre la dynamique interne du système multipôle à travers la visualisation de son graphe de fluence et l'analyse de ses composantes.

## Fonctionnalités

- Calcul de la matrice génératrice du multipôle.
- Visualisation du graphe de fluence du système.
- Analyse des composantes fortement connexes et des boucles dans le graphe.
- Calcul de la fonction de transfert à l'aide de la méthode de Mason.
- Vérification de l'adaptation du système et identification des pertes.

## Bibliothèques Utilisées

- `sympy` : Utilisé pour les opérations mathématiques symboliques.
- `networkx` : Employé pour la création, la manipulation et l'étude de la structure, de la dynamique et des fonctions des réseaux complexes.
- `matplotlib` : Utilisé pour la visualisation des graphes.
- `numpy` : Utilisé pour les calculs numériques.
- J'ai réutilisé le code de l'algorithme de Mason, Johnson et Tarjan ainsi que de la classe graph du [projet GitHub signalflowgrapher](https://github.com/hanspi42/signalflowgrapher/), qui étaient bien clairs et précis, et je les ai adaptés pour mon projet.

## Structure du Projet

```
SFG/
│
│
├── main.py
│
├── ui/
│   └── inputs.py
│
├── mathematics/
│   ├── matrix_operations.py
│   ├── signal_processing.py
│   └── signalflow_algorithms/
│       ├── common/
│       ├── __init__.py
│       └── algorithms/
│           ├── __init__.py
│           ├── johnson.py
│           ├── tarjan.py
│           └── mason.py 
│
└── graph/
    ├── graph_initialization.py
    └── algorithms/
        ├── find_paths.py
        ├── graph_operations.py
        ├── graph.py
        └── loop_group.py
```

## Comment Utiliser

Pour exécuter ce projet, assurez-vous d'avoir toutes les dépendances nécessaires installées. Lancez ensuite le script `main.py` :

```bash
python main.py
```

Suivez les instructions à l'écran pour procéder à l'analyse et à la visualisation.

---

### README in English

# Multipole Analysis and Graph Visualization

This project aims to analyze a multipole to obtain its transfer function, using the study of the signal flow graph. The main goal is to provide an efficient and visual way to understand the internal dynamics of the multipole system through the visualization of its signal flow graph and the analysis of its components.

## Features

- Calculation of the multipole's generating matrix.
- Visualization of the system's signal flow graph.
- Analysis of strongly connected components and loops in the graph.
- Calculation of the transfer function using Mason's method.
- Verification of system matching and identification of losses.

## Libraries Used

- `sympy`: Used for symbolic mathematical operations.
- `networkx`: Used for the creation, manipulation, and study of the structure, dynamics, and functions of complex networks.
- `matplotlib`: Used for graph visualization.
- `numpy`: Used for numerical calculations.
- I reused the code from Mason, Johnson, and Tarjan's algorithm and the graph class from the [GitHub project signalflowgrapher](https://github.com/hanspi42/signalflowgrapher/), which were very clear and precise, and adapted them for my project.

## Project Structure

```
SFG/
│
│
├── main.py
│
├── ui/
│   └── inputs.py
│
├── mathematics/
│   ├── matrix_operations.py
│   ├── signal_processing.py
│   └── signalflow_algorithms/
│       ├── common/
│       ├── __init__.py
│       └── algorithms/
│           ├── __init__.py
│           ├── johnson.py
│           ├── tarjan.py
│           └── mason.py 
│
└── graph/
    ├── graph_initialization.py
    └── algorithms/
        ├── find_paths.py
        ├── graph_operations.py
        ├── graph.py
        └── loop_group.py
```

## How to Use

To run this project, ensure all necessary dependencies are installed. Then, launch the `main.py` script:

```bash
python main.py
```

Follow the on-screen instructions to proceed with the analysis and visualization.
