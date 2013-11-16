import os

class A(object):
    def __init__(self):
        self.css_filename = ''

    def set_css_filename(self, css_filename):
        if os.path.basename(css_filename):
            self.css_filename = css_filename
        else:
            self.css_filename = ''

def foo(msg):
    css_filename = []
    a = A()
    a.set_css_filename(css_filename)

foo('foo\nbar')
