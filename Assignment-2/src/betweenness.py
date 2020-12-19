import time

from collections import deque


def betweennessCentrality(adjGraph):
    """
    Compute betweenness centrality for all nodes of a graph

    Parameters
    ----------
    adjGraph: src.graph.AdjGraph
        Graph object for which centrality needs to be computed
    ----------

    Returns
    -------
    betweenness_centrality : dict
        Dictionary with node ID as key and betweenness centrality being value

    diff: float
       time taken to calculate betweenness for all nodes
    ----------

    To compute centrality, all shortest paths between all pairs of nodes need
    to be computed and all such paths such that node s lies on the shortest path
    Brandes' algorithm is used to compute fraction of such paths

    The value of betweenness for each node is normalized by dividing by (n - 1) * (n - 2)
    which is twice the number of pairs excluding the node s
    """

    start = time.time()
    n = len(adjGraph)
    graph = adjGraph.SNAPGraph
    betweenness_centrality = {}

    for node in graph.Nodes():
        betweenness_centrality[node.GetId()] = 0.0

    for node in graph.Nodes():
        reachable, parents, pathCounts = shortestPaths(adjGraph, node)
        # Delta from Brandes' Algorithm
        delta = dict.fromkeys(reachable, 0)

        while reachable:
            w = reachable.pop()
            coeff = (1 + delta[w]) / pathCounts[w]

            for v in parents[w]:
                delta[v] += pathCounts[v] * coeff

            if w != node:
                betweenness_centrality[w] += delta[w]

    # No factor of 2 since it is an undirected graph and we're normalizing for it when calculating betweenness
    normalizationConstant = 1 / ((n - 1) * (n - 2))
    for k, v in betweenness_centrality.items():
        betweenness_centrality[k] *= normalizationConstant

    end = time.time()
    diff = end - start

    return (betweenness_centrality, diff)


def shortestPaths(adjGraph, startNode):
    """
    For a given startNode, `shortestPaths` returns a list of values that Brandes'
    algorithm needs

    Parameters
    ----------
    adjGraph: src.graph.AdjGraph
        Graph object of which startNode is element
    startNode: snap.TUNGraphNodeI
        Object of SNAP's internal Node class
    ----------

    Returns
    -------
    reachable: list
        List of all nodes reachable from startNode when traversing in a breadth-first fashion

    parents: dict
        For a given node key, gives a list of predecssor nodes as value

    pathCounts: dict
        For a given node, number of ways of reaching it
    ----------

    Reference for Brandes' algorithm was taken from: https://www.cl.cam.ac.uk/teaching/1617/MLRD/handbook/brandes.pdf
    Delta(s) is the ratio of shortest paths that go through node s for all pairs of shortest paths between any pair of nodes in the graph
    """

    graph = adjGraph.SNAPGraph
    adj = adjGraph.adj

    reachable = []
    parents = {}
    pathCounts = {}
    distances = {}

    for node in graph.Nodes():
        parents[node.GetId()] = []
        pathCounts[node.GetId()] = 0

    pathCounts[startNode.GetId()] = 1.0
    distances[startNode.GetId()] = 0

    queue = deque()
    queue.append(startNode.GetId())
    while queue:
        u = queue.popleft()
        reachable.append(u)

        for v in adj[u]:
            if v not in distances:
                # Add neighbours of present elements to queue
                queue.append(v)
                distances[v] = distances[u] + 1

            if distances[v] == distances[u] + 1:
                pathCounts[v] += pathCounts[u]
                # If node is at same distance, add u to parents list of v
                parents[v].append(u)

    return reachable, parents, pathCounts
