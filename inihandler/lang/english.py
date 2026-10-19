#
#    Basic message and error variables/text
#

# Make sure we empty all variables upon "init" (or language change)
MSG = {}
ERR = {}
WARN = {}

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
MSG['init'] = "ini-handler initialized."
MSG['lang_default'] = "Init default messages."
MSG['conf_read'] = "Configuration loaded."
MSG['conf_load'] = "Loading configuration from"


MSG['imported'] = "Imported configuration."

# Change / move -> ERR ?
MSG['file_not_found'] = "Configuration file not found"
MSG['invalid_data'] = "Invalid data"
# Change / move -> WARN ?
MSG['memory_only'] =  "No file path provided. Operating in memory-only mode."

#MSG[''] = 
#MSG[''] = 



#
#   Warning Messages
#   These are for "sub-optimal" handling for provided configuration
#   In most - probably all - cases, an internal work-around can be provided
#
WARN['lang_miss'] = f"{W}: Provided language could not be loaded."
WARN['backup_start'] = f"{W}: Restoring to default configuration."
WARN['backup_end'] = f"{W}: Restored configuration from default settings."
WARN['bForcedCommentStyle_differs'] = f"{W}: Comment indicator differs from forced comment syle"
WARN[''] = f"{W}: "
WARN[''] = f"{W}: "
WARN[''] = ""


#
#   Error Messages
#   These are "fatal", ABORT worthy (allthough not always required)
#
ERR['language'] = f"{E}: Provided language not found:"
ERR['backup_fail'] = f"{E}: Failed to restore default config."
ERR['backup_miss'] = f"{E}: Path to configuration-backup provided, but missing or invalid"

ERR['buffer'] = f"{E}: Some buffer problem."
ERR['value'] =  f"{E}: Value mismatch."
ERR['generic'] = f"{E}: Error"
ERR['import'] = f"{E}: Could not import configuration."
ERR['empty'] = f"{E}: Valid dict format, but empty values."


