#!/bin/sh
cp /data/memory_source.db /data/memory.db 2>/dev/null
rm -rf /data/clean
mkdir /data/clean

for f in /workspace/*.md; do
  [ -f "$f" ] && { cat "$f" > "/data/clean/$(basename $f)"; }
done

for dir in memory hooks workflows; do
  [ -d "/workspace/$dir" ] && (
    cd /workspace && find "$dir" -maxdepth 3 -type f \( -name "*.md" -o -name "*.yaml" -o -name "*.json" \) | while read f; do
      mkdir -p "/data/clean/$(dirname $f)"
      cat "$f" > "/data/clean/$f"
    done
  )
done

exec /usr/local/bin/sqlpage
