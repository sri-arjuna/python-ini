#
#    Basic message and error variables/text
#

# Make sure we empty all variables upon "init" (or language change)
_MSG = {}
_ERR = {}
_WARN = {}

#
#   Verbose messages
#   These are for "positive" messages
#
_MSG["conf_read"] = "Configuration loaded."
_MSG["imported"] = "Imported configuration."
_MSG["backup"] = "Restoring to default configuration."
# Change / move -> ERR ?
_MSG["file_not_found"] = "Configuration file not found"
_MSG["invalid_data"] = "Invalid data"
# Change / move -> WARN ?
_MSG["memory_only"] =  "No file path provided. Operating in memory-only mode."

#_MSG[""] = 


#
#   Error Messages
#   These are "fatal", ABORT worthy (allthough not always required)
#
_ERR["buffer"] = "Some buffer problem."
_ERR["value"] =  "Value mismatch."
_ERR["generic"] = "Error"
_ERR["import"] = "Could not import configuration."
_ERR["empty"] = "Valid dict format, but empty values."
_ERR["backup"] = f"Could not restore default configuration."


#
#   Warning Messages
#   These are for "sub-optimal" handling for provided configuration
#   In most - probably all - cases, an internal work-around can be provided
#
_WARN["bForcedCommentStyle_differs"] = "WARNING: comment indicator differs from forced comment syle"
_WARN[""] = ""
_WARN[""] = ""
_WARN[""] = ""

