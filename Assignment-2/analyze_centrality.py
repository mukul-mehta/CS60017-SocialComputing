import os
import snap

from config import CONFIG
from src.graph import AdjGraph


def readNodes(filename):
    """
    Read a centrality file and return top 100 nodes as a set

    Parameters
    ----------
    filename: str or pathlib.Path
        Name of the file to read
    ----------

    Returns
    ----------
    _: set
        Returns a set of top 100 nodes sorted by centrality value
    ----------
    """

    filePath = os.path.join(CONFIG['CENTRALITIES_PATH'], filename)
    f = open(filePath)

    data = f.readlines()
    nodes = [node[0:4] for node in data][:100]
    nodes = [int(node.strip()) for node in nodes]

    return set(nodes)


def _closenessOverlap(elistPath):
    """
    Compute overlap between our values of closeness centrality and SNAP's internal implementation

    Parameters
    ----------
    elistPath: str or pathlib.Path
        Edge list of the graph to compute centralities on
    ----------

    Returns
    ----------
    calculatedNodes: set
        Top 100 nodes by closeness centrality according to our implementation

    SNAPNodes: set
        Top 100 nodes by closeness centrality according to the SNAP implementation (snap.GetClosenessCentr)

    len(overlap): int
        Count of overlapping nodes between the 2 sets
    ----------

    Reads from file our values of closeness centrality and then calls the SNAP function
    Once we have 2 sets of top 100 nodes, perform a set.intersection() call for common elements between both sets
    """

    adjGraph = AdjGraph(elistPath, separator=" ")
    graph = adjGraph.SNAPGraph
    calculatedNodes = readNodes("closeness.txt")

    SNAPCC = {}
    for node in graph.Nodes():
        SNAPCC[node.GetId()] = snap.GetClosenessCentr(graph, node.GetId())

    SNAPCC = {k: v for k, v in sorted(
        SNAPCC.items(), key=lambda x: x[1], reverse=True)}

    SNAPNodes = list(SNAPCC.keys())[:100]
    SNAPNodes = set([int(node) for node in SNAPNodes])

    overlap = SNAPNodes.intersection(calculatedNodes)
    return (calculatedNodes, SNAPNodes, len(overlap))


def _betweennessOverlap(elistPath, nodeFrac=0.8):
    """
    Compute overlap between our values of betweenness centrality and SNAP's internal implementation

    Parameters
    ----------
    elistPath: str or pathlib.Path
        Edge list of the graph to compute centralities on

    nodeFrac: float, default = 0.8
        Node Fraction to randomly sample nodes when using SNAP's internal betweenness centrality function
    ----------

    Returns
    ----------
    calculatedNodes: set
        Top 100 nodes by betweenness centrality according to our implementation

    SNAPNodes: set
        Top 100 nodes by betweenness centrality according to the SNAP implementation (snap.GetBetweennessCentr)

    len(overlap): int
        Count of overlapping nodes between the 2 sets
    ----------

    Reads from file our values of betweenness centrality and then calls the SNAP function
    Once we have 2 sets of top 100 nodes, perform a set.intersection() call for common elements between both sets
    """

    adjGraph = AdjGraph(elistPath, separator=" ")
    graph = adjGraph.SNAPGraph
    calculatedNodes = readNodes("betweenness.txt")

    Nodes = snap.TIntFltH()
    Edges = snap.TIntPrFltH()
    snap.GetBetweennessCentr(graph, Nodes, Edges, nodeFrac)
    SNAPBC = {}
    for node in Nodes:
        SNAPBC[node] = Nodes[node]

    SNAPBC = {k: v for k, v in sorted(
        SNAPBC.items(), key=lambda x: x[1], reverse=True)}

    SNAPNodes = list(SNAPBC.keys())[:100]
    SNAPNodes = set([int(node) for node in SNAPNodes])

    overlap = SNAPNodes.intersection(calculatedNodes)
    return (calculatedNodes, SNAPNodes, len(overlap))


def _pageRankOverlap(elistPath, alpha=0.85):
    """
    Compute overlap between our values of PageRank centrality and SNAP's internal implementation

    Parameters
    ----------
    elistPath: str or pathlib.Path
        Edge list of the graph to compute centralities on

    alpha: float, default = 0.85
        Damping factor for PageRank computations
    ----------

    Returns
    ----------
    calculatedNodes: set
        Top 100 nodes by PageRank centrality according to our implementation

    SNAPNodes: set
        Top 100 nodes by PageRank centrality according to the SNAP implementation (snap.GetPageRank)

    len(overlap): int
        Count of overlapping nodes between the 2 sets
    ----------

    Reads from file our values of PageRank centrality and then calls the SNAP function
    Once we have 2 sets of top 100 nodes, perform a set.intersection() call for common elements between both sets
    """

    adjGraph = AdjGraph(elistPath, separator=" ")
    graph = adjGraph.SNAPGraph
    calculatedNodes = readNodes("pagerank.txt")

    SNAPPR = {}
    PRankH = snap.TIntFltH()
    snap.GetPageRank(graph, PRankH, alpha)
    for item in PRankH:
        SNAPPR[item] = PRankH[item]

    SNAPPR = {k: v for k, v in sorted(
        SNAPPR.items(), key=lambda x: x[1], reverse=True)}

    SNAPNodes = list(SNAPPR.keys())[:100]
    SNAPNodes = set([int(node) for node in SNAPNodes])

    overlap = SNAPNodes.intersection(calculatedNodes)
    return (calculatedNodes, SNAPNodes, len(overlap))


if __name__ == "__main__":

    elistName = CONFIG["ELIST_NAME"]
    elistPath = os.path.join(CONFIG['DATASET_PATH'], elistName)

    _, _, closenessOverlap = _closenessOverlap(elistPath)
    print(f"#overlaps for Closeness Centrality: {closenessOverlap}")

    _, _, betweennessOverlap = _betweennessOverlap(
        elistPath, nodeFrac=CONFIG['BETWEENNESS_NODEFRAC'])
    print(f"#overlaps for Betweenness Centrality: {betweennessOverlap}")

    _, _, pagerankOverlap = _pageRankOverlap(
        elistPath, alpha=0.8)
    print(f"##overlaps for PageRank Centrality: {pagerankOverlap}")
