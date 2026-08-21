#!/bin/bash
# Submit every sitemap URL to IndexNow. Run after any push: bash ping.sh
KEY=$(cat "$(dirname "$0")/indexnow-key.txt")
python3 - "$KEY" <<'PY'
import json, subprocess, re, sys
key=sys.argv[1]
sm=subprocess.run(['curl','-s','https://westernlegal.co.uk/sitemap.xml'],capture_output=True,text=True).stdout
urls=re.findall(r'<loc>(https://[^<]*)</loc>',sm)
open('/tmp/indexnow.json','w').write(json.dumps({"host":"westernlegal.co.uk","key":key,
  "keyLocation":f"https://westernlegal.co.uk/{key}.txt","urlList":urls}))
print(f'submitting {len(urls)} URLs')
for ep in ["https://api.indexnow.org/indexnow","https://www.bing.com/indexnow",
           "https://yandex.com/indexnow","https://search.seznam.cz/indexnow"]:
    r=subprocess.run(['curl','-s','-o','/dev/null','-w','%{http_code}','-X','POST',ep,
      '-H','Content-Type: application/json','--data','@/tmp/indexnow.json'],capture_output=True,text=True).stdout
    print(f'  {ep.split("/")[2]:24s} {r}')
PY
