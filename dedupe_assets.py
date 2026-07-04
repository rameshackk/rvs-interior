import sys
import os
import hashlib

def file_hash(path, block_size=65536):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(block_size), b''):
            h.update(chunk)
    return h.hexdigest()

def dedupe(dirpath):
    seen = {}
    duplicates = []
    for root, dirs, files in os.walk(dirpath):
        for name in files:
            full = os.path.join(root, name)
            try:
                h = file_hash(full)
            except Exception as e:
                print(f"Skipping {full}: {e}")
                continue
            if h in seen:
                duplicates.append((full, seen[h]))
            else:
                seen[h] = full
    if not duplicates:
        print('No duplicates found.')
        return
    print('Found duplicates:')
    for dup, original in duplicates:
        print(f'DUP: {dup}\n  ORIG: {original}')
    # remove duplicates
    for dup, original in duplicates:
        try:
            os.remove(dup)
            print(f'Removed duplicate: {dup}')
        except Exception as e:
            print(f'Failed to remove {dup}: {e}')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: dedupe_assets.py <assets_dir>')
        sys.exit(1)
    dirpath = sys.argv[1]
    if not os.path.isdir(dirpath):
        print(f'Not a directory: {dirpath}')
        sys.exit(1)
    dedupe(dirpath)
