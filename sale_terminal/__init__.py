import csv
import heapq
from collections import defaultdict, Counter

class SaleTerminal:
  """ A Sale Terminal
    Calculates the total of items scanned based on a registry
  
  """
  
  def __init__(self):
    """ Public API methods should use other methods of construction, such as from_csv

    """
    self.registry = defaultdict(list)
    self.cart = Counter()

  def scan(self, product):
    """ Scan a single item identified by a string
      If the scanned item is not present in the registry, a ValueError is raised

    """
    if not product in self.registry:
      raise ValueError("Product not in registry: "+product)
    self.cart[product] += 1
    return self.cart[product]

  def total(self):
    """ Calculates the total of the scanned items
      Calculation is done when this method is called

    """
    #registry = copy(self.registry)
    total = 0.0
    for product, count in self.cart.most_common():
      for quantity, price in reversed(self.registry[product]):
        #TODO Bug here
        total += (count / quantity) * price
        count = (count - (count % quantity)) if (count / quantity > 0) else count
      if count != 0:
        raise ValueError("Product does not include a 1 quantity in registry: "+product)
    return total

  def register_product(self, product, quantity, price):
    """ Register a product in the form of product string, quantity and price
        The product string is matched during the scan method
        This method can accept multiple entries for the same product to simulate bulk pricing by varying quantities

    """
    heapq.heappush(self.registry[product], (quantity, price))

  #TODO make a model out of the file instead of this
  #TODO check that it include a 1 quantity value
  def from_csv(csv_path):
    """ Registers products in a batch by a CSV
      CSV is used to identify product, quantity and price per row

    """
    terminal = SaleTerminal()
    with open(csv_path) as csv_file:
      reader = csv.DictReader(csv_file)
      for row in reader:
        terminal.register_product(row[PRODUCT], row[QUANTITY], row[PRICE])
    return terminal
