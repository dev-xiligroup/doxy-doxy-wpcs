""" Sub class of comment_class
"""
import imp
import re
import CommentCalls.modules.xili_mod_comment_class as xili_mod_comment_class
imp.reload( xili_mod_comment_class ) # for dev
from CommentCalls.modules.xili_mod_comment_class import CommentClass

class CommentApply(CommentClass):

    """ sub class to comment do_action

    Attributes:
        calling_self (CommentClass): a way to collect infos from calling (not parent) class
        indent_line (TYPE): Description
        key_id (TYPE): Description
        now (TYPE): Description
    """

    def __init__(self, indent_line, now, key_id, calling_self ):

        CommentClass.__init__(self, indent_line )
        self.now = now
        self.key_id = key_id
        self.calling_self = calling_self
        self.filter_name = "vide"
        #
    def header_lines(self, li ):
        """Summary

        Args:
            li (int): count of lines

        Returns:
            TYPE: Description
        """
        dict_apply_filters = self.calling_self.dict_apply_filters[self.key_id]

        # searchfuncname = self.calling_self.searchfuncname
        #
        li = self.first_line (li)
        if 'summary' in dict_apply_filters:
            elements = [ dict_apply_filters['summary'].format(filtername = self.filter_name)]
            li = self.append_line( elements, li )
        else:
            elements = [ "Applying all the filters named {filtername}.".format(filtername = self.filter_name) ]
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
        """ build a very tiny comment

        Args:
            indent_line (TYPE): Description
            summary (TYPE): Description
        """
        self.indent_line = indent_line # can be not the same when instancing !

        dict_apply_filters = self.calling_self.dict_apply_filters[self.key_id]
        # self.summary = summary
        li = 0
        #
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
                        elements = [ "@param ", param, " ", dict_apply_filters['name_of_key'][indice], "."]
                    else:
                        # param contains the quotes
                        self.filter_name = param
                        elements = [ "@param ", param, " ", dict_apply_filters['name_of_called_filters']]
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
                        elements = [ "@var <type> ", param.replace("$", r"\$"), " ", dict_apply_filters['result_desc'][indice], "."]
                    else:
                        fi = fi + 1
                        if fi == 1:
                            elements = [ "@param <type> ", param.replace("$", r"\$"), " ", dict_apply_filters['first_param_desc']]
                        else:
                            elements = [ "@param <type> ", param.replace("$", r"\$"), " ", dict_apply_filters['param_desc'][indice]]
                    elements.insert(0, ' * ')
                    linep = self.build_line( elements )

            if indice == 'index':
                # modify l-1 because previous is an array
                linel = self.linesp[li - 1]
                self.linesp[li - 1] = linel.replace("<type>", "array")
            # list of lines
            self.linesp.append(linep)
            li = li + 1
        lines_body = self.linesp.copy() # instead = because clone
        li_body = li
        # can build header with name_of_called_filters
        self.linesp.clear() # not = [] which is a def !
        li = 0
        li = self.header_lines( li )
        self.linesp.extend(lines_body)
        li += li_body
        li = self.footer_lines( li ) # in parent class
        self.li = li # to be used in insert
        return li, self.linesp
        #
