#!/usr/bin/env python3
"""Verify all synced files have correct content."""
import json
import os
import re

JSON_PATH = r'C:\Users\nopsi\Desktop\metaverse工程\card\CHUNITHM-Metaverse.json'
YAML_ROOT = r'C:\Users\nopsi\Desktop\metaverse工程\backup\20260710_225819\世界书源文件'

with open(JSON_PATH, 'r', encoding='utf-8') as f:
    data = json.load(f)

npc_dir = os.path.join(YAML_ROOT, 'NPC')

def find_npc_yaml(comment):
    for fname in os.listdir(npc_dir):
        if not fname.endswith('.yaml'):
            continue
        basename = fname[:-5]
        parts = basename.split('_', 1)
        char_name = parts[1] if len(parts) > 1 else basename
        if char_name == comment:
            return os.path.join(npc_dir, fname)
    return None

# Check potentially problematic entries where names overlap
check_list = [
    ('25', '拔示巴', '地上真人篇_拔示巴'),
    ('125', '尼亚拔示巴', '乐园事变_尼亚拔示巴'),
    ('128', '拔示巴Metaverse', '乐园事变_拔示巴Metaverse'),
    ('27', '威廉', '次元放浪记_威廉'),
    ('111', '威廉2', '次元放浪记_威廉2'),
    ('26', '艾莉尼', '次元放浪记_艾莉尼'),
    ('112', '艾莉尼0', '次元放浪记_艾莉尼0'),
    ('38', '安克', '次元放浪记_安克'),
    ('113', '安克0', '次元放浪记_安克0'),
]

errors = []
for eid, comment, expected_fname in check_list:
    v = data['entries'][eid]
    json_name = ''
    if '<npc' in v['content']:
        m = re.search(r'<npc[^>]*name="([^"]*)"', v['content'])
        if m:
            json_name = m.group(1)
    
    yaml_path = find_npc_yaml(comment)
    yaml_fname = os.path.basename(yaml_path)[:-5] if yaml_path else 'NOT FOUND'
    
    match_ok = yaml_fname == expected_fname
    
    # Read first few lines of YAML
    yaml_preview = ''
    if yaml_path and os.path.exists(yaml_path):
        with open(yaml_path, 'r', encoding='utf-8') as f:
            yaml_preview = f.readline().strip()
    
    status = '✓' if match_ok else '✗ MISMATCH'
    print(f"[{eid}] comment='{comment}' npc_name='{json_name}' expected='{expected_fname}' actual='{yaml_fname}' {status} first_line='{yaml_preview}'")
    
    if not match_ok:
        errors.append(f"{comment}: expected {expected_fname}, got {yaml_fname}")

if errors:
    print(f"\n{len(errors)} ERRORS:")
    for e in errors:
        print(f"  {e}")
else:
    print("\nAll checks passed!")
