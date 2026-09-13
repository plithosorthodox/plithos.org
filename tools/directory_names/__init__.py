# -*- coding: utf-8 -*-
"""What each body in the directory is called, and where it sits, per language.

The directory's page has been written in twenty-two languages since it
shipped - its heading, its lede, the caveat, the group labels, the country
chips. The rows themselves were not, and that left a Greek reader with a
Greek page wrapped around an English list.

Three kinds of text sit on a row and they are not the same kind of thing:

  - The **address** is not translated, ever. It is what you write on an
    envelope, and it is reproduced exactly as the body itself prints it,
    Turkish or Cyrillic or Greek. So is the website.
  - The **local** name is the body's own, in its own language, and is
    likewise left alone.
  - The **name** and the **seat** are translated here. "The Church of
    Constantinople" is not a proper name; it is the English label of the
    list it was read from, and in Greek it should read as Greek. A city has
    a received form in every one of these languages, and this site's own
    saints' lives are full of them - Constantinople, Moscow, Athens,
    Alexandria and Damascus are named on nearly every page of the calendar.

So the rule for filling one of these files is the rule the rest of the site
was built by: **gather, do not compose.** Look the city up in what this
site already publishes in that language before writing it. Where a name has
a received form in the language's own liturgical books, use the received
form and do not re-render it.

Each language is one file, so the lanes do not collide:

    tools/directory_names/el.py      NAMES = {...}   SEATS = {...}

NAMES is keyed by the row's id, SEATS by the English seat, so two Churches
in the same city share one entry, and STYLED by the row's id again - that
last being the name a body gives itself, which is a different thing from the
name the list it was read from gives it, and in some languages the same
thing. A key left out simply falls back to English on the page, which is how
a language half-done still reads.

    python3 tools/directory_words.py --audit    checks every word
    python3 tools/directory_words.py --write    folds them into the data
"""
import importlib
import os

LANGS = "en el ru ro uk de es ar fr pt it sr ka zh ja ko sw hy arc hi bn ur".split()


def load(lang):
    """(names, seats, styled), empty where the file is not there yet."""
    try:
        m = importlib.import_module("directory_names." + lang)
    except ImportError:
        try:
            m = importlib.import_module("tools.directory_names." + lang)
        except ImportError:
            return {}, {}, {}
    return (dict(getattr(m, "NAMES", {})), dict(getattr(m, "SEATS", {})),
            dict(getattr(m, "STYLED", {})))


def written():
    """The languages that have a file at all."""
    here = os.path.dirname(os.path.abspath(__file__))
    return [L for L in LANGS
            if os.path.exists(os.path.join(here, L + ".py"))]
