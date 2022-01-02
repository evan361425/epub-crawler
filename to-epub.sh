#!/usr/bin/bash

file="$1"
title="$2"

echo "Start parsing $file..."

echo "Title $title..."
printf "%% %s\n" "$title" > "$file.txt"

function 69shu() {
  jq -r '.title' "$file.jl" | \
    sed 's/\..*//'
}

function wfxs() {
  jq -r '.title' "$file.jl" | \
    awk '{print $1}' | \
    cut -c 2- | \
    rev | \
    cut -c 2- | \
    rev
}

paste -d' ' <(69shu) <(cat "$file.jl") | \
  sort -n | \
  sed 's/^[0-9]* //' | \
  jq -r '("\n# " + .title + "\n\n" + .content + "\n")' \
  >> "$file.txt"

opencc -i "$file.txt" -c s2twp.json | pandoc -o "$title.epub"
