from typing import List
from posa_algorithm import Graph

class BacktrackingAlgorithm:
    def __init__(self, graph: Graph):      
        self.graph = graph
        self.n = graph.num_vertices
        self.path = []
        self.visited = set()

    def isSafe(self, vertex: int, graph: Graph, path: List[int], pos: int):
        
        if not graph.has_edge(path[pos - 1], vertex):
            return False

        return vertex not in path   

    def hamCycleUtil(self, graph: Graph, path: List[int], pos: int, n: int):
        
        if pos == n:
           
            return graph.has_edge(path[pos - 1], path[0])

        for v in range(1, n):
            if self.isSafe(v, graph, path, pos):
                path[pos] = v

                if self.hamCycleUtil(graph, path, pos + 1, n):
                    return True

                path[pos] = -1

        return False

    def find_hamiltonian_cycle(self, graph: Graph) -> List[int]:
        n = graph.num_vertices
        path = [-1] * n
        
        path[0] = 0

        if not self.hamCycleUtil(graph, path, 1, n):
            return []

        path.append(path[0])
        return path
