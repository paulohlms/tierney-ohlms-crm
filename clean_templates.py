#!/usr/bin/env python3
"""Clean template files - remove BOM and ensure UTF-8 encoding."""
import os

files_to_clean = [
    'templates/client_detail.html',
    'templates/timesheets_list.html',
    'templates/timesheet_form.html',
    'templates/settings.html'
]

for filepath in files_to_clean:
    if not os.path.exists(filepath):
        print(f"Skipping {filepath} - file does not exist")
        continue
    
    # Read file content
    try:
        with open(filepath, 'rb') as f:
            content = f.read()
        
        # Remove BOM if present
        if content.startswith(b'\xef\xbb\xbf'):
            content = content[3:]
            print(f"{filepath}: Removed BOM")
        
        # Check for FF bytes in first 100 bytes
        if b'\xff' in content[:100]:
            print(f"{filepath}: WARNING - Contains FF bytes in first 100 bytes")
            # Try to decode as UTF-16 and re-encode as UTF-8
            try:
                # Try UTF-16 LE
                text = content.decode('utf-16-le')
                content = text.encode('utf-8')
                print(f"{filepath}: Converted from UTF-16 LE to UTF-8")
            except:
                try:
                    # Try UTF-16 BE
                    text = content.decode('utf-16-be')
                    content = text.encode('utf-8')
                    print(f"{filepath}: Converted from UTF-16 BE to UTF-8")
                except:
                    # Try to read as text and re-encode
                    try:
                        text = content.decode('utf-8', errors='ignore')
                        content = text.encode('utf-8')
                        print(f"{filepath}: Cleaned UTF-8 encoding")
                    except Exception as e:
                        print(f"{filepath}: ERROR - Could not clean: {e}")
                        continue
        
        # Write back as UTF-8 without BOM
        with open(filepath, 'wb') as f:
            f.write(content)
        
        print(f"{filepath}: Cleaned and saved as UTF-8")
        
    except Exception as e:
        print(f"{filepath}: ERROR - {e}")

print("Done cleaning template files")

