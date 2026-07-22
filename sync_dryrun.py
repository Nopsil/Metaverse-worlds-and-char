#!/usr/bin/env python3
"""Dry run: test matching without writing files."""
import json
import os
import re

JSON_PATH = r'C:\Users\nopsi\Desktop\metaverse工程\card\CHUNITHM-Metaverse.json'
YAML_ROOT = r'C:\Users\nopsi\Desktop\metaverse工程\backup\20260710_225819\世界书源文件'

with open(JSON_PATH, 'r', encoding='utf-8') as f:
    data = json.load(f)

entries = data['entries']

# Index NPC YAML files
npc_dir = os.path.join(YAML_ROOT, 'NPC')
npc_files = [f for f in os.listdir(npc_dir) if f.endswith('.yaml')]

def find_npc_yaml(comment):
    for fname in npc_files:
        basename = fname[:-5]
        parts = basename.split('_', 1)
        char_name = parts[1] if len(parts) > 1 else basename
        if char_name == comment:
            return fname
    # Try with dot variations
    for fname in npc_files:
        basename = fname[:-5]
        parts = basename.split('_', 1)
        char_name = parts[1] if len(parts) > 1 else basename
        if char_name.replace('_', '·') == comment:
            return fname
        if char_name.replace('·', '_') == comment:
            return fname
    return None

# Known non-NPC entries
non_npc = {'世界设定', '时间线', '系统规则', '扮演准则',
           'Metaverse核心层', '中间层世界群', '最外周部', '地上世界',
           '势力_框架主脑', '势力_工厂', '势力_MIR系列', '势力_涅墨西斯',
           '势力_革新者', '势力_LOGOS', '势力_拾荒者', '势力_IDC',
           '势力_恩迪商会', '势力_独立旅人', '卡斯比裂谷', '安特路亚'}

matched = 0
unmatched = []
for eid in sorted(entries.keys(), key=int):
    entry = entries[eid]
    comment = entry['comment']
    has_npc = '<npc' in entry['content']
    
    if comment in non_npc:
        print(f"[{eid}] {comment} → non-NPC (has_npc={has_npc})")
        matched += 1
        continue
    
    yaml_name = find_npc_yaml(comment)
    if yaml_name:
        print(f"[{eid}] {comment} → NPC/{yaml_name} ✓")
        matched += 1
    else:
        print(f"[{eid}] {comment} → NO MATCH ✗")
        unmatched.append(comment)

print(f"\nMatched: {matched}, Unmatched: {len(unmatched)}")
if unmatched:
    print("Unmatched NPCs:")
    for u in unmatched:
        print(f"  - {u}")
    print("\nAll NPC YAML files:")
    for f in sorted(npc_files):
        basename = f[:-5]
        parts = basename.split('_', 1)
        print(f"  {f} → char='{parts[1] if len(parts) > 1 else basename}'")
