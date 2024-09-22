#!/usr/bin/env python3

# Copyright (C) 2024, The Valkey contributors
# All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause

import os
import re
import json
import argparse
import sys
import yaml
from datetime import date

import command_syntax

# Standard man page headings according to 'man man-pages', in standard order
standard_headings = {
    'NAME',                     # Inserted automatically
    'LIBRARY',                  # Not used (possibly use module API functions)
    'SYNOPSIS',                 # Inserted automatically for commands. Written
                                # explicitly as "## Usage" for programs.
    'CONFIGURATION',            # Explicit for valkey.conf(4)
    'DESCRIPTION',              # Inserted automatically before any text unless
                                # another standard heading starts the text
    'OPTIONS',                  # Uses for programs
    'EXIT STATUS',              # [Normally only in Sections 1, 8]
    'RETURN VALUE',             # We use REPLY instead, automatic for commands
    'ERRORS',
    'ENVIRONMENT',
    'FILES',
    'VERSIONS',                 # We use HISTORY instead, automatic for commands
    'ATTRIBUTES',               # [Normally only in Sections 2, 3]
    'STANDARDS',
    'NOTES',                    # Inserted automatically for deprecated commands
    'CAVEATS',
    'BUGS',
    'EXAMPLES',
    'AUTHORS',                  # Discouraged
    'REPORTING BUGS',
    'COPYRIGHT',
    'SEE ALSO'                  # Inserted automatically for commands
}

class ManStructure:
    """Render markdown with H1 for the standard man-page headings and some other quirks."""
    def __init__(self, data):
        self.__dict__.update(data)
    def __getattr__(self, prop):
        return self.__dict__.get(prop)

    def print_top(self):
        print('---')
        print('title: %s' % self.name.upper())
        if self.pagetype == 'command':
            print('section: 3valkey')
            print('header: Valkey Command Manual')
        elif self.pagetype == 'program':
            print('section: 1')
            print('header: Valkey Manual')
        elif self.pagetype == 'config':
            print('section: 4')
            print('header: Valkey Configuration Manual')
        else:
            print('section: 7')
            print('header: Valkey Manual')
        print('footer: Valkey Documentation')
        print('date: %s' % self.date)
        print('adjusting: left')
        print('---')
        print('# NAME', end="\n\n")
        if self.summary:
            print('%s - %s' % (self.name, self.summary), end="\n\n")
        elif self.title:
            print('%s - %s' % (self.name, self.title), end="\n\n")
        else:
            print('%s' % (self.name), end="\n\n")
        if self.syntax:
            print("# SYNOPSIS", end="\n\n")
            print(self.syntax, end="\n\n")

    def print_middle(self):
        if self.pagetype != 'command':
            return
        if self.resp2 or self.resp3:
            print("# REPLY", end="\n\n")
            if self.resp2 == self.resp3:
                print(self.resp2, end="\n\n")
            else:
                if self.resp2:
                    print("## RESP2", end="\n\n")
                    print(self.resp2, end="\n\n")
                if self.resp3:
                    print("## RESP3", end="\n\n")
                    print(self.resp3, end="\n\n")
            
        if self.complexity:
            print("# COMPLEXITY", end="\n\n")
            print(self.complexity, end="\n\n")
        if self.acl_categories:
            acl = " ".join(self.acl_categories)
            print("# ACL CATEGORIES", end="\n\n")
            print(acl, end="\n\n")

        if self.since or self.history:
            print("# HISTORY", end="\n\n")
            if self.since:
                print("* Available since: %s" % self.since)
            if self.history:
                for entry in self.history:
                    print("* Changed in %s: %s" % (entry[0], entry[1]))
            print()

        if self.deprecated_since:
            print("# NOTES", end="\n\n")
            if self.replaced_by:
                print("This command is deprecated (since %s) and replaced by %s." %
                      (self.deprecated_since, self.replaced_by), end="\n\n")
            else:
                print("This command is deprecated since %s." % self.deprecated_since, end="\n\n")

    def print_bottom(self):
        if self.see_also_commands:
            print("# SEE ALSO", end="\n\n")
            see_also = ", ".join(["**" + cmd.lower().replace(' ', '-') + "**(3valkey)"
                                  for cmd in self.see_also_commands.keys()])
            print(see_also, end="\n\n")

    def rewrite_heading(self, heading):
        heading = heading.strip()
        if heading == "## Usage":
            heading = "# SYNOPSIS"
        elif heading.startswith("##") and heading[2:].strip().upper() in standard_headings:
            # If any of the standard headings are used explicitly as H2, we
            # format them as man page standard headings with H1 and in all-caps.
            # This is the case for valkey-server, valkey-cli, valkey-benchmark,
            # etc. where we write out Options, Description, etc. explicitly.
            heading = heading[1:].upper()
        elif heading.startswith("# "):
            heading = heading.upper()
        return heading + "\n"

    def rewrite_link(self, url, fragment):
        # Don't edit links. Another script rewrites them to manpage references.
        return url + fragment

