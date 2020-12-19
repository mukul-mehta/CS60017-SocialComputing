import os

from config import CONFIG
from src.graph import AdjGraph
from src.closeness import closenessCentrality
from src.betweenness import betweennessCentrality
from src.pagerank import biasedPageRank


def writeCentrality(filename, data):
    """
    Write centrality values to disk in a sorted order

    Parameters
    ----------
    filename: str or pathlib.Path
        Name of the file to write to

    data: dict
        Dictionary with node ID keys and centrality measure values
    ----------

    When writing to disk, sort `data` by the value in descending order
    For each node, write a new line with <NODE ID>\t<CENTRALITY_VALUE>
    """

    filePath = os.path.join(CONFIG['CENTRALITIES_PATH'], filename)
    f = open(filePath, "w")

    data = {k: v for k, v in sorted(
        data.items(), key=lambda x: x[1], reverse=True)}

    for k, v in data.items():
        text = f"{k:<4}\t{v:.6f}\n"
        f.write(text)


def getCloseness(elistPath):
    """
    Driver function to compute closeness centrality with our implementation

    Parameters
    ----------
    elistPath: str or pathlib.Path
        Edge list of the graph to compute centralities on
    ----------

    Returns
    ----------
    time: float
        Time taken to calculate those centrality values
    ----------

    Compute closeness centrality values and call function `writeCentrality` to write them to disk
    """
    adjGraph = AdjGraph(elistPath, separator=" ")
    closeness_centrality, time = closenessCentrality(adjGraph)
    writeCentrality("closeness.txt", closeness_centrality)
    return time


def getBetweenness(elistPath):
    """
    Driver function to compute betweenness centrality with our implementation

    Parameters
    ----------
    elistPath: str or pathlib.Path
        Edge list of the graph to compute centralities on
    ----------

    Returns
    ----------
    time: float
        Time taken to calculate those centrality values
    ----------

    Compute betweenness centrality values and call function `writeCentrality` to write them to disk
    """

    adjGraph = AdjGraph(elistPath, separator=" ")
    betweenness_centrality, time = betweennessCentrality(adjGraph)
    writeCentrality("betweenness.txt", betweenness_centrality)
    return time


def getPageRank(elistPath, alpha, maxiter, tolerance):
    """
    Driver function to compute PageRank centrality with our implementation

    Parameters
    ----------
    elistPath: str or pathlib.Path
        Edge list of the graph to compute centralities on

    alpha: float
        Damping factor for PR

    maxiter: int
        Max number of iterations to run PR

    tolerance: float
        Allowed limit for difference of node PR's across iterations
    ----------

    Returns
    ----------
    time: float
        Time taken to calculate those centrality values
    ----------

    Compute PageRank values and call function `writeCentrality` to write them to disk
    """

    adjGraph = AdjGraph(elistPath, separator=" ")
    graph = adjGraph.SNAPGraph

    preference_vector = []
    for node in graph.Nodes():
        id = node.GetId()
        if (id % 4) == 0:
            preference_vector.append(id)

    pageRank, convIter, time = biasedPageRank(
        adjGraph, preference_vector=preference_vector, alpha=alpha,
        max_iterations=maxiter, tolerance=tolerance)

    writeCentrality("pagerank.txt", pageRank)
    return pageRank, convIter, time


if __name__ == "__main__":

    elistName = CONFIG["ELIST_NAME"]
    elistPath = os.path.join(CONFIG['DATASET_PATH'], elistName)

    if not os.path.exists(elistPath):
        raise Exception(f"The elist {elistPath} does not exist!")

    timeCC = getCloseness(elistPath)
    # print(
    #     f"Closeness centrality calculation -> {timeCC} seconds | {timeCC / 60} minutes")

    timeBC = getBetweenness(elistPath)
    # print(
    #     f"Betweenness centrality calculation -> {timeBC} seconds | {timeBC / 60} minutes")

    pageRank, convIter, timePR = getPageRank(elistPath, alpha=CONFIG['PAGERANK_ALPHA'],
                                             maxiter=CONFIG['PAGERANK_MAXITER'],
                                             tolerance=CONFIG['PAGERANK_TOLERANCE'])
    # print(
    #     f"PageRank centrality calculation -> {timePR} seconds  |  {timePR / 60} minutes")
