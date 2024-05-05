#!/usr/bin/env python3

"""
Copyright 2024 Viktor Söderqvist <viktor.soderqvist@est.tech>
All rights reserved.
SPDX-License-Identifier: BSD-3-Clause

This file can be used in two ways:

1. As a standalone script. Try --help for help.

2. As a Python module.

       import command_syntax
       json = json.load(f)

       # All commands in the file
       print(command_syntax.render_all(json))

       # A specific command in the file
       print(command_syntax.render("HSET", json["HSET"]))
"""

import json
import argparse
import sys

info = '''\
Arguments syntax rendering:

  simple                       foo
  optional                     [foo]
  multiple                     foo [foo...]
  multiple + optional          [foo...]

  oneof                        <foo | bar>
  oneof + optional             [foo | bar]
  oneof + multiple             <foo | bar> [<foo | bar>...]
  oneof + multiple + optional  [<foo | bar>...]

  block                        foo bar
  block + optional             [foo bar]
  block + multiple             foo bar [foo bar ...]
  block + multiple + optional  [foo bar [foo bar ...]]

Note: This help text uses "foo" and "bar" as the first and second metasyntactic
variables in syntax examples as described in RFC3092.
'''

def render(name, body, conf={}):
    """Render and print the syntax(es) of a command.

    A JSON file is an object with one key entry on the form {name: body}.

    The conf object is to control some details of the rendering.
    """

    # Set defaults for missing conf fields.
    defaults = {'<': '<', '>': '>',
                '[': '[', ']': ']',
                'markdown': False,
                'split': False,
                'simplify': True}
    defaults.update(conf)
    conf = defaults

    # Some internal helper functions. They depend on the conf object.
    def rewrite(arg):
        """slightly rearrange json object for consistency and simplicity"""
        # Repair: Token type without token? Use name as token.
        if arg["type"] == "pure-token" and "token" not in arg and "name" in arg:
            arg["token"] = arg["name"]
    
        # Rewrite "one of multiple optional alternatives" to "optional alternatives".
        # <[foo] | [bar] | [baz]>  ==>  [foo | bar | baz]
        if conf['simplify'] and arg["type"] == "oneof" and all(subarg.get("optional") for subarg in arg["arguments"]):
            arg["optional"] = True
            for subarg in arg["arguments"]:
                del subarg["optional"]
    
        # Rewrite for simpler rendering: Turn combined token-arg into a block of
        # two: A pure-token arg followed by an arg without token.
        if "token" in arg and arg["type"] != "pure-token":
            tokenarg = {"type": "pure-token",
                        "token": arg["token"]}
            del arg["token"]
            wrapper = {"type": "block",
                       "arguments": [tokenarg, arg]}
            if arg.get("multiple_token"):
                # The whole thing is repeated. Move "multiple" to the wrapper.
                wrapper["multiple"] = True
                if "multiple" in arg:
                    del arg["multiple"]
            if arg.get("optional"):
                # The whole thing is optional. Move "optional" to the wrapper.
                wrapper["optional"] = True
                del arg["optional"]
                # Replace arg with the wrapper.
            arg = wrapper
    
        return arg
    
    def fmt1(s):
        """Format 1, used for fixed tokens (uppercase)"""
        s = s.upper()
        return "**`" + s + "`**" if conf['markdown'] else s
    
    def fmt2(s):
        """Format 2, used for variables (lowercase, italic)"""
        return "_" + s + "_" if conf['markdown'] else s
    
    def arg_syntax(arg):
        """Render the syntax of one argument (JSON object)"""
        syntax = ''
        arg = rewrite(arg)
        type = arg["type"]
    
        if type == "oneof":
            # foo | bar
            subsyntax = " | ".join([arg_syntax(subarg) for subarg in arg["arguments"]])
            if arg.get("multiple") and arg.get("optional"):
                # [<foo | bar>...]
                syntax = conf['<'] + subsyntax + conf['>']
                syntax = conf['['] + syntax + "..." + conf[']']
            elif arg.get("multiple"):
                # <foo | bar> [<foo | bar>...]
                syntax = conf['<'] + subsyntax + conf['>']
                syntax = syntax + " " + conf['['] + syntax + "..." + conf[']']
            elif arg.get("optional"):
                # [foo | bar]
                syntax = conf['['] + subsyntax + conf[']']
            else:
                # <foo | bar>
                syntax = conf['<'] + subsyntax + conf['>']
        elif type == "block":
            # foo bar
            syntax = args_syntax(arg["arguments"])
            if arg.get("multiple"):
                # foo bar [foo bar ...]
                syntax = syntax + " " + conf['['] + syntax + " ..." + conf[']']
            if arg.get("optional"):
                # [foo bar]
                # [foo bar [foo bar ...]]
                syntax = conf['['] + syntax + conf[']']
        else:
            # Simple arg (token or variable)
            # foo
            if type == "pure-token":
                syntax = fmt1(arg["token"])
            else:
                syntax = fmt2(arg["display"] if "display" in arg else arg["name"])
    
            if arg.get("multiple") and arg.get("optinoal"):
                # [foo...]
                syntax = conf['['] + syntax + "..." + conf[']']
            elif arg.get("multiple"):
                # foo [foo...]
                syntax = syntax + " " + conf['['] + syntax + "..." + conf[']']
            elif arg.get("optional"):
                # [foo]
                syntax = conf['['] + syntax + conf[']']
        return syntax
    
    def args_syntax(args):
        """Render the syntax of a list of arguments"""
        return " ".join([arg_syntax(arg) for arg in args])

    def command_syntax_clause(name, body, arguments):
        """Render a syntax line using the given arguments"""
        syntax = fmt1(name)
        if 'container' in body:
            syntax = fmt1(body["container"]) + ' ' + syntax
        if len(arguments) > 0:
            syntax = syntax + " " + args_syntax(arguments)
        return syntax
    
    def use_multiline(body):
        """Determines whether to split the syntax into multiple lines/usages"""
        if not conf['split']:
            return False
        if "arguments" not in body or len(body["arguments"]) != 1:
            return False
        arg = body["arguments"][0]
        if not "arguments" in arg or arg.get("type") != "oneof" or arg.get("optional"):
            return False
        # Split into multiple lines if one of them is complex (has subargs).
        for subarg in arg["arguments"]:
            if "arguments" in subarg:
                return True
            # All subargs are simple, so we still want them on one line, e.g.
            # CLIENT CACHING <YES | NO>
        return False

    # Now the actual work.
    syntax = ''
    if "arguments" not in body:
        return command_syntax_clause(name, body, [])
    elif use_multiline(body):
        # Multiple variants on top level = multiple syntaxes of the
        # command as a whole. Display them one by one.
        syntaxes = [command_syntax_clause(name, body, [variant]) for variant in body["arguments"][0]["arguments"]]
        return "\n".join(syntaxes)
    else:
        return command_syntax_clause(name, body, body["arguments"])

