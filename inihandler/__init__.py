from .ini import ConfigHandler
from typing import Union as _Union

def handler(file_path="", bInstantSave=True, bStrict=True, bForcedCommentStyle: _Union[None, str]=None, bVerbose=False, sVerbosePrefix="", SEP="=", sEncoding="utf-8", sDefaultBackupConfig=""):
    """
    Initialize the ini-handler, the one that preserves file comments on normal saves!

    Errors will always be printed to "stderr".

    Supported comment-single/on-line styles are: "#", ";", "//", "|"

    Supported comment-MULTI-line styles are: "*/", "-->", '\"\"\"'


    :param file_path: Path to the .ini **file**, or a **nested dict**: {"Section 1": {"var1": "value1"}, "Section 2": {"variable_name": "its value"}}
    :param bInstantSave: If True, saves to file on every 'set()'.
    :param bStrict: True/Default expects '[Section]', where as 'False' will expect ONLY 'variable = value'
    :param bForcedCommentStyle: If set to a non-None string (e.g., "#"), it enforces that only that specific comment style is accepted for all parsing. Set to None for flexible, multi-style comment handling, incl multi-line comments.
    :param bVerbose: If True, prints basic status messages.
    :param sVerbosePrefix: This will print '[sVerbosePrefix] message' instead of just 'message'
    :param SEP: The separator for key-value pairs (default "=" for cross-platform compatability).
    :param sEncoding: On rare occasions your files might not be "utf-8", here you can handle such cases.
    :param sDefaultBackupConfig: Expects "path/to/file", this will be used if required "file_path" doesnt exist) and/or if/when its config became invalid.
    """
    return ConfigHandler(file_path, bInstantSave=bInstantSave, bStrict=bStrict, bForcedCommentStyle=bForcedCommentStyle, bVerbose=bVerbose, sVerbosePrefix=sVerbosePrefix, SEP=SEP, sEncoding=sEncoding, sDefaultBackupConfig=sDefaultBackupConfig)
