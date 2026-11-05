# Digital Forensics Portfolio Project

> Educational demonstration using **synthetic evidence only**. No real person's data is included. Results require analyst validation and should not be treated as proof of wrongdoing.

## Skills demonstrated
RFC email parsing, header review, URL and attachment extraction, indicator reporting, defensible investigative limits.

## Run (Python 3.9+; standard library only)
```bash
python email_triage.py samples/training_message.eml --output report.json
python -m unittest discover -s tests -v
```

## Evidence handling
All example files are fictional. Preserve originals, verify hashes, document timestamps/time zones, and maintain a chain of custody before using any process in a real investigation.

## Limitations
This is **triage**, not attribution or a phishing verdict. It does not perform SPF/DKIM/DMARC verification, URL reputation checks, malware execution, or sandboxing. Never open unknown links or attachments.

## Suggested next steps
Add screenshots from your own run, a sample investigator report, and a brief explanation of what you learned. Only list forensic tools you have personally operated.
