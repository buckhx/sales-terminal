import heapq

MAX_HEAP = -1
MIN_HEAP = 1

class HashHeap:
  """ A class that represents a hash backed heap
      Functions like a priority queue where priorities are unique
  """

  def __init__(self, htype=MAX_HEAP):
    """ Defaults to a max-heap
        Can be passed MAX_HEAP like HashHeap(htype=hash_heap.MAX_HEAP) 
    """
    self.htype = htype
    self.keys = set()
    self.heap = []

  def push(self, key, item):
    """ Pushes a key, item and maintains heap invariant based on key
        If object already contains the key, the value will be updated
    """
    key = self.htype*key
    if key in self.keys: #perform an update
      [(self.heap.insert(i, (key,item)), self.heap.pop(i+1)) for i, ki in enumerate(self.heap) if ki[0] == key]
    else:
      heapq.heappush(self.heap, (key, item))
      self.keys.add(key)

  def pop(self):
    """ Returns and removes the first element according to invariant
    """
    key, item = heapq.heappop(self.heap)
    self.keys.remove(key)
    return self.htype*key, item

  def xpeek(self, count):
    """ Generator to return the first count elements
    """
    return ( (self.htype*k, v) for k,v in heapq.nsmallest(count, self.heap) )

  def peek(self):
    """ Returns the first element or None if empty
    """
    if self.size() == 0:
      return None
    return [kv for kv in self.xpeek(1)][0]

  def size(self):
    """ Returns the number of keys
    """
    return len(self.keys)

  def __contains__(self, key):
    return self.htype*key in self.keys

  def __len__(self):
    return self.size()
