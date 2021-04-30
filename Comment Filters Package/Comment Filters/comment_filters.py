"""Comment Filters - Writing function calls comments according WPCS."""


import re
from datetime import datetime
import sublime
import sublime_plugin


__copyright__ = "Copyright © 2021 Michel dev.xiligroup"
__license__ = "GNU General Public License v2 or later"

# exercises and tests in python to comment filters
#  inside functions in WP - 20210422 - xili
# implemented cases apply_filters and do_action
# v 210426 - settings file added
# v 210423
# v 210427 - add anonym function call
# v 210430 - some improvements and pylint control - add format in since
'''
    # examples of key bindings when cursor is in target line containing functions

    { "keys": ["command+o"],"command": "comment_filters", "args": {
      "function_name": "apply_filters"  }}
     ,
     { "keys": ["ctrl+o"],"command": "comment_filters", "args": {
     "function_name": "do_action"  }
     ,
     { "keys": ["ctrl+i"],"command": "comment_filters","args": {
      "function_prefix": "_", "@since":"biding version"  }}
'''


class CommentFiltersCommand(sublime_plugin.TextCommand):

    """
    Comment Filters.

    Writing function calls comments according WPCS
    command : comment_filters
    """

    def run(self, edit, **args):
        """
        Comment Filters run.

        Args:
            edit (TYPE): Description
            **args: Seems to be a wildcard to make all other params available w/o error message
        """
        def goto_start_previous():
            # goto start of previous line of the current cursor where is function to comment
            for sel in self.view.sel():
                line = self.view.rowcol(sel.begin())[0]
                self.view.insert(edit, self.view.text_point(line, 0), "\n")
            self.view.run_command("move", {"by": "lines", "extend": False, "forward": False})
        # print("start python")

        my_settings_name = 'CommentFilters.sublime-settings'
        my_settings = sublime.load_settings(my_settings_name)
        # list of dicts
        # create default one
        default_dict = {}
        settings_default = 0
        if my_settings:  # file exists
            dict_apply_filters = my_settings.get('apply_filters')
            dict_do_action = my_settings.get('do_action')
            dict_anonymous = my_settings.get('anonymous')
            dict_since = my_settings.get('@since')
            dict_dev_id = my_settings.get('@by')
            # other function
        if not my_settings or not dict_apply_filters:
            default_dict['apply_filters'] = {
                'name_of_key': {'index': '[key]', 'string': ''},
                'name_of_called_filters': '[name of the called filters ].',
                'result_desc': {'index': '[key of result description]', 'string': '[result description]'},
                'first_param_desc': 'The original (non filtered) [description].',
                'param_desc': {'index': '[key description]', 'string': '[description]'}
            }
            dict_apply_filters = default_dict['apply_filters']
            my_settings.set('apply_filters', dict_apply_filters)
            settings_default = 1
        # do_action
        if not my_settings or not dict_do_action:
            default_dict['do_action'] = {
                'name_of_called_actions': {'index': '[key]', 'first': '[name of called actions].', 'string': '!'},
                'arg_desc': {'index': '[key of argument]', 'string': '[description of argument passed to the callback].'}
            }
            dict_do_action = default_dict['do_action']
            my_settings.set('do_action', dict_do_action)
            settings_default = settings_default + 10
        # anonymous
        if not my_settings or not dict_anonymous:
            default_dict['anonymous'] = {
                'key_or_param': {'index': '[key name] of ', 'string': ''},
                'name_key_or_string': {'index': '[key name].', 'string': '[the string].'},
                'first_param_desc': 'The first param [description].',
                'param_desc': {'index': '[key description]', 'string': '[description]'}
            }
            dict_anonymous = default_dict['anonymous']
            my_settings.set('anonymous', dict_anonymous)
            settings_default = settings_default + 100
        # other function
        #
        if settings_default:
            my_settings.set('updated', 'updated to default: ' + str(settings_default))
            sublime.save_settings(my_settings_name)  # save default values
        # print("start action")
        posi = self.view.sel()[0].b
        # current line in "region"
        selection = self.view.full_line(posi)
        row, col = self.view.rowcol(selection.begin())
        # get indents
        indent_region = self.view.find('^\t+', self.view.text_point(row, 0))
        indent_line = self.view.substr(indent_region)
        # current line in string
        cur_line = self.view.substr(selection)

        # regex limited to the line
        equal_pos = re.search(" = ", cur_line)
        # if ( equal_pos ) :
        #   colequal = equal_pos.start()
        #   give region of function name after equal with sublime method - not used
        #   funcname = self.view.word( self.view.text_point(row, colequal + 4) )
        if dict_since:  # from settings
            since = dict_since
        else:
            ispresent = '@since' in args  # from args in key binding
            if ispresent:
                since = args['@since']
            else:
                since = '[my first version]'
        now = datetime.now()  # used in since if format
        # developer id
        if dict_dev_id:  # from settings
            dev_id = dict_dev_id
        else:
            ispresent = '@by' in args  # from args in key binding
            if ispresent:
                dev_id = args['@by']
        # target function
        ispresent = 'function_name' in args
        if ispresent:
            searchfuncname = args['function_name']  # send via parameters args
        else:
            searchfuncname_w = self.view.word(posi)
            searchfuncname = self.view.substr(searchfuncname_w)
        x = re.search(searchfuncname, cur_line)
        if x and equal_pos and searchfuncname == 'apply_filters':

            # formatted for searchfuncname
            apply_params = re.findall(r"(\$\w+|\'\w+')", cur_line)

            para = indent_line + "/**\n"
            para1 = indent_line + " * Applying the filters\n" + indent_line + " *\n" + indent_line + " * @since " + since.format(now = now, dev = dev_id) + "\n" + indent_line + " *\n"

            para3 = indent_line + " */"
            # goto start of previous line
            goto_start_previous()
            self.view.run_command("insert_snippet", {"contents": para})
            self.view.run_command("insert_snippet", {"contents": para1})
            fi = 0
            linesp = []
            l = 0
            for param in apply_params:
                # detect name
                if param == param.replace("$", r"\$"):
                    x0 = re.search(param, cur_line)
                    xix = re.search(r"\[" + param + r"\]", cur_line)
                    if xix:
                        indice = 'index'
                    else:
                        indice = 'string'
                    if x0:
                        if x0.start() < x.start():
                            linep = indent_line + " * @param " + param + " " + dict_apply_filters['name_of_key'][indice] + ".\n"
                        else:
                            # param contains the quotes
                            linep = indent_line + " * @param " + param + " " + dict_apply_filters['name_of_called_filters'] + "\n"
                else:
                    the_param = param.replace("$", r"\$")
                    only_param = "(" + the_param + r"[ ,\[])"
                    x1 = re.search(only_param, cur_line)
                    xix = re.search(r"\[\s" + param.replace("$", r"\$") + r"\s\]", cur_line)
                    if xix:
                        indice = 'index'
                    else:
                        indice = 'string'
                    if x1:
                        if x1.start() < x.start():
                            linep = indent_line + " * @var <type> " + param.replace("$", r"\$") + " " + dict_apply_filters['result_desc'][indice] + ".\n"
                        else:
                            fi = fi + 1
                            if fi == 1:
                                linep = indent_line + " * @param <type> " + param.replace("$", r"\$") + " " + dict_apply_filters['first_param_desc'] + "\n"
                            else:
                                linep = indent_line + " * @param <type> " + param.replace("$", r"\$") + " " + dict_apply_filters['param_desc'][indice] + "\n"
                if indice == 'index':
                    # modify l-1 because previous is an array
                    linel = linesp[l - 1]
                    linesp[l - 1] = linel.replace("<type>", "array")
                # list of lines
                linesp.append(linep)
                l = l + 1
            for linep in linesp:
                self.view.run_command("insert_snippet", {"contents": linep})
            # end of comment
            self.view.run_command("insert_snippet", {"contents": para3})
        # end apply_filters
        elif not equal_pos and x and searchfuncname == 'do_action':
            para = indent_line + "/**\n"
            para1 = indent_line + " * Fires [to allow a plugin to do a description]?\n" + indent_line + " *\n" + indent_line + " * @since " + since.format(now = now, dev = dev_id) + "\n" + indent_line + " *\n"
            para3 = indent_line + " */"
            # goto start of previous line
            goto_start_previous()
            self.view.run_command("insert_snippet", {"contents": para + para1})
            apply_params = re.findall(r"(\$\w+|\'\w+')", cur_line)
            fi = 0
            linesp = []
            l = 0
            for param in apply_params:
                if param == param.replace("$", r"\$"):
                    x0 = re.search(param, cur_line)
                    xix = re.search(r"\[" + param + r"\]", cur_line)
                    if xix:
                        indice = 'index'
                    else:
                        fi = fi + 1
                        if fi == 1:
                            indice = 'first'  # detect name of actions
                        else:
                            indice = 'string'
                    linep = indent_line + " * @param " + param + " " + dict_do_action['name_of_called_actions'][indice] + "\n"
                else:
                    xix = re.search(r"\[\s" + param.replace("$", r"\$") + r"\s\]", cur_line)
                    if xix:
                        indice = 'index'
                    else:
                        indice = 'string'
                    linep = indent_line + " * @param <type> " + param.replace("$", r"\$") + " " + dict_do_action['arg_desc'][indice] + "\n"
                if indice == 'index':
                    # modify l-1 because previous is an array
                    linel = linesp[l - 1]
                    linesp[l - 1] = linel.replace("<type>", "array")
                # list of lines
                linesp.append(linep)
                l = l + 1
            for linep in linesp:
                self.view.run_command("insert_snippet", {"contents": linep})
            self.view.run_command("insert_snippet", {"contents": para3})
        # end do_action
        else:
            # print("anonym")
            # print( "anonym = " + searchfuncname )
            # two cases with or w/ equal_pos
            searchfuncname_w = self.view.word(posi)  # via word don't contain $ !
            searchfuncname = self.view.substr(searchfuncname_w)
            print(searchfuncname)
            ispresent = 'function_prefix' in args
            if ispresent and args['function_prefix'] != '':
                prefix = searchfuncname.startswith(args['function_prefix'])
            else:
                prefix = True
            if not (("$" + searchfuncname) in cur_line) and not (("'" + searchfuncname + "'") in cur_line) and prefix:
                x = re.search(searchfuncname, cur_line)
                apply_params = re.findall(r"(\$\w+|\'\w+')", cur_line)  # param and string
                # indexes = re.findall ( "(\[ \$\w+ \]|\['\w+'])", cur_line ) # index between []
                para = indent_line + "/**\n"
                para1 = indent_line + " * Function call " + searchfuncname + "\n" + indent_line + " *\n" + indent_line + " * @since " + since.format(now = now, dev = dev_id) + "\n" + indent_line + " *\n"

                para3 = indent_line + " */"
                # goto start of previous line
                goto_start_previous()
                self.view.run_command("insert_snippet", {"contents": para})
                self.view.run_command("insert_snippet", {"contents": para1})
                fi = 0
                linesp = []
                l = 0
                for param in apply_params:
                    # detect name
                    if param == param.replace("$", r"\$"):
                        x0 = re.search(param, cur_line)
                        xix = re.search(r"\[" + param + r"\]", cur_line)
                        if xix:
                            indice = 'index'
                        else:
                            indice = 'string'
                        if x0:
                            if x0.start() < x.start():
                                linep = indent_line + " * @param " + param + " " + dict_anonymous['name_key_or_string'][indice] + "\n"
                            else:
                                linep = indent_line + " * @param " + param + " " + dict_anonymous['name_key_or_string'][indice] + "\n"
                    else:
                        the_param = param.replace("$", r"\$")
                        only_param = "(" + the_param + r"[ ,\[])"
                        x1 = re.search(only_param, cur_line)
                        xix = re.search(r"\[\s" + param.replace("$", r"\$") + r"\s\]", cur_line)
                        if xix:
                            indice = 'index'
                        else:
                            indice = 'string'
                        if x1:
                            if x1.start() < x.start():
                                linep = indent_line + " * @var <type> " + param.replace("$", r"\$") + " [" + dict_anonymous['key_or_param'][indice] + "result description].\n"
                            else:
                                fi = fi + 1
                                if fi == 1:
                                    linep = indent_line + " * @param <type> " + param.replace("$", r"\$") + " " + dict_anonymous['first_param_desc'] + "\n"
                                else:
                                    linep = indent_line + " * @param <type> " + param.replace("$", r"\$") + " " + dict_anonymous['param_desc'][indice] + "\n"
                    if indice == 'index':
                        # modify l-1 because previous is an array
                        linel = linesp[l - 1]
                        linesp[l - 1] = linel.replace("<type>", "array")
                    # list of lines
                    linesp.append(linep)
                    l = l + 1
                for linep in linesp:
                    self.view.run_command("insert_snippet", {"contents": linep})
                # end of comment
                self.view.run_command("insert_snippet", {"contents": para3})
            else:
                print('not a function (or w/o prefix !')
