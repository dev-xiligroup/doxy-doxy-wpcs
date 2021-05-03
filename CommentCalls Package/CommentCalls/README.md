# CommentCalls : examples of couple context - keys

In this page, some small examples of dict in anonymous element of CommentCalls.sublime-settings are explained.

## context
### key
- name
- line
### operand
- regular expression for regex operator (soon info for escape char in settings)
- string for (not_)equal
### operator
can be:
- regex_match
- not_regex_match
- equal
- not_equal

## example #1 : context in anonymous
`{
			"context":
			[
			// first key : the name must start with prefix_
				{
					"key": "name",
					"operand": "^prefix_",
					"operator": "regex_match"
				},
			// second key : the line must not contain “actions or filters” in code or comment at end of the line
				{
					"key": "line",
					"operand": "actions|filters",
					"operator": "not_regex_match"
				}
			],
			// it is the first line of the comment
			"summary": "Function call {funcname} with prefix",
			// case when first param must be highlighted
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