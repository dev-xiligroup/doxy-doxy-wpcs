import sublime
import sublime_plugin
import re
	# exercises and tests in python to comment filters inside functions in WP - 20210422 - xili
	# implemented cases apply_filters and do_action
	# v 210426 - settings file added
	# v 210423
'''
	# examples of key bindings when cursor is in target line containing functions

	{ "keys": ["command+o"],"command": "comment_filters", "args": {
      "function_name": "apply_filters"  }}
     ,
     { "keys": ["ctrl+o"],"command": "comment_filters", "args": {
     "function_name": "do_action"  }
'''

class CommentFiltersCommand(sublime_plugin.TextCommand):

	def run(self, edit, **args ): # Seems to be a wildcard to make all other params available w/o error message

		def goto_start_previous():
			# goto start of previous line of the current cursor where is function to comment
			for sel in self.view.sel():
				line = self.view.rowcol(sel.begin())[0]
				self.view.insert(edit, self.view.text_point(line, 0), "\n")
			self.view.run_command("move", { "by": "lines", "extend": False, "forward": False })

		my_settings_name = 'CommentFilters.sublime-settings'
		my_settings = sublime.load_settings(my_settings_name)
		# list of dicts
		# create default one
		default_dict = {}
		if my_settings: # file exists
			dict_apply_filters = my_settings.get('apply_filters')
			dict_do_action = my_settings.get('do_action')
			# other function
		if not my_settings or not dict_apply_filters:
			default_dict['apply_filters'] = {
				'name_of_called_filters': '[name of the called filters ].',
			 	'first_param_desc': 'The original (non filtered) [description].',
			 	'param_desc':'[description].'
			}
			dict_apply_filters = default_dict['apply_filters']
			my_settings.set('apply_filters', dict_apply_filters )
		# do_action
		if not my_settings or not dict_do_action:
			default_dict['do_action'] = {
				'name_of_called_actions': '[name of called actions].',
			 	'arg_desc':'[description of argument passed to the callback].'
			}
			dict_do_action = default_dict['do_action']
			my_settings.set('do_action', dict_do_action )
		# other function
		#
		sublime.save_settings(my_settings_name) # save default values

		posi = self.view.sel()[0].b
		# current line in "region"
		selection = self.view.full_line(posi)
		row, col = self.view.rowcol(selection.begin())
		# get indents
		indent_region = self.view.find('^\t+', self.view.text_point(row, 0))
		indent_line = self.view.substr( indent_region )
		# current line in string
		cur_line = self.view.substr(selection)

		# regex limited to the line
		equal_pos = re.search (" = ", cur_line)
		# if ( equal_pos ) :
			# colequal = equal_pos.start()
			# give region of function name after equal with sublime method - not used
			# funcname = self.view.word( self.view.text_point(row, colequal + 4) )
		searchfuncname = args['function_name'] # send via parameters args
		x = re.search(searchfuncname, cur_line)
		if x and equal_pos and searchfuncname == 'apply_filters':
			# formatted for searchfuncname
			apply_params = re.findall ("(\$\w+|\'\w+')", cur_line )

			para =  indent_line + "/**\n"
			para1 = indent_line + " * Applying the filters\n" + indent_line + " *\n" + indent_line + " * @since [first version]\n" + indent_line + " *\n"

			para3 =  indent_line + " */"
			# goto start of previous line
			goto_start_previous()
			self.view.run_command("insert_snippet", {"contents": para })
			self.view.run_command("insert_snippet", {"contents": para1 })
			fi = 0
			for param in apply_params:
				# detect name
				if param == param.replace ("$", "\$"):
					x0 = re.search(param, cur_line)
					if x0 :
						if x0.start() < x.start():
							linep = indent_line + " * @param " + param + " [name of index].\n"
						else :
							linep = indent_line + " * @param " + param + " " + dict_apply_filters['name_of_called_filters'] + "\n"
				else:
					x1 = re.search(param.replace ("$", "\$"), cur_line)
					if x1 :
						if x1.start() < x.start():
							linep = indent_line + " * @var <type> " + param.replace ("$", "\$") + " [result description].\n"
						else:
							fi = fi + 1
							if fi == 1:
								linep = indent_line + " * @param <type> " + param.replace ("$", "\$") + " " + dict_apply_filters['first_param_desc'] + "\n"
							else:
								linep = indent_line + " * @param <type> " + param.replace ("$", "\$") + " " + dict_apply_filters['param_desc'] + "\n"
				self.view.run_command("insert_snippet", {"contents": linep })

			# end of comment
			self.view.run_command("insert_snippet", {"contents": para3 })
		# end apply_filters
		elif x and searchfuncname == 'do_action':
			para =  indent_line + "/**\n"
			para1 = indent_line + " * Fires [to allow a plugin to do a description]?\n" + indent_line + " *\n" + indent_line + " * @since [first version]\n"
			para3 =  indent_line + " */"
			# goto start of previous line
			goto_start_previous()
			self.view.run_command("insert_snippet", {"contents": para + para1 })
			apply_params = re.findall ("(\$\w+|\'\w+')", cur_line )
			for param in apply_params:
				if param == param.replace ("$", "\$"):
					x0 = re.search(param, cur_line)
					linep = indent_line + " * @param " + param + " " + dict_do_action['name_of_called_actions'] + "\n"
				else:
					linep = indent_line + " * @param <type> " + param.replace ("$", "\$") + " " + dict_do_action['arg_desc'] +"\n"
				self.view.run_command("insert_snippet", {"contents": linep })
			self.view.run_command("insert_snippet", {"contents": para3 })
		# end do_action