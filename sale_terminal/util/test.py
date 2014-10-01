from hash_heap import HashHeap, MAX_HEAP

class TestHashHeap:

  def test_push(self):
    hh = HashHeap(htype=MAX_HEAP)
    [hh.push(x, str(x)) for x in xrange(5)]
    assert hh.size() == 5
    hh.push(1,'1')
    assert hh.size() == 5

  def test_pop(self):
    hh = HashHeap(htype=MAX_HEAP)
    [hh.push(x, str(x)) for x in xrange(5)]
    [hh.push(x, str(x)) for x in xrange(5)]
    assert hh.pop() == (4,'4')

  def test_contains(self):
    hh = HashHeap(htype=MAX_HEAP)
    [hh.push(x, str(x)) for x in xrange(5)]
    assert 1 in hh

  def test_peek(self):
    hh = HashHeap(htype=MAX_HEAP)
    [hh.push(x, str(x)) for x in xrange(5)]
    assert hh.peek() == (4,'4')
    assert [x for x in hh.xpeek(count=2)] == [(4,'4'),(3,'3')]
