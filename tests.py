#from sale_terminal.test import TestSaleTerminal
import sale_terminal

def test_bulk_ABCDABAA():
  terminal = sale_terminal.from_csv('data/test_registry.csv')
  terminal.scan_bulk('ABCDABAA')
  assert terminal.total() == 32.40

def test_bulk_CCCCCC():
  terminal = sale_terminal.from_csv('data/test_registry.csv')
  terminal.scan_bulk('CCCCCCC')
  assert terminal.total() == 7.25

def test_bulk_ABCD():
  terminal = sale_terminal.from_csv('data/test_registry.csv')
  terminal.scan_bulk('ABCD')
  assert terminal.total() == 15.40
