from rdflib import Graph as RdfGraph
import numpy as np

class GraphTransformer:
    """
    Transform a graph in turtle representation into adjacency matrix
    requred to build Graph.
    """

    def __init__(self):
        self.nodeId = dict()
        self.relId = dict()
        self.nodeIdCount = 0
        self.relIdCount = 0

    def generateAdjacency(self, graphPath):
        count = 0
        for rdfGraph in self._readTurtleGraph(graphPath):
            self._generateIndices(rdfGraph)
            count += 1
            if count % 10000 == 0:
                print("Generated IDs for {} facts".format(count))

        print("Generated all IDs")
        facts = []
        for sub, pred, obj in self._readTurtleGraph(graphPath):
            facts.append([self.nodeId[sub], self.nodeId[obj], self.relId[pred]])

        adj = np.asarray(facts)
        return adj


    def _generateIndices(self, rdfGraph):
        for sub, pred, obj in rdfGraph:
            # Set subject id
            try:
                self.nodeId[sub]
            except KeyError:
                self.nodeId[sub] = self._nextNodeId()

            # Set object id
            try:
                self.nodeId[obj]
            except KeyError:
                self.nodeId[obj] = self._nextNodeId()

            # Set predicate id
            try:
                self.relId[pred]
            except KeyError:
                self.relId[pred] = self._nextRelationshipId()

    def _nextNodeId(self):
        nextId = self.nodeIdCount
        self.nodeIdCount += 1
        return nextId

    def _nextRelationshipId(self):
        nextId = self.relIdCount
        self.relIdCount += 1
        return nextId

    def _readTurtleGraph(self, graphPath):
        with open(graphPath, 'r') as graphFile:
            while True:
                line = graphFile.readline()
                rdfGraph = RdfGraph()
                rdfGraph.parse(data=line, format='ttl')
                yield rdfGraph


g = GraphTransformer()
g.generateAdjacency("/home/sascha/dbpedia.ttl")