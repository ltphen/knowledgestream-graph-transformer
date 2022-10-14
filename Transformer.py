from transformer.GraphTransformer import GraphTransformer
from transformer.Graph import Graph
from transformer.ContractedLineGraph import ContractedLineGraph
from os.path import join
import os, argparse

def main():
    args = parseArguments()
    createDirecotryStructure(args.output)
    
    # Create adjacency matrix
    graphTransformer = GraphTransformer(args.output)
    adjacency = graphTransformer.generateAdjacency(args.graph)
    
    # Create and save graph
    graph = Graph(adjacency, graphTransformer.getShape())
    graph.save_graph(join(args.output, "data/kg/_undir"))
    
    # Create contracted line graph
    contractedLineGraph = ContractedLineGraph(adjacency, graphTransformer.relIdCount)
    
def parseArguments():
    argumentParser = argparse.ArgumentParser()
    argumentParser.add_argument("-g", "--graph", required=True, help="Knowledgegraph in turtle format")
    argumentParser.add_argument("-o", "--output", required=False, default=".")
    return argumentParser.parse_args()
    
def createDirecotryStructure(outputPath):
    try:
        os.mkdir(join(outputPath, "data"))
        os.mkdir(join(outputPath, "data/kg"))
        os.mkdir(join(outputPath, "data/kg/_undir"))
        os.mkdir(join(outputPath, "data/relsim"))
    except FileExistsError:
        pass

if __name__ == '__main__':
    main()