"""
    Module xili_mod_calls_select

    to select according context keys list
"""
import re

class CommentCallsSelect():
    """
        manage selections
        w/o __init__, this class is not really an object, the self is the calling main class "self"
        fixed with @staticmethod now w/o self
    """
    @staticmethod
    def is_selected (searchfuncallname, searchline, current_dict ):
        """Summary

        Args:
            searchfuncallname (string): target name

        Returns:
            integer: key selected in dict_anonymous
        """
        # current_dict = self.dict_anonymous
        keyr = -1
        key_d = 0
        while key_d < len(current_dict):
            # test if context is present, if not accept by default
            if not "context" in current_dict[key_d]:
                keyr = key_d
                break
            print(len(current_dict[key_d]["context"]))
            key_k = 0
            keyruler = []
            while key_k < len(current_dict[key_d]["context"]):
                keyruler.append(-1)
                key_k_kind = current_dict[key_d]["context"][key_k]["key"]
                if key_k_kind == "line":
                    searchtarget = searchline
                else:
                    searchtarget = searchfuncallname
                operator = current_dict[key_d]["context"][key_k]["operator"]
                operand = current_dict[key_d]["context"][key_k]["operand"]
                # test if
                print( 'operand: ' + operand)
                x = re.search( operand, searchtarget )
                if operator == "regex_match":
                    if x:
                        keyruler[key_k] = key_d

                elif operator == "not_regex_match":
                    if not x:
                        keyruler[key_k] = key_d

                elif operator == "equal":
                    if searchtarget == operand:
                        keyruler[key_k] = key_d

                elif operator == "not_equal":
                    if searchtarget != operand:
                        keyruler[key_k] = key_d

                key_k += 1
            # rule AND so all the keys == key_d
            co = keyruler.count(key_d)
            print(keyruler)
            if co == len(keyruler):
                keyr = key_d
                break
            key_d += 1
            # end while
        return keyr # anonymous key selected