class WebStructure:
    """This one uses H2 headings. There's only one H1 on web pages."""
    def __init__(self, data):
        self.__dict__.update(data)
    def __getattr__(self, prop):
        return self.__dict__.get(prop)

    def print_top(self):
        title = self.title if self.title else self.name
        print('---')
        print('title: %s &middot; Valkey' % title)
        print('---')
        print("# %s" % title, end="\n\n")
        if self.summary:
            print(self.summary, end="\n\n")
        if self.pagetype == 'command':
            if self.syntax:
                print("## Usage", end="\n\n")
                print(self.syntax, end="\n\n")

    def print_middle(self):
        if self.resp2 or self.resp3:
            if self.resp2 == self.resp3:
                print("## Reply", end="\n\n")
                print(rewrite_links(self.resp2, self), end="\n\n")
            else:
                if self.resp2:
                    print("## Reply RESP2", end="\n\n")
                    print(rewrite_links(self.resp2, self), end="\n\n")
                if self.resp3:
                    print("## Reply RESP3", end="\n\n")
                    print(rewrite_links(self.resp3, self), end="\n\n")
        if self.complexity:
            print("## Complexity", end="\n\n")
            print(self.complexity, end="\n\n")
        if self.acl_categories:
            acl = " ".join(self.acl_categories)
            print("## ACL Categories", end="\n\n")
            print(acl, end="\n\n")

    def print_bottom(self):
        if self.history or self.since or self.deprecated_since:
            print("## History", end="\n\n")
            if self.since:
                print("* %s: Introduced." % self.since)
            if self.history:
                for entry in self.history:
                    print("* %s: %s" % (entry[0], entry[1]))
            if self.deprecated_since:
                if self.replaced_by:
                    print("* %s: Deprecated; replaced by %s." % (self.deprecated_since, self.replaced_by))
                else:
                    print("* %s: Deprecated." % self.deprecated_since)
            print()
        if self.see_also_commands:
            print("## See also", end="\n\n")
            see_also = ", ".join(['[%s](%s "%s")' % (cmd, cmd.lower().replace(' ', '-') + self.suffix, summary)
                                  for (cmd, summary) in self.see_also_commands.items()])
            print(see_also + '.', end="\n\n")

    def rewrite_heading(self, heading):
        return heading

    def rewrite_link(self, url, fragment):
        # This is internal links only
        if url.endswith(".md"):
            url = url[0:-3] + self.suffix
        elif url.endswith("/"):
            url = url + 'index' + self.suffix
        return url + fragment

def loadjson(filename):
    """Loads a JSON file or exits the program"""
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except json.decoder.JSONDecodeError as err:
        print("Error processing %s: %s" % (filename, err), file=sys.stderr)
        exit(1)
    except FileNotFoundError as err:
        print(err, file=sys.stderr)
        exit(1)

def get_reply(name, resp_json_file):
    json = loadjson(resp_json_file)
    if name in json:
        return "\n\n".join(json[name])
    else:
        return None

def acl_categories(json):
    flags = set(json["command_flags"] if "command_flags" in json else [])
    acl   = set(json["acl_categories"] if "acl_categories" in json else [])
    if "WRITE" in flags:
        acl.add("WRITE")
    if "READONLY" in flags and "SCRIPTING" not in acl:
        acl.add("READ")
    if "ADMIN" in flags:
        acl.add("ADMIN")
        acl.add("DANGEROUS")
    if "PUBSUB" in flags:
        acl.add("PUBSUB")
    if "FAST" in flags:
        acl.add("FAST")
    if "BLOCKING" in flags:
        acl.add("BLOCKING")
    if "FAST" not in acl:
        acl.add("SLOW")
    return ["@" + cat.lower() for cat in sorted(acl)]

