import os as _os
import sys as _sys
import shutil as _shutil
from .tools import LoadFile
from .tools import vars

#
#    Basic message variables
#    for easier re-use
#
##vars.MSG = {}
#vars.ERR = {}
#vars.WARN = {}
#_lang_dir = f"{_os.curdir}/inihandler/lang"
#print(_lang_dir)

class INIhandler:
    def __init__(self, file_path: vars.StringOrDict="", bInstantSave: bool=True, bStrict: bool=True, bForcedCommentStyle: vars.NoneOrString=None, bVerbose: bool=False, sVerbosePrefix: str="", SEP: str="=", sEncoding: str="utf-8", sDefaultBackupConfig: str="", lang: str="english"):
        """
        Initialize the ini-handler, the one that preserves file comments on normal saves!
        
        Errors will always be printed to "stderr".
    
        Supported comment-single/on-line styles are: "#", ";", "//", "|"
    
        Supported comment-MULTI-line styles are: "*/", "-->", '\"\"\"'
    
    
        :param file_path: Path to the .ini **file**, or a **nested dict**: {"Section 1": {"var1": "value1"}, "Section 2": {"variable_name": "its value"}}
        :param bInstantSave: If True, saves to file on every 'set()'.
        :param bStrict: True/Default expects '[Section]', where as 'False' will expect ONLY 'variable = value'
        :param bForcedCommentStyle: If set to a non-None string (e.g., "#"), it enforces that only that specific comment style is accepted for all parsing. Set to 'None' for flexible, multi-style comment handling, incl multi-line comments.
        :param bVerbose: If True, prints basic status messages.
        :param sVerbosePrefix: This will print '[sVerbosePrefix] message' instead of just 'message'
        :param SEP: The separator for key-value pairs (default "=" for cross-platform compatability).
        :param sEncoding: On rare occasions your files might not be "utf-8", here you can handle such cases.
        :param sDefaultBackupConfig: Expects "path/to/file", this will be used if required "file_path" doesnt exist) and/or if/when its config became invalid.
        :param lang: Defaults to 'english' for 'messages', currently no other languages are supported
        """
        class _DataContainer:
            def __init__(self): #, section: str, variable: any
                """
                Provides data used to save, return, export. This is not supposed to be called by user

                :param quick: NESTED DICT, provides easy and quick access to values:: value = quick["section"]["variable"]
                :param lines: LIST, contains all lines of file_path, if one was provided.
                :param raw: STR, contains the the whole file in its original form.
                :param comment_before: NESTED DICT, to avoid any unwanted side effects if there are multiple variables/keys in a filed.
                :param comment_on_line: NESTED DICT, to avoid any unwanted side effects if there are multiple variables/keys in a filed, "on line" comments will be printed at position 20, or 1 space after value.
                """
                self.quick = {}
                self.lines = []
                self.raw = ""
                self.comment_before = {}
                self.comment_on_line = {}
        
        self.file_path = file_path
        # Disable bInstantSave if nothing was passes as file_path
        self.bInstantSave = bInstantSave if file_path else False
        self.encoding = sEncoding
        self.bStrict = bStrict
        self.bVerbose = bVerbose
        self._sVerbosePrefix = sVerbosePrefix
        self._sep = SEP
        self.sDefaultBackupConfig = sDefaultBackupConfig
        self.bForcedCommentStyle = bForcedCommentStyle
        self.lang = lang

        # --- Update to load_data and load_file ---
        # (No change needed here as load functions only read data, they don't apply forced comments)
        # --- Update to save ---
        # Logic in save() must check self.bForcedComment before writing comment_before or comment_on_line.
        self.__data = _DataContainer()
        self.__data.quick = {}
        self.__data.raw = ""
        self.__data.comment_before = {}
        self.__data.comment_on_line = {}
        # Internal bool to ease handling -> expecting str(file_path) by default.
        self._isDict = False

        # Lets ini the language messages
        vars.lang_list()
        #MSG, ERR, WARN = "", "", ""
        vars.lang_set(lang)

        # Lets be lazy
        self._print_verbose(vars.MSG["init"])
        self._load_any()
        self._print_verbose(vars.MSG["conf_read"])

        # Prepare things global?
        

    #
    #   Default functions
    #
    def _print_verbose(self, message, bOverWriteErrorMessage=False):
        """
        Prints message if bVerbose = True

        If sVerbosePrefix is passed, it prints: [sVerbosePrefix] message
        """
        if self.bVerbose or bOverWriteErrorMessage:
            if self._sVerbosePrefix == "":
                print(message)
            else:
                print(f"[{self._sVerbosePrefix}] {message}")
        elif bOverWriteErrorMessage:
            # This is basicly for errors
            if self._sVerbosePrefix == "":
                print(message, file=_sys.stderr)
            else:
                print(f"[{self._sVerbosePrefix}] {message}", file=_sys.stderr)

    def _flush(self):
        """This will flush all data from memory."""
        self.__data.quick = {}
        self.__data.raw = ""
        self.__data.comment_before = {}
        self.__data.comment_on_line = {}

    def __validate_data(self, content: dict) -> bool:
        """
        Verifies the structure of the configuration data.

        Strict: All top-level entries must be sections (dicts).

        Lazy: Top-level entries must be strings (well, single dict - ONLY :: var=val ;; no [Sections]).
        """
        if not content:
            return False

        if self.bStrict:
            # In strict mode, if we find a single non-dict item at the top level,
            # it means the user forgot a [Section] header.
            for key, value in content.items():
                if not isinstance(value, dict):
                    self._print_verbose(f"Strict Validation Error: Key '{key}' must be a section (dict).", bOverWriteErrorMessage=True)
                    return False
            return True
        else:
            # Lazy mode: Expecting a simple config
            # As long as it's a dict (variable = value), it's valid - which we already ensured by entering this function
            return True

    def __ResetConfig(self):
        """Restores the configuration file from the provided backup path."""
        self._print_verbose(vars.WARN['backup_start'])
        if self.sDefaultBackupConfig and _os.path.exists(self.sDefaultBackupConfig):
            try:
                # shutil.copy2 preserves metadata (like timestamps) 
                # shutil.copy just copies the content.
                _shutil.copy2(str(self.sDefaultBackupConfig), str(self.file_path))
                self._print_verbose(f"{vars.WARN['backup_end']} -> {self.file_path}")
                return True
            except Exception as e:
                # This is an error and thus most be forced
                self._print_verbose(f"{vars.ERR['backup_fail']} -> {self.file_path}:\n{e}", bOverWriteErrorMessage=True)
                return False
        else:
            # This is an error and thus most be forced
            self._print_verbose(f"{vars.ERR['backup_miss']} -> '{self.sDefaultBackupConfig}'.", bOverWriteErrorMessage=True)
            return False

    
    
    ############################################################################
    #
    #   LOAD DATA STUFF
    #
    ############################################################################

    def _load_any(self):
        """Lazy 'bootstrap' loader, this simply redirects the class-wide provided **class.file_path** to its optimized **load_* after some basic verifications**"""
        # Import Messages
        #global vars.MSG, vars.ERR, vars.WARN

        #
        #   Prepare file handling
        #   Check type instance, and call optimized functions accordingly
        #   We'll be using EITHER load_file (file) OR load_data (dict)
        #
        if isinstance(self.file_path, str):
            self._print_verbose(f"{vars.MSG['conf_load']}: 'str' ({self.file_path}).")
            self.load_file()
            return True
        elif isinstance(self.file_path, dict):
            self._isDict = True
            self._print_verbose(f"{vars.MSG['conf_load']} 'dict'.")
            # There is no instant save, if its dict/memory only!
            self.bInstantSave = False
            self.load_data()
            return True
        else:
            # Invalid data // should not be possible to reach
            if not self.sDefaultBackupConfig == "":
                return self.__ResetConfig()
            else:
                self._print_verbose(f"Invalid : {self.file_path}\n{vars.ERR["value"]}", bOverWriteErrorMessage=True)
                return False
            
    def load_data(self, data_overwrite:dict = {}):
        """
        Read/Import (new) settings from provided class.file_path as DICT. ***This does NOT allow for comments***!
        
        After minimal sanity check, flush any old memory and reading provided data.

        :param file_overwrite: Only used when importing, if empty uses already saved **class.file_path**,
        """
        # Import Messages
        #global vars.MSG, vars.ERR


        this_data:dict = {}
        if not data_overwrite == {}: 
            if self.__validate_data(data_overwrite):
                this_data=dict(data_overwrite)
            else:
                # valid dict, but empty
                self._print_verbose(vars.ERR["value"], bOverWriteErrorMessage=True)
                return False
        else:
            # It should already had been verified wether self.file_path is a dict or not... (from self._load_any())
            # However, PyLance is a brat and moans about this unless we double check/verify for dict.
            if isinstance(self.file_path, dict):
                if self.__validate_data(self.file_path):
                    this_data=self.file_path.copy()
                else:
                    # valid dict, but empty
                    self._print_verbose(vars.ERR['empty'], bOverWriteErrorMessage=True)
                    return False
            else:
                # This would actualy be very bad
                if not self.sDefaultBackupConfig == "":
                    if self.__ResetConfig():
                        self.load_data()
                        return True
                    else:
                        return FileNotFoundError
                else:
                    self._print_verbose(vars.MSG["invalid_data"], bOverWriteErrorMessage=True)
                    #self._print_verbose(f"Invalid : {self.file_path}\n{vars.ERR["value"]}", bOverWriteErrorMessage=True)
                    return False

        # Ok, basic sanity seems fine
        # Lets reset data storage, wether its first read or import/overwrite
        self._flush()

        # Lets try to aactualy load the data
        try:
            self.__data.quick = this_data
            self._print_verbose(f"{vars.MSG['conf_read']}")
            return True
        except ImportError: 
            self._print_verbose(vars.ERR["import"], bOverWriteErrorMessage=True)
            raise UnboundLocalError(this_data)
        except Exception as e:
            self._print_verbose(f"{vars.ERR['generic']}: {e}", bOverWriteErrorMessage=True)
            raise Exception(this_data)
    
    def load_file(self, file_overwrite: str=""):
        """
        Read/Import (new) settings from provided class.file_path as STR

        After minimal sanity check, flush any old memory and reading provided file.
        
        :param file_overwrite: Only used when importing, if empty uses already saved **class.file_path**,
        """
        if file_overwrite: 
            this_file=str(file_overwrite)
        else:
            this_file=str(self.file_path)

        # Import Messages
        #global vars.MSG, vars.ERR, vars.WARN
        
        # Import variables
        bForcedCommentStyle = self.bForcedCommentStyle
        SEP = self._sep
        global _comments_multi_end
        global _comments_multi_start
        isMultiLine = None # Either "None", or found index of list
        

        # Lets verify file exists, or at least a default config
        if not _os.path.exists(str(this_file)):
            self._print_verbose(f"{vars.MSG["file_not_found"]}: {this_file}")
            if not self.sDefaultBackupConfig == "":
                # Message is handled from "reset" internaly"
                if not self.__ResetConfig():
                    # Reset failed, we need to abort :(
                    raise FileNotFoundError
            else:
                # No default config provided, abort...
                raise FileNotFoundError

        # Seems fine so far...
        # Lets prepare some little helper functions here to ease readability
        # Yes, most of this could be wrote directly in code, i still prefer this approach


        # Lets flush any old data (in case of import) and try to read the file
        self._flush()
        try:
            with open(this_file, 'r', encoding=self.encoding) as f:
                current_section = ""
                last_section = ""
                # We'll be preparing ordered lists to save comments in a 2nd loop (outside of with)
                order_sections = []
                order_variables = []
                tmp_list = []

                # I'd like to save all of "f" in self.__data.raw
                # TODO: While we wont work with that right now, this might be nice for an "undo" feature
                self.__data.raw = str(f)

                for line in f:
                    clean_line = line.strip()
                    # This is what we'll parse afterwards.
                    # Now, lets just fill this chronologicly
                    self.__data.lines.append(clean_line)

                    # Lets prepare comment buffer
                    var, val = "", ""
                    if LoadFile._isComment(clean_line, bForcedCommentStyle=bForcedCommentStyle) or clean_line == "":
                        tmp_list.append(clean_line)
                        continue
                    
                    # This could be enough, but since we're parsing anyway line by line..
                    # Lets assign any found data to self.__data.quick as well
                    elif LoadFile._isSection(clean_line):
                        last_section = current_section
                        current_section = LoadFile._getSection(clean_line)
                        if not tmp_list == []:
                            # Has comments
                            if not current_section in self.__data.comment_before:
                                self.__data.comment_before[current_section] = []
                            self.__data.comment_before[current_section] = tmp_list
                            # Data is saved, lets reset container
                            tmp_list = []
                        if not current_section in order_sections:
                            order_sections.append(current_section)
                        continue

                    # Hope for values...
                    elif LoadFile._isValue(clean_line, self._sep):
                        # Lets make sure, we're only getting the data
                        if LoadFile._hasOnLineComment(clean_line, bForcedCommentStyle=bForcedCommentStyle, SEP=SEP):
                            tmp, com = "", ""
                            tmp, com = LoadFile._SplitCommentAfterValue(clean_line)
                            var, val = LoadFile._SplitVarValue(tmp, SEP=self._sep)

                            # Since we're at it, lets also save the "on line comment"
                            self.__data.comment_on_line[f"{current_section}.{var}"] = [com]
                        else:
                            var, val = LoadFile._SplitVarValue(clean_line, SEP=self._sep)

                        # Save data
                        if self.bStrict or current_section == "":
                            if current_section not in self.__data.quick:
                                self.__data.quick[current_section] = {}
                            self.__data.quick[current_section][var] = val
                        else:
                            self.__data.quick[var] = val

                        # Prepare line entry for comments_before
                        if not tmp_list == []:
                            # Has comments - sicne last var/section occourence/change
                            if not self.bStrict or current_section == "":
                                self.__data.comment_before[var] = []
                                self.__data.comment_before[var] = tmp_list
                            else:
                                self.__data.comment_before[f"{current_section}.{var}"] = []
                                self.__data.comment_before[f"{current_section}.{var}"] = tmp_list
                            # Reset list
                            tmp_list = []
                        
                        ##### We're at the bottom of checks anyway, so continue is not needed...
                        # Since we added multi-line-comments, and this was a proper value, we do need to....
                        continue
                    else:
                        # If we reach this point, the line was  unhandled....
                        # So we're doing the latest addition of supporting multi-line-comment (allthough that usualy isnt the case for regular ini files)
                        #self._print_verbose(f"Unhandled line (does this work???): {clean_line}",bOverWriteErrorMessage=True)
                        if isMultiLine:
                            # Its "open" (aka a not-None value is set), expecting an integer
                            # Since its "open", we can add the current line EITHER way...
                            # However, since this is expected to be a comment, we do not trim whitespace
                            if not self.bStrict or current_section == "":
                                self.__data.comment_before[var] = []
                                self.__data.comment_before[var] = line
                            else:
                                self.__data.comment_before[f"{current_section}.{var}"] = []
                                self.__data.comment_before[f"{current_section}.{var}"] = line
                            
                            # Lets check wether we can close/end the multi line comment or not
                            if vars.comments_multi_end[isMultiLine] in clean_line:
                                # We have found the closing tag
                                isMultiLine = None
                        else:
                            # At this point, it must be either an opening for a multi line, 
                            # or somethign different entirely...
                            i = 0
                            for mli in vars.comments_multi_start:
                                if clean_line.startswith(mli) or mli in clean_line:
                                    # It is the start of a multi line comment
                                    # so lets get the index
                                    while i < len(vars.comments_multi_start):
                                        if mli != vars.comments_multi_start[i]:
                                            print(f"DEBUG:: {i} is small than {len(vars.comments_multi_start)}")
                                            i += 1
                                        else:
                                            # its the right one
                                            isMultiLine = i
                                            break
                                    print(f"DEBUG:: found mult line maker: {mli} at index: {i} --- sadly this isnt even shown yet")

                                    # Lets add it to the comments:
                                    if not self.bStrict or current_section == "":
                                        self.__data.comment_before[var] = []
                                        self.__data.comment_before[var] = line
                                    else:
                                        self.__data.comment_before[f"{current_section}.{var}"] = []
                                        self.__data.comment_before[f"{current_section}.{var}"] = line

                                    # Value is added, lets...
                                    continue
                            # We have not found a multiline comment indicator
                            # so basicly, the current line remains unhandled...
                            self._print_verbose(f"Unhandled line - last else/most inner: {line}", bOverWriteErrorMessage=True)
                        # If we reach this point, the current line still isnt handled...
                        # lets print out a warning / information
                        self._print_verbose(f"Unhandled line - outside: {line}", bOverWriteErrorMessage=True)
                    # At this point, i actualy would expect 3 error messages to appear
                    # this is at the same "height" (indent) as the top IF and following "ELIF"'s, hence, if none "grip", we should see this
                    self._print_verbose(f"Unhandled line (outside if blocks): {clean_line}",bOverWriteErrorMessage=True)


        except Exception as e:
            self._print_verbose(f"Error loading file: {e}")


    def export(self, file_path: str="", bDict=False):
        """
        Exports configuration

        :param file_path: Will save new file_path
        :param bDict: If True will return a dict, but all comments will get lost!
        """
        if bDict:
            # False by default, so if its true, we can stop here
            return self.__data.quick #.values
        elif file_path != "":
            # Double check if something was passed
            # Will be handled as path/file
            self.save(file_export=file_path)
        else:
            # bDict is still False and nothing was passed as file_path
            raise FileNotFoundError()


    def save(self, file_export=None):
        """
        Save configuration file
        
        :param file_overwrite: is for internal use/export, please use '<your-instance-name>.export(filename)' instead
        """
        if file_export: 
            this_file = str(file_export)
        else:
            this_file = str(self.file_path)
        
        if not self.file_path and not file_export:
            self._print_verbose("Save failed: No file path provided for memory-only mode.")
            return False
        
        try:
            with open(this_file, 'w', encoding=self.encoding) as f:
                # We iterate through the quick dict. 
                # Python 3.7+ preserves insertion order, matching your load_file sequence.
                for key, content in self.__data.quick.items():
                    
                    # SCENARIO 1: Nested Structure (Sections)
                    # This triggers if bStrict was True OR current_section was ""
                    if isinstance(content, dict):
                        section_name = key
                        
                        # 1. Write 'comment_before' for the Section Header
                        if section_name in self.__data.comment_before:
                            for comment in self.__data.comment_before[section_name]:
                                f.write(comment + "\n")
                        
                        # 2. Write the Section Header
                        f.write(f"[{section_name}]\n")
                        
                        # 3. Write the Variables within that section
                        for var, val_list in content.items():
                            if isinstance(val_list, str) or isinstance(val_list, bool) or isinstance(val_list, int) or isinstance(val_list, float) :
                                val = val_list
                            elif isinstance(val_list, list):
                                val = val_list[0] if val_list else ""
                            else:
                                self._print_verbose(f"val_list = {type(val_list)}", True)
                                raise TypeError
                            
                            # The key for comments in load_file was "section.variable"
                            comp_key = f"{section_name}.{var}"
                            
                            # Handle comment_before (Nested)
                            if comp_key in self.__data.comment_before:
                                for comment in self.__data.comment_before[comp_key]:
                                    f.write(comment + "\n")
                            
                            # Handle comment_on_line
                            on_line_comment = ""
                            if comp_key in self.__data.comment_on_line:
                                # Taking the first comment in the list as per load_file
                                on_line_comment = " #" + self.__data.comment_on_line[comp_key][0]
                            
                            f.write(f"{var}{self._sep}{val}{on_line_comment}\n")
                        
                        # Add a newline between sections
                        f.write("\n")

                    # SCENARIO 2: Flat Structure (Root level)
                    # This triggers if bStrict was False AND current_section was NOT ""
                    else:
                        # In this case, 'key' is the variable name, 'content' is [value]
                        var = key
                        val = content[0] if content else ""
                        
                        # Handle comment_before (Flat - no section prefix)
                        if var in self.__data.comment_before:
                            for comment in self.__data.comment_before[var]:
                                f.write(comment + "\n")
                        
                        # Handle comment_on_line (Checking for the flat key just in case)
                        on_line_comment = ""
                        if var in self.__data.comment_on_line:
                            on_line_comment = " #" + self.__data.comment_on_line[var][0]
                        
                        f.write(f"{var}{self._sep}{val}{on_line_comment}\n")

            self._print_verbose(f"Saved to: {this_file}")
            return True
        except Exception as e:
            self._print_verbose(f"Error saving file: {e}")
            return False

    def get(self, section:str, variable:str):
        """Retrieve a value from a specific section its variable"""
        if self.bStrict:
            if section in self.__data.quick:
                try:
                    return self.__data.quick[section][variable]
                except Exception as e:
                    self._print_verbose(f"KEY; get: DICT -> __data.quick --> {self.__data.quick} ;;; sec: {section}, var: {variable}")
                    raise Exception
                #except KeyError:        raise KeyError
                #except IndexError:      raise IndexError
                #except LookupError:     raise LookupError
            else:
                self._print_verbose(f"No '{section}' or '{variable}' found in '{self.file_path}'...", bOverWriteErrorMessage=True)
        else:
            self.get_simple(variable)

    def get_simple(self, variable: str):
        """Retrieve value for variable, if **bStrict=False**"""
        if variable in self.__data.quick:
            try:
                return self.__data.quick[variable]
            except Exception as e:
                self._print_verbose(f"KEY; get_simple: DICT -> __data.quick --> {self.__data.quick} ;;; var: {variable}")
                raise Exception
            #except KeyError:        raise KeyError
            #except IndexError:      raise IndexError
            #except LookupError:     raise LookupError
        else:
            self._print_verbose(f"No '{variable}' found in '{self.file_path}'...", bOverWriteErrorMessage=True)
    
    def set(self, section:str, variable: str, value) -> bool:
        """Set a value and optionally trigger an instant save."""
        if self.bStrict:
            try:
                self.__data.quick[section][variable] = value
                if self.bInstantSave and self.file_path:
                    self.save()
                return True
            except Exception as e:
                self._print_verbose(f"KEY; get: DICT -> __data.quick --> {self.__data.quick} ;;; sec: {section}, var: {variable}, val: {value}")
                raise Exception
            #except KeyError:        raise KeyError
            #except IndexError:      raise IndexError
            #except LookupError:     raise LookupError
            #except Exception as e:
            #    self._print_verbose(e, bOverWriteErrorMessage=True)
            #    return False
        else:
            return self.set_simple(variable, value)

    def set_simple(self, variable: str, value) -> bool:
        """"""
        try:
            self.__data.quick[variable] = value
            if self.bInstantSave and self.file_path:
                self.save()
            return True
        except KeyError:        raise KeyError
        except IndexError:      raise IndexError
        except LookupError:     raise LookupError
        except Exception as e:
            self._print_verbose(e, bOverWriteErrorMessage=True)
            return False

    def _get_comments(self):
        return self.__data.comment_before #.items()
    def _get_quick(self):
        return self.__data.quick

    def list_sections(self, bString=False) -> vars.ListOrString:
        """
        Returns a list of available sections.
        
        :param bString: This will return a string from the *"list, of, sections, in, your, config"*
        """
        sections = list(self.__data.quick.keys())
        if bString:
            return str(", ".join(sections))
        else:
            return sections

    def list_variables(self, section: str, bString=False) -> vars.ListOrString:
        """Returns a list of variables """
        vars = list(self.__data.quick[section].keys())
        if bString:
            return ", ".join(vars)
        else:
            return vars

    def list_variables_simple(self, bString=False) -> vars.ListOrString:
        """Returns a list of variables for a config without [Sections]"""
        vars = list(self.__data.quick.keys())
        if bString:
            return ", ".join(vars)
        else:
            return vars
        
    def dump(self):
        """
        Dump sections and values on screen.
        
        This is practical to test/verify for a valid config file that you want to ship with your project.
        """
        if self.bStrict:
            # This expects one or more [Sections]
            for sec in self.list_sections():
                print(f"[{sec}]")
                for entry in self.list_variables(sec):
                    print(f"    {entry}{self._sep}{self.get(sec, entry)}")
        else:
            # Its a lazy config...
            # So everything is just: variable = value // var = "val"
            for entry in self.list_variables_simple():
                print(f"    {entry}{self._sep}{self.get_simple(entry)}")
        