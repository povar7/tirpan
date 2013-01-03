_ = unicode

def make_css_dict(tup):
    """
    Basically, make a named tuple.
    """
    return {
        "id": tup[0],
        "user": tup[1],
        "translation": tup[2],
        "filename": tup[3],
        "navigation": tup[4],
        "images": tup[5],
        "javascript": tup[6],
        }

CSS_FILES = [
        # Basic Ash style sheet
        ["Basic-Ash",     1, _("Basic-Ash"),
         'Web_Basic-Ash.css',     None, [], []],

        # Basic Blue style sheet with navigation menus
        ["Basic-Blue",    1, _("Basic-Blue"),
         'Web_Basic-Blue.css',    "narrative-menus.css", [], []],
]

def process_list(data):
    """
    Gather all of the web resources together, and allow override files
    if available.
    """
    retdict = {}
    for css in data:
        retdict[css[0]] = make_css_dict(css)
    return retdict

x = process_list(CSS_FILES)
print x