def render_all(json, conf={}):
    """Return syntaxes for all commands in a parsed commands JSON file"""
    # syntaxes = []
    # for name, body in json.items():
    #     syntaxes.append(one(name, body, conf))
    syntaxes = [render(name, body, conf) for name, body in json.items()]
    return "\n".join(syntaxes)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="command-syntax.py",
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description='Render "Usage" syntax from JSON files.',
                                     epilog=info)
    parser.add_argument('--oneof-left', default = '<', metavar='STR', help='Default "<"')
    parser.add_argument('--oneof-right', default = '>', metavar='STR', help='Default ">"')
    parser.add_argument('--optional-left', default = '[', metavar='STR', help='Default "["')
    parser.add_argument('--optional-right', default = ']', metavar='STR', help='Default "]"')
    parser.add_argument('--markdown', action='store_true', help='Insert markdown bold and italics')
    parser.add_argument('--split', action='store_true', help='Split into multiple lines if possible')
    parser.add_argument('--no-simplify', action='store_true', help="Disable rewrite to simpler syntax")
    parser.add_argument('filename', nargs='+', help='Command JSON file(s)')
    args = parser.parse_args()
    conf = {'<': args.oneof_left,
            '>': args.oneof_right,
            '[': args.optional_left,
            ']': args.optional_right,
            'markdown': args.markdown,
            'split': args.split,
            'simplify': not args.no_simplify}
    for filename in args.filename:
        try:
            with open(filename, "r") as f:
                d = json.load(f)
                syntax = render_all(d, conf)
                print(syntax)
        except json.decoder.JSONDecodeError as err:
            print("Error processing %s: %s" % (filename, err), file=sys.stderr)
            exit(1)
        except FileNotFoundError as err:
            print(err, file=sys.stderr)
            exit(1)
