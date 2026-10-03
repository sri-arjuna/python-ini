import inihandler

#
#   Set vars for files
#   easier to reuse
#
sDefault = "test/test-mixed.ini"
sLazy = "test/test-lazy.cfg"
sSpecific = "test/test-specific.conf"

#
#   Load an ini with default settings
#

print(f"Loading ini: {sDefault}")
ini_default = inihandler.handler(sDefault, bVerbose=True)
# Test output
#print(ini_default.get("section", "sooooo"))
ini_default.dump()

#
#   Load an ini/config file without any [Sections]
#   aka: a shell-like config
#
#   you'd differ between a BASH-shell or a C-Shell by setting a different SEP
#   but we dont do this here
#
print(f"Loading ini: {sLazy}")
ini_lazy  = inihandler.handler(sLazy, bStrict=False, bVerbose=True)
# Test output
#ini_lazy.get_simple("some")
#ini_lazy.get_simple("other")
ini_lazy.dump()

#
#   Last but not least,
#   lets work with some specifics!
#
print(f"Loading ini: {sSpecific}")
ini_spec  = inihandler.handler(sSpecific, SEP=" : ", bForcedCommentStyle=";", bVerbose=True)
# Test output
#ini_spec.get("urls", "url")
#ini_spec.get("urls", "url_fails")
#ini_spec.get("other", "some_string")
ini_spec.dump()
