import sys

import getopt

LONGOPTS = [
    "action=", 
    "class=",
    "config=",
    "debug=",
    "display=",
    "disable-sound", 
    "disable-crash-dialog", 
    "enable-sound",
    "espeaker=",
    "export=",
    "force-unlock",
    "format=",
    "gdk-debug=", 
    "gdk-no-debug=", 
    "gtk-debug=", 
    "gtk-no-debug=", 
    "gtk-module=", 
    "g-fatal-warnings",
    "help",
    "import=", 
    "load-modules=",
    "list" 
    "name=",
    "oaf-activate-iid=", 
    "oaf-ior-fd=", 
    "oaf-private",
    "open=",
    "options=",
    "screen=",
    "show", 
    "sm-client-id=", 
    "sm-config-prefix=", 
    "sm-disable",
    "sync",
    "usage", 
    "version",
    "qml",
]


SHORTOPTS = "O:i:e:f:a:p:d:c:lLhuv?s"

class ArgParser:
    def __init__(self, args):
        """
        Pass the command line arguments on creation.
        """
        self.args = args
        self.parse_args()

    def parse_args(self):
        options, leftargs = getopt.getopt(self.args[1:], SHORTOPTS, LONGOPTS)

argpars = ArgParser(sys.argv)
