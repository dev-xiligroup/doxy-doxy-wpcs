# doxy-doxy-wpcs
Very first example of User settings for doxydoxygen 2021 sublime plugin to try to implement comments according WPCS in WP dev source.
and to avoid “red” lines via sniffer phpcs + wpcs in Sublime Text 3 when adding comments…

copy the content of json in User part settings of doxydoxygen (menu preferences, Package settings)

## Sublime Text 3 : python script to comment WP filters

v 210426 - with settings in ~/Library/Application Support/Sublime Text 3/Packages/User named:
- CommentFilters.sublime.settings (editable via Sublime preferences)
User can now adapt the contents of labels and descriptions. 

v 210423 - very first version
The Script named comment_filters.py to upload in
~/Library/Application Support/Sublime Text 3/Packages/User
contains command “comment_filters” to add a detailled multilines comment (according PhpCS+WPCS) above :
- apply_filters
- do_action

The command can be called via key bindings.

As exercises and tests, some answers to these questions are solved:
- what is view, region and point in sublime API ?
- how to create an empty line above the target line ?
- basic features in Python
- how to keep indentation of the target line ?
- how to do regex finding in the target line using Python re class ?
- how to display char $ in insert_snippet command with escaping ?
- how to pass arguments in class ?