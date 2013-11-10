import const
import locale

#list of manuals on wiki, map locale code to wiki extension, add language codes
#completely, or first part, so pt_BR if Brazilian portugeze wiki manual, and 
#nl for Dutch (nl_BE, nl_NL language code)
MANUALS = {
    'nl' : '/nl',
    'fr' : '/fr',
    'sq' : '/sq',
    'mk' : '/mk',
    'de' : '/de',
    'fi' : '/fi',
    'ru' : '/ru',
}

#first, determine language code, so nl_BE --> wiki /nl
LANG = locale.getlocale()[0]
if not LANG:
    LANG = 'C'
#support environment overrule:
try: 
    if not os.environ['LANGUAGE'] or \
            os.environ['LANGUAGE'].split(':')[0] == LANG:
        pass
    else:
        LANG = os.environ['LANGUAGE'].split(':')[0]
except:
    pass
EXTENSION = ''
try:
    EXTENSION = MANUALS[LANG]
except KeyError:
    pass
try:
    if not EXTENSION :
        EXTENSION = MANUALS[LANG.split('_')[0]]
except KeyError:
    pass

def help(webpage='', section=''):
    """
    Display the specified webpage and section from the Gramps 3.0 wiki.
    """
    if not webpage:
        link = const.URL_WIKISTRING + const.URL_MANUAL_PAGE + EXTENSION
    else:
        link = const.URL_WIKISTRING + webpage + EXTENSION
        if section:
            link = link + '#' + section

WIKI_HELP_PAGE = '%s_-_Entering_and_Editing_Data:_Detailed_-_part_3' % \
                 const.URL_MANUAL_PAGE
WIKI_HELP_SEC  = unicode('manual|Tags')

help(webpage=WIKI_HELP_PAGE, section=WIKI_HELP_SEC)
a = 1