def command_see_also(group, commands_per_group_file, exclude_command):
    """Returns a dict {command: summary} of the commands in the given group"""
    commands_per_group = loadjson(commands_per_group_file)
    commands = commands_per_group.get(group)
    if not commands:
        return []
    return {k: v.get("summary") for (k, v) in commands.items() if not v.get("deprecated") and k != exclude_command}

def rewrite_links(text, renderer):
    def repl_link_match(match):
        # Match groups: 1 = before link, 2 = URL without fragment, 3 = URL fragment if any, 4 = after link
        url = match.group(2)
        # Rewrite external links to internal ones.
        url = re.sub(r'^https?://valkey\.io/(commands|topics)/([^/]+)$', r'../\1/\2.md', url)
        url = re.sub(r'^https?://valkey\.io/(commands|topics|clients|modules)/$', r'../$1/', url)
        fragment = match.group(3) if match.group(3) else ''
        link = renderer.rewrite_link(url, fragment)
        return match.group(1) + link + match.group(4)
    # inline links [text](url)
    text = re.sub(r'(\]\()((?:../\w+/|./)?(?:[^/\)\#]+\.md)?)(#[^\)]*)?(\))', repl_link_match, text)
    # link labels [label]: url
    text = re.sub(r'^(\[[\w\d-]+\]: *)((?:../\w+/|./)?(?:[^/\)\#]+\.md)?)(#[^\)\s]*)?()\s*$', repl_link_match, text)
    return text

