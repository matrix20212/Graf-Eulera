import numpy as np
import random
from pyvis.network import Network

def generate_graph(n, p):
    A = np.zeros((n, n), dtype=int)
    for i in range(n):
        for j in range(i+1, n):
            if random.random() < p:
                A[i][j] = A[j][i] = 1
    return A

def degree_sequence(A):
    return np.sum(A, axis=1)

def has_eulerian_cycle(A):
    return all(degree_sequence(A) % 2 == 0)

def connect_vertices(A, i, j):
    A[i][j] = A[j][i] = 1

def disconnect_vertices(A, i, j):
    A[i][j] = A[j][i] = 0

def find_vertices_with_odd_degrees(degrees):
    return [i for i, degree in enumerate(degrees) if degree % 2 != 0]

def make_eulerian(A):
    while not has_eulerian_cycle(A):
        degrees = degree_sequence(A)
        odd_vertices = find_vertices_with_odd_degrees(degrees)
        v1, v2 = random.sample(odd_vertices, 2)
        if not A[v1][v2]:
            connect_vertices(A, v1, v2)
        else:
            common_neighbors = [v for v in range(len(A)) if A[v1][v] and A[v2][v]]
            if common_neighbors:
                neighbor = random.choice(common_neighbors)
                disconnect_vertices(A, v1, neighbor)
                disconnect_vertices(A, v2, neighbor)
            else:
                disconnect_vertices(A, v1, v2)
    return A

n = 10  # Romiar grafu
p = 0.7  # prawdopodobieństwo

# Generowanie losowego grafu
A = generate_graph(n, p)
print("Initial graph:")
print(A)

# Tworzenie grafu Eulerowskiego
A = make_eulerian(A)
print("Eulerian graph:")
print(A)

# Zapis do pliku
with open("graph.txt", "w") as file:
    for row in A:
        row_str = ''.join(map(str, row))
        row_sum = sum(row)
        file.write(row_str + " | " + str(row_sum) + "\n")

# Rysowanie grafu
g = Network(height="800px",width="100%")

file = open("graph.txt","r")

# Generowanie wierzchołków
color=["red","blue","green","#03fc73","#42270b","pink","purple","black","orange","#00bfff"]
for i in range(n):   
    g.add_node(i, label=str(i),color=color[i])

j = 0
i = 0

# Wczytanie danych z pliku i konwersja do zapisu macierzowego
B = []
for line in file.readlines():
    binary_string, _ = line.split(' | ')  # Podział na część binarną i liczbę
    binary_array = np.array([int(char) for char in binary_string])  # Konwersja na tablicę numpy
    B.append(binary_array)

A = np.array(B)

# Rysowanie krawędzi
for i in range(n):
    for j in range(i+1, n):
        if A[i][j] == 1:
            g.add_edge(i, j,smooth=False)

# Obliczanie ilosci krawędzi
i=0
for _ in g.get_edges():
    i=i+1
print("Liczba krawędzi = " + str(i))

# Obliczenie gęstości
D = (2 * i) / (n * (n - 1))
print("Gęstość grafu = " + str(round(D,3)))

# Wypisanie wrzystkich powiązań
print(g.get_adj_list())

g.hrepulsion(node_distance=300)
g.toggle_physics(True)
g.barnes_hut()
g.show('graph-visualization.html', True, False)