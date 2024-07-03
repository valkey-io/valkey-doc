# Copyright (C) 2024, The Valkey contributors
# All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause

# Path to the code repo.
VALKEY_ROOT ?= ../valkey

# Where to install man pages
INSTALL_MAN_DIR ?= /usr/local/share/man

# Where to put the generated pages.
BUILD_DIR ?= _build
MD_DIR ?= $(BUILD_DIR)/md
MAN_DIR ?= $(BUILD_DIR)/man
HTML_DIR ?= $(BUILD_DIR)/html

# -----------------------------------

.PHONY: all man html md clean distclean install uninstall

all: man

# ---- Sanity check ----

ifeq ("$(wildcard $(VALKEY_ROOT))","")
    $(error Please provide the VALKEY_ROOT variable pointing to the Valkey source code)
endif

ifeq ("$(shell which pandoc)","")
    $(error Please install pandoc)
endif

# ---- Source files ----

topics   = $(wildcard topics/*)
commands = $(wildcard commands/*.md)

topics_md   = $(filter %.md,$(topics))
topics_pics = $(filter-out %.md,$(topics))

# ---- Temp files ----

# JSON files for the commands that have a .md file (excluding undocumented commands).
json_for_documented_commands = $(commands:commands/%.md=$(VALKEY_ROOT)/src/commands/%.json)

$(BUILD_DIR)/.commands-per-group.json: $(VALKEY_ROOT)/src/commands/. utils/build-command-groups.py | $(BUILD_DIR)
	utils/build-command-groups.py $(json_for_documented_commands) > $@
$(BUILD_DIR):
	mkdir -p $@

# ---- Pre-processed markdown files (make md) ----

md_topics_dir = $(MD_DIR)/topics
md_topics = $(topics:topics/%=$(md_topics_dir)/%)
$(md_topics): | $(md_topics_dir)

md_commands_dir  = $(MD_DIR)/commands
md_commands      = $(commands:commands/%=$(md_commands_dir)/%)
$(md_commands): | $(md_commands_dir)

md_targets = $(md_topics) $(md_commands) $(md_commands_dir)/index.md

$(md_topics_dir) $(md_commands_dir):
	mkdir -p $@

$(md_topics_dir)/%.md: topics/%.md utils/preprocess-markdown.py | $(md_topics_dir)
	utils/preprocess-markdown.py $< > $@
$(md_topics_dir)/%.png: topics/%.png | $(md_topics_dir)
	cp $< $@
$(md_topics_dir)/%.gif: topics/%.gif | $(md_topics_dir)
	cp $< $@

$(md_commands_dir)/index.md: $(BUILD_DIR)/.commands-per-group.json groups.json utils/build-command-index.py | $(md_commands_dir)
	utils/build-command-index.py --suffix .md \
	 --groups-json groups.json \
	 --commands-per-group-json $(BUILD_DIR)/.commands-per-group.json > $@

$(md_commands_dir)/%.md: commands/%.md $(VALKEY_ROOT)/src/commands/%.json $(BUILD_DIR)/.commands-per-group.json \
                         utils/preprocess-markdown.py utils/command_syntax.py
	utils/preprocess-markdown.py --page-type command \
	 --commands-per-group-json $(BUILD_DIR)/.commands-per-group.json \
	 --valkey-root $(VALKEY_ROOT) $< > $@

# ---- HTML (make html) ----

html_topics_dir = $(HTML_DIR)/topics
html_topics     = $(topics_md:topics/%.md=$(html_topics_dir)/%.html)
html_topics_pics = $(topics_pics:topics/%=$(html_topics_dir)/%)
$(html_topics): | $(html_topics_dir)

html_commands_dir = $(HTML_DIR)/commands
html_commands     = $(commands:commands/%.md=$(html_commands_dir)/%.html)
$(html_commands): | $(html_commands_dir)

html_targets = $(html_topics) $(html_topics_pics) $(html_commands) $(html_commands_dir)/index.html

$(html_topics_dir) $(html_commands_dir):
	mkdir -p $@

$(html_topics_dir)/%.html: topics/%.md utils/preprocess-markdown.py | $(html_topics_dir)
	utils/preprocess-markdown.py --suffix .html $< | pandoc -s --to html -o $@ -
$(html_topics_dir)/%.png: topics/%.png | $(html_topics_dir)
	cp $< $@
$(html_topics_dir)/%.gif: topics/%.gif | $(html_topics_dir)
	cp $< $@

$(html_commands_dir)/index.html: $(BUILD_DIR)/.commands-per-group.json groups.json utils/build-command-index.py | $(html_commands_dir)
	utils/build-command-index.py --suffix .html \
	 --groups-json groups.json \
	 --commands-per-group-json $(BUILD_DIR)/.commands-per-group.json \
	 | pandoc -s --to html -o $@ -
$(html_commands_dir)/%.html: commands/%.md $(VALKEY_ROOT)/src/commands/%.json $(BUILD_DIR)/.commands-per-group.json \
                             utils/preprocess-markdown.py utils/command_syntax.py
	utils/preprocess-markdown.py --suffix .html --page-type command \
	 --commands-per-group-json $(BUILD_DIR)/.commands-per-group.json \
	 --valkey-root $(VALKEY_ROOT) $< \
	 | pandoc -s --to html -o $@ -

# ---- Man pages (make man) ----

# Split topics into configs, programs and topics
progs = valkey-cli valkey-server valkey-benchmark valkey-sentinel valkey-check-rdb valkey-check-aof
programs = $(progs:valkey-%=topics/%.md)
configs = topics/valkey.conf.md

man1_src = $(filter $(programs),$(topics_md))
man3_src = $(commands)
man4_src = $(filter $(configs),$(topics_md))
man7_src = $(filter-out $(programs) $(configs) topics/index.md,$(topics_md))

# Target man pages
man1     = $(man1_src:topics/%.md=$(MAN_DIR)/man1/valkey-%.1)
man3     = $(man3_src:commands/%.md=$(MAN_DIR)/man3/%.3valkey)
man4     = $(man4_src:topics/%.md=$(MAN_DIR)/man4/%.4)
man7     = $(man7_src:topics/%.md=$(MAN_DIR)/man7/valkey-%.7) $(MAN_DIR)/man7/valkey-commands.7 $(MAN_DIR)/man7/valkey.7

man_targets = $(man1) $(man3) $(man4) $(man7)

$(man1): | $(MAN_DIR)/man1
$(man3): | $(MAN_DIR)/man3
$(man4): | $(MAN_DIR)/man4
$(man7): | $(MAN_DIR)/man7
$(MAN_DIR)/man1 $(MAN_DIR)/man3 $(MAN_DIR)/man4 $(MAN_DIR)/man7:
	mkdir -p $@

man_scripts = utils/preprocess-markdown.py utils/command_syntax.py utils/links-to-man.py

$(MAN_DIR)/man1/valkey-%.1: topics/%.md $(man_scripts)
	utils/preprocess-markdown.py --man --page-type program $< \
	 | utils/links-to-man.py - | pandoc -s --to man -o $@ -
$(MAN_DIR)/man3/%.3valkey: commands/%.md $(VALKEY_ROOT)/src/commands/%.json $(BUILD_DIR)/.commands-per-group.json $(man_scripts)
	utils/preprocess-markdown.py --man --page-type command \
	 --commands-per-group-json $(BUILD_DIR)/.commands-per-group.json \
	 --valkey-root $(VALKEY_ROOT) $< \
	 | utils/links-to-man.py - | pandoc -s --to man -o $@ -
$(MAN_DIR)/man4/%.4: topics/%.md $(man_scripts)
	utils/preprocess-markdown.py --man --page-type config $< \
	 | utils/links-to-man.py - | pandoc -s --to man -o $@ -
$(MAN_DIR)/man7/valkey-%.7: topics/%.md $(man_scripts)
	utils/preprocess-markdown.py --man --page-type topic $< \
	 | utils/links-to-man.py - | pandoc -s --to man -o $@ -
$(MAN_DIR)/man7/valkey.7: topics/index.md $(man_scripts)
	utils/preprocess-markdown.py --man --page-type topic $< \
	 | utils/links-to-man.py - | pandoc -s --to man -o $@ -
$(MAN_DIR)/man7/valkey-commands.7: $(BUILD_DIR)/.commands-per-group.json groups.json utils/build-command-index.py
	utils/build-command-index.py --man \
	 --groups-json groups.json \
	 --commands-per-group-json $(BUILD_DIR)/.commands-per-group.json \
	 | pandoc -s --to man -o $@ -

.PHONY: install-man uninstall-man
install-man: man | $(INSTALL_MAN_DIR)/man1 $(INSTALL_MAN_DIR)/man3 $(INSTALL_MAN_DIR)/man4 $(INSTALL_MAN_DIR)/man7
	cp $(MAN_DIR)/man1/valkey*.1 $(INSTALL_MAN_DIR)/man1/
	cp $(MAN_DIR)/man3/*.3valkey $(INSTALL_MAN_DIR)/man3/
	cp $(MAN_DIR)/man4/valkey*.4 $(INSTALL_MAN_DIR)/man4/
	cp $(MAN_DIR)/man7/valkey*.7 $(INSTALL_MAN_DIR)/man7/

$(INSTALL_MAN_DIR)/man1 $(INSTALL_MAN_DIR)/man3 $(INSTALL_MAN_DIR)/man4 $(INSTALL_MAN_DIR)/man7:
	mkdir -p $@

uninstall-man:
	rm $(INSTALL_MAN_DIR)/man1/valkey*.1
	rm $(INSTALL_MAN_DIR)/man3/*.3valkey
	rm $(INSTALL_MAN_DIR)/man4/valkey*.4
	rm $(INSTALL_MAN_DIR)/man7/valkey*.7

# -------

# All targets
targets = $(man_targets) $(html_targets) $(md_targets)

md: $(md_targets)

html: $(html_targets)

man: $(man_targets)

clean:
	rm -f $(targets) $(BUILD_DIR)/.commands-per-group.json
distclean:
	rm -rf $(BUILD_DIR)

install: install-man

uninstall: uninstall-man
