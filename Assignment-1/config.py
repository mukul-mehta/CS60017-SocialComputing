import os
from pathlib import Path

RANDOM_SEED = 42

DATASET_PATH = Path("./SNAP-DATA")
SUBGRAPH_PATH = Path("./subgraphs")
PLOT_PATH = Path("./plots")

if not os.path.exists(DATASET_PATH):
    os.mkdir(DATASET_PATH)

if not os.path.exists(SUBGRAPH_PATH):
    os.mkdir(SUBGRAPH_PATH)

if not os.path.exists(PLOT_PATH):
    os.mkdir(PLOT_PATH)


CONFIG = {
    'RANDOM_SEED': RANDOM_SEED,
    'DATASET_PATH': DATASET_PATH,
    'SUBGRAPH_PATH': SUBGRAPH_PATH,
    'PLOT_PATH': PLOT_PATH
}
