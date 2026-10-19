""""
    This file provides tools during the loading file procedure.

    Basicly: bools and splits

    © 2026 by Simon Arjuna Erat, Switzerland
"""
#
#   Imports
#
import sys as _sys
from . import vars

#
#   Functions
#
def __hasQuotes(this_line:str) -> bool:
    """Simply check wether quotes were found, and wether it has at least 2 - open & close - ones"""
    found = 0           # Counter for the loop
    if not this_line:
        # Line was empty
        return False
    
    # Start parsing
    for q in vars.quotes:
        if this_line.count(q) == 2:
            # Its a valid count value
            return True

    # if we reach here...
    # Either only "single quotes" (like this stupid example: i'm fine) were used, or no quotes at all
    return False

def __getValidQuoteChar(this_line:str) -> str:
    """
    Expects a line that DOES contain quotes
    
    Returns indicator char for valid quotes
    """
    # Yes this is slightly similar to __hasQuotes(), 
    # but we return something different
    for q in vars.quotes:
        if 2 == this_line.count(q):
            # seems valid
            return q
    # while it should not reach here
    # lets return an empty string
    return ""

def __getPostValueComment(this_line:str):
    """Returns everything AFTER value, aka cut before comment indicator"""
    if __hasQuotes(this_line):
        # Need to get position of closing quote
        # then "split/cut there"
        quote = __getValidQuoteChar(this_line)
        # Expecting to split at each occourence of a quote
        posQ = this_line.find(quote, 3) #split(quote)[2]
        tmp = this_line[posQ + 1]
        work_line = tmp.strip()
    else:
        # No (valid-) quotes found, just split at found vars.comments[]
        work_line = this_line.strip()

    # Now we need to split at FIRST comment indicator
    posC = len(work_line)
    posC_new = 0
    for com in vars.comments:
        # Lets ensure we only get the pos from the earliest find within the string
        posC_new = work_line.find(com)

        if posC_new != -1 and posC_new < posC:
            posC = posC_new

    if posC == len(work_line):
        return ""
    else:
        return work_line[posC + 1].strip()


def _isComment(this_line: str, bForcedCommentStyle: vars.NoneOrString = None) -> bool:
    """Is a comment?"""
    ret = False
    # First, lets check for forced comment
    if bForcedCommentStyle:
        # Its not None
        if this_line.startswith(bForcedCommentStyle):
            # Yes, it does start with a forced comment style
            ret = True

    for com in vars.comments:
        if str(this_line).startswith(com):
            # Lets double check if it was a forced one,
            # and/or act with the the current found one differs from the forced one
            if bForcedCommentStyle and com != bForcedCommentStyle:
                # We have a forced comment style, but the used/found comment indicator differs
                print(f"{vars.WARN["bForcedCommentStyle_differs"]}: '{com}' != bForcedCommentStyle='{bForcedCommentStyle}'", file=_sys.stderr)
            ret = True
            break
    # No valid comment was found    
    return ret

