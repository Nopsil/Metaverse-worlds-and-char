#!/usr/bin/env python3
"""Final comprehensive verification: check all 131 YAML files + 130 synced entries."""
import json
import os
import re

JSON_PATH = r'C:\Users\nopsi\Desktop\metaverse工程\card\CHUNITHM-Metaverse.json'
YAML_ROOT = r'C:\Users\nopsi\Desktop\metaverse工程\backup\20260710_225819\世界书源文件'

with open(JSON_PATH, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Collect all YAML files
all_yaml = []
for root, dirs, files in os.walk(YAML_ROOT):
    for f in files:
        if f.endswith('.yaml'):
            all_yaml.append(os.path.relpath(os.path.join(root, f), YAML_ROOT))

print(f"Total YAML files: {len(all_yaml)}")
print(f"Total JSON entries: {len(data['entries'])}")

# Verify each YAML file has content
empty = []
for rel in all_yaml:
    path = os.path.join(YAML_ROOT, rel)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read().strip()
    if not content:
        empty.append(rel)
    # Check for leftover XML tags
    if '<npc' in content or '</npc>' in content:
        print(f"  WARNING: XML tags in {rel}")

if empty:
    print(f"\nEMPTY FILES ({len(empty)}):")
    for e in empty:
        print(f"  {e}")
else:
    print("No empty files ✓")

# Check that no XML tags remain
has_xml = []
for rel in all_yaml:
    path = os.path.join(YAML_ROOT, rel)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    if '<npc' in content or '</npc>' in content:
        has_xml.append(rel)

if has_xml:
    print(f"\nFILES WITH XML TAGS ({len(has_xml)}):")
    for x in has_xml:
        print(f"  {x}")
else:
    print("No leftover XML tags ✓")

# Summary of categories
npc_count = len([f for f in all_yaml if f.startswith('NPC/')])
geo_count = len([f for f in all_yaml if f.startswith('地理/')])
other = len(all_yaml) - npc_count - geo_count
print(f"\nBreakdown: NPC={npc_count}, 地理={geo_count}, Other={other}")
print("\nVerification complete!")
