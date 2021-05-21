"""Comment Calls - Writing function calls comments according WPCS.

- exercises and tests in python to comment filters
 inside functions in WP - 20210422 - xili
 implemented cases apply_filters and do_action
 # v 210503 - New name, New source’s structure
 # v 210505 - add final cursor position choice (begin or end of comment or previous in target line)
 # v 210508 - comment is now an objet (class) and 3 subclasses
 # v 210510 - more methods in CommentClass - " ".join() replace loop
 # v 210512 - possible to edit settings, key bindings and command Palette via menu or palette
 # v 210513 - hook on_post_save to help reloading components at the development stage
 # v 210521 - fixes @staticmethod
To introduce modules and classes (and to compare with previous code Comment Filters), the new name of plugin is CommentCalls.
"""

import imp  # not importlib with st3
import re
from datetime import datetime
import sublime
import sublime_plugin

# needs a prefix with plugin folder and name w/o space.

import CommentCalls.modules.xili_mod_calls_settings as xili_mod_calls_settings
imp.reload( xili_mod_calls_settings ) # for dev
from CommentCalls.modules.xili_mod_calls_settings import CommentCallsSettings
from CommentCalls.modules.xili_mod_calls_settings import CcEditSettingsCommand # run command inside

import CommentCalls.modules.xili_mod_calls_select
imp.reload( CommentCalls.modules.xili_mod_calls_select ) # for dev
from CommentCalls.modules.xili_mod_calls_select import CommentCallsSelect # @staticmethod

import CommentCalls.modules.xili_mod_comment_class as xili_mod_comment
imp.reload( xili_mod_comment ) # for dev
import CommentCalls.modules.xili_mod_comment_do as xili_mod_comment_do
imp.reload( xili_mod_comment_do ) # for dev
import CommentCalls.modules.xili_mod_comment_apply as xili_mod_comment_apply
imp.reload( xili_mod_comment_apply ) # for dev
import CommentCalls.modules.xili_mod_comment_anonym as xili_mod_comment_anonym
imp.reload( xili_mod_comment_anonym ) # for dev

__copyright__ = "Copyright © 2021 Michel dev.xiligroup"
__license__ = "GNU General Public License v2 or later"

