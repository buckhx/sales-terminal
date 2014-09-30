import csv
import heapq
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
    self.registry = defaultdict(list)
    self.registry_keys = defaultdict(set)
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
    for product, count in self.gen_cart_product_counts():
      for quantity, price in self.gen_registry_quantity_prices(product):
        total += (count / quantity) * price
        count = count % quantity
      if count != 0:
        raise ValueError("Product does not include a 1 quantity in registry: {0}".format(product))
    return total

  def gen_registry_quantity_prices(self, product):
    """ Generator to get (quantity,price) ordered by quantity in descending order
    """
    return ((abs(quantity),price) for quantity,price in self.registry[product])

  def gen_cart_product_counts(self):
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
    quantity = -quantity
    keys, heap = self.registry_keys[product], self.registry[product]
    if quantity in keys:
      [heap.remove(rm) for rm in [qp for qp in heap if qp[0] == quantity]]
      heapq.heapify(heap)
    keys.add(quantity)
    heapq.heappush(heap, (quantity, price))

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
      terminal.register_product(row['product'], int(row['quantity']), float(row['price']))
  return terminal
