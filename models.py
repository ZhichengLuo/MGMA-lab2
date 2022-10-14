import networkx as nx
import random

def LinearThreshold(G: nx.Graph, seeds: list):
    if len(seeds) == 0:
        return [], []
    assert type(seeds[0]) == type(list(G)[0]), 'seeds must be the same type as graph nodes'

    infected_nodes = seeds.copy()
    uninfected_nodes = [n for n in list(G) if n not in infected_nodes]
    random.seed(100)
    acceptance_threshold = {n:random.random() for n in list(G)}
    infection_log = list()
    infection_log.append(infected_nodes.copy())
    
    while True:
        infected_by_step = list()
        activate_any = False
        new_uninfected_nodes = uninfected_nodes[:]
        for node in uninfected_nodes:
            d = 1 / G.degree(node)
            s = 0
            for ne in G.neighbors(node):
                if ne in infected_nodes:
                    s += d
            if s > acceptance_threshold[node]:
                activate_any = True
                infected_by_step.append(node)
                infected_nodes.append(node)
                new_uninfected_nodes.remove(node)
        if not activate_any:
            break
        uninfected_nodes = new_uninfected_nodes
        infection_log.append(infected_by_step)
    return infected_nodes, infection_log


def IndependantCascade(G: nx.Graph, seeds: list, activation_prob: float = 0.5):
    assert type(seeds[0]) == type(list(G)[0]), 'seeds must be the same type as graph nodes'

    infected_nodes = seeds.copy()
    uninfected_nodes = [n for n in list(G) if n not in infected_nodes]
    # record the edge that can't be use for activation again
    # only need to record when activation fails
    used_edges = list()  

    infection_log = list()
    infection_log.append(infected_nodes.copy())
    
    while True:
        infected_by_step = list()
        activate_any = False
        new_uninfected_nodes = uninfected_nodes[:]
        for node in uninfected_nodes:
            activated_neighbors = [ne for ne in G.neighbors(node) if ne in infected_nodes]
            valid_neighbors = [ne for ne in activated_neighbors if (ne, node) not in used_edges]
            if len(valid_neighbors) == 0:
                continue
            prob = 1 - (1-activation_prob) ** len(valid_neighbors)
            random.seed(100)
            ran = random.random()
            if ran <= prob:
                # Activation succeeds
                activate_any = True
                infected_by_step.append(node)
                infected_nodes.append(node)
                new_uninfected_nodes.remove(node)
            else:
                used_edges += [(ne, node) for ne in valid_neighbors]
        if not activate_any:
            break
        uninfected_nodes = new_uninfected_nodes
        infection_log.append(infected_by_step)
    return infected_nodes, infection_log


def greedy_seeds(G : nx.Graph, budget : int, model, **model_kwds):
    seeds = []
    for i in range(budget):
        print(f'finding {i+1}/{budget}')
        res = model(G, seeds, **model_kwds)
        old_score = len(res[0])
        max_gain = 0
        max_gain_node = None
        for n in list(G):
            if n in seeds:
                continue
            res = model(G, seeds+[n], **model_kwds)
            score = len(res[0])
            gain = score - old_score
            if gain > max_gain:
                max_gain = gain
                max_gain_node = n
        if max_gain_node:
            seeds.append(max_gain_node)
        else:
            break
    return seeds