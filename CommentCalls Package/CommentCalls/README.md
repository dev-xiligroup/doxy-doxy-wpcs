# CommentCalls : examples of couple context - keys

In this page, some small example of dict in CommentCalls.sublime-settings are explained.

`{
			"context":
			[
			// first key : the name must start with prefix_
				{
					"key": "name",
					"operand": "^prefix_",
					"operator": "regex_match"
				},
				{
					"key": "line",
					"operand": "actions|filters",
					"operator": "not_regex_match"
				}
			],
			"summary": "Function call {funcname} with prefix",
			"first_param_desc": "The first param [description].",
			"key_or_param":
			{
				"index": "[key name] of ",
				"string": ""
			},
			"name_key_or_string":
			{
				"index": "[key name].",
				"string": "[the string]."
			},
			"param_desc":
			{
				"index": "[key description]",
				"string": "[description]"
			}
}`