from typing import List
from graph.algorithms.graph import Graph, Node

def strongly_connected_components(graph: Graph) -> List[List[Node]]:
    index_counter = [0]
    stack = []
    lowlink = {}
    index = {}
    result = []

    def _strong_connect(node: Node):
        index[node] = index_counter[0]
        lowlink[node] = index_counter[0]
        index_counter[0] += 1
        stack.append(node)

        successors = node.outgoing
        for successor in successors:
            if successor.end not in index:
                _strong_connect(successor.end)
                lowlink[node] = min(lowlink[node], lowlink[successor.end])
            elif successor.end in stack:
                lowlink[node] = min(lowlink[node], index[successor.end])

        if lowlink[node] == index[node]:
            connected_component = []

            while True:
                successor = stack.pop()
                connected_component.append(successor)
                if successor == node:
                    break
            result.append(connected_component[:])

    for node in graph.nodes:
        if node not in index:
            _strong_connect(node)

    return result
