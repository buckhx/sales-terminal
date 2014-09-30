from nose.tools import assert_raises
from . import SaleTerminal

class TestSaleTerminal:

  @classmethod
  def setup(self):
    self.terminal = SaleTerminal()

  def test_scan(self):
    self.terminal.register_product("A", 6, 5.00)
    assert_raises(ValueError, self.terminal.scan, "DERP")
    assert self.terminal.scan("A") == 1
    assert self.terminal.scan("A") == 2

  def test_bulk_scan(self):
    self.terminal.register_product("A", 6, 5.00)
    self.terminal.register_product("B", 6, 5.00)
    self.terminal.register_product("C", 6, 5.00)
    self.terminal.register_product("D", 6, 5.00)
    assert_raises(ValueError, self.terminal.scan_bulk, "DERP")
    assert self.terminal.scan("A")
    assert self.terminal.scan_bulk("ABBCD") == {'A': 2, 'B': 2, 'C': 1, 'D':1}

  def test_total(self):
    self.terminal.register_product("A", 1, 1.25)
    self.terminal.register_product("A", 6, 6)
    self.terminal.scan("A")
    assert 1.25 == self.terminal.total()
    [self.terminal.scan("A") for x in xrange(5)]
    assert 6.00 == self.terminal.total()
    self.terminal.scan("A")
    assert 7.25 == self.terminal.total()

  def test_register_product(self):
    self.terminal.register_product("Z", 6, 5.00)
    self.terminal.register_product("Z", 6, 6.00)
    assert len([x for x in self.terminal.gen_registry_quantity_prices("Z")]) == 1
    self.terminal.register_product("Z", 6, 1)
    self.terminal.scan("Z")
    assert_raises(ValueError, self.terminal.register_product, "Z", -1, 5)
    assert_raises(ValueError, self.terminal.register_product, "Z", 0, 5)
    assert_raises(ValueError, self.terminal.register_product, "Z", 1, -5)
