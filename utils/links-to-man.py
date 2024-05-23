#!/usr/bin/env python3

# Copyright 2024 Viktor Söderqvist <viktor.soderqvist@est.tech>
# All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause

import argparse
import re

info = """
This markdown-to-markdown preprocessing script replaces links like
../commands/info.md, ../topics/transactions.md with manpage style references
like **info**(3valkey), **valkey-transactions**(7), etc.
"""

parser = argparse.ArgumentParser(prog="links-to-man.py",
                                 description='Replace some links in markdown with manpage references',
                                 epilog=info)
parser.add_argument('--is-command-page', action='store_true',
                    help="""If specied, the current page is a command page.
                            Otherwise, it's assumed to be a topic page.""")
parser.add_argument('filename', help='Markdown file, or - for stdin')
args = parser.parse_args()

filename = 0 if args.filename == '-' else args.filename
with open(filename, "r") as f:
    content = f.read()

linklabels = {} # label => URL, for links on the form [text][label] where label is defined elsewhere.

def normalize_label(label):
    return label.strip().casefold()


# Collect link labels (inspired by https://github.github.com/gfm/#link-reference-definition)
for match in re.finditer(r'^ {0,3}\[([^\[\]]+)\]: *(\S+) +("[^"]*")? *$', content, re.MULTILINE):
    label = normalize_label(match.group(1))
    if label in linklabels:
        continue
    url = match.group(2)
    #title = match.group(3)
    linklabels[label] = url

def page_to_man(text, dir, name):
    """dir/name.md or dir/(empty name)"""
    name = name.lower()
    if dir == 'commands':
        if name == '' or name == '.':
            return '**valkey-commands**(7) %s' % text
        else:
            return '**%s**(3valkey)' % name
    elif dir == 'topics':
        if name == '' or name == '.':
            return '**valkey**(7)'
        elif name == 'valkey.conf':
            return '**valkey.conf**(4)'
        elif name in ['cli', 'check-aof', 'check-rdb', 'benchmark', 'server', 'sentinel']:
            return '**valkey-%s**(1)' % name
        elif text == '':
            return '**valkey-%s**(7)' % name
        else:
            return '**valkey-%s**(7) %s' % (name, text)
    elif dir == 'clients' and name == '':
        return '[%s](https://valkey.io/clients/)' % text
    elif dir == 'modules' and name == '':
        return '[%s](https://valkey.io/modules/)' % text

    return None

def link_to_man(text, url):
    """Returns a replacement for a link [text](url), or None"""
    if text == url:
        text = '' # Don't print a label if it's identical to the URL (for autolinked URLs)
    elif text.lower().replace(' ', '-').removeprefix('valkey-') == url.removesuffix('.md').strip('/.').removeprefix('commands/').removeprefix('topics/'):
        text = '' # Text is close enough to the page name. Show only page name.
    url = re.sub(r'#.*$', '', url) # strip URL fragment
    match = re.search(r'^../(commands|topics)/([^/]+)\.md$', url)
    if match:
        return page_to_man(text, match.group(1), match.group(2))
    if url == './':
        return page_to_man(text, 'commands' if args.is_command_page else 'topics', '')
    match = re.search('https?://valkey.io/(commands|topics)/([^/]+)$', url)
    if match:
        return page_to_man(text, match.group(1), match.group(2))
    match = re.search(r'^([^/]+)\.md$', url)
    if match:
        dir = 'commands' if args.is_command_page else 'topics'
        return page_to_man(text, dir, match.group(1))
    match = re.search(r'^(?:..|https?://valkey.io)/(commands|topics|clients|modules)/$', url)
    if match:
        return page_to_man(text, match.group(1), '')
    # https://man7.org/linux/man-pages/man5/proc.5.html ==> proc(5)
    match = re.search(r'^https?://man7\.org/linux/man-pages/man\d/([^/\.]+)\.(\d)\.html$', url)
    if match:
        return '**%s**(%s)' % (match.group(1), match.group(2))
    # https://linux.die.net/man/2/fsync ==> fsync(2)
    match = re.search(r'^https?://linux.die.net/man/(\d)/([^/\.]+)$', url)
    if match:
        return '**%s**(%s)' % (match.group(2), match.group(1))
    # https://man.cx/accept%282%29 where %28 = "(", %29 = ")" ==> accept(2)
    match = re.search(r'^https?://man.cx/([^/\.%]+)%28(\d)%29$', url)
    if match:
        return '**%s**(%s)' % (match.group(1), match.group(2))
    # https://man.cx/epoll_ctl, https://man.cx/accept ==> epoll_ctl(2), etc.
    match = re.search(r'^https?://man.cx/(accept|epoll_\w+)$', url)
    if match:
        return '**%s**(2)' % match.group(1)
    return None

# Inline links: [text](url)

def inline_link_repl_callback(match):
    text = match.group(1)
    url = match.group(2).strip()
    repl = link_to_man(text, url)
    return repl if repl else match.group(0) # Keep original

content = re.sub(r'\[([^\[\]\n]+)\]\(([^\(\)\n]+)(?: +"([^\(\)\"\n]+)")?\)', inline_link_repl_callback, content)

# Ref style links: [text][label]

def ref_link_repl_callback(match):
    text = match.group(1)
    label = normalize_label(match.group(2))
    if label not in linklabels:
        return match.group(0) # Keep original
    url = linklabels[label]
    repl = link_to_man(text, url)
    return repl if repl else match.group(0)

content = re.sub(r'\[([^\[\]+])\]\[([^\[\]]+)\]', ref_link_repl_callback, content)

print(content)
