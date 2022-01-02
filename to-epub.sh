#!/usr/bin/bash

file="$1"
title="$2"

echo "Start parsing $file..."

jq -r '.title' "$file.jl" | \
  awk '{print $1}' | \
  cut -c 2- | \
  rev | \
  cut -c 2- | \
  rev > "temp.index.txt"

paste -d' ' <(cat temp.index.txt) <(cat "$file.jl") > "$file.index.txt"

echo "Title $title..."
printf "%% %s\n" "$title" > "$file.txt"

sort -n "$file.index.txt" | \
  sed 's/^[0-9]* //' | \
  jq -r '("\n# " + .title + "\n\n" + .content + "\n")' \
  >> "$file.txt"

pandoc "$file.txt" -o "$title.epub"

rm temp.index.txt
rm "$file.index.txt"
