from transformer.GraphTransformer import GraphTransformer
from transformer.Graph import Graph
import os, argparse

def main():
    args = parseArguments()
    createDirecotryStructure()
    
    # Create adjacency matrix
    graphTransformer = GraphTransformer()
    adjacency = graphTransformer.generateAdjacency(args.graph)
    
    # Create and save graph
    graph = Graph(adjacency, graphTransformer.getShape())
    graph.save_graph("./data/kg/_undir")
    
def parseArguments():
    argumentParser = argparse.ArgumentParser()
    argumentParser.add_argument("-g", "--graph", required=True, help="Knowledgegraph in turtle format")
    return argumentParser.parse_args()
    
def createDirecotryStructure():
    try:
        os.mkdir("data")
        os.mkdir("data/kg")
        os.mkdir("data/kg/_undir")
    except FileExistsError:
        pass

if __name__ == '__main__':
    main()