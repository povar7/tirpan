def _print_locale():
    """ Test function.
    """
    categories = {}
    def _init_categories(categories=categories):
        for k,v in globals().items():
            if k[:3] == 'LC_':
                categories[k] = v
    _init_categories()
    try:
        del categories['LC_ALL']
    except KeyError:
        pass

_print_locale()
a = 1
