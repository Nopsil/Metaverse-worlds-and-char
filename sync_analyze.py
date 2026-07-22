#!/usr/bin/env python3
"""Analyze JSON entries and YAML files, produce mapping."""
import json
import os
import re
from pathlib import Path

JSON_PATH = r'C:\Users\nopsi\Desktop\metaverse工程\card\CHUNITHM-Metaverse.json'
YAML_ROOT = r'C:\Users\nopsi\Desktop\metaverse工程\backup\20260710_225819\世界书源文件'

with open(JSON_PATH, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Collect all YAML files
yaml_files = {}
for root, dirs, files in os.walk(YAML_ROOT):
    for f in files:
        if f.endswith('.yaml'):
            full = os.path.join(root, f)
            rel = os.path.relpath(full, YAML_ROOT)
            yaml_files[f] = full

print(f"Total YAML files: {len(yaml_files)}")
print(f"Total JSON entries: {len(data['entries'])}")

# List all JSON entries with their comment and content preview
for k in sorted(data['entries'].keys(), key=int):
    v = data['entries'][k]
    c = v['comment']
    ct = v['content'][:120].replace('\n', '\\n')
    has_npc = '<npc' in v['content']
    has_xml = '---' in v['content'] and '<npc' in v['content']
    print(f'\n--- Entry {k}: comment="{c}" has_npc={has_npc} ---')
    print(f'  Content preview: {ct}')
    if has_npc:
        # Extract name from <npc name="...">
        m = re.search(r'<npc[^>]*name="([^"]*)"', v['content'])
        if m:
            print(f'  NPC name: {m.group(1)}')
