from rdflib import Graph as RdfGraph
from rdflib import Literal
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
        ### Generate IDs
        count = 0
        graphIterator = self._getGraphIterator(graphPath)
        for rdfGraph in graphIterator():
            self._generateIndices(rdfGraph)
            count += 1
            if count % 10000 == 0:
                print("Generated IDs for {} facts".format(count))

        print("Generated all IDs")
        self._saveIDs()
        print("Saved IDs")

        ### Generate adjacency matrix
        facts = []
        count = 0
        graphIterator = self._getGraphIterator(graphPath)
        for rdfGraph in graphIterator():
            for sub, pred, obj in rdfGraph:
                if type(obj) == Literal:
                    obj = '"{}"@{}'.format(obj, obj.language)
                facts.append([self.nodeId[sub], self.nodeId[obj], self.relId[pred]])
                count += 1
                if count % 10000 == 0:
                    print("Generated array for {} facts".format(count))

        adj = np.asarray(facts)
        print("Created adjacency matrix")
        return adj
    
    def getShape(self):
        nodes = len(self.nodeId.keys())
        relationships = len(self.relId.keys())
        return (nodes, nodes, relationships)

    def _generateIndices(self, rdfGraph):
        for sub, pred, obj in rdfGraph:
            # Set subject id
            try:
                self.nodeId[sub]
            except KeyError:
                self.nodeId[sub] = self._nextNodeId()

            # Set object id
            try:
                if type(obj) == Literal:
                    obj = '"{}"@{}'.format(obj, obj.language)
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

    def _getGraphIterator(self, graphPath):
        graphFile = open(graphPath, 'r')
        def graphIterator():
            while line := graphFile.readline():
                rdfGraph = RdfGraph()
                rdfGraph.parse(data=line, format='ttl')
                yield rdfGraph
            graphFile.close()

        return graphIterator
    
    def _saveIDs(self):
        with open("data/kg/nodes.txt", 'w') as nodesFile:
            for resource in self.nodeId.keys():
                nodesFile.write("{} {}\n".format(self.nodeId[resource], resource))
        
        with open("data/kg/relations.txt", 'w') as relationsFile:
            for relation in self.relId.keys():
                relationsFile.write("{} {}\n".format(self.relId[relation], relation))