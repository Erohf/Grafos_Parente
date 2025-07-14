import time
from typing import Dict, Tuple
from posa_algorithm import Graph, Optional, List
from backtracking_algorithm import BacktrackingAlgorithm
import random
import threading
import queue

def create_guaranteed_hamiltonian_graph(n_vertices: int) -> Graph:

    graph = Graph(n_vertices)
    
    vertices = list(range(n_vertices))
    random.shuffle(vertices)
    
    vertex_positions = {v: i for i, v in enumerate(vertices)}
    
    for i in range(n_vertices - 1):
        graph.add_edge(vertices[i], vertices[i + 1])
    
    graph.add_edge(vertices[-1], vertices[0])
    
    import math
    connections_per_vertex = max(1, int(math.sqrt(n_vertices)))
    max_attempts_per_edge = n_vertices * 3
    
    vertices_to_process = vertices.copy()
    random.shuffle(vertices_to_process)
    
    for vertex in vertices_to_process:
        edges_added = 0
        total_attempts = 0
        
        while edges_added < connections_per_vertex and total_attempts < max_attempts_per_edge:
            pos = vertex_positions[vertex]
            min_distance = n_vertices // 4
            
            possible_targets = [v for v in vertices if abs(vertex_positions[v] - pos) >= min_distance]
            
            if not possible_targets:
                break
                
            target = random.choice(possible_targets)
            target_pos = vertex_positions[target]
            
            if (target != vertex and 
                not graph.has_edge(vertex, target) and
                abs(pos - target_pos) >= min_distance and
                not (pos == 0 and target_pos == n_vertices - 1) and
                not (pos == n_vertices - 1 and target_pos == 0)):
                
                graph.add_edge(vertex, target)
                edges_added += 1
            
            total_attempts += 1
    
    return graph

def test_algorithms(size: int, time_limit: float = 5.0) -> dict:
    
    graph = create_guaranteed_hamiltonian_graph(size)
    results = {
        'tamanho': size,
        'posa': {'sucesso': False, 'tempo': 0.0, 'tentativas': 0},
        'backtracking': {'sucesso': False, 'tempo': 0.0}
    }
    
    posa = PosaAlgorithm(graph)
    posa_start = time.perf_counter()
    attempts = 0
    posa_result = None
    
    def run_posa(result_queue, time_queue):
        nonlocal attempts
        start_time = time.perf_counter()
        try:
            while time.perf_counter() - start_time < time_limit:
                attempts += 1
                result = posa.find_hamiltonian_cycle(max_iterations=5000)
                if result is not None:
                    end_time = time.perf_counter()
                    result_queue.put(result)
                    time_queue.put(end_time - start_time)
                    break
            else:
                end_time = time.perf_counter()
                time_queue.put(end_time - start_time)
        except:
            end_time = time.perf_counter()
            time_queue.put(end_time - start_time)

    result_queue = queue.Queue()
    time_queue = queue.Queue()
    thread = threading.Thread(target=run_posa, args=(result_queue, time_queue))
    thread.daemon = True
    thread.start()
    thread.join(timeout=time_limit)
    
    if thread.is_alive():
        posa_result = None
        posa_time = time_limit
    else:
        try:
            posa_result = result_queue.get_nowait()
            posa_time = time_queue.get_nowait()
        except queue.Empty:
            posa_result = None
            posa_time = time.perf_counter() - posa_start
    results['posa']['sucesso'] = posa_result is not None
    results['posa']['tempo'] = posa_time
    results['posa']['tentativas'] = attempts
    
    backtracking = BacktrackingAlgorithm(graph)
    backtracking_start = time.perf_counter()
    backtracking_result = []
    backtracking_finished = False

    def run_backtracking(result_queue, time_queue):
        start_time = time.perf_counter()
        try:
            result = backtracking.find_hamiltonian_cycle(graph)
            end_time = time.perf_counter()
            result_queue.put(result)
            time_queue.put(end_time - start_time)
        except:
            end_time = time.perf_counter()
            result_queue.put([])
            time_queue.put(end_time - start_time)

    result_queue = queue.Queue()
    time_queue = queue.Queue()
    thread = threading.Thread(target=run_backtracking, args=(result_queue, time_queue))
    thread.daemon = True
    thread.start()
    thread.join(timeout=time_limit)
    
    if thread.is_alive():
        backtracking_result = []
        backtracking_time = time_limit
    else:
        try:
            backtracking_result = result_queue.get_nowait()
            backtracking_time = time_queue.get_nowait()
        except queue.Empty:
            backtracking_result = []
            backtracking_time = time.perf_counter() - backtracking_start
    
    results['backtracking']['sucesso'] = len(backtracking_result) > 0
    results['backtracking']['tempo'] = backtracking_time
    
    return results

def main():
   
    print("Comparando o Algoritmo de Pósa vs Algoritmo de Backtracking")
    print("=" * 100)
    print(f"{'Tam.':<8} {'Sucesso Pósa':<15} {'Tempo Pósa':<12} "
          f"{'Sucesso Backtracking':<20} {'Tempo Backtracking':<15}")
    print("-" * 85)
    
   
    for base_size in range(20, 91, 10):
        range_results = {
            'posa_successes': 0,
            'backtracking_successes': 0,
            'posa_times': [],
            'backtracking_times': []
        }
        
        for size in range(base_size, base_size + 10):
            results = test_algorithms(size)
            
            if results['posa']['sucesso']:
                range_results['posa_successes'] += 1
            if results['backtracking']['sucesso']:
                range_results['backtracking_successes'] += 1
                
            range_results['posa_times'].append(results['posa']['tempo'])
            range_results['backtracking_times'].append(results['backtracking']['tempo'])
            
            print(f"{size:<8} {str(results['posa']['sucesso']):<15} "
                  f"{results['posa']['tempo']:.6f}s{'  ':<2} "
                  f"{str(results['backtracking']['sucesso']):<20} {results['backtracking']['tempo']:.6f}s")
        
        avg_posa_time = sum(range_results['posa_times']) / len(range_results['posa_times'])
        avg_backtracking_time = sum(range_results['backtracking_times']) / len(range_results['backtracking_times'])
        
        print(f"\nResumo do intervalo {base_size}-{base_size+9}:")
        print(f"Pósa: {range_results['posa_successes']}/10 sucessos, Tempo médio: {avg_posa_time:.6f}s")
        print(f"Backtracking: {range_results['backtracking_successes']}/10 sucessos, "
              f"Tempo médio: {avg_backtracking_time:.6f}s")
        print("-" * 100)
    
    print("=" * 100)

if __name__ == "__main__":
    from posa_algorithm import PosaAlgorithm
    main()
