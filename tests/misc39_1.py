import os
import platform

import const

LOCALEDOMAIN = 'gramps'

if "GRAMPSI18N" in os.environ:
    LOCALEDIR = os.environ["GRAMPSI18N"]
elif os.path.exists( os.path.join(const.ROOT_DIR, "lang") ):
    LOCALEDIR = os.path.join(const.ROOT_DIR, "lang")
elif os.path.exists(os.path.join(const.PREFIXDIR, "share/locale")):
    LOCALEDIR = os.path.join(const.PREFIXDIR, "share/locale")
else: 
    LOCALEDIR = None

def mac():
    from const import MACOS
    if platform.system() in MACOS:
        return True
    return False

if mac():
    import misc39_2
    misc39_2.mac_setup_localization(LOCALEDIR, LOCALEDOMAIN)
    b = True
else:
    b = False

a = 1
print b
