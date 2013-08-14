class Quantity:
  """Class representing physical quantities typically to be plotted"""
  def __init__(self, name, title, unit, expression):
    self.name = name
    self.title = title
    self.unit = unit
    self.expression = expression


class Cut:
  """Facilitate selection bookkeeping in playn (Py)ROOT.
  Simplify generation of a cut-flow table and N-1 plots."""
  def __init__(self, quantity, condition):
    self.quantity = quantity   # an instance of Quantity
    self.condition = condition # a string like '> 40'

  def __repr__(self):
    return self.quantity.expression + " " + self.condition


class Selection:
  """Holds a list of Cuts. Enables to iterate on them."""
  def __init__(self, cuts):
    self.cuts = cuts

  def __repr__(self):
    """Returns an "and" of cuts in the form of string for TTree::Draw."""
    return " & ".join(["(%s)" % cut for cut in self.cuts])

  def cuts(self):
    return self.cuts[:]

  def nMinus1(self, cut):
    cuts = self.cuts[:]
    cuts
