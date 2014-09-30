sale-terminal
==============

A sales terminal to scan products and get get the total based on a product registry

Here's an example of usage
    terminal = sale_terminal.from_csv("product registry")
    terminal.scan("A")
    terminal.scan("B")
    print terminal.total()
    terminal.scan("CCCDDDAAAADDDD")
    print terminal.total()
