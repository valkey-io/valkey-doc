#!/usr/bin/perl

# Copyright (C) 2024, The Valkey contributors
# All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause

# Checks for intenal broken links. Checks some other things too, like orphan
# pages (nobody links to the orphan page) and the number of external links.

use warnings;
use strict;

my $root = __FILE__ =~ s![^/]*$!!r . "../";
$root =~ s%[^/\.]+/\.\./$%%;
my @files = glob("${root}{topics,commands}/*");

my %targets;
for (@files) {
    s/^$root//;
    $targets{$_} = 0;
}

my %directory_targets = ("commands/" => 0,
                         "clients/" => 0,
                         "modules/" => 0,
                         "topics/" => 0);

my ($num_abs_url, $num_abs_path, $num_broken, $num_valid, $num_generated) = (0,0,0,0,0);
for (@files) {
    my $filename = $root . $_;
    next unless m!([^/]*)/([^/]*\.md)$!;
    my ($dir, $basename) = ($1, $2);

    open(my $in, "<", $filename) or die "Can't open $filename: $!";
    my $n = 0;
    for my $line (<$in>) {
        $n++;
        my @links = ();
        if ($line =~ /^\[[^\]]+\]:\s*(\S+)/) {
            push @links, $1;
        } else {
            @links = $line =~ /\]\(([^\)]+)\)/g;
        }

        for (@links) {
            if (/^\w+:/) {
                # Skip absolute URL with a scheme.
                $num_abs_url++;
                next;
            }
            next if /^#/;       # Skip links within the page
            s/[\?\#].*$//;      # Strip ?foo and #foo
            if (m!^/!) {
                $num_abs_path++;
                print "$filename:$n: Link with absolute path: $_\n";
                next;
            }

            if (/^$/) {
                print "$filename:$n: Empty? $line\n";
                exit;
            }
            my $target;
            if (m!^\.\./(.*)$!) {
                $target = $1;
            } elsif (m!^\./$!) {
                $target = "$dir/";
            } else {
                $target = "$dir/$_";
            }

            if (!defined $targets{$target}) {
                if (defined $directory_targets{$target}) {
                    $directory_targets{$target}++;
                    $num_generated++;
                    next;
                }
                $num_broken++;
                print "$filename:$n: Broken link: $_\n";
                next;
            }
            $num_valid++;
            $targets{$target}++;
        }
    }
    close $in;
}

# Count orphans
my $num_orphans = 0;
for (keys %targets) {
    $num_orphans++ if $targets{$_} == 0 && /^topics/;
}

print "---\n",
    "Internal absolute links  : $num_abs_path\n",
    "Internal broken links    : $num_broken\n",
    "Links to generated pages : $num_generated\n",
    "Links to existing pages  : $num_valid\n",
    "External links           : $num_abs_url\n",
    "Orphan pages             : $num_orphans\n";
print "---\n";
print "Links to generated pages (not in this repo):\n";
for (sort keys %directory_targets) {
    printf("[%2d] %s\n", $directory_targets{$_}, $_);
}
if ($num_orphans) {
    print "---\n";
    print "Orphans:\n";
    for (sort keys %targets) {
        if ($targets{$_} == 0 && /^topics/) {
            print("  $_\n");
        }
    }
}
print "---\n";

exit($num_broken || $num_abs_path ? 1 : 0);
