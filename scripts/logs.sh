#!/usr/bin/env bash
source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/_lib.sh"

if [ $# -eq 0 ]; then
  dc logs -f --tail=200
else
  dc logs -f --tail=200 "$@"
fi