class CommentCallsCommand(sublime_plugin.TextCommand):

    """
    Comment Calls.
    sub-class of sublime_plugin.TextCommand
    Writing function calls comments according WPCS
    command : comment_calls
    """
    def run(self, edit, **args):
        """
        run

        Args:
            edit (class): Api class
            **args: dict of arguments (** = unknown by default)
        """
        def insert_comment_lines(linesp):
            length = 0
            line_cursor = []
            for linep in linesp:
                line_cursor.append([self.view.sel()[0], len(linep)]) # begin line in list
                self.view.run_command("insert_snippet", {"contents": linep})
                length += len(linep.replace(r"\$","m"))
            return length, line_cursor
            #
        def goto_start_previous():
            # goto start of previous line of the current cursor where is function to comment
            # print( "sel " + str( len(self.view.sel())))
            sel = self.view.sel()[0] # instead - for sel in self.view.sel():
            line = self.view.rowcol(sel.begin())[0] # row from point
                # print(line)
            self.view.insert(edit, self.view.text_point(line, 0), "\n")
            self.view.run_command("move", {"by": "lines", "extend": False, "forward": False})

        # a = xili_mod_settings.CommentCallsCommandSettings.settings( self )
        a = CommentCallsSettings.settings() # @staticmethod
        # settings from module
        self.dict_apply_filters = a['apply_filters'] # xili_mod_settings.dict_apply_filters
        self.dict_do_action = a['do_action'] # xili_mod_settings.dict_do_action
        self.dict_anonymous = a['anonymous'] # xili_mod_settings.dict_anonymous

        if a['since']: # xili_mod_settings.dict_since:  # from settings
            self.since = a['since']
        else:
            # from args in key binding
            if '@since' in args:
                self.since = args['@since']
            else:
                self.since = '[my first version]'
        if a['author']: # xili_mod_settings.dict_author:  # from settings
            self.author = a['author']
        else:
            # from args in key binding
            if '@author' in args:
                self.author = args['@author']
            else:
                self.author = ''
        now = datetime.now()  # used in since if format
        # developer id
        if a['dev_id']: # xili_mod_settings.dict_dev_id:  # from settings
            self.dev_id = a['dev_id'] # xili_mod_settings.dict_dev_id
        else:
            ispresent = '@by' in args  # from args in key binding
            if ispresent:
                self.dev_id = args['@by']
            else:
                self.dev_id = ""

        mycursor = self.view.sel()[0]

        length = 0
        posi = self.view.sel()[0].a
        # current line in "region"
        selection = self.view.full_line(posi)
        row, col = self.view.rowcol(selection.begin()) # tuple of the start of the line
        # get indents
        indent_region = self.view.find('^\t+', self.view.text_point(row, 0))
        indent_line = self.view.substr(indent_region)
        # current line in string
        cur_line = self.view.substr(selection)

        # regex limited to the line
        equal_pos = re.search(" = ", cur_line)
        # target function

        if 'function_name' in args:
            searchfuncname = args['function_name']  # send via parameters args
        else:
            searchfuncname_w = self.view.word(posi)
            searchfuncname = self.view.substr(searchfuncname_w)

        if re.search(r";|\(|\)|,|\[|\]", searchfuncname):
            sublime.error_message("[CommentCalls] Cursor is not around a name of a function call.")
            raise TypeError( searchfuncname + " <-- Cursor is not around a name of a function call !!!")

        x = re.search(searchfuncname, cur_line)
        self.searchfuncname = searchfuncname
        if x and equal_pos and searchfuncname == 'apply_filters':
            # selection or not
            if isinstance(self.dict_apply_filters, list ):
                in_selection = CommentCallsSelect.is_selected( searchfuncname, cur_line, self.dict_apply_filters )
            else:
                in_selection = 0
                self.dict_apply_filters = [ self.dict_apply_filters ]
            if in_selection > -1:
                # goto start of previous line
                goto_start_previous()
                begin_cursor = self.view.sel()[0]
                #linesp = xili_mod_comm_apply.Comment_apply_filters( self, cur_line, indent_line, x, now )
                CommentApply = xili_mod_comment_apply.CommentApply( indent_line, now, in_selection, self ) # sub class
                nbl, linesp = CommentApply.build_comment( indent_line, cur_line, x ) #
                length, lines_cursor = insert_comment_lines( linesp )
            else:
                print('no context and keys !')
                # end apply_filters
        elif not equal_pos and x and searchfuncname == 'do_action':
            # selection or not
            if isinstance(self.dict_do_action, list ):
                in_selection = CommentCallsSelect.is_selected( searchfuncname, cur_line, self.dict_do_action )
            else:
                in_selection = 0
                self.dict_do_action = [ self.dict_do_action ]
            if in_selection > -1:
                goto_start_previous()
                begin_cursor = self.view.sel()[0]
                #
                CommentDo = xili_mod_comment_do.CommentDo( indent_line, now, in_selection, self ) # sub class
                nbl, linesp = CommentDo.build_comment( indent_line, cur_line )
                # post treatment before insertion (ex. pop a line)
                if "popline" in self.dict_do_action[in_selection]:
                    nbl, linesp, del_line = CommentDo.pop_line(self.dict_do_action[in_selection]["popline"]) # example 4 = @author
                    print(del_line)
                length, lines_cursor = insert_comment_lines( linesp )
            else:
                print('no context and keys !')
                # end do_action
        else: # anonymous
            searchfuncname_w = self.view.word(posi)  # via word don't contain $ !
            self.searchfuncallname = self.view.substr(searchfuncname_w)
            print(self.searchfuncallname)
            # avoid to comment comments !
            xc = re.search(r"\/\/", cur_line)
            pos1 = posi
            while pos1 > 0:
                pos = self.view.find_by_class(pos1, False, sublime.CLASS_LINE_START)
                region = sublime.Region(pos, pos1)
                pos1 = pos
                text = self.view.substr(region)
                match = re.search(r"function (\w+)\(",str(text), flags=re.S)
                if match:
                    if isinstance(args['cursor'],tuple):
                        title = match.groups(1)[0] # first in tuple
                    else:
                        title = match.groups(1)
                    # print(match.groups)
                    print("The name of the function containing is ",title)
                    break

            x = re.search(self.searchfuncallname, cur_line)
            if xc and xc.start() < x.start():
                not_in_comment = False
            else:
                not_in_comment = True
            if not (("$" + self.searchfuncallname) in cur_line) and not (("'" + self.searchfuncallname + "'") in cur_line) and not_in_comment:
                # select the good function name according settings
                in_selection = CommentCallsSelect.is_selected( self.searchfuncallname, cur_line, self.dict_anonymous )
                if in_selection > -1:
                    goto_start_previous()
                    begin_cursor = self.view.sel()[0]
                    # linesp = xili_mod_comm_anonym.Comment_Anonymous( self, cur_line, indent_line, x, now, in_selection )
                    CommentAnonym = xili_mod_comment_anonym.CommentAnonym( indent_line, now, in_selection, self ) # sub class
                    nbl, linesp = CommentAnonym.build_comment( indent_line, cur_line, x )
                    # post treatment before insertion (ex. with insertion)
                    if "insertline" in self.dict_anonymous[in_selection]:
                        if isinstance(self.dict_anonymous[in_selection]["insertline"], dict):
                            insertline = self.dict_anonymous[in_selection]["insertline"]
                            nbl, linesp = CommentAnonym.insert_paragraph(insertline["pos"],insertline["elements"])
                    length, lines_cursor = insert_comment_lines( linesp )
                else:
                    print('no context and keys !')
                # end anonymous
            else:
                print('not a function or inside comment !')
            # cursor move to original place, begin, one line and col or end of intserted comment
            # example in key binding
            #   { "keys": ["command+ctrl+i"],"command": "comment_calls", "args": {"cursor": [3,10] }}
            #
        end_cursor = self.view.sel()[0]
        if 'cursor' in args:
            new_sel = []
            if args['cursor'] == 'previous':
                # +1 because insertion inside goto_start_previous
                new_sel.append(sublime.Region(mycursor.a + length + 1, mycursor.b + length + 1))
            elif args['cursor'] == 'begin':
                new_sel.append(sublime.Region(begin_cursor.a + len(indent_line), begin_cursor.b + len(indent_line)))
            elif isinstance(args['cursor'],list): # row, col (not type() == list and not == 'list')

                line_cursor, len_line = lines_cursor[args['cursor'][0]]
                #print(line_cursor)
                #print(args['cursor'][1])
                #print(len_line)
                # tab_in_space = self.view.settings().get('tab_size') * len(indent_line)
                #print(len(indent_line))
                if len_line - len(indent_line) > args['cursor'][1]: # to avoid going to next line
                    colcur = args['cursor'][1]
                else:
                    colcur = len_line - len(indent_line) - 1
                new_sel.append(sublime.Region(
                    line_cursor.a + len(indent_line) + colcur, # if tab one ident per \t (not space)
                    line_cursor.b + len(indent_line) + colcur
                ))
            self.view.sel().clear()
            self.view.sel().add_all(new_sel)
        region = self.view.lines(sublime.Region(begin_cursor.a, end_cursor.a))
        if not isinstance(region, list):
            region = [region]

        self.view.add_regions("test", region, "region.greenish", "circle",
            sublime.HIDDEN)
           # flags=sublime.DRAW_EMPTY | sublime.DRAW_NO_FILL)
        # end of comment (end)

class DevRefreshListener(sublime_plugin.EventListener):

    """ specific event for this plugin in dev
    """

    def on_post_save(self, view):
        """tests if one of the files of plugin was saved !
        """
        in_dev_step = 'CommentCalls' in view.settings().get('development') # in current user's preferences
        # print("Before test...")
        # the catalog of the plugin's modules
        plugin_files = [
            "modules/xili_mod_calls_settings.py",
            "modules/xili_mod_comment_anonym.py",
            "modules/xili_mod_comment_apply.py",
            "modules/xili_mod_comment_do.py",
            "modules/xili_mod_comment_class.py",
            "modules/xili_mod_data.py",
            "modules/xili_mod_calls_select.py"
        ]
        if in_dev_step and view.file_name().endswith(".py"):
            for plugin_file in plugin_files:
                if view.file_name().endswith(plugin_file):
                    print("After saving this file (view): ", view.file_name())
                    sublime_plugin.reload_plugin('CommentCalls.xili_comment_calls') # the root of this plugin

    # end
