from ggettext import gettext as _

def foo(msg):
    return msg

x = foo(_("Progress Information"))
print x
