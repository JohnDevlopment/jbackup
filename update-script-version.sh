#!/bin/bash

declare -r ROOTDIR=$(dirname $(realpath "$0"))
declare -r BASENAME=$(basename $(realpath "$0"))

tempfiles=()

## usage: assert EXPRESSION [MESSAGE]
function assert {
    if ! eval "$1"; then
	local prog lineno
	lineno=$(caller | awk '{ print $1; }')
	prog=$(realpath $(caller | awk '{ print $2; }'))

	echo -n "assertion failed: '$1'" >&2
	if [ -n "$2" ]; then
	    echo ", $2 ('$prog' line $lineno)" >&2
	else
	    echo " ('$prog' line $lineno)" >&2
	fi
	exit 1
    fi
}

## usage: die MSG [CODE]
function die {
    echo -e "$BASENAME: $1" >&2
    exit ${2:-1}
}

## usage: make_temp [-m MODE]
function make_temp {
    while getopts :m: OPT; do
	case $OPT in
	    m)
		local mode="$OPTARG"
		;;
	    *)
		die "usage: $0 [-m MODE]" 2
	esac
    done
    shift $(( OPTIND - 1 ))
    OPTIND=1

    local tmpfile=$(mktemp)

    if [ -n "$mode" ]; then
	chmod $mode $tmpfile || {
	    rm $tmpfile
	    return 1
	}
    fi

    tempfiles+=("$tmpfile")
    echo $tmpfile
}

## usage: __cleanup
function __cleanup {
    rm -fv "${tempfiles[@]}"
}

trap __cleanup EXIT

# Script that reads from STDIN and extracts the version number
# STDIN is either from pyproject.toml or __init__.py
perl_verstdin=$(make_temp -m +x)
cat > $perl_verstdin <<"EOF"
#!/usr/bin/env perl
use warnings;
use strict;

my $text = do {
    local $/;
    <STDIN>
};

die "did not find version string"
    unless ($text =~ m/^(?:__version__|version)\s*=\s*"(.+)"/m);

print $1;
EOF

Package=${1:?provide the package name}

test -f pyproject.toml || die "pyproject.toml does not exist"
test -f $Package/__init__.py || die "$Package/__init__.py does not exist"

newversion=$($perl_verstdin < pyproject.toml)
oldversion=$($perl_verstdin < $Package/__init__.py)

echo "The old version is $oldversion, and the new version is $newversion"

perl_replacever=$(make_temp -m +x)
cat > $perl_replacever <<"EOF"
#!/usr/bin/env perl

use warnings;
use strict;

my $text = do {
    local $/;
    <STDIN>
};

my $version = shift || die "missing arg: version";

die "failed to substitute text"
    unless ($text =~ s/^(__version__\s*=\s*)"(.+)"/$1"$version"/m);

print $text;
EOF

newtext=$($perl_replacever $newversion < $Package/__init__.py)
if [ -n "$newtext" ]; then
    echo "$newtext" > $Package/__init__.py
fi
