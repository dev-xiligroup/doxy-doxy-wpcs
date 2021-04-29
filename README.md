# doxy-doxy-wpcs
Very first example of User settings for doxydoxygen 2021 sublime plugin to try to implement comments according WPCS in WP dev source.
and to avoid “red” lines via sniffer phpcs + wpcs in Sublime Text 3 when adding comments…

copy the content of json in User part settings of doxydoxygen (menu preferences, Package settings)

## Sublime Text 3 : python script to comment WP filters and function calls…

**v 210428** - some major changes:
- script is now in a folder uploadable in folder packages (don’t forget to add ‘Comment Filters’ in Package Control.sublime-settings - list : installed_packages. With this config, Main menu includes Preferences Settings from this folder !
- In addition to apply_filters and do_action, script is now able to comment other function calls. ‘anonymous’ in User settings file.
- some improvements and better key detection (array)
- …

<img src=“../main/docs/CommentedFunctionCall.png title=“Commented Function Call” alt=“Screenshot Commented Function Call”>

**v 210426** - with settings in ~/Library/Application Support/Sublime Text 3/Packages/User named:
- CommentFilters.sublime.settings (editable via Sublime preferences)
User can now adapt the contents of labels and descriptions. 

**v 210423** - very first version
The Script named comment_filters.py to upload in
~/Library/Application Support/Sublime Text 3/Packages/User
contains command “comment_filters” to add a detailled multilines comment (according PhpCS+WPCS) above :
- apply_filters
- do_action

![Screenshot of WP php](../main/docs/CommentedApply_Filters.png)

The command can be called via key bindings.

As exercises and tests, some answers to these questions are solved:
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