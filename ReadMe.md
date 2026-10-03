# INI Comments
This is a ini-file handler that preserves comments.

For various projects of mine, I prefer to provide comments within an ini file for others to know their meanings, or other options.

While configParser is nice, it always removed any/all comments from the file, so this project solves that issue.


### Features:
- Supports: "#", ";" and "//" as line comments
- Preserve comments
- Handles "line comment" and "comments behind values"
- Custom "separator" (default: "=")
- Allows toggle between: "instant save" or "on purpose"
- May handle "lazy" (bStrict=False) ini files, that do not have any "[Section]"s (this is required for the saving, wether manual or automatic)
- Allows for fallback/non-existing config 


# Usage:
How to handle this class:

## Available commands:
- my_ini.export(args)
- my_ini.get(args)
- my_ini.get_simple(args)
- my_ini.list_sections()
- my_ini.list_variables(args)
- my_ini.load_data()
- my_ini.load_file()
- my_ini.save()
- my_ini.set(args)
- my_ini.set_simple(args)


### Import:
```python
import inicomments
```

### Initialize:
```python
my_ini = inicomments.handler("/path/to/file")
```

### Working with values:
```python
# Get value:
current_value = my_ini.get("SectionName", "VariableName")
print(current_value)

# Set Value:
my_ini.set("SectionName", "VariableName", "NewValue")
```

### Special Handling:
If you have ``bInstantSave=False`` you simply call: ``my_ini.save()`` at whatever point you want/need to save the file.



# Example File:
Here is an example of a - *very chaotic, but still work-able* - ini file:

```
# Most used comment
; But you can apply any comment style
// that fits your project

[section]
variable = some value
someting = with a comment // like this
ofCourse = this would ; work as well
sooooo = "would this ; if you" ; apply quotes

```