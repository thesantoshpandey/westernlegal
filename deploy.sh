#!/bin/bash
# The only deploy path. Runs the audit, pushes to main, pings the search engines.
set -e
cd "$(dirname "$0")"
echo "== audit =="
python3 audit.py || { echo "AUDIT FAILED. Nothing deployed."; exit 1; }
echo "== push =="
git add -A
git commit -m "${1:-Site update}" || echo "nothing to commit"
git push origin main
echo "== waiting for Vercel =="
sleep 45
echo "== ping search engines =="
bash ping.sh
echo "== done =="
