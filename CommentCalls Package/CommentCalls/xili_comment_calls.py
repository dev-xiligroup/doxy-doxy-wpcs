"""Comment Calls - Writing function calls comments according WPCS.

- exercises and tests in python to comment filters
 inside functions in WP - 20210422 - xili
 implemented cases apply_filters and do_action
 # v 210503 - New name, New source’s structure
To introduce modules and classes (and to compare with previous code Comment Filters), the new name of plugin is CommentCalls.
"""

import imp  # not importlib with st3
import re
from datetime import datetime
# import sublime
import sublime_plugin

# needs a prefix with plugin folder name w/o space.
# import CommentCalls.modules.xili_mod_settings as xili_mod_settings
# imp.reload( xili_mod_settings ) # for dev
# import CommentCalls.modules.xili_mod_calls_settings as xili_mod_settings
# imp.reload( xili_mod_settings ) # for dev
from CommentCalls.modules.xili_mod_calls_settings import CommentCallsSettings
from CommentCalls.modules.xili_mod_calls_select import CommentCallsSelect
# imp.reload( CommentCallsSettings ) # for dev
import CommentCalls.modules.xili_mod_comm_apply as xili_mod_comm_apply
imp.reload( xili_mod_comm_apply ) # for dev
import CommentCalls.modules.xili_mod_comm_do as xili_mod_comm_do
imp.reload( xili_mod_comm_do ) # for dev
import CommentCalls.modules.xili_mod_comm_anonym as xili_mod_comm_anonym
imp.reload( xili_mod_comm_anonym ) # for dev

__copyright__ = "Copyright © 2021 Michel dev.xiligroup"
__license__ = "GNU General Public License v2 or later"

class CommentCallsCommand(sublime_plugin.TextCommand):

    """
    Comment Calls.

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
            for linep in linesp:
                self.view.run_command("insert_snippet", {"contents": linep})
        def goto_start_previous():
            # goto start of previous line of the current cursor where is function to comment
            for sel in self.view.sel():
                line = self.view.rowcol(sel.begin())[0]
                self.view.insert(edit, self.view.text_point(line, 0), "\n")
            self.view.run_command("move", {"by": "lines", "extend": False, "forward": False})

        # a = xili_mod_settings.CommentCallsCommandSettings.settings( self )
        a = CommentCallsSettings.settings( self )
        # settings from module
        self.dict_apply_filters = a['apply_filters'] # xili_mod_settings.dict_apply_filters
        self.dict_do_action = a['do_action'] # xili_mod_settings.dict_do_action
        self.dict_anonymous = a['anonymous'] # xili_mod_settings.dict_anonymous

        if a['since']: # xili_mod_settings.dict_since:  # from settings
            self.since = a['since']
        else:
            ispresent = '@since' in args  # from args in key binding
            if ispresent:
                self.since = args['@since']
            else:
                self.since = '[my first version]'
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
        # target function
        ispresent = 'function_name' in args
        if ispresent:
            searchfuncname = args['function_name']  # send via parameters args
        else:
            searchfuncname_w = self.view.word(posi)
            searchfuncname = self.view.substr(searchfuncname_w)
        x = re.search(searchfuncname, cur_line)
        if x and equal_pos and searchfuncname == 'apply_filters':
            # print ( searchfuncname )
            # goto start of previous line
            goto_start_previous()
            linesp = xili_mod_comm_apply.Comment_apply_filters( self, cur_line, indent_line, x, now )
            insert_comment_lines( linesp )
                # end apply_filters
        elif not equal_pos and x and searchfuncname == 'do_action':
            goto_start_previous()
            linesp = xili_mod_comm_do.Comment_do_action( self, cur_line, indent_line, now )
            insert_comment_lines( linesp )
                # end do_action
        else: # anonymous
            searchfuncname_w = self.view.word(posi)  # via word don't contain $ !
            self.searchfuncallname = self.view.substr(searchfuncname_w)
            print(self.searchfuncallname)
            # avoid to comment comments !
            xc = re.search(r"\/\/", cur_line)
            x = re.search(self.searchfuncallname, cur_line)
            if xc and xc.start() < x.start():
                not_in_comment = False
            else:
                not_in_comment = True
            if not (("$" + self.searchfuncallname) in cur_line) and not (("'" + self.searchfuncallname + "'") in cur_line) and not_in_comment:
                # select the good function name according settings
                in_selection = CommentCallsSelect.is_selected( self, self.searchfuncallname, cur_line )
                if in_selection > -1:
                    goto_start_previous()
                    linesp = xili_mod_comm_anonym.Comment_Anonymous( self, cur_line, indent_line, x, now, in_selection )
                    insert_comment_lines( linesp )
                else:
                    print('no context and keys !')
                # end anonymous
            else:
                print('not a function or inside comment !')
