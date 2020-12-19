"""
AdjGraph built from SNAP's TUNGraph class
Creates an adjacency view list of the graph and provides
access via index to make it easier to use graph[s] to refer
to node s of the graph instead of calling the graph.GetNI(s) method
"""
from snap import PUNGraph, PNGraph, LoadEdgeList


class AdjGraph:

    def __init__(self, edgeListFilePath, directed=False, srcColumnId=0, destColumnId=1, separator='\t'):
        """
        Initialize an AdjGraph from an edgeList file
        Parameters
        ----------
        edgeListFilePath: str or pathlib.Path
            Path of the edgeList to construct the graph

        directed: bool, default = False
            Set to True if Graph is directed. Graph is then constructed using
            SNAP's TNGraph class else in case of undirected snap.TUNGraph is used

        srcColumnId: int, default = 0
            Column number of source node in the edge list file

        destColumnId: int, default = 1
            Column number of destination node in the edge list file

        separator: str, default = '\t'
            Separator to use between columns
        ----------

        Examples
        ----------
        import pathlib
        from src.graph import AdjGraph
        eListPath = pathlib.Path("subgraphs/facebook.elist")

        adjGraph = AdjGraph(elistPath, directed=False)
        graph = AdjGraph.SNAPGraph
        n = len(adjGraph) # Gives Number of Nodes
        for node in adjGraph:

        """
        if not directed:
            base = PUNGraph
        else:
            base = PNGraph

        self._graph = LoadEdgeList(base, edgeListFilePath,
                                   srcColumnId, destColumnId, separator)
        self.is_directed = directed
        self.adj = self.getAdj()
        self.SNAPGraph = self._graph
        self.maxNodeID = self._maxNodeID()

    def __len__(self):
        """
        ___len__ magic method lets us use the len() method on AdjGraph class
        len(g) where g is an object of AdjGraph will return the number of nodes in the graph
        """

        n = self._graph.GetNodes()
        return n

    def __getitem__(self, index):
        """
        Parameters
        ----------
        index: int
            ID of the Node to fetch
        ----------

        __getitem__ allows for calling nodes by indexing
        To fetch node with ID 200, call Graph[200] instead of having to
        call Graph.SNAPGraph.GetNI(200) to get the SNAP Node object for the given node
        """

        try:
            return self._graph.GetNI(index)
        except:
            raise KeyError(f"Node {index} not present")

    def fetchGraph(self):
        return self._graph

    def getAdj(self):
        """
        Generate the adjacency view of a graph
        The function returns a dictionary where keys are Node IDs and
        value is also a dictionary with {nodeID: {}}. An empty dictionary is used
        since the graph is unweighted

        adj[200] will give all nodes that are neighbours of Node 200
        """

        adj = {}
        subGraph = self._graph
        for node in subGraph.Nodes():
            if not node.GetId() in adj:
                adj[node.GetId()] = {}
            for v in node.GetOutEdges():
                adj[node.GetId()][v] = {}
        return adj

    def _maxNodeID(self):
        maxNodeID = 0
        for node in self._graph.Nodes():
            if node.GetId() > maxNodeID:
                maxNodeID = node.GetId()

        return maxNodeID
