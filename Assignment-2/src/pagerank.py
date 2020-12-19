import time


def biasedPageRank(adjGraph, preference_vector=None, alpha=0.85, max_iterations=128, tolerance=1.0e-9):
    """
    Compute the biased PageRank centrality of all nodes in the graph
    Calculate the PageRank values using the standard power-iteration method

    Parameters
    ----------
    adjGraph: src.graph.AdjGraph
        Graph object for which centrality needs to be computed

    preference_vector: list, default = None
        List of nodes to bias PageRank for by giving them high d(u) score and 0 for rest of the nodes

    alpha: float, default = 0.85
        Damping parameter when performing random walk on Graph. Defaults to original paper value

    max_iterations: int, default = 128
        Max number of iterations to run in the power-iteration method

    tolerance: float, default = 1.0e-9
        If difference in 2 consecutive PageRank vectors is less than n * tolerance, we assume it has converged
        Here n is the number of nodes
    ----------

    Returns
    -------
    pageRank : dict
        Dictionary with node ID as key and PageRank centrality being value

    convIteration: int
        Iteration number when we stopped iterating and the values of PageRank converged

    diff: float
       time taken to calculate closenessCentrality for all nodes
    ----------

    Implement the biased version where instead of giving all nodes same value of d(u), we bias towards
    a known set of nodes by setting their d(u) values to 1 / len(preference_vector) and rest of the d(u)
    values to zero. This is done to boost ranking of pages in our preference vector and their neighbours since
    in each iteration, there is a probability of performing random walk instead of going to any of the neighbours

    After each iteration, the PageRank values are normalized such that their sum is 1. Then absolute values
    of error are computed to check if err < n * tolerance. If it is true, we know that we can stop
    further iterations since there will be no further convergence
    """

    start = time.time()
    graph = adjGraph.SNAPGraph
    n = len(adjGraph)

    d = {node.GetId(): 0.0 for node in graph.Nodes()}

    # If preference_vector is not None, then set values of d[u] according to the given vector
    if preference_vector:
        s = len(preference_vector)
        for node in preference_vector:
            d[node] = 1 / s
    else:
        d = {node.GetId(): 1 / n for node in graph.Nodes()}

    pageRank = d.copy()
    convIteration = max_iterations

    # Iterate for a fixed `max_iterations` times, but we can break early as well
    for idx in range(max_iterations):
        prevIter = pageRank
        # Compute PR(u) according to the algorithm. All nodes v distribute their PR's equally among all nodes they point to
        for u in graph.Nodes():
            t = 0.0
            for v in u.GetOutEdges():
                temp = pageRank[v] / graph.GetNI(v).GetOutDeg()
                t += temp

            pageRank[u.GetId()] = alpha * t + (1 - alpha) * d[u.GetId()]

        # Normalize PageRank values after each iteration to make their sum as 1
        normSum = sum(pageRank.values())
        pageRank = {k: v / normSum for k, v in pageRank.items()}

        # Calculate error values for this iterations
        nodeErrors = [abs(pageRank[i.GetId()] - prevIter[i.GetId()])
                      for i in graph.Nodes()]
        err = sum(nodeErrors)
        if err < n * tolerance:
            convIteration = idx + 1
            break

    end = time.time()
    diff = end - start
    return (pageRank, convIteration, diff)
