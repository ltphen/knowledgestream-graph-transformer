import math, time
import numpy as np
from numpy.linalg import norm
from transformer.OccurrenceCounter import OccurrenceCounter
from os.path import join

class ContractedLineGraph:
    def __init__(self, adjacency, numberOfPredicates:int):
        # List of assertions in the form (subjectID, objectID, predicateID)
        # as generated by GraphTransformer
        self.adjacency = adjacency
        self.numberOfPredicates = numberOfPredicates
        
    def generate(self, experimentPath:str):
        """
        Perform all steps to calculate the required
        cosine similarity between predicates.
        """
        start = time.time()
        clg = self.generateClg()
        end = time.time()
        print("Generated contracted line graph in {} seconds".format(end - start))
        self.saveClg(join(experimentPath, "contracted-line-graph.npy"), clg)
        print("Saved contracted line graph")
        start = time.time()
        tfIdf = self.generateTfIdf(clg)
        end = time.time()
        print("Calculated TF-IDF in {} seconds".format(end - start))
        start = time.time()
        self.generateCosineSimilarity(tfIdf)
        end = time.time()
        print("Calculated cosine similarity in {} seconds".format(end - start))
        self.saveCoSim(join(experimentPath, "predicate-similarity.npy"))
        print("Saved cosine similarity")
        
    def generateClg(self):
        """
        Generate a contracted line graph (clg) out of the graph provided
        as list of assertions in self.adjacency.
        """

        clg = np.eye(self.numberOfPredicates, self.numberOfPredicates)
        
        # resourceDict[resourceID] = [all facts that contain that resource]
        resourceDict = dict()
        for fact in self.adjacency:
            self._addToResourceDict(resourceDict, fact)
            
        count = 0
        # All facts in one list have one resource in common.
        # Walk through list, count co-occurrences of predicates.
        
        jobs = []
        for resource in resourceDict.keys():
            jobRunner = OccurrenceCounter(resourceDict[resource], clg)
            jobs.append(jobRunner)
            jobRunner.start()
            
        for job in jobs:
            job.join()
            
        return clg
                    
    def generateTfIdf(self, clg):
        tfIdf = np.eye(self.numberOfPredicates, self.numberOfPredicates)
        for i in range(self.numberOfPredicates):
            for j in range(i+1, self.numberOfPredicates):
                score = self._calculateTfIdf(i, j, clg)
                tfIdf[i, j] = score
                tfIdf[j, i] = score
        return tfIdf
                
    def generateCosineSimilarity(self, tfIdf):
        self.coSim = np.eye(self.numberOfPredicates, self.numberOfPredicates)
        for i in range(self.numberOfPredicates):
            for j in range(i+1, self.numberOfPredicates):
                sim = self._calculateCosineSimilarity(tfIdf[i], tfIdf[j])
                self.coSim[i, j] = sim
                self.coSim[j, i] = sim 
    
    def saveCoSim(self, path:str):
        np.save(path, self.coSim)
        
    def saveClg(self, path:str, clg):
        np.save(path, clg)
        
    def _addToResourceDict(self, rDict:dict, fact):
        if not fact[0] in rDict.keys():
            rDict[fact[0]] = []
        if not fact[1] in rDict.keys():
            rDict[fact[1]] = []
            
        rDict[fact[0]].append(fact)
        rDict[fact[1]].append(fact)
    
    def _calculateCosineSimilarity(self, iVec, jVec):
        return np.dot(iVec, jVec,) / (norm(iVec) * norm(jVec))
    
    def _calculateTfIdf(self, ri:int, rj:int, clg):
        """
        C'(ri, rj, R) = log(1 + Cij) * log(R / |{ri | Cij > 0}|)
        R is the number of predicates
        """
        factor1 = math.log(1 + clg[ri, rj])
        factor2 = math.log(self.numberOfPredicates / self._countCoOccurences(ri, clg))
        return factor1 * factor2
        
    def _countCoOccurences(self, ri:int, clg):
        counter = 0
        for j in range(self.numberOfPredicates):
            if clg[ri, j] > 0:
                counter += 1
        return counter 
