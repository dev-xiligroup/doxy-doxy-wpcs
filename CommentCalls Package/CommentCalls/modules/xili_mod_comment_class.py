'''xili_mod_comment_class and his sub-class
'''
class CommentClass():

    def __init__(self, indent_line ):
        """Summary

        Args:
            indent_line (TYPE): Description
            now (TYPE): Description
            key_id (TYPE): Description
        """
        self.indent_line = indent_line
        self.linesp = []
        self.li = 0

    def empty_comment(self, li):
        """Summary

        Args:
            li (TYPE): Description

        Returns:
            TYPE: Description
        """
        li = self.header_lines(li)
        li = self.footer_lines(li)
        # print(self.linesp)
        return li, self.linesp

    def build_line(self, elements ):
        """Summary

        Args:
            elements (TYPE): Description

        Returns:
            TYPE: Description
        """
        linep = self.indent_line
        for element in elements:
            linep += element
        linep += "\n"
        return linep
        #
    def append_line(self, elements, l ):
        """Summary

        Args:
            elements (TYPE): Description
            l (TYPE): Description

        Returns:
            TYPE: Description
        """
        linep = CommentClass.build_line( self, elements )
        self.linesp.append(linep)
        l += 1
        return l
        #
    def header_lines( self, li):
        """Summary

        Args:
            li (TYPE): Description

        Returns:
            TYPE: Description
        """
        elements = ["/**"]
        li = self.append_line(elements, li)

        elements = [" *"]
        li = self.append_line(elements, li )
        return li
        #
    def footer_lines( self, li):
        """Summary

        Args:
            li (TYPE): Description
        """
        linep = self.indent_line + " */" # w/o return
        self.linesp.append(linep)
        return li

    def build_comment(self, indent_line, summary ):
        """ build a very tiny comment

        Args:
            indent_line (TYPE): Description
            summary (TYPE): Description
        """
        self.indent_line = indent_line
        # self.summary = summary
        li = 0
        # dict_comment = self.dict_do_action # for test from calling class
        # searchfuncname = self.searchfuncname
        li = self.header_lines( li )
        elements = [" *", summary ]
        li = self.append_line(elements, li )
        li = self.footer_lines( li )
        return li, self.linesp
        #