def main():
    docdir = os.path.dirname(os.path.abspath(__file__)) + "/../"
    resp2_default = docdir + "resp2_replies.json"
    resp3_default = docdir + "resp3_replies.json"
    parser = argparse.ArgumentParser(prog="preprocess-markdown.py",
                                     description='Build a complete markdown page from input markdown and JSON files.',
                                     epilog="")
    parser.add_argument('--page-type', default='topic', choices=['topic', 'command', 'program', 'config'])
    parser.add_argument('--valkey-root', help='Root directory of the code repo')
    parser.add_argument('--command-json', help='Command JSON file in code repo')
    parser.add_argument('--commands-per-group-json', help='JSON file generated by build-command-groups.py')
    parser.add_argument('--resp2-replies-json', default=resp2_default, help='RESP2 replies JSON file')
    parser.add_argument('--resp3-replies-json', default=resp3_default, help='RESP2 replies JSON file')
    parser.add_argument('--suffix', default='.md',
                        help='Suffix to use in internal links instead of .md for non-manpage usage')
    parser.add_argument('--base-url', default='https://valkey.io/', help='Used for transforming absolute links to relative ones.')
    parser.add_argument('--man', action='store_true', help='Generate markdown for man page')
    parser.add_argument('filename', help='Markdown file')
    args = parser.parse_args()

    # We can use git to find the last change of the file, but only if we're in a git repo.
    # yyyymmdd = os.popen('git log -1 --pretty="format:%cs" ' + args.filename).read()
    mtime = os.stat(args.filename).st_mtime
    yyyymmdd = date.fromtimestamp(mtime).isoformat()

    name0 = re.sub(r'^.*/([^/]+)\.md$', r'\1', args.filename) # "client-kill"

    # Pagename = name of man page excluding section. (Only used for man pages.)
    if args.page_type == 'command':
        pagename = name0
    elif args.page_type == 'topic' and name0 == 'index':
        pagename = 'valkey'
    elif args.page_type == 'config' and name0 == 'valkey.conf':
        pagename = name0
    else:
        pagename = 'valkey-' + name0
    data = {
        "name": pagename,
        "date": yyyymmdd,
        "suffix": args.suffix,
        "pagetype": args.page_type
    }

    if args.page_type == 'command':
        if args.command_json:
            command_json = args.command_json
        elif args.valkey_root:
            command_json = args.valkey_root + '/src/commands/' + name0 + '.json'
        else:
            print("I need --command-json or --valkey-root", file=sys.stderr)
            exit(1)

        command_metadata = loadjson(command_json)
        name  = name0.replace("-", " ", 1).upper()                # "CLIENT KILL"
        name1 = name.split(' ', maxsplit=1)[-1]                   # "KILL"
        if name1 not in command_metadata:
            # Some commands' filenames look like subcommands, but they're not.
            name  = name0.upper()                                 # "RESTORE-ASKING"
            name1 = name

        command_metadata = command_metadata[name1]

        syntax = command_syntax.render(name1, command_metadata, {'split': True, 'markdown': True})
        syntax = syntax.replace("\n", "\\\n") # Explicit linebreak between the clauses.

        data.update({
            "title": name,    # e.g. "CLIENT KILL"
            "syntax": syntax,
            "resp2": get_reply(name, args.resp2_replies_json),
            "resp3": get_reply(name, args.resp3_replies_json),
            "summary": command_metadata.get("summary"),
            "complexity": command_metadata.get("complexity"),
            "since": command_metadata.get("since"),
            "history": command_metadata.get("history"),
            "acl_categories": acl_categories(command_metadata),
            "group": command_metadata.get("group"),
            "see_also_commands": command_see_also(command_metadata.get("group"), args.commands_per_group_json, name)
        })
        if "deprecated_since" in command_metadata:
            data["deprecated_since"] = command_metadata["deprecated_since"]
        if "replaced_by" in command_metadata:
            # Remove old marks that something is NOT a command, e.g. `!GET`.
            replaced_by = re.sub(r'`!([A-Z -]+)`', r'`\1`', command_metadata["replaced_by"])
            data["replaced_by"] = replaced_by

    r = None # Populate it later, when we have parsed frontmatter.

    # Encoding "utf-8-sig" deletes the silly UTF-8 BOM added by MS Notepad.
    with open(args.filename, "r", encoding="utf-8-sig") as f:
        lines = [line for line in f]
    frontmatter_str = ''
    frontmatter = {}
    middle_stuff_printed = False
    state = 0 # 0 = start of file, 1 = in yaml metadata, 2 = start of body, 3 = before description, 4 = in or after description
    prevline = None
    for line in lines:
        if state == 0:
            if line.startswith("---"):
                state = 1
                continue
            else:
                state = 2
        elif state == 1:
            if line.startswith("---"):
                state = 2
                frontmatter = yaml.safe_load(frontmatter_str)
            else:
                frontmatter_str = frontmatter_str + line
            continue

        # If we're here, the frontmatter has been parsed and the actual
        # markdown starts.
        if (state == 2):
            # Start of body. Init the renderer.
            if "title" in frontmatter and "title" not in data:
                data["title"] = frontmatter["title"]
            r = ManStructure(data) if args.man else WebStructure(data)
            # Before the start of the body, we print some stuff.
            r.print_top()
            state = 3

        # Now we're in the body of the file

        # Remove old marks that something is NOT a command, e.g. `!GET`.
        line = re.sub(r'`!([A-Z -]+)`', r'`\1`', line)

        # Rewrite links
        line = rewrite_links(line, r)

        # Rewrite underlined headings to ATX style headings, for later processing.
        if prevline is not None:
            if line.startswith('---'):
                line = '## ' + prevline
                prevline = None
            elif line.startswith('==='):
                line = '# ' + prevline
                prevline = None

        # Print the previous line. We do this to be able to detect two-line
        # markdown things like headering with underline.
        if prevline is not None:
            if state == 3 and prevline.strip() != "":
                state = 4
                # Insert a Description heading after the page header, unless the
                # text already starts with a heading.
                if not prevline.startswith("#"):
                    print(r.rewrite_heading("## Description"))
            if prevline.startswith("#"):
                print(r.rewrite_heading(prevline))
            else:
                print(prevline, end='')

        # Insert some stuff before the Notes or Example(s) section.
        if not middle_stuff_printed:
            if line.startswith("## Notes") or line.startswith("## Example"):
                r.print_middle()
                middle_stuff_printed = True

        prevline = line

    # The last line that hasn't yet been printed.
    print(prevline);

    if not middle_stuff_printed:
        print()
        r.print_middle()

    print()
    r.print_bottom()

main()

# If we want Authors, we can get it from git blame:
# git blame --line-porcelain FILE | sed -n 's/^author //p' | sort | uniq -c | sort -rn
