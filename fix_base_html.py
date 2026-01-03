#!/usr/bin/env python3
"""Convert base.html from UTF-16 to UTF-8."""
import sys

filepath = 'templates/base.html'

# Read as UTF-16 LE (has FF FE BOM)
with open(filepath, 'rb') as f:
    content = f.read()

# Remove UTF-16 BOM if present
if content.startswith(b'\xff\xfe'):
    content = content[2:]

# Decode from UTF-16 LE
try:
    text = content.decode('utf-16-le')
except UnicodeDecodeError:
    # Try UTF-16 BE
    text = content.decode('utf-16-be')

# Write as UTF-8 without BOM
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(text)

print(f"Converted {filepath} from UTF-16 to UTF-8")

# Verify
with open(filepath, 'rb') as f:
    verify = f.read()
    print(f"Verification: Has BOM={verify.startswith(b'\\xef\\xbb\\xbf')}, Has FF={b'\\xff' in verify}")
    print(f"First 50 chars: {verify[:50].decode('utf-8', errors='ignore')}")

