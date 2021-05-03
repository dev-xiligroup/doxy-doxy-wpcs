# Sublime Text 3 : python script to comment WP filters and function calls…

This package is a new big upgrade of Comment Filters package

## history
**v 210503** - New name, New source’s structure

To introduce modules and classes (*and to compare with previous code*), the new name of plugin is CommentCalls.

- The previous source is split in (short) modules (1+6).
- For commenting “anonymous” functions: rules, context and key can be multiple as visible in ‘CommentCalls.sublime-settings’. To apply rules, the first efficient in list is chosen. Inside a rule, all the keys must applicable !
- Soon more examples in docs. 

## As exercises and tests, some answers to these questions are solved:
- what is view, region and point in sublime API ?
- how to create an empty line above the target line ?
- basic features in Python
- how to keep indentation of the target line ?
- how to do regex finding in the target line using Python re class ?
- how to display char $ in insert_snippet command with escaping ?
- how to pass arguments in class ?
- how to manage dictionary and settings file ?
- how to add a settings sub-menu for preferences in package (Main.sublime-menu) ?
- create package info visible in packages list command with metadata.json
- how to create a package and avoid orphan deletion !
- how to format string and date,
- how to install/insert pylint with sublimelinter,
### SINCE OOP sources in sublime text 3 python’s context :
- how to split a script in efficient modules
- how to import (part or full) modules (and refresh during development time)
- …
