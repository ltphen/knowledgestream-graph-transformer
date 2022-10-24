import threading

class OccurrenceCounterLock(threading.Thread):
    count = 0
    locks = dict()
    
    def __init__(self, factList, clg):
        threading.Thread.__init__(self)
        self.factList = factList
        self.clg = clg
        
    def run(self):
        for i in range(len(self.factList)-1):
            for j in range(i+1, len(self.factList)):
                fact1 = self.factList[i]
                fact2 = self.factList[j]

                self.acquireLock(fact1, fact2)
                # Hinders two thread form working
                # on the same predicates at the same time.
                self.clg[fact1[2], fact2[2]] += 1
                self.clg[fact2[2], fact1[2]] += 1
                self.releaseLock(fact1, fact2)

            OccurrenceCounterLock.count += 1
            if OccurrenceCounterLock.count % 10000 == 0:
                print("Generated CLG for {} facts".format(OccurrenceCounterLock.count))

    def acquireLock(self, fact1, fact2):
        key = self._createKey(fact1, fact2)
        if not key in OccurrenceCounterLock.locks.keys():
            OccurrenceCounterLock.locks[key] = threading.Lock()
            
        OccurrenceCounterLock.locks[key].acquire()
    
    def releaseLock(self, fact1, fact2):
        key = self._createKey(fact1, fact2)
        OccurrenceCounterLock.locks[key].release()

    def _createKey(self, fact1, fact2):
        pred1 = fact1[2]
        pred2 = fact2[2]
        if pred2 < pred1:
            pred1, pred2 = pred2, pred1
        return (pred1, pred2)