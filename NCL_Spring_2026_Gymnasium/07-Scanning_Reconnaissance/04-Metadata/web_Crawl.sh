#!/usr/bin/env bash

BASE="http://metadata.services.cityinthe.cloud:1338/latest"

# simple recursive crawler for "directory listing" style endpoints
crawl() {
  local path="$1"
  local body
  body=$(curl -s "$BASE/$path")

  # if it's not a directory listing (i.e., no trailing slashes/child keys), just print it
  if ! echo "$body" | grep -qE '^[A-Za-z0-9._-]+/?$'; then
    echo "$path: $body"
    return
  fi

  # directory: iterate children
  while IFS= read -r child; do
    [ -z "$child" ] && continue
    crawl "${path%/}/$child"
  done <<< "$body"
}

# Crawl meta-data and dynamic, then search for the flag pattern
(
  crawl "meta-data/"
  crawl "dynamic/"
  echo "user-data: $(curl -s "$BASE/user-data")"
) | tee all_metadata.txt

# Search for flags (SKY or NCL format)
grep -Eo '(SKY|NCL)-[A-Z]{4}-[0-9]{4}' all_metadata.txt | sort -u
