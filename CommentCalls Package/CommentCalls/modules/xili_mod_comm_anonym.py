"""anonymous function
"""
import re

def Comment_Anonymous ( self, cur_line, indent_line, x, now, key_id ):
    """Summary

    Args:
        cur_line (string): the current line to comment
        indent_line (string): contains tabs
        x (region) : where is the target name
        now (date): Description
        key_id (integer): id of the rule from settings

    Returns:
        list:  comment lines
    """

    def build_line( elements ):
        linep = indent_line
        for element in elements:
            linep += element
        linep += "\n"
        return linep
        #
    def append_line( elements, l):
        linep = build_line( elements )
        linesp.append(linep)
        l += 1
        return l
        #
    fi = 0
    linesp = []
    li = 0
    dict_anonymous = self.dict_anonymous[key_id]
    searchfuncname = self.searchfuncallname

    elements = ["/**"]
    li = append_line(elements, li)

    if 'summary' in dict_anonymous:
        elements = [ " * ", dict_anonymous['summary'].format(funcname = searchfuncname)]
        li = append_line(elements, li)
    else:
        elements = [ " * Function call ", searchfuncname ]
        li = append_line(elements, li)

    elements = [" *"]
    li = append_line(elements, li)
    elements = [" * @since ", self.since.format(now = now, dev = self.dev_id)]
    li = append_line(elements, li)
    if self.author:
        elements = [" * @author ", self.author]
        li = append_line(elements, li)
    elements = [" *"]
    li = append_line(elements, li )

    apply_params = re.findall(r"(\$\w+|\'\w+')", cur_line)  # param and string
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
                    elements = [" * @param ", param, " ", dict_anonymous['name_key_or_string'][indice] ]
                linep = build_line( elements )
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
                    elements = [" * @var <type> ", param.replace("$", r"\$"), " [", dict_anonymous['key_or_param'][indice], "result description]"  ]
                else:
                    fi = fi + 1
                    if fi == 1:
                        elements = [" * @param <type> ", param.replace("$", r"\$"), " ", dict_anonymous['first_param_desc']]
                    else:
                        elements = [" * @param <type> ", param.replace("$", r"\$"), " ", dict_anonymous['param_desc'][indice]]
                linep = build_line( elements )
        if indice == 'index':
            # modify l-1 because previous is an array
            linel = linesp[li - 1]
            linesp[li - 1] = linel.replace("<type>", "array")
        # list of lines
        linesp.append(linep)
        li = li + 1
    # end
    linep = indent_line + " */" # w/o return
    linesp.append(linep)
    return linesp
