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
        if elements:
            elements.insert(0, ' * ')
        else:
            elements.insert(0, ' *') # empty line
        linep = CommentClass.build_line( self, elements )
        self.linesp.append(linep)
        l += 1
        return l
        #
    def insert_line(self, pos, elements ):
        """Summary
        Args:
            elements (TYPE): Description
            pos (TYPE): Description
        """
        # test if possible
        if elements and elements[0] != "":
            elements.insert(0, ' * ')
        else:
            elements.insert(0, ' *') # empty line

        if 1 < pos < self.li:
            linep = CommentClass.build_line( self, elements )

            self.linesp.insert( pos, linep)
            self.li += 1
        return self.li, self.linesp
            #
    def insert_paragraph(self, pos, elements ):
        """ Insert
            multiples lines
        Args:
            pos (int): row based 0
            elements (list): must be (or not) a list of list of elements
        """
        # test elements as list of lists
        if isinstance(elements, list):
            if isinstance(elements[0], list):
                for line_element in elements:
                    self.insert_line(pos, line_element )
                    pos += 1
            else:
                self.insert_line(pos, elements ) # only one line
        else:
            print("elements is not a list")
        return self.li, self.linesp #no change
        #
    def pop_line(self, pos ):
        """Summary
        Args:
            elements (TYPE): Description
            pos (TYPE): Description
        """
        # test if possible
        r = ''
        if 1 < pos < self.li:
            r = self.linesp.pop( pos )
            self.li -= 1
        return self.li, self.linesp

    def first_line (self, li):
        linep = self.indent_line + "/**" # w/o return
        linep += "\n"
        self.linesp.append(linep)
        return li
        #
    def header_lines( self, li):
        """Summary

        Args:
            li (TYPE): Description

        Returns:
            TYPE: Description
        """
        li = self.first_line( li )
        elements = []
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
        self.li = li # to be used in insert
        return li, self.linesp
        #
