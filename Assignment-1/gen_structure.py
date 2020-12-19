import os
import snap
import sys

from shutil import move
from statistics import mean, pvariance
from config import CONFIG


def meanVariance(values):
    """
        Calculate mean and variance of a list

        Args:
        values (list) -> List of real values

        Return:
        mean (float) -> Mean of the given values
        variance (float) -> Variance of given values
    """

    _mean = mean(values)
    _variance = pvariance(values)

    return (_mean, _variance)

def graphStructure(elistName, elistPath):
    """
        Calculate properties of the graph as given in the assignment

        Args:
        elistName (str) -> Input elist name
        elistPath (pathlib.Path) -> Input elist using which graph needs to be built

        Return:
        RESULTS (dict) -> Dictionary containing results for different subparts of the assignment
    """

    RESULTS = {}
    subGraph = snap.LoadEdgeList(snap.PUNGraph, elistPath, 0, 1)

    # Part 1 (Size of the network)
    RESULTS['nodeCount'] = subGraph.GetNodes()
    RESULTS['edgeCount'] = subGraph.GetEdges()

    # Part 2 (Degree of nodes in the network)
    maxDegree = 0
    maxDegreeNodes = []
    degree7Count = 0

    for node in subGraph.Nodes():
        if node.GetDeg() == 7:
            degree7Count += 1

        maxDegree = max(maxDegree, node.GetDeg())

    for node in subGraph.Nodes():
        if node.GetDeg() == maxDegree:
            maxDegreeNodes.append(node.GetId())

    plotFilename = f"deg_dist_{elistName}"
    # Since it is an undirected graph, in/out degree is unimportant
    snap.PlotOutDegDistr(subGraph, plotFilename)

    RESULTS['maxDegree'] = maxDegree
    RESULTS['maxDegreeNodes'] = ','.join(map(str, maxDegreeNodes))
    RESULTS['degree7Count'] = degree7Count

    # Part 3 (Paths in the network)
    # Full Diameter Calculation
    fullDiameters = {
        10: snap.GetBfsFullDiam(subGraph, 10, False),
        100: snap.GetBfsFullDiam(subGraph, 100, False),
        1000: snap.GetBfsFullDiam(subGraph, 1000, False)
    }
    fullMean, fullVariance = meanVariance(fullDiameters.values())
    fullDiameters['mean'] = fullMean
    fullDiameters['variance'] = fullVariance
    RESULTS['fullDiameters'] = fullDiameters

    # Effective Diameter Calculation
    effDiameters = {
        10: snap.GetBfsEffDiam(subGraph, 10, False),
        100: snap.GetBfsEffDiam(subGraph, 100, False),
        1000: snap.GetBfsEffDiam(subGraph, 1000, False),
    }
    effMean, effVariance = meanVariance(effDiameters.values())
    effDiameters['mean'] = effMean
    effDiameters['variance'] = effVariance
    RESULTS['effDiameters'] = effDiameters

    plotFilename = f"shortest_path_{elistName}"
    snap.PlotShortPathDistr(subGraph, plotFilename)

    # Part 4 (Components of the network)
    edgeBridges = snap.TIntPrV()
    articulationPoints = snap.TIntV()
    RESULTS['fractionLargestConnected'] = snap.GetMxSccSz(subGraph)
    snap.GetEdgeBridges(subGraph, edgeBridges)
    snap.GetArtPoints(subGraph, articulationPoints)
    RESULTS['edgeBridges'] = len(edgeBridges)
    RESULTS['articulationPoints'] = len(articulationPoints)

    plotFilename = f"connected_comp_{elistName}"
    snap.PlotSccDistr(subGraph, plotFilename)

    # Part 5 (Connectivity and clustering in the network)
    RESULTS['avgClusterCoefficient'] = snap.GetClustCf(subGraph, -1)
    RESULTS['triadCount'] = snap.GetTriadsAll(subGraph, -1)[0]
    
    nodeX = subGraph.GetRndNId(Rnd)
    nodeY = subGraph.GetRndNId(Rnd)
    RESULTS['randomClusterCoefficient'] = (nodeX, snap.GetNodeClustCf(subGraph, nodeX))
    RESULTS['randomNodeTriads'] = (nodeY, snap.GetNodeTriads(subGraph, nodeY))
    RESULTS['edgesTriads'] = snap.GetTriadEdges(subGraph)

    plotFilename = f"clustering_coeff_{elistName}"
    snap.PlotClustCf(subGraph, plotFilename)

    return RESULTS

