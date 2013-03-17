import abc
import ast



class Defect(object):
  __metaclass__ = abc.ABCMeta

  def __init__(self, node, options = []):
    self.options =  options
    self.node = node

  def trace(self):
    if len(self.node.args) == 1 and isinstance(self.node.args[0], ast.Name):
      var_node = self.node.args[0]
      self.trace_walk(var_node.link, list(var_node.link.nodeType)[0])

  def trace_walk(self, node, type):
    # print node.__dict__
    if 'assign' in node.inverse_relationship:
      for dep, args in node.inverse_relationship['assign']:
        if dep.__class__.__name__ == 'UsualVarTypeGraphNode':
          print node.name, ':=', dep.name
          self.trace_walk(dep, type)
        else:
          for tp in dep.nodeType:
            print node.name, ':=', tp

  @abc.abstractmethod
  def title(self):
    return "Defect Title"

  def __repr__(self):
    return self.title()


#Default Defects

class ImportDefect(Defect):
  def title(self):
    title = 'Cannot import %s' % self.options['name']
    if 'from' in self.options:
      title += ' from %s' % self.options['from']
    return title

class FuncCallDefect(Defect):
  def title(self):
    return 'Cannot resolve func call'
