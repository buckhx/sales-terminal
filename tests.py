from sale_terminal import SaleTerminal

terminal = SaleTerminal()
terminal.register_product("A",1,1.25)
terminal.register_product("A",6,6.00)
terminal.scan("A")
assert 1.25 == terminal.total()
[terminal.scan("A") for x in xrange(5)]
print terminal.total()
