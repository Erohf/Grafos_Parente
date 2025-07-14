import random
from typing import List, Set, Dict, Optional, Tuple


class Graph:
    
    def __init__(self, num_vertices: int):

        self.num_vertices = num_vertices
        self.adjacency_list: Dict[int, Set[int]] = {i: set() for i in range(num_vertices)}
    
    def add_edge(self, u: int, v: int) -> None:

        if 0 <= u < self.num_vertices and 0 <= v < self.num_vertices:
            self.adjacency_list[u].add(v)
            self.adjacency_list[v].add(u)
    
    def get_neighbors(self, vertex: int) -> Set[int]:

        return self.adjacency_list[vertex]
    
    def has_edge(self, u: int, v: int) -> bool:

        return v in self.adjacency_list[u]


class PosaAlgorithm:

    
    def __init__(self, graph: Graph):

        self.graph = graph
        self.path: List[int] = []
        self.processed_vertices: Set[int] = set()
        self.endpoint_history: Dict[Tuple[int, int], Set[int]] = {}  # (path_length, endpoint) -> set of processed neighbors
        
    def rotational_transformation(self, path: List[int], edge_to_x: Tuple[int, int]) -> Tuple[List[int], int]:

        current_endpoint, x = edge_to_x
        
        if x not in path:
            return path, current_endpoint
        
        x_index = path.index(x)
        
        if x_index == len(path) - 1:
            return path, current_endpoint
        
        new_path = path[:x_index + 1] + path[x_index + 1:][::-1]
        new_endpoint = new_path[-1]
        
        return new_path, new_endpoint
    
    def get_unprocessed_neighbors(self, vertex: int) -> Set[int]:

        neighbors = self.graph.get_neighbors(vertex)
        path_length = len(self.path)
        
        key = (path_length, vertex)
        if key in self.endpoint_history:
            processed_for_this_state = self.endpoint_history[key]
            return neighbors - processed_for_this_state
        
        return neighbors
    
    def mark_neighbor_processed(self, endpoint: int, neighbor: int) -> None:

        path_length = len(self.path)
        key = (path_length, endpoint)
        
        if key not in self.endpoint_history:
            self.endpoint_history[key] = set()
        
        self.endpoint_history[key].add(neighbor)
    
    def find_hamiltonian_cycle(self, max_iterations: int = 10000) -> Optional[List[int]]:

        import time
        
        if self.graph.num_vertices == 0:
            return None
        
        initial_vertex = random.randint(0, self.graph.num_vertices - 1)
        self.path = [initial_vertex]
        self.processed_vertices = {initial_vertex}
        self.endpoint_history = {}
        
        iterations = 0
        
        while iterations < max_iterations:
            iterations += 1
            
            time.sleep(0.002)
            
            current_endpoint = self.path[-1]
            
            unprocessed_neighbors = self.get_unprocessed_neighbors(current_endpoint)
            
            if not unprocessed_neighbors:
                return None
            
            x = random.choice(list(unprocessed_neighbors))
            self.mark_neighbor_processed(current_endpoint, x)
            
            if x not in self.processed_vertices:
                self.path.append(x)
                self.processed_vertices.add(x)
            else:
                new_path, new_endpoint = self.rotational_transformation(self.path, (current_endpoint, x))
                
                path_length = len(new_path)
                key = (path_length, new_endpoint)
                
                if key not in self.endpoint_history:
                    self.path = new_path
            
            if len(self.path) == self.graph.num_vertices:
                start_vertex = self.path[0]
                end_vertex = self.path[-1]
                
                if self.graph.has_edge(start_vertex, end_vertex):
                    return self.path + [start_vertex]
        
        return None
    
    def find_hamiltonian_cycle_multiple_attempts(self, num_attempts: int = 100, 
                                                max_iterations_per_attempt: int = 1000) -> Optional[List[int]]:
       
        for attempt in range(num_attempts):
            self.path = []
            self.processed_vertices = set()
            self.endpoint_history = {}
            
            result = self.find_hamiltonian_cycle(max_iterations_per_attempt)
            if result is not None:
                print(f"Ciclo hamiltoniano encontrado na tentativa {attempt + 1}")
                return result
        
        print(f"Nenhum ciclo hamiltoniano encontrado após {num_attempts} tentativas")
        return None


def create_sample_graph() -> Graph:
    
    graph = Graph(5)
    
    graph.add_edge(0, 1)
    graph.add_edge(1, 2)
    graph.add_edge(2, 3)
    graph.add_edge(3, 4)
    graph.add_edge(4, 0)
    graph.add_edge(0, 2)  
    graph.add_edge(1, 3)  
    
    return graph


def create_complete_graph(n: int) -> Graph:
    
    graph = Graph(n)
    for i in range(n):
        for j in range(i + 1, n):
            graph.add_edge(i, j)
    return graph


def print_graph_info(graph: Graph) -> None:
   
    print(f"Grafo com {graph.num_vertices} vértices:")
    for vertex in range(graph.num_vertices):
        neighbors = sorted(graph.get_neighbors(vertex))
        print(f"Vértice {vertex}: vizinhos = {neighbors}")
    print()


def main():
   
    print("Algoritmo de Pósa para Encontrar Ciclos Hamiltonianos")
    print("=" * 50)
    
    print("Testando com grafo de exemplo:")
    sample_graph = create_sample_graph()
    print_graph_info(sample_graph)
    
    posa = PosaAlgorithm(sample_graph)
    cycle = posa.find_hamiltonian_cycle_multiple_attempts(num_attempts=50)
    
    if cycle:
        print(f"Ciclo hamiltoniano encontrado: {cycle}")
        print(f"Comprimento do ciclo: {len(cycle) - 1} (mais retorno ao início)")
    else:
        print("Nenhum ciclo hamiltoniano encontrado")
    
    print("\n" + "=" * 50)
    
    print("Testando com grafo completo (K4):")
    complete_graph = create_complete_graph(4)
    print_graph_info(complete_graph)
    
    posa_complete = PosaAlgorithm(complete_graph)
    cycle_complete = posa_complete.find_hamiltonian_cycle_multiple_attempts(num_attempts=20)
    
    if cycle_complete:
        print(f"Ciclo hamiltoniano encontrado: {cycle_complete}")
        print(f"Comprimento do ciclo: {len(cycle_complete) - 1} (mais retorno ao início)")
    else:
        print("Nenhum ciclo hamiltoniano encontrado")
    
    print("\n" + "=" * 50)
    
    print("Testando com grafo completo (K6):")
    large_complete_graph = create_complete_graph(6)
    print(f"Grafo com {large_complete_graph.num_vertices} vértices (grafo completo)")
    
    posa_large = PosaAlgorithm(large_complete_graph)
    cycle_large = posa_large.find_hamiltonian_cycle_multiple_attempts(num_attempts=10)
    
    if cycle_large:
        print(f"Ciclo hamiltoniano encontrado: {cycle_large}")
        print(f"Comprimento do ciclo: {len(cycle_large) - 1} (mais retorno ao início)")
    else:
        print("Nenhum ciclo hamiltoniano encontrado")


if __name__ == "__main__":
    main()
