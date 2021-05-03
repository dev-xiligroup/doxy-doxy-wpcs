"""the new settings (not a sub class)
"""
import re
import imp
import sublime
# default data in other modules (ready for updgrade)
import CommentCalls.modules.xili_mod_data as xili_mod_data
imp.reload( xili_mod_data ) # for dev

class CommentCallsSettings():

    """ settings in class to load live (after sublime-settings modifications)
    """

    def settings(self):
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
