"""lines of do_action  comment call
"""
import re

def Comment_do_action ( self, cur_line, indent_line, now ):
    """
    Specific comments if do_action
    Args:
        cur_line (string): the current line to comment
        indent_line (string): contains tabs
        now (date): Description
    Returns:
        list: lines to insert
    """
    dict_do_action = self.dict_do_action
    apply_params = re.findall(r"(\$\w+|\'\w+')", cur_line)
    fi = 0
    linesp = []
    l = 0

    linep = indent_line + "/**\n"
    linesp.append(linep)
    l += 1
    linep = indent_line + " * Fires [to allow a plugin to do to describe]?\n" + indent_line + " *\n" + indent_line + " * @since " + self.since.format(now = now, dev = self.dev_id) + "\n" + indent_line + " *\n"
    linesp.append(linep)
    l += 1

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
    # end
    linep = indent_line + " */"
    linesp.append(linep)
    l += 1
    return linesp