def _hasOnLineComment(this_line: str, bForcedCommentStyle: vars.NoneOrString = None, SEP=vars.DEFAULT_SEP) -> bool:
    """
    Checks whether the line has a comment after the value, that is NOT inside quotes.

    This may only be checked AFTER _isComment(line).

    This function should only return True/False quickly
    """
    # Reminder: Establish a priority list
    # 1. if no entries of vars.comments[] was found -> False
    # 2. if any quotes were found, only check past the closing quote

    #global bForcedCommentStyle  # this will be assigned to "sep" (lower case) -> comment indicator
    #global SEP                  # this is the var = val indicator, SEP (capital letter)

    # Expect an comment separator
    sep = None
    if not bForcedCommentStyle:
        for com in vars.comments: 
            if com in this_line:
                # TODO possible issue -> stupid example:  'var=val // we have #3 problems with this value ; maybe more'
                sep = com
                # The above said, doesnt really matter wether we "overwrite" sep, or break on first find...
                break
    else:
        # Only 1 "style" of comments is allowed
        if bForcedCommentStyle in this_line:
            sep = bForcedCommentStyle

    if not sep:
        # No valid comment indicator found
        return False
        #sep = vars.comments[0]  # default to '#'

    if __hasQuotes(this_line):
        if not __getPostValueComment(this_line) == "":
            # Its not empty, so we have a comment there
            # Now writing this... this seems like a "double check"
            # at least we'll be calling the __getPostValueComment twice.. 
            #here for the check, and then afterwards for the actual use...
            return True


    if not SEP in this_line:
        return False
    
    # Find the separator
    sep_idx = this_line.find(sep)
    if sep_idx == -1:
        # Basicly: its at the start
        return False
    
    # Extract the part after the separator
    comment_part = this_line[sep_idx + 1:].strip()
    
    # If the part after separator is only whitespace, it's not a comment
    if not comment_part:
        return False
    
    # Check if the comment character appears inside double or single quotes
    # Find the first closing quote for the opening quote
    quote = None
    found = 0           # Counter for the loop
    hasQuotes = None
    for q in vars.quotes:
        if q in this_line:
            found += 1
            hasQuotes = True
            quote = q
    if found >= 2:
        # Both quote types were found... how to handle?
        hasQuotes = True
    elif not quote:
        # No quotes found, simple handling
        hasQuotes = False

    #
    #   Lets handle accordingly
    #
    if hasQuotes:
        # TODO
        pass
    else:
        # No quotes were found
        # Comment indicator WAS found (or we would have aported several lines above)
        # So, since comment indicator found, but line has no quotes -> True
        return True

    quote_start = this_line.find("'", sep_idx)
    quote_end = this_line.find("'", quote_start + 1) if quote_start != -1 else -1
    if 0 < sep_idx < quote_start < quote_end and quote_end < len(this_line):
        # Comment is inside quotes, skip it
        pass
    else:
        # Find double quotes
        if quote_start == -1:
            quote_start = this_line.find('"', sep_idx)
            quote_end = this_line.find('"', quote_start + 1) if quote_start != -1 else -1
        
        if 0 < sep_idx < quote_start < quote_end and quote_end < len(this_line):
            # Comment is inside quotes, skip it
            pass
        else:
            # Check if the comment character appears after the value
            for com in vars.comments:
                if sep in this_line[sep_idx + 1:].strip():
                    return True
    
    return False

def _SplitCommentAfterValue(this_line: str, comment_char:str = "#") -> vars.StringAndString:
    """"
    If 'this_line' has a comment after value, it returns: value, comment

    :param this_line: Pass string to function
    :param vars.StringAndString: Retrieve as: "line, comment = _SplitCommentAfterValue(line_current)"
    """
    parts = this_line.split(comment_char, 1)
    return parts[0].strip(), parts[1].strip()

def _isSection(this_line: str) -> bool:
    """Returns True if 'this_line' is a section: '[something]'"""
    if this_line.startswith('[') and this_line.endswith(']'):
        return True
    else:
        return False

def _getSection(this_line: str) -> str:
    """Returns only 'section' name"""
    return this_line[1:-1].strip()

def _isValue(this_line: str, SEP="=") -> bool:
    """This checks wether its a variable = value , while NOT being within a comment.
    
    Allthough a comment should not get passed here, we just want to ensure it.
    """
    for com in vars.comments:
        if this_line.startswith(com):
            # Line started with a comment, lets abort
            return False
    if SEP in this_line:
        # Seperator found
        return True
    return False

def _SplitVarValue(this_line: str, SEP:str = "=") -> vars.StringAndString:
    """
    This expects 'this_line' to be already 'cleaned' from any possible 'on line comments'.
    
    Returns: Variable/Key, Value
    """
    parts = this_line.split(SEP, 1)
    return parts[0].strip(), parts[1].strip()


