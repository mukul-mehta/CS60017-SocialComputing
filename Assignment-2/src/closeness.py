import time


def closenessCentrality(adjGraph):
    """
    Compute closeness centrality for all nodes of a graph

    Parameters
    ----------
    adjGraph: src.graph.AdjGraph
        Graph object for which centrality needs to be computed
    ----------

    Returns
    -------
    closeness_centrality : dict
        Dictionary with node ID as key and closeness centrality being value

    diff: float
       time taken to calculate closenessCentrality for all nodes
    ----------

    To compute centrality, distances between all pairs of nodes need
    to be computed. For single node to all other node shortest distances,
    BFS is implemented since the given graph is taken to be unweighted

    In case of disconnected components in a graph, distance is set to INT_MAX
    which results in 0 closeness centrality for that node
    """

    start = time.time()
    graph = adjGraph.SNAPGraph
    closeness_centrality = {}

    for node in graph.Nodes():
        nDist = allNodesDistance(adjGraph, node)
        distSum = sum(nDist.values())

        if distSum == 0:
            closeness_centrality[node.GetId()] = 0.0
        else:
            closeness_centrality[node.GetId()] = (len(nDist) - 1) / distSum

    end = time.time()
    diff = end - start

    return (closeness_centrality, diff)


def allNodesDistance(adjGraph, startNode):
    """
    For a startNode, generates a dictionary with key as startNode and values being
    distances to all other nodes reachable from startNode

    Parameters
    ----------
    adjGraph: src.graph.AdjGraph
        Graph object of which startNode is element
    startNode: snap.TUNGraphNodeI
        Object of SNAP's internal Node class
    ----------

    Returns
    -------
    _: dict
        Dictionary with value being distances of all other reachable nodes from startNode
    ----------

    This method calls the BFS method, which is a generator and yields (node, level)
    for each node it finds when traversing in a Breadth-First fashion. The return value
    is converted to a dictionary which is returned when BFS is complete
    """

    source = {startNode.GetId(): 1}
    return dict(BFS(adjGraph, source))


def BFS(adjGraph, source):
    """
    Starting from source, find distance of all reachable nodes
    in a Breadth First Manner

    Parameters
    ----------
     adjGraph: src.graph.AdjGraph
        Graph object on which BFS is run
    source : dict
        Starting node
    """

    adj = adjGraph.adj
    levels = {}
    currentLevel = 0
    n = len(adj)

    # Generate the set of nodes you traverse next (Starting with source)
    neighbourList = set(source)
    while neighbourList:
        bfsNodes = neighbourList
        neighbourList = set()
        reachable = []

        for v in bfsNodes:
            if v not in levels:
                levels[v] = currentLevel
                reachable.append(v)
                # Yield from the generator function for each node a tuple (node, levelOfThatNode)
                # Result is stored in the return dict of function `allNodesDistance`
                yield (v, currentLevel)

        if len(levels) == n:
            return

        for v in reachable:
            # Add neighbours of present elements to iterate over in the next level
            neighbourList.update(adj[v])
        currentLevel += 1
