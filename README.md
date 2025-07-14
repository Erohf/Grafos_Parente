# Algoritmo de Pósa e Algoritmo Backtracking para Detecção de Ciclos Hamiltonianos

Este projeto implementa o **Algoritmo de Pósa**, um algoritmo heurístico desenvolvido por Louis Pósa em 1976 para encontrar ciclos hamiltonianos em grafos. Um ciclo hamiltoniano é um ciclo que visita cada vértice do grafo exatamente uma vez e retorna ao vértice inicial.
E também implementa o **Algoritmo Backtracking**, que explora sistematicamente todas as possíveis configurações de caminhos usando recursão e retrocesso.

## Visão Geral

O algoritmo de Pósa é particularmente significativo na teoria dos grafos por ter sido uma das primeiras abordagens heurísticas eficazes para o problema do ciclo hamiltoniano, que é NP-completo. O algoritmo usa uma combinação de técnicas de extensão de caminho, rotação e histórico de estados para buscar ciclos hamiltonianos.

O algoritmo Backtracking, por sua vez, tenta adicionar recursivamente os vértices restantes, um por um. Se um vértice válido for encontrado, prossegue; caso contrário, retrocede e tenta outra opção. É uma abordagem determinística que garante encontrar uma solução se ela existir.

## Descrição dos Algoritmos

### Algoritmo de Pósa

O algoritmo de Pósa implementado funciona através dos seguintes passos:

1. **Inicialização**: Começa com um vértice aleatório
2. **Extensão de Caminho**: Estende o caminho atual adicionando vértices não visitados
3. **Seleção Aleatória**: Escolhe aleatoriamente um vizinho não processado do vértice atual
4. **Transformação Rotacional**: Quando encontra um vértice já visitado, aplica uma transformação rotacional para reorganizar o caminho
5. **Histórico de Estados**: Mantém um histórico de vizinhos processados para cada estado (comprimento do caminho, vértice final) para evitar repetições
6. **Terminação**: Continua até que um ciclo hamiltoniano seja encontrado ou o limite de iterações seja atingido

### Algoritmo Backtracking

O algoritmo backtracking funciona através dos seguintes passos:

1. **Escolha do vértice inicial**: Começa sempre com o vértice 0
2. **Extensão recursiva**: Para cada posição no caminho, tenta todos os vértices possíveis
3. **Verificação de segurança**: Verifica se o vértice candidato está conectado ao anterior e não foi visitado
4. **Backtracking**: Se não conseguir estender o caminho, retrocede e tenta outras opções
5. **Verificação do ciclo**: Ao completar o caminho, verifica se o último vértice conecta de volta ao primeiro

### Características Principais

#### Algoritmo de Pósa:
- **Seleção Aleatória**: Usa escolhas aleatórias para explorar diferentes possibilidades
- **Transformação Rotacional**: Reorganiza partes do caminho quando encontra vértices já visitados
- **Histórico de Estados**: Evita processar os mesmos vizinhos para o mesmo estado
- **Múltiplas Tentativas**: Suporta execução com múltiplas tentativas independentes

#### Algoritmo Backtracking:
- **Exploração Sistemática**: Explora todas as possibilidades de forma ordenada
- **Garantia de Completude**: Se existe uma solução, o algoritmo a encontrará
- **Estrutura Recursiva**: Usa recursão para construir o caminho incrementalmente

## Arquivos

- `posa_algorithm.py` - Implementação principal do algoritmo de Pósa e classe Graph
- `backtracking_algorithm.py` - Implementação principal do algoritmo backtracking  
- `compare_algorithms.py` - Script de comparação entre os dois algoritmos com testes automatizados
- `README.md` - Este arquivo de documentação

## Uso

### Uso Básico - Algoritmo de Pósa

