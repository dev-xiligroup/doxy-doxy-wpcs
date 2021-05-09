""" Sub class of comment_class
"""
import imp
import re
import CommentCalls.modules.xili_mod_comment_class as xili_mod_comment_class
imp.reload( xili_mod_comment_class ) # for dev
from CommentCalls.modules.xili_mod_comment_class import CommentClass

class CommentAnonym(CommentClass):

    """sub class to comment anonymous

    Attributes:
        calling_self (CommentClass): a way to collect infos from calling (not parent) class
        filter_name (str): Name of the filter/action
        indent_line (str): tabulation of the lines
        key_id (int): Id of selected settings
        li (int): row
        now (date): today
    """

    def __init__(self, indent_line, now, key_id, calling_self ):
        CommentClass.__init__(self, indent_line )
        self.now = now
        self.key_id = key_id # not yet used
        self.calling_self = calling_self
        #
    def header_lines(self, li ):
        """ First lines

        Args:
            li (int): row

        Returns:
            int: row
        """

        dict_anonymous = self.calling_self.dict_anonymous[self.key_id]
        searchfuncname = self.calling_self.searchfuncname
        #
        li = self.first_line (li)
        if 'summary' in dict_anonymous:
            elements = [ dict_anonymous['summary'].format(funcname = searchfuncname)]
            li = self.append_line( elements, li )
        else:
            elements = [ "Function call {funcname} [description]".format(funcname = searchfuncname), "." ]
            li = self.append_line( elements, li )

        elements = []
        li = self.append_line( elements, li )
        # print(self.calling_self.since)
        elements = ["@since ", self.calling_self.since.format(now = self.now, dev = self.calling_self.dev_id)]
        li = self.append_line( elements, li )
        if self.calling_self.author:
            elements = ["@author ", self.calling_self.author]
            li = self.append_line( elements, li )
        elements = []
        li = self.append_line( elements, li )
        #
        return li
        #
    def build_comment(self, indent_line, cur_line, x ):
        """build a comment

        Args:
            indent_line (str): tabulation of the lines
            cur_line (str): the target line
            x (re): result of search

        Returns:
            row and list lines
        """
        self.indent_line = indent_line # can be not the same when instancing !
        dict_anonymous = self.calling_self.dict_anonymous[self.key_id]
        # self.summary = summary
        li = 0
        # dict_comment = self.dict_do_action # for test from calling class
        # searchfuncname = self.searchfuncname
        li = self.header_lines( li )
        fi = 0
        apply_params = re.findall(r"(\$\w+|\'\w+')", cur_line)
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
                        elements = [
                            " * @var ",
                            param,
                            " ",
                            dict_anonymous['name_key_or_string'][indice]
                        ]
                    else:
                        elements = ["@param ", param, " ", dict_anonymous['name_key_or_string'][indice] ]
                    elements.insert(0, ' * ')
                    linep = self.build_line( elements )
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
                        elements = ["@var <type> ", param.replace("$", r"\$"), " [", dict_anonymous['key_or_param'][indice], "result description]"  ]
                    else:
                        fi = fi + 1
                        if fi == 1:
                            elements = ["@param <type> ", param.replace("$", r"\$"), " ", dict_anonymous['first_param_desc']]
                        else:
                            elements = ["@param <type> ", param.replace("$", r"\$"), " ", dict_anonymous['param_desc'][indice]]
                    elements.insert(0, ' * ')
                    linep = self.build_line( elements )
            if indice == 'index':
                # modify l-1 because previous is an array
                linel = self.linesp[li - 1]
                self.linesp[li - 1] = linel.replace("<type>", "array")
            # list of lines
            self.linesp.append(linep)
            li = li + 1

        li = self.footer_lines( li ) # in parent class
        self.li = li # to be used in insert
        return li, self.linesp
        #
