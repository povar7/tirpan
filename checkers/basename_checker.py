import ast
from typenodes import TypeBaseString, TypeUnknown

class BasenameChecker(object):
  def __init__(self, collector):
    self.collector = collector

  def visit_call(self, node):
      if isinstance(node.func, ast.Attribute) and node.func.attr == 'basename' and len(node.args) == 1:
        nodeTypes = node.args[0].link.nodeType
        if any(not isinstance(elem, (TypeBaseString, TypeUnknown)) for elem in nodeTypes):
          self.collector.add_defect("Basename argument error", node)

