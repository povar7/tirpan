import ast
from configure import config
from checkers import BasenameChecker, ReturnChecker
from defect_collector import DefectCollector
from defect import Defect

class Detector(object):
  def __init__(self):
    self.collector = DefectCollector()
    self.checker = Checker(self.collector)

  def check(self, module):
    #print module.name
    self.checker.visit(module.ast)

  def defects(self, klass = Defect):
    return [d for d in self.collector.defects if isinstance(d, klass)]

  def count_defects(self,klass):
    return len([d for d in self.defects() if isinstance(d, klass)])


class Checker(ast.NodeVisitor):
    models = []
    klasses = [BasenameChecker, ReturnChecker]
    
    def __init__(self, collector):
      for klass in self.klasses:
        self.models.append(klass(collector))


    def visit(self, node):
      nodename = node.__class__.__name__.lower()

      self.try_call("before_" + nodename, node)
      if nodename == 'functiondef':
        try:
          for template in node.link.templates.values():
            for ast in template.ast:
              self.visit(ast)
        except:
          pass
      else:
        super(Checker, self).visit(node)
      self.try_call("after_" + nodename, node)

    def try_call(self, method_name, args):
      for model in self.models:
          if hasattr(model, method_name):
            method = getattr(model, method_name)
            if callable(method):
                method(args)

detector = Detector()