#!/usr/bin/env python3
"""
Batch check and convert all HTML template files to UTF-8 encoding.

This script:
1. Scans the templates directory for all .html files
2. Detects encoding issues (UTF-16, BOM, FF bytes)
3. Converts all files to clean UTF-8 without BOM
4. Preserves all content including Jinja2 tags
5. Reports any issues found
"""

import os
import sys
from pathlib import Path

# Template directory
TEMPLATES_DIR = Path("templates")

def detect_encoding(filepath):
    """Detect the encoding of a file."""
    with open(filepath, 'rb') as f:
        content = f.read()
    
    issues = []
    
    # Check for UTF-16 BOM
    if content.startswith(b'\xff\xfe'):
        return 'utf-16-le', issues + ['UTF-16 LE BOM detected']
    elif content.startswith(b'\xfe\xff'):
        return 'utf-16-be', issues + ['UTF-16 BE BOM detected']
    
    # Check for UTF-8 BOM
    if content.startswith(b'\xef\xbb\xbf'):
        issues.append('UTF-8 BOM detected')
    
    # Check for FF bytes (corruption indicator)
    if b'\xff' in content[:100]:
        issues.append('FF bytes found in first 100 bytes (possible corruption)')
    
    # Try to detect UTF-16 by pattern (null bytes between characters)
    if len(content) > 2 and content[0] != 0 and content[1] == 0:
        # Check if it's UTF-16 LE pattern
        sample = content[:100]
        if len(sample) % 2 == 0:
            # Check if every other byte is null (UTF-16 LE pattern)
            null_count = sum(1 for i in range(1, min(50, len(sample)), 2) if sample[i] == 0)
            if null_count > 20:  # More than 40% null bytes in odd positions
                return 'utf-16-le', issues + ['UTF-16 LE pattern detected (no BOM)']
    
    # Default to UTF-8
    return 'utf-8', issues

def convert_to_utf8(filepath, source_encoding):
    """Convert a file to UTF-8 without BOM."""
    try:
        # Read with detected encoding
        if source_encoding == 'utf-16-le':
            with open(filepath, 'rb') as f:
                content = f.read()
                # Remove BOM if present
                if content.startswith(b'\xff\xfe'):
                    content = content[2:]
                text = content.decode('utf-16-le')
        elif source_encoding == 'utf-16-be':
            with open(filepath, 'rb') as f:
                content = f.read()
                # Remove BOM if present
                if content.startswith(b'\xfe\xff'):
                    content = content[2:]
                text = content.decode('utf-16-be')
        else:
            # UTF-8 - just remove BOM if present
            with open(filepath, 'rb') as f:
                content = f.read()
                if content.startswith(b'\xef\xbb\xbf'):
                    content = content[3:]
                text = content.decode('utf-8', errors='replace')
        
        # Write as UTF-8 without BOM
        with open(filepath, 'w', encoding='utf-8', newline='\n') as f:
            f.write(text)
        
        return True, None
    except Exception as e:
        return False, str(e)

def verify_utf8(filepath):
    """Verify a file is valid UTF-8."""
    try:
        with open(filepath, 'rb') as f:
            content = f.read()
        
        # Check for BOM
        if content.startswith(b'\xef\xbb\xbf'):
            return False, 'Still has UTF-8 BOM'
        
        # Check for FF bytes (corruption)
        if b'\xff' in content[:100]:
            return False, 'Still has FF bytes in first 100 bytes'
        
        # Try to decode as UTF-8
        content.decode('utf-8')
        
        return True, None
    except UnicodeDecodeError as e:
        return False, f'Not valid UTF-8: {e}'
    except Exception as e:
        return False, f'Error: {e}'

def main():
    """Main function to process all template files."""
    if not TEMPLATES_DIR.exists():
        print(f"Error: Templates directory '{TEMPLATES_DIR}' not found!")
        sys.exit(1)
    
    # Find all HTML files
    html_files = list(TEMPLATES_DIR.glob("*.html"))
    
    if not html_files:
        print(f"No HTML files found in {TEMPLATES_DIR}")
        return
    
    print(f"Found {len(html_files)} HTML template file(s)")
    print("=" * 70)
    
    results = {
        'total': len(html_files),
        'clean': 0,
        'converted': 0,
        'errors': 0,
        'issues': []
    }
    
    for filepath in sorted(html_files):
        print(f"\nProcessing: {filepath.name}")
        
        # Detect encoding
        encoding, issues = detect_encoding(filepath)
        
        if issues:
            print(f"  Issues found: {', '.join(issues)}")
            results['issues'].append((filepath.name, issues))
        
        # If already UTF-8 and no issues, skip
        if encoding == 'utf-8' and not issues:
            # Verify it's clean
            is_valid, error = verify_utf8(filepath)
        if is_valid:
            print(f"  [OK] Already clean UTF-8")
            results['clean'] += 1
            continue
        else:
            print(f"  [WARN] Verification failed: {error}")
        
        # Convert to UTF-8
        print(f"  Converting from {encoding} to UTF-8...")
        success, error = convert_to_utf8(filepath, encoding)
        
        if not success:
            print(f"  [ERROR] Conversion failed: {error}")
            results['errors'] += 1
            continue
        
        # Verify conversion
        is_valid, verify_error = verify_utf8(filepath)
        if is_valid:
            print(f"  [OK] Successfully converted to clean UTF-8")
            results['converted'] += 1
        else:
            print(f"  [WARN] Conversion completed but verification failed: {verify_error}")
            results['errors'] += 1
    
    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Total files: {results['total']}")
    print(f"Already clean: {results['clean']}")
    print(f"Converted: {results['converted']}")
    print(f"Errors: {results['errors']}")
    
    if results['issues']:
        print(f"\nFiles with issues found:")
        for filename, issues in results['issues']:
            print(f"  - {filename}: {', '.join(issues)}")
    
    if results['errors'] > 0:
        print("\n[WARN] Some files had errors. Please review manually.")
        sys.exit(1)
    else:
        print("\n[SUCCESS] All template files are now clean UTF-8!")

if __name__ == "__main__":
    main()

