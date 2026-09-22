from .ini import ConfigHandler

def handler(file_path="", bInstantSave=True, bStrict=True, bVerbose=False, sVerbosePrefix="", SEP="=", sEncoding="utf-8", sDefaultBackupConfig=""):
    """
    Initialize the config handler, the one that preserves file comments on normal saves!

    Errors will always be printed.

    :param file_path: Path to the .ini **file**, or a **nested dict**: {"Section 1": {"var1": "value1"}, "Section 2": {"variable_name": "its value"}}
    :param bInstantSave: If True, saves to file on every 'set()'.
    :param bStrict: True/Default expects '[Section]', where as 'False' will expect ONLY 'variable = value'
    :param bVerbose: If True, prints basic status messages.
    :param sVerbosePrefix: This will print '[sVerbosePrefix] message' instead of just 'message'
    :param SEP: The separator for key-value pairs (default "=" for cross-platform compatability).
    :param sEncoding: On rare occasions your files might not be "utf-8", here you can handle such cases.
    :param sDefaultBackupConfig: Expects "path/to/file", this will be used if required "file_path" doesnt exist) and/or if/when its config became invalid.
    """
    return ConfigHandler(file_path, bInstantSave=bInstantSave, bStrict=bStrict, bVerbose=bVerbose, sVerbosePrefix=sVerbosePrefix, SEP=SEP, sEncoding=sEncoding, sDefaultBackupConfig=sDefaultBackupConfig)
