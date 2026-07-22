#!/usr/bin/env python3
"""Extract and print full content of a few NPC entries for analysis."""
import json

JSON_PATH = r'C:\Users\nopsi\Desktop\metaverse工程\card\CHUNITHM-Metaverse.json'

with open(JSON_PATH, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Print full content of entries 22 (贝尔泽布特), 37 (阿斯托尔 - markdown format), 18 (狄安娜)
for eid in ['22', '37', '18', '30', '27']:
    v = data['entries'][eid]
    print(f"\n{'='*60}")
    print(f"Entry {eid}: comment={v['comment']}")
    print(f"Content ({len(v['content'])} chars):")
    print(v['content'])
    print(f"{'='*60}")
