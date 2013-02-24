from defect import Defect
from typenodes    import TypeNone

class ReturnDefect(Defect):
  def title(self):
    return "Return on class init method"

class ReturnChecker(object):
  def __init__(self, collector):
    self.collector = collector
    self.in_initialize = False

  def before_return(self, node):
    if self.in_initialize and node.value and any(not isinstance(x, TypeNone) for x in node.value.link.nodeType):
      self.collector.add_defect(ReturnDefect(node))

  def before_functiondef(self, node):
    self.in_initialize = node.name == '__init__'

  def after_functiondef(self, node):
    self.in_initialize = False
    



