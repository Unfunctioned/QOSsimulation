import heapq
from Utilities.ItemTypes.CapacityItem import CapacityItem
from Simulation.NetworkEnvironment.NetworkSlice import NetworkSlice
'''Class to store capacity allocations of a network'''
class AllocationQueue(object):
    
    def __init__(self) -> None:
        self.heap : list[CapacityItem]
        self.heap = []
        
    def __iter__(self):
        self.current = 0
        return self
    
    def __next__(self) -> CapacityItem:
        item = self.heap[self.current]
        self.current += 1
        if self.current == self.size():
            raise StopIteration
        return item 
        
    def Peek(self) -> CapacityItem:
        if len(self.heap) == 0:
            return None
        return self.heap[0]
    
    def Put(self, item : CapacityItem):
        heapq.heappush(self.heap, item)
            
    
    def Get(self) -> CapacityItem:
        _, item = heapq.heappop(self.heap)
        return item
    
    def size(self):
        return len(self.heap)