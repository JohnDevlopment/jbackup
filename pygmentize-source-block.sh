#!/bin/bash

declare -r BASENAME=$(basename $(realpath "$0"))

## usage: die MSG [CODE]
die() {
    echo -e "$BASENAME: $1" >&2
    exit ${2:-1}
}

# If any of the arguments are -h, print help and exit
for arg in "$@"; do
    if [ "$arg" == "-h" ] || [ "$arg" == "--help" ]; then
	cat <<EOF
Usage: $BASENAME [LEXER]
EOF
	exit
    fi
done

# die if $EDITOR is not set
[ -n "$EDITOR" ] || die "\$EDITOR not set"

# Temp file
tmpfile=$(mktemp)
trap "rm $tmpfile" EXIT

# No arguments are provided
if [[ -z $1 ]]; then
    # Input file prompt using fzf
    ifile=$(fzf)
    if [ ! -f "$ifile" ]; then
	die "$ifile does not exist"
    fi

    # Guess file type from extension and set lexer
    case "$ifile" in
	*.py)
	    lexer=python
	    ;;
	*)
	    die "File type not supported"
    esac

    # Copy content to temp file
    cat "$ifile" > "$tmpfile"
else
    # Argument is a lexer
    lexer="$1"
fi

# Output file
read -e -p 'Output file: ' ofile
test -n "$ofile" || die "File not provided"

# Edit temp file
$EDITOR "$tmpfile"

pygmentize -l $lexer -o "$ofile" $tmpfile
