#!/bin/bash
# Submit sitemap URLs to the Bing Webmaster JSON/REST API.
# Requires BING_API_KEY in the environment. Never commit the key.
# Usage: BING_API_KEY=xxx bash bing.sh   [or export it in your shell profile]
if [ -z "$BING_API_KEY" ]; then
  echo "BING_API_KEY not set, skipping Bing submission"
  exit 0
fi
python3 - "$BING_API_KEY" <<'PY'
import json, subprocess, re, sys
key=sys.argv[1]
site="https://westernlegal.co.uk"
q=subprocess.run(['curl','-s',f'https://ssl.bing.com/webmaster/api.svc/json/GetUrlSubmissionQuota?siteUrl={site}&apikey={key}'.replace('{site}',site).replace('{key}',key)],capture_output=True,text=True).stdout
try:
    daily=json.loads(q)['d']['DailyQuota']
except Exception:
    print('could not read quota:',q[:120]); daily=0
print(f'Bing daily quota remaining: {daily}')
if daily<1:
    print('no quota left today, skipping'); raise SystemExit(0)
sm=subprocess.run(['curl','-s',site+'/sitemap.xml'],capture_output=True,text=True).stdout
urls=re.findall(r'<loc>(https://[^<]*)</loc>',sm)
urls=urls[:daily]
open('/tmp/bing.json','w').write(json.dumps({"siteUrl":site,"urlList":urls}))
r=subprocess.run(['curl','-s','-w','\n%{http_code}','-X','POST',
  f'https://ssl.bing.com/webmaster/api.svc/json/SubmitUrlBatch?apikey={key}'.replace('{key}',key),
  '-H','Content-Type: application/json; charset=utf-8','--data','@/tmp/bing.json'],capture_output=True,text=True).stdout
print(f'submitted {len(urls)} URLs -> HTTP {r.strip().splitlines()[-1]}')
PY
