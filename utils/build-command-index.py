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

parser = argparse.ArgumentParser(prog="build-command-index.py",
                                 description='Create an overview page of all commands, commands/index.md')
parser.add_argument('--suffix', default='.md',
                    help='Suffix to use in internal links instead of .md for non-manpage usage')
parser.add_argument('--man', action='store_true', help='Generate markdown for man page')
parser.add_argument('--date', default='', help='Date on the form YYYY-MM-DD')
parser.add_argument('--version', default='', help='Version on the form X.Y.Z')
parser.add_argument('--groups-json', help='groups.json')
parser.add_argument('--commands-per-group-json', help='commands-per-groups.json')
args = parser.parse_args()

with open(args.groups_json, "r") as f:
    groups = json.load(f)
with open(args.commands_per_group_json, "r") as f:
    commands_per_group = json.load(f)

if args.man:
    print("---")
    print("title: VALKEY-COMMANDS(7)")
    print('header: Valkey Command Manual')
    print('footer: %s' % args.version)
    print('date: %s' % args.date)
    print('adjusting: left')
    print("---")
    print('# NAME', end="\n\n")
    print("valkey-commands - The full list of Valkey commands", end="\n\n")
    print("# DESCRIPTION", end="\n\n")
    print("Commands per group.", end="\n\n")
else:
    print("---")
    print('title: Commands &middot; Valkey')
    print("---")
    print("# Valkey Commands", end="\n\n")

if not args.man:
    # Links to groups within the page
    print("Commands groups:")
    for (groupname, groupobj) in groups.items():
        if groupname not in commands_per_group:
            continue # No commands in this group
        anchor = groupname.replace(' ', '-').replace('_', '-')
        print("[%s](#%s)" % (groupobj["display"], anchor))
    print()

for (groupname, commands) in commands_per_group.items():
    if groupname not in groups and groupname.replace('_', '-') in groups:
        groupname = groupname.replace('_', '-')
    if groupname in groups:
        g = groups[groupname]
        if g["display"].lower().replace(' ', '-') == groupname:
            print('## %s' % g["display"], end="\n\n")
        else:
            print('## <a name="%s">%s</a>' % (groupname, g["display"]), end="\n\n")
        description = g["description"]
    else:
        print("## %s" % groupname.replace('_', ' '), end="\n\n")
        description = ''

    if args.man:
        for (name, obj) in commands.items():
            summary = obj["summary"]
            if obj.get("deprecated"):
                summary = summary + " Deprecated."
            pagename = name.replace(' ', '-').lower()
            print("**%s**(3valkey): %s" % (pagename, summary), end="\n\n")
    else:
        print(description)
        print("<table>")
        for (name, obj) in commands.items():
            summary = obj["summary"]
            if obj.get("deprecated"):
                summary = summary + " Deprecated."
            pagename = name.replace(' ', '-').lower()
            print("<tr><td>")
            url = pagename + args.suffix
            print("[`%s`](%s)" % (name, url))
            print("</td><td>%s</td></tr>" % summary)
        print("</table>")
    print()

if args.man:
    print("# SEE ALSO", end="\n\n")
    print("**valkey**(7), **valkey-data-types**(7)")
