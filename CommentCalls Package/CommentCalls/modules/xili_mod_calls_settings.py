"""the new settings (not a sub class)
"""
import os
import re
import imp
import sublime
import sublime_plugin
# default data in other modules (ready for updgrade)
import CommentCalls.modules.xili_mod_data as xili_mod_data
imp.reload( xili_mod_data ) # for dev

class CommentCallsSettings():

    """ settings in class to load live (after sublime-settings modifications)
    """
    @staticmethod
    def settings():
        """Summary
        Returns:
            TYPE: Description
        """

        my_settings_name = 'CommentCalls.sublime-settings'
        my_settings = sublime.load_settings(my_settings_name)
        # list of dicts
        # create default one
        # default_dict = {}
        set_dict = {}
        settings_default = 0
        if my_settings:  # file exists
            set_dict['apply_filters'] = my_settings.get('apply_filters')
            set_dict['do_action'] = my_settings.get('do_action')
            set_dict['anonymous'] = my_settings.get('anonymous')
            set_dict['since'] = my_settings.get('@since')
            set_dict['author'] = my_settings.get('@author')
            set_dict['dev_id'] = my_settings.get('@by')
        if set_dict['apply_filters'] and set_dict['do_action'] and set_dict['anonymous']:
            # minimum requested
            return set_dict
        if not my_settings or not set_dict['apply_filters']:
            set_dict['apply_filters'] = xili_mod_data.default_dict['apply_filters']
            my_settings.set('apply_filters', set_dict['apply_filters'])
            settings_default = 1
                # do_action
        if not my_settings or not set_dict['do_action']:
            set_dict['do_action'] = xili_mod_data.default_dict['do_action']
            my_settings.set('do_action', set_dict['do_action'])
            settings_default = settings_default + 10
        # anonymous
        if not my_settings or not set_dict['anonymous']:
            set_dict['anonymous'] = xili_mod_data.default_dict['anonymous']
            my_settings.set('anonymous', set_dict['anonymous'])
            settings_default = settings_default + 100
        # other function
        #
        if settings_default:
            my_settings.set('updated', 'updated to default: ' + str(settings_default))
            sublime.save_settings(my_settings_name)  # save default values
        return set_dict

class CcEditSettingsCommand(sublime_plugin.ApplicationCommand):

    """ Command used in key bindings
    """

    def run(self, base_file, user_file=None, default=None):
        """
        See example in Main.sublime-menu
        Thanks to Sebastien !

        Args:
            base_file (path): The file in plugin module
            user_file (None, path): The file in User
            default (None, string): Default content of file not exist
        """
        module_name = os.path.splitext(os.path.dirname(os.path.realpath(__file__)).split(os.sep)[-2])[0] # -2 because in /modules

        def fix_module_name(fmt):
            if fmt:
                fmt = fmt.replace("${module_name}", module_name)
            return fmt

        base_file = fix_module_name(base_file)
        user_file = fix_module_name(user_file)

        #print(base_file)
        #print(user_file)

        if default is None:
            if base_file.endswith("sublime-settings"):
                default = "// Settings in here override those in \"%s\",\n// and are overridden in turn by syntax-specific settings.\n{\n\t$0\n}\n" % (base_file)
            elif base_file.endswith("sublime-commands"):
                default = "// Add custom commands to the palette.\n[\n\t$0\n]\n"
            elif base_file.endswith("sublime-keymap"):
                default = "// Add custom shortcuts (or use 'unbound' as command to remove existing one).\n[\n\t$0\n]\n"
            else:
                default = "[\n\t$0\n]\n"
            default = default.replace("${", "\\${")

        if int(sublime.version()) >= 3116:
            sublime.run_command("edit_settings", {
                "base_file": base_file,
                "user_file": user_file,
                "default": default,
            })
