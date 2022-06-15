from GraphTransformer import GraphTransformer
from Graph import Graph
import os

def createDirecotryStructure():
    try:
        os.mkdir("data")
        os.mkdir("data/kg")
        os.mkdir("data/kg/_undir")
    except FileExistsError:
        pass

createDirecotryStructure()

graphTransformer = GraphTransformer()
adjacencyMatrix = graphTransformer.generateAdjacency("/home/sascha/head.ttl")
graph = Graph(adjacencyMatrix, graphTransformer.getShape())
graph.save_graph("./data/kg/_undir")