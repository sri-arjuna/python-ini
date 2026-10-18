import inihandler

#
#   Set vars for files
#   easier to reuse
#
sStable = "test/test-stable.ini"
sDefault = "test/test-mixed.ini"
sLazy = "test/test-lazy.cfg"
sSpecific = "test/test-specific.conf"

#
#   Load an ini with stable formating and default settings
#
print(f"\nLoading ini: {sStable}")
ini_stable = inihandler.handler(sStable, SEP=" = ", sVerbosePrefix="Stable Example")
# Test output
ini_stable.dump()

#
#   Load an ini with default settings
#   bVerbose=True, 
#
print(f"\nLoading ini: {sDefault}")
ini_default = inihandler.handler(sDefault, sVerbosePrefix="Default/Mixed Example")
# Test output
ini_default.dump()

#
#   Load an ini/config file without any [Sections]
#   aka: a shell-like config
#
#   you'd differ between a BASH-shell or a C-Shell by setting a different SEP
#   but we dont do this here
#
print(f"\nLoading ini: {sLazy}")
ini_lazy  = inihandler.handler(sLazy, bStrict=False, bVerbose=True, sVerbosePrefix="Lazy Example")
# Test output
ini_lazy.dump()

#
#   Last but not least,
#   lets work with some specifics!
#
print(f"\nLoading ini: {sSpecific}")
ini_spec  = inihandler.handler(sSpecific, SEP=" : ", bForcedCommentStyle=";", bVerbose=True, sVerbosePrefix="Specific Changes")
# Test output
ini_spec.dump()