```python
from posa_algorithm import Graph, PosaAlgorithm

# Criar um grafo
graph = Graph(5)
graph.add_edge(0, 1)
graph.add_edge(1, 2)
graph.add_edge(2, 3)
graph.add_edge(3, 4)
graph.add_edge(4, 0)
graph.add_edge(0, 2)  # Adicionar uma diagonal
graph.add_edge(1, 3)  # Adicionar outra diagonal

# Encontrar ciclo hamiltoniano com uma única tentativa
posa = PosaAlgorithm(graph)
cycle = posa.find_hamiltonian_cycle()

if cycle:
    print(f"Ciclo hamiltoniano encontrado: {cycle}")
else:
    print("Nenhum ciclo hamiltoniano encontrado")

# Ou usar múltiplas tentativas (recomendado)
cycle = posa.find_hamiltonian_cycle_multiple_attempts(num_attempts=50, max_iterations_per_attempt=1000)
```

### Uso Básico - Algoritmo Backtracking

### Uso Básico - Algoritmo Backtracking

``` python
from backtracking_algorithm import BacktrackingAlgorithm
from posa_algorithm import Graph

# Criar um grafo
graph = Graph(5)
graph.add_edge(0, 1)
graph.add_edge(1, 2)
graph.add_edge(2, 3)
graph.add_edge(3, 4)
graph.add_edge(4, 0)

# Encontrar ciclo hamiltoniano
backtracking = BacktrackingAlgorithm(graph)
cycle = backtracking.find_hamiltonian_cycle(graph)

if cycle:
    print("✓ Ciclo hamiltoniano encontrado:", cycle)
else:
    print("✗ Nenhum ciclo hamiltoniano encontrado")
```

### Criando Grafos de Teste

O projeto inclui funções auxiliares para criar diferentes tipos de grafos:

```python
from posa_algorithm import create_sample_graph, create_complete_graph

# Grafo de exemplo pré-definido
sample_graph = create_sample_graph()

# Grafo completo (todos os vértices conectados entre si)
complete_graph = create_complete_graph(6)  # K6
```

### Tipos de Grafos Suportados

A implementação pode lidar com vários tipos de grafos:

- **Grafos completos** (Kn) - Sempre têm ciclos hamiltonianos para n ≥ 3
- **Grafos ciclo** (Cn) - O próprio ciclo é um ciclo hamiltoniano
- **Grafos roda** (Wn) - Geralmente têm ciclos hamiltonianos
- **Grafos grade** - Podem ou não ter ciclos dependendo das dimensões
- **Grafos personalizados** - Qualquer estrutura de grafo não direcionado

### Grafos de Exemplo Incluídos

A implementação inclui vários grafos de exemplo para teste:

- **Grafo de exemplo (5 vértices)**: Grafo com ciclo básico e algumas diagonais adicionais
- **Grafos completos (Kn)**: Todos os vértices conectados entre si - sempre têm ciclos hamiltonianos para n ≥ 3
- **Grafos garantidamente hamiltonianos**: Gerados automaticamente pelo script de comparação

## Executando o Código

### Execute a demonstração principal do algoritmo de Pósa:
```bash
python posa_algorithm.py
```

### Execute a comparação entre os algoritmos:
```bash
python compare_algorithms.py
```

O script de comparação (`compare_algorithms.py`) testa ambos os algoritmos em grafos de diferentes tamanhos (20-90 vértices), cada um garantido de ter um ciclo hamiltoniano. Ele reporta o sucesso/falha e o tempo gasto por cada algoritmo, com um limite de tempo de 5 segundos por tentativa.

## Complexidade dos Algoritmos

### Algoritmo de Pósa
- **Complexidade de Tempo**: O(n!) no pior caso, mas frequentemente tem desempenho melhor na prática devido às transformações rotacionais e múltiplas tentativas
- **Complexidade de Espaço**: O(n) para armazenar o caminho, vértices processados e histórico de estados
- **Características**: Heurístico, não garante encontrar solução mesmo se existir

### Algoritmo Backtracking
- **Complexidade de Tempo**: O(n!) no pior caso (explora todas as permutações possíveis)
- **Complexidade de Espaço**: O(n) para armazenar o caminho recursivo
- **Características**: Determinístico, garante encontrar solução se existir

## Base Teórica

### Problema do Ciclo Hamiltoniano

