import csv
from util.hash_heap import HashHeap, MAX_HEAP
from collections import defaultdict, Counter

class SaleTerminal:
  """ A Sale Terminal
      Calculates the total of items scanned based on a registry
  """

  #TODO pull registry out to a UniqueHeap
  def __init__(self):
    """ Public API methods should use other methods of construction, such as from_csv
        registry_keys is used to facilitate a unique heap
        registry is a list of min-heaps (heapq is only a min-heap)
        We convert quantities to negative values as the priority value in the heap simulating a max-heap
    """
    self.registry = defaultdict(HashHeap)
    self.cart = Counter()

  def scan(self, product):
    """ Scan a single item identified by a string
        If the scanned item is not present in the registry, a ValueError is raised
        Returns count of scanned object after scanning
    """
    if not product in self.registry:
      raise ValueError("Product not in registry: "+product)
    self.cart[product] += 1
    return self.cart[product]

  def scan_bulk(self, bulk):
    """ Scan in order
        If any of the products in bulk are not in the registry, none are scanned and an error thrown
        Returns a dict of the product count for all objects that were scanned
    """
    scanned = set([])
    # throw error if no in registry
    [self.scan(product) for product in bulk if product not in self.registry]
    # actually scan
    [(self.scan(product), scanned.add(product)) for product in bulk]
    return dict([(product, self.cart[product]) for product in scanned])

  def total(self):
    """ Calculates the total of the scanned items
        Calculation is done when this method is called
    """
    total = 0.0
    for product, count in self.xcart_product_counts():
      for quantity, price in self.xregistry_quantity_prices(product):
        total += (count / quantity) * price
        count = count % quantity
      if count != 0:
        raise ValueError("Product does not include a 1 quantity in registry: {0}".format(product))
    return total

  def xregistry_quantity_prices(self, product):
    """ Generator to get (quantity,price) ordered by quantity in descending order
    """
    print self.registry[product].heap
    return self.registry[product].xpeek(len(self.registry[product]))

  def xcart_product_counts(self):
    """ Generator to get all of the (product, count) in the cart
    """
    return ((product, count) for product, count in self.cart.most_common())

  def register_product(self, product, quantity, price):
    """ Register a product in the form of product string, quantity and price
        The product string is matched during the scan method
        This method can accept multiple entries for the same product to simulate bulk pricing by varying quantities
    """
    if quantity <= 0:
      raise ValueError("Cannot add product {0} with a negative or zero quantity: {1}".format(product, quantity))
    if price < 0:
      raise ValueError("Cannot add product {0} with a negative price: {1}".format(product, price))
    self.registry[product].push(int(quantity), float(price))

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
      terminal.register_product(row['product'], row['quantity'], row['price'])
  return terminal
