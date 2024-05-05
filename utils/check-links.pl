#!/usr/bin/perl

#
# Checks for intenal broken links. Checks some other things too, like orphan
# pages (nobody links to the orphan page) and the number of external links.
#

use warnings;
use strict;

my $dry = 1; # dry run (enable for debugging)

my $root = __FILE__ =~ s![^/]*$!!r . "../";
$root =~ s%[^/\.]+/\.\./$%%;
my @files = glob("${root}{topics,commands}/*");

my %targets;
for (@files) {
    s/^$root//;
    $targets{$_} = 0;
}

my %generated_targets = ("commands/" => 0,
                         "clients/" => 0,
                         "modules/" => 0);

my ($num_abs_url, $num_abs_path, $num_broken, $num_valid, $num_generated) = (0,0,0,0,0);
for (@files) {
    my $filename = $root . $_;
    next unless m!([^/]*)/([^/]*\.md)$!;
    my ($dir, $basename) = ($1, $2);

    #print "$dir / $basename\n";
    #exit;

    open(my $in, "<", $filename) or die "Can't open $filename: $!";
    open(my $out, ">", "$filename~~~") or die "Can't create $filename~~~: $!" unless $dry;
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
            if (m!^../(.*)$!) {
                $target = $1;
            } else {
                $target = "$dir/$_";
            }

            if (!defined $targets{$target}) {
                if (defined $generated_targets{$target}) {
                    $generated_targets{$target}++;
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
    close $out unless $dry;
    rename "$filename~~~", $filename unless $dry;
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
for (sort keys %generated_targets) {
    printf("[%2d] %s\n", $generated_targets{$_}, $_);
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