def movePlots(plotPath):
    """
        Move all .png plots to their correct location as specified by the argument to the function

        Args:
        plotPath (pathlib.Path) -> Path to move the plots to

        Return:
        None
    """
    for file in os.listdir(os.getcwd()):
        if file.endswith('.png') or file.endswith('.tab') or file.endswith('.plt'):
            move(os.path.join(os.getcwd(), file), os.path.join(plotPath, file))

if __name__ == "__main__":
    # Accept the name of the subgraph (.elist) as a CLI argument and check if it exists
    if len(sys.argv) < 2:
        raise Exception("Please specify name of the elist as a command line argument")

    elistName = sys.argv[1]
    elistPath = os.path.join(CONFIG['SUBGRAPH_PATH'], elistName)

    if not os.path.exists(elistPath):
        raise Exception(f"The elist {elistPath} does not exist!")

    # Set seed value for SNAP's random function to the value set in configuration
    Rnd = snap.TRnd(CONFIG['RANDOM_SEED'])
    Rnd.Randomize()

    RESULTS = graphStructure(elistName=elistName, elistPath=elistPath)

    PLOT_PATH = CONFIG['PLOT_PATH']
    movePlots(PLOT_PATH)

    # Print all required values
    print(f"Number of nodes: {RESULTS['nodeCount']}")
    print(f"Number  of edges: {RESULTS['edgeCount']}")
    print(f"Number of nodes with degree=7: {RESULTS['degree7Count']}")
    print(f"Node id(s) with highest degree: {RESULTS['maxDegreeNodes']}")
    print(f"Approximate full diameter by sampling 10 nodes: {RESULTS['fullDiameters'][10]}")
    print(f"Approximate full diameter by sampling 100 nodes: {RESULTS['fullDiameters'][100]}")
    print(f"Approximate full diameter by sampling 1000 nodes: {RESULTS['fullDiameters'][1000]}")
    print(f"Approximate full diameter (mean and variance): {RESULTS['fullDiameters']['mean'] :.4f},{RESULTS['fullDiameters']['variance'] :.4f}")
    print(f"Approximate effective diameter by sampling 10 nodes: {RESULTS['effDiameters'][10] :.4f}")
    print(f"Approximate effective diameter by sampling 100 nodes: {RESULTS['effDiameters'][100] :.4f}")
    print(f"Approximate effective diameter by sampling 1000 nodes: {RESULTS['effDiameters'][1000] :.4f}")
    print(f"Approximate effective diameter (mean and variance): {RESULTS['effDiameters']['mean'] :.4f},{RESULTS['effDiameters']['variance'] :.4f}")
    print(f"Fraction of nodes in largest connected component: {RESULTS['fractionLargestConnected'] :.4f}")
    print(f"Number of edge bridges: {RESULTS['edgeBridges']}")
    print(f"Number of articulation points: {RESULTS['articulationPoints']}")
    print(f"Average clustering coefficient: {RESULTS['avgClusterCoefficient'] :.4f}")
    print(f"Number of triads: {RESULTS['triadCount']}")
    print(f"Clustering coefficient of random node {RESULTS['randomClusterCoefficient'][0]}: {RESULTS['randomClusterCoefficient'][1] :.4f}")
    print(f"Number of triads random node {RESULTS['randomNodeTriads'][0]} participates: {RESULTS['randomNodeTriads'][1]}")
    print(f"Number of edges that participate in at least one triad: {RESULTS['edgesTriads']}")
