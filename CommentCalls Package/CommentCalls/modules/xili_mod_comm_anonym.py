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
        TYPE: Description
    """
    dict_anonymous = self.dict_anonymous[key_id]
    searchfuncname = self.searchfuncallname

    apply_params = re.findall(r"(\$\w+|\'\w+')", cur_line)  # param and string
    fi = 0
    linesp = []
    l = 0

    linep = indent_line + "/**\n"
    linesp.append(linep)
    l += 1
    if 'summary' in dict_anonymous:
        linep = indent_line + " * " + dict_anonymous['summary'].format(funcname = searchfuncname) + "\n" + indent_line + " *\n" + indent_line + " * @since " + self.since.format(now = now, dev = self.dev_id) + "\n" + indent_line + " *\n"
    else:
        linep = indent_line + " * Function call " + searchfuncname + "\n" + indent_line + " *\n" + indent_line + " * @since " + self.since.format(now = now, dev = self.dev_id) + "\n" + indent_line + " *\n"
    linesp.append(linep)
    l += 1

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
    # end
    linep = indent_line + " */"
    linesp.append(linep)
    l += 1
    return linesp
