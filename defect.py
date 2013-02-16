import abc

class Defect(object):
  __metaclass__ = abc.ABCMeta

  def __init__(self, node, options = []):
    self.options =  options
    self.node = node

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
