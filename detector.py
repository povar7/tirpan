import ast
from configure import config
from checkers import BasenameChecker
from defect_collector import DefectCollector


class Detector(object):
  def __init__(self):
    self.collector = DefectCollector()
    self.checker = Checker(BasenameChecker, self.collector)

  def check(self, module):
    #print module.name
    self.checker.visit(module.ast)

  def defects(self):
    return self.collector.defects

  def count_defects(self,klass):
    return len([d for d in self.defects() if isinstance(d, klass)])


class Checker(ast.NodeVisitor):
    model = None

    def __init__(self, klass, collector):
        self.model = klass(collector)


    def visit(self, node):
        nodename = node.__class__.__name__.lower()

        if nodename == 'functiondef':
            try:
                for template in node.link.templates.values():
                    for ast in template.ast:
                        self.visit(ast)
            except:
                pass
        else:
            methodName = "visit_" + nodename
            #print methodName
            if hasattr(self.model, methodName):
                method = getattr(self.model, methodName)
                if callable(method):
                    method(node)
            super(Checker, self).visit(node)

detector = Detector()