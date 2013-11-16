import os, subprocess

def get_available_translations(dir, domain):
    """
    Get a list of available translations.

    :returns: A list of translation languages.
    :rtype: unicode[]

    """
    languages = ["en"]

    if dir is None:
        return languages

    for langdir in os.listdir(dir):
        mofilename = os.path.join( dir, langdir,
                                   "LC_MESSAGES", "%s.mo" % domain )
        if os.path.exists(mofilename):
            languages.append(langdir)

    languages.sort()

    return languages

def mac_setup_localization(dir, domain):
    defaults = "/usr/bin/defaults"
    find = "/usr/bin/find"
    locale_dir = "/usr/share/locale"
    available = get_available_translations(dir, domain)

    def mac_language_list():
        languages = []
        try:
            languages = subprocess.Popen(
                [defaults,  "read", "-app", "Gramps", "AppleLanguages"],
                stderr=open("/dev/null"),
                stdout=subprocess.PIPE). \
                communicate()[0].strip("()\n").split(",\n")
        except OSError:
            pass

        if len(languages) == 0 or (len(languages) == 1 and languages[0] == ""):
#            try:
            languages = subprocess.Popen(
                    [defaults, "read", "-g", "AppleLanguages"],
                    stderr=open("/dev/null"),
                    stdout=subprocess.PIPE). \
                    communicate()[0].strip("()\n").split(",\n")
#            except OSError:
#                pass
        usable = []
        for lang in languages:
            lang = lang.strip().strip('"').replace("-", "_", 1)
            if lang == "cn_Hant": #Traditional; Gettext uses cn_TW
                lang = "cn_TW"
            if lang == "cn_Hans": #Simplified; Gettext uses cn_CN
                lang = "cn_CN"

            if lang.startswith("en"): # Gramps doesn't have explicit
                usable.append("C")    # English translation, use C
                continue
            if lang in available or lang[:2] in available:
                usable.append(lang)

        return usable

    def mac_get_locale():
        locale = ""
        calendar = ""
        currency = ""
        default_locale = ""
        try:
            default_locale = subprocess.Popen(
                [defaults, "read", "-app", "Gramps", "AppleLocale"],
                stderr = open("/dev/null"),
                stdout = subprocess.PIPE).communicate()[0]
        except OSError:
            pass
        if not default_locale:
            try:
                default_locale = subprocess.Popen(
                    [defaults, "read", "-g", "AppleLocale"],
                    stderr = open("/dev/null"),
                    stdout = subprocess.PIPE).communicate()[0]
            except OSError:
                return (locale, calendar, currency)

        div = default_locale.split("@")
        locale = div[0]
        if len(div) > 1:
            div = div[1].split(";")
            for phrase in div:
                try:
                    (name, value) = phrase.split("=")
                    if name == "calendar":
                        calendar = value
                    elif name == "currency":
                        currency = value
                except OSError:
                    pass

        return (locale, calendar, currency)

    def mac_get_collation():
        collation = ""
        try:
            collation = subprocess.Popen(
                [defaults, "read", "-app", "Gramps", "AppleCollationOrder"],
                stderr = open("/dev/null"),
                stdout = subprocess.PIPE).communicate()[0]
        except OSError:
            pass
        if not collation:
            try:
                collation = subprocess.Popen(
                    [defaults, "read", "-g", "AppleCollationOrder"],
                    stderr = open("/dev/null"),
                    stdout = subprocess.PIPE).communicate()[0]
            except OSError:
                pass

        return collation

# Locale.setlocale() will throw if any LC_* environment variable isn't
# a fully qualified one present in
# /usr/share/locale. mac_resolve_locale ensures that a locale meets
# that requirement.
    def mac_resolve_locale(loc):
        if len(loc) < 2:
            return None
        if len(loc) >= 5 and os.path.exists(os.path.join(locale_dir, loc[:5])):
            return loc[:5]
        if len(loc) > 2:
            loc = loc[:2]
    # First see if it matches lang
        if (lang.startswith(loc)
            and os.path.exists(os.path.join(locale_dir, lang[:5]))):
            return lang[:5]
        else:
    # OK, no, look through the translation list, but that's not likely
    # to be 5 letters long either
            for l in translations:
                if (l.startswith(loc) and len(l) >= 5
                    and os.path.exists(os.path.join(locale_dir, l[:5]))):
                    return l[:5]
                    break

            else:
    # so as a last resort, pick the first one for that language.
                locale_list = subprocess.Popen(
                    [find, locale_dir, "-name", loc + "_[A-Z][A-Z]"],
                    stderr = open("/dev/null"),
                    stdout = subprocess.PIPE). \
                    communicate()[0].strip("()\n").split(",\n")
                if len(locale_list) > 0:
                    return os.path.basename(locale_list[0])
                else:
                    return None

# The action starts here

    (loc, currency, calendar)  = mac_get_locale()
    collation = mac_get_collation()
    translations = mac_language_list()

    if not os.environ.has_key("LANGUAGE"):
        if len(translations) > 0:
            if os.environ.has_key("MULTI_TRANSLATION"):
                os.environ["LANGUAGE"] = ":".join(translations)
            else:
                os.environ["LANGUAGE"] = translations[0]
        elif (len(locale) > 0 and locale in available
              and not locale.starts_with("en")):
            os.environ["LANGUAGE"] = locale
        elif (len(collation) > 0 and collation in available
              and not collation.starts_with("en")):
            os.environ["LANGUAGE"] = collation

    if not os.environ.has_key("LANG"):
        lang = "en_US"
        loc = mac_resolve_locale(loc)
        if loc != None:
            lang = loc
            collation = mac_resolve_locale(collation)
            if not os.environ.has_key("LC_COLLATE") and collation != None:
                os.environ["LC_COLLATE"] = collation

        elif len(collation) > 0:
            lang = mac_resolve_locale(collation)
        if lang != None:
            os.environ["LANG"] = lang
