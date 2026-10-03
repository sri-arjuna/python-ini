#
#    Basic message and error variables/text
#

# Make sure we empty all variables upon "init" (or language change)
_MSG = {}
_ERR = {}

#
#   Verbose messages
#
_MSG["conf_read"] = "Configuration loaded."
_MSG["file_not_found"] = "Configuration file not found"
_MSG["memory_only"] =  "No file path provided. Operating in memory-only mode."
_MSG["invalid_data"] = "Invalid data"
_MSG["imported"] = "Imported configuration."
_MSG["backup"] = "Restoring to default configuration."
#_MSG[""] = 

#
#   Error Messages
#
_ERR["buffer"] = "Some buffer problem."
_ERR["value"] =  "Value mismatch."
_ERR["generic"] = "Error"
_ERR["import"] = "Could not import configuration."
_ERR["empty"] = "Valid dict format, but empty values."
_ERR["backup"] = f"Could not restore default configuration."
