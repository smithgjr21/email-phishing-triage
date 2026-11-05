#!/usr/bin/env python3
"""Parse a saved .eml and generate a cautious indicator summary."""
import argparse
import json
import re
from email import policy
from email.parser import BytesParser
from pathlib import Path
from urllib.parse import urlsplit

URL_RE=re.compile(r'https?://[^\s<>"\']+',re.IGNORECASE)
def inspect(path):
    with Path(path).open('rb') as stream:
        mail=BytesParser(policy=policy.default).parse(stream)
    from_address=str(mail.get('From',''))
    reply_to=str(mail.get('Reply-To',''))
    subjects=str(mail.get('Subject',''))
    attachments=[];urls=[]
    for part in mail.walk():
        if part.is_multipart():continue
        if part.get_filename():
            attachments.append({'filename':part.get_filename(),'content_type':part.get_content_type()})
        if part.get_content_type() in ('text/plain','text/html'):
            try:
                payload=part.get_content()
                if isinstance(payload,str):urls.extend(URL_RE.findall(payload))
            except (UnicodeDecodeError,LookupError,ValueError):pass
    urls=sorted(set(u.rstrip('.,);') for u in urls))
    indicators=[]
    if reply_to and from_address and reply_to.casefold()!=from_address.casefold():
        indicators.append('Reply-To differs from From (manual verification required)')
    if any(a['filename'].lower().endswith(('.exe','.js','.vbs','.scr')) for a in attachments):
        indicators.append('Attachment has a potentially executable extension')
    if any(urlsplit(u).scheme=='http' for u in urls):
        indicators.append('Unencrypted HTTP URL in message')
    return {'subject':subjects,'from':from_address,'reply_to':reply_to,'date':str(mail.get('Date','')),
            'message_id':str(mail.get('Message-ID','')),'urls':urls,'attachments':attachments,'review_indicators':indicators,
            'note':'Indicators are leads, not conclusive evidence of phishing; authentication and sender identity not validated.'}

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('eml');parser.add_argument('--output');args=parser.parse_args()
    report=json.dumps(inspect(args.eml),indent=2)
    if args.output:Path(args.output).write_text(report+'\n',encoding='utf-8')
    print(report)
if __name__=='__main__':main()
