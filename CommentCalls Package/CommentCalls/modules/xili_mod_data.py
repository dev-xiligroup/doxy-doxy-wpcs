"""Summary

Attributes:
    person1 (TYPE): Description
"""

person1 = {
    "name": "John",
    "age": 68,
    "country": "Norway"
}

default_dict = {
    'apply_filters' : {
        'name_of_key': {'index': '[key]', 'string': ''},
        'name_of_called_filters': '[Name of the called filters ].',
        'result_desc': {'index': '[key of result description]', 'string': '[result description]'},
        'first_param_desc': 'The original (non filtered) [description].',
        'param_desc': {'index': '[key description]', 'string': '[description]'}
        },
    'do_action' : {
        'name_of_called_actions': {'index': '[key]', 'first': '[name of called actions].', 'string': '!'},
        'arg_desc': {'index': '[key of argument]', 'string': '[description of argument passed to the callback].'}
        },
    'anonymous' : [{
        'context':[
            {'key':'name', 'operator': 'not_regex_match',  'operand': '^prefix_'}
        ],
        'key_or_param': {'index': '[key name] of ', 'string': ''},
        'name_key_or_string': {'index': '[key name].', 'string': '[the string].'},
        'first_param_desc': 'The first param [description].',
        'param_desc': {'index': '[key description]', 'string': '[description]'}
        },
        {
        'context':[
            {'key':'name', 'operator': 'regex_match',  'operand': '^prefix_'}
        ],
        "summary": "Function call {funcname} with prefix",
        'key_or_param': {'index': '[key name] of ', 'string': ''},
        'name_key_or_string': {'index': '[key name].', 'string': '[the string].'},
        'first_param_desc': 'The first param [description].',
        'param_desc': {'index': '[key description]', 'string': '[description]'}
        }
        ]
    }
