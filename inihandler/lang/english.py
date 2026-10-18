#
#    Basic message and error variables/text
#

# Make sure we empty all variables upon "init" (or language change)
_MSG = {}
_ERR = {}
_WARN = {}

#
#   Re-Used vars for easier translation...
#   Specialy since WARNING and ERROR should have that "prefix"
#
W = "WARNING"
E = "ERROR"

#
#   Verbose messages
#   These are for "positive" and/or "progress" messages
#   Listed in order of apperance (handling "top level" first though... with default settings)
#
_MSG['init'] = "ini-handler initialized."
_MSG['lang_default'] = "Init default messages."
_MSG['conf_read'] = "Configuration loaded."
_MSG['conf_load'] = "Loading configuration from"


_MSG['imported'] = "Imported configuration."

# Change / move -> ERR ?
_MSG['file_not_found'] = "Configuration file not found"
_MSG['invalid_data'] = "Invalid data"
# Change / move -> WARN ?
_MSG['memory_only'] =  "No file path provided. Operating in memory-only mode."

#_MSG[''] = 
#_MSG[''] = 



#
#   Warning Messages
#   These are for "sub-optimal" handling for provided configuration
#   In most - probably all - cases, an internal work-around can be provided
#
_WARN['lang_miss'] = f"{W}: Provided language could not be loaded."
_WARN['backup_start'] = f"{W}: Restoring to default configuration."
_WARN['backup_end'] = f"{W}: Restored configuration from default settings."
_WARN['bForcedCommentStyle_differs'] = f"{W}: Comment indicator differs from forced comment syle"
_WARN[''] = f"{W}: "
_WARN[''] = f"{W}: "
_WARN[''] = ""


#
#   Error Messages
#   These are "fatal", ABORT worthy (allthough not always required)
#
_ERR['backup_fail'] = f"{E}: Failed to restore default config."
_ERR['backup_miss'] = f"{E}: Path to configuration-backup provided, but missing or invalid"

_ERR['buffer'] = f"{E}: Some buffer problem."
_ERR['value'] =  f"{E}: Value mismatch."
_ERR['generic'] = f"{E}: Error"
_ERR['import'] = f"{E}: Could not import configuration."
_ERR['empty'] = f"{E}: Valid dict format, but empty values."