O problema do ciclo hamiltoniano pergunta se um dado grafo contém um ciclo que visita cada vértice exatamente uma vez. Este problema é:
- **NP-completo** para grafos gerais
- **Solúvel em tempo polinomial** para classes especiais de grafos (ex: grafos torneio)

### Condições Suficientes

Vários teoremas fornecem condições suficientes para ciclos hamiltonianos:

1. **Teorema de Ore**: Se deg(u) + deg(v) ≥ n para cada par de vértices não adjacentes, então o grafo tem um ciclo hamiltoniano
2. **Teorema de Dirac**: Se cada vértice tem grau ≥ n/2, então o grafo tem um ciclo hamiltoniano

### Contribuição de Pósa

O algoritmo de Pósa foi revolucionário porque:
- Forneceu uma abordagem heurística prática para um problema NP-completo
- Introduziu a técnica de rotação, que se tornou influente em algoritmos posteriores
- Demonstrou que estratégias de busca inteligentes poderiam frequentemente encontrar soluções eficientemente

## Limitações

### Algoritmo de Pósa
- É heurístico e pode não encontrar um ciclo hamiltoniano mesmo se um existir
- O desempenho depende da aleatoriedade das escolhas
- Requer múltiplas tentativas para melhorar a taxa de sucesso

### Algoritmo Backtracking  
- Complexidade exponencial pode tornar inviável para grafos grandes
- Tempo de execução pode ser muito alto mesmo para grafos médios
- Abordagem determinística pode ser ineficiente em certos tipos de grafo

## Extensões e Melhorias

A implementação básica pode ser estendida com:

1. **Melhores heurísticas** para seleção de vértices no algoritmo de Pósa
2. **Estratégias de rotação mais sofisticadas** 
3. **Abordagens híbridas** combinando ambos os algoritmos
4. **Otimizações de poda** para o algoritmo backtracking
5. **Processamento paralelo** para explorar múltiplos caminhos simultaneamente
6. **Detecção precoce de impossibilidade** usando condições suficientes conhecidas

## Comparação de Desempenho

O script `compare_algorithms.py` fornece uma comparação empírica detalhada entre os dois algoritmos, testando:

- **Grafos de tamanhos variados** (20-90 vértices)
- **Taxa de sucesso** de cada algoritmo
- **Tempo médio de execução** 
- **Limite de tempo configurável** (padrão: 5 segundos)
- **Grafos garantidamente hamiltonianos** para testes justos

### Resultados Típicos
- **Pósa**: Geralmente mais rápido quando encontra solução, mas pode falhar em alguns casos
- **Backtracking**: Mais confiável (sempre encontra se existe), mas pode ser muito lento para grafos maiores

## Valor Educacional

Esta implementação é valiosa para:
- Entender algoritmos heurísticos vs. determinísticos
- Aprender sobre teoria dos grafos e ciclos hamiltonianos
- Estudar problemas NP-completos e diferentes abordagens de solução
- Comparar trade-offs entre tempo de execução e garantias de solução
- Explorar o equilíbrio entre sofisticação algorítmica e desempenho prático
- Análise empírica de algoritmos através de benchmarks automatizados

## Estrutura do Projeto

```
Grafos/
├── posa_algorithm.py           # Algoritmo de Pósa + classe Graph
├── backtracking_algorithm.py   # Algoritmo Backtracking  
├── compare_algorithms.py       # Comparação e benchmarks
├── README.md                   # Documentação
```

## Requisitos

- Python 3.6+
- Bibliotecas padrão: `time`, `random`, `typing`, `threading`, `queue`
- Nenhuma dependência externa necessária

## Referências

- Pósa, L. (1976). "Hamiltonian circuits in random graphs"
- Ore, O. (1960). "Note on Hamilton circuits"  
- Dirac, G. A. (1952). "Some theorems on abstract graphs"
- Cormen, T. H., et al. (2009). "Introduction to Algorithms" - Capítulo sobre problemas NP-completos

## Licença

Esta implementação é fornecida para fins educacionais e pode ser livremente usada e modificada.
