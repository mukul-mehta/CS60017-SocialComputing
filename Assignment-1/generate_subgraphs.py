import os
import snap
from pathlib import Path

from config import CONFIG


Rnd = snap.TRnd(CONFIG['RANDOM_SEED'])
Rnd.Randomize()

datasets = {
    'amazon': os.path.join(CONFIG['DATASET_PATH'], "com-amazon.ungraph.txt"),
    'facebook': os.path.join(CONFIG['DATASET_PATH'], "facebook_combined.txt")
}

subgraphs = {
    'amazon': os.path.join(CONFIG['SUBGRAPH_PATH'], "amazon.elist"),
    'facebook': os.path.join(CONFIG['SUBGRAPH_PATH'], "facebook.elist")
}

graphs = {
    'amazon': snap.LoadEdgeList(snap.PUNGraph, datasets['amazon'], 0, 1, '\t'),
    'facebook': snap.LoadEdgeList(snap.PUNGraph, datasets['facebook'], 0, 1, ' ')
}

# Create Amazon Subgraph according to the rule given
amazonSubgraph = snap.PUNGraph.New()
for node in graphs['amazon'].Nodes():
    nodeID = node.GetId()

    if nodeID % 4 == 0:
        if not amazonSubgraph.IsNode(nodeID):
            amazonSubgraph.AddNode(nodeID)

for edge in graphs['amazon'].Edges():
    sourceNode, destNode = edge.GetId()

    if sourceNode % 4 != 0 or destNode % 4 != 0:
        continue
    
    if not amazonSubgraph.IsNode(sourceNode):
        amazonSubgraph.AddNode(sourceNode)

    if not amazonSubgraph.IsNode(destNode):
        amazonSubgraph.AddNode(destNode)

    amazonSubgraph.AddEdge(sourceNode, destNode)  

# Create Facebook Subgraph according to the rule given
FBSubgraph = snap.PUNGraph.New()
for node in graphs['facebook'].Nodes():
    nodeID = node.GetId()

    if nodeID % 5 != 0:
        if not FBSubgraph.IsNode(nodeID):
            FBSubgraph.AddNode(nodeID)

for edge in graphs['facebook'].Edges():
    sourceNode, destNode = edge.GetId()

    if sourceNode % 5 == 0 or destNode % 5 == 0:
        continue

    if not FBSubgraph.IsNode(sourceNode):
        FBSubgraph.AddNode(sourceNode)

    if not FBSubgraph.IsNode(destNode):
        FBSubgraph.AddNode(destNode)
    
    FBSubgraph.AddEdge(sourceNode, destNode)


snap.SaveEdgeList(amazonSubgraph, subgraphs['amazon'])
snap.SaveEdgeList(FBSubgraph, subgraphs['facebook'])
