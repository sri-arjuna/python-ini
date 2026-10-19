""""
    This file handles basic variable-delivery.

    Basicly: definitions, constants and language (dict) translations (and related functions)

    © 2026 by Simon Arjuna Erat, Switzerland
"""

#
#   Imports
#
import os as _os
from typing import Union as _Union
from typing import Tuple as _Tuple

#
#   Types
#
StringOrDict = _Union[str, dict]
ListOrString = _Union[list, str]
NoneOrString = _Union[None, str]
StringAndString = _Tuple[str, str]

#
#   Constants / Lists
#
_lang_dir = f"{_os.curdir}/inihandler/lang"
MSG = {}
ERR = {}
WARN = {}
comments = ["#", ";", ":", "//", "|"]
comments_multi_start = ["/*", "<!--", '"""']
comments_multi_end = ["*/", "-->", '"""']
quotes = ["'", '"']
DEFAULT_TRUE = True
DEFAULT_FALSE = False
DEFAULT_SEP = "="

######################################################
#
#               Language Functions
#
######################################################

def lang_set(language: str) -> bool:
    """
    Set message/warning/error language to 'language'

    Currently, only english is supported
    """
    global MSG
    global ERR
    global WARN
    global _lang_dir

    # Set default language
    from ..lang.english import MSG, ERR, WARN

    # Try loading "custom" language
    if language.lower() != "english":
        try:
            # Factualy, as of now -> this is supposed to fail!
            # TODO: Obviously, this needs better handling
            from ..lang.language import MSG, ERR, WARN # type: ignore
            return True

        except Exception:
            # Allthough the above improper syntax would probably result in a different error...
            # Because no other language is available, we'll raise it as "ImportError" for now.
            raise ImportError(f"{ERR['language']} {language}")
    else:
        # Language does not need to be changed
        # So, everything is good :)
        return True

def lang_list() -> list:
    """List supported languages"""
    global _lang_dir
    result = []

    # Lets check for content in language dir
    for entry in _os.listdir(_lang_dir):
        # Lets make sure we only list files
        if _os.path.isfile(entry):
            # And remove the py extension
            result.append(entry[:2])
    return list(result)
