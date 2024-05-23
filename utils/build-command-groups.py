#!/usr/bin/env python3

# Copyright 2024 Viktor Söderqvist <viktor.soderqvist@est.tech>
# All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause

import json
import argparse
import sys
import re

parser = argparse.ArgumentParser(prog="build-command-groups.py",
                                 description='creates a JSON file categorizing commands per group')
parser.add_argument('filename', nargs='+', help='JSON files')
args = parser.parse_args()

groups = {}

for filename in args.filename:
    with open(filename, "r") as f:
        j = json.load(f)

    name0 = re.sub(r'^.*/([^/]+)\.json$', r'\1', filename)    # "client-kill"
    name  = name0.replace("-", " ", 1).upper()                # "CLIENT KILL"
    name1 = name.split(' ', maxsplit=1)[-1]                   # "KILL"
    if name1 not in j:
        # Some commands' filenames look like subcommands, but they're not.
        name  = name0.upper()                                 # "RESTORE-ASKING"
        name1 = name

    cmd = j[name1]

    g = cmd["group"] if "group" in cmd else "other"
    if g not in groups:
        groups[g] = {}

    obj = {
        "name": name,
        "summary": cmd.get("summary")
    }
    if "deprecated_since" in cmd:
        obj["deprecated"] = True
    if "doc_flags" in j:
        if "DEPRECATED" in cmd["doc_flags"]:
            obj["deprecated"] = True # Just in case "deprecated_since" wasn't set
        if "SYSCMD" in cmd["doc_flags"]:
            obj["syscmd"] = True

    groups[g][name] = obj

print(json.dumps(groups, indent=4, sort_keys=True))
