# Valkey documentation

This repo contains the Valkey documentation in Markdown format, which is used
for generating content for the website and man pages.

## Installing man pages

This repo comes with a Makefile to build and install man pages.

    make VALKEY_ROOT=path/to/valkey VALKEY_BLOOM_ROOT=path/to/valkey-bloom VALKEY_JSON_ROOT=path/to/valkey-json
    sudo make install INSTALL_MAN_DIR=/usr/local/share/man

Prerequisites: GNU Make, Python 3, Python 3 YAML (pyyaml), Pandoc.
Additionally, the scripts need access to the valkey and valkey-json code repos,
where metadata files about the commands are stored. Additionally
access to the valkey-bloom repo is optional.

The pages are generated under `_build/man/` by default. The default install
location is `/usr/local/share/man` (in the appropriate subdirectories).

To uninstall the man pages, run as root `make uninstall INSTALL_MAN_DIR=/usr/local/share/man`.

It's also possible to build local HTML files for local usage, using `make html`.
These HTML files are generated under `_build/html/` by default. The starting
point of the documentation is `topics/index.html`.

## Writing docs

The content of this doc repo is backing the documentation on the website, man
pages and potentially other formats. Links between pages are *relative* and
point directly to the `.md` files as they are stored in this repo. Don't start
links with `/`. This makes sure the links point to existing files regardless of
where in the file system the docs are located, which makes it easier to find
broken links. In text editors and in the GitHub user inteface, it's possible to
click on the links to open the corresponding Markdown page.

Examples: `../commands/get.md` or `replication.md`.

A few exceptions are links to the `topics/`, `commands/`, `clients/` and
`modules/` directories, which end with a slash. These pages are generated (with
the exception of `topics/` which is in `topics/index.md`).

Examples: `../commands/#sorted-set`, `../topics/`, `./`.

### Topics

The files under `topics/` are generic documentation pages. The `index.md` page is a starting point.

In the top of these files, there's a frontmatter metadata section, between two
lines of three dashes (`---`). These are YAML fields of which we use only the
`title` field (and possibly `linkTitle`). The title field is used instead of an
H1 heading in each of the pages.

### Clients, modules, libraries, tools

We maintain links to clients, modules, libraries and tools in various langauges in
JSON files stored under `clients/`, `modules/`, `libraries/` and `tools/`
respectively.

**Note**:  Clients listed here, while fully compatible with Valkey, are not all official clients for Valkey.
They are maintained by their original developers.

All clients are listed under language specific sub-folders of [clients](./clients)

The path follows the pattern: ``clients/{language}/{repository}.json``.
The ``{language}`` component of the path is the path-safe representation
of the full language name which is mapped in [languages.json](./languages.json).

Each client's JSON object represents the details displayed on the [clients documentation page](https://valkey.io/clients/), which are also detailed in [clients/README.md](clients/README.md). 

For example [clients/go/valkey-go.json](./clients/go/valkey-go.json):

```json
{
    "name": "valkey-go",
    "description": "A fast Golang Valkey client that supports Client Side Caching and Auto Pipelining.",
    "recommended": true
}
```

Modules, libraries and tools follow a similar structure under their respective directories.

### Commands

The command pages under `commands/` in this repo are not complete without some
metadata from the Valkey repo, namely the JSON files in the `src/commands/`
folder. The content of these JSON files is combined with the Markdown files in
this repo when the documentation is rendered.

See: https://github.com/valkey-io/valkey/tree/unstable/src/commands/

For each command there's a Markdown file with a complete, human-readable
description.
We process these files to provide a better experience.

*   Inside text, all commands should be written in all caps, in between
    backticks.
    For example: `INCR`.

The reply types and descriptions are stored in separate JSON files in this doc repo.
Each command will have a description and both RESP2 and RESP3 return values.
When adding or editing return values, be sure to edit both files. Use the following
links for the reply type.
Regarding the return values, these are contained in the files:

* `resp2_replies.json`
* `resp3_replies.json`

Each file is a dictionary with a matching set of keys. Each key is an array of strings that,
when processed, produce Markdown content. Here's an example:

```json
{
  ...
  "ACL CAT": [
    "One of the following:",
    "* [Array reply](topics/protocol.md#arrays): an array of [Bulk string reply](topics/protocol.md#bulk-strings) elements representing ACL categories or commands in a given category.",
    "* [Simple error reply](topics/protocol.md#simple-errors): the command returns an error if an invalid category name is given."
  ],
  ...
}
```

### Styling guidelines

Please use the following formatting rules (aiming for smaller diffs that are easier to review):

* Please avoid writing lines that are too long.
  That makes the diff harder to review when only one word is changed.
* Single linebreaks are not significant in Markdown, so when editing an existing
  sentence or paragraph, don't change the existing linebreaks. That just makes
  reviewing harder.
* Start every sentence on a new line.

### Checking your work

After making changes to the documentation, you can use the [spellchecker-cli package](https://www.npmjs.com/package/spellchecker-cli)
to validate your spelling as well as some minor grammatical errors. You can install the spellchecker locally by running:

```bash
npm install --global spellchecker-cli
```

You can than validate your spelling by running the following

```
spellchecker
```

Any exceptions you need for spelling can be added to the `wordlist` file.
Text within backticks is not checked, so using backticks for command names,
parameter values and similar is a good idea to avoid getting spelling errors for
things like that.
