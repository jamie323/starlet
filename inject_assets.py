#!/usr/bin/env python3
"""Inject updated assets into the game by patching autoFetch()."""

# This script demonstrates how to merge the updated JSON files.
# In the browser, we'll modify index.html to load the updated files.

import json
from pathlib import Path

def merge_assets():
    """Merge all asset JSON files into a single game data object."""
    
    # Load base structure
    with open('starlet-v6-part1.json') as f:
        merged = json.load(f)
    
    # Load and merge other parts
    for part_file in ['starlet-v6-part2-updated.json', 'starlet-v6-part3.json', 'starlet-v6-part4-updated.json']:
        with open(part_file) as f:
            part_data = json.load(f)
        
        if 'assets' in part_data:
            if 'assets' not in merged:
                merged['assets'] = {}
            merged['assets'].update(part_data['assets'])
    
    return merged

if __name__ == '__main__':
    data = merge_assets()
    print(json.dumps(data, indent=2))
