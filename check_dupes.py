#!/usr/bin/env python3
"""Check which NPC files were written to by specific entries."""
import json

JSON_PATH = r'C:\Users\nopsi\Desktop\metaverse工程\card\CHUNITHM-Metaverse.json'
with open(JSON_PATH, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Check entries that share similar names
check = ['拔示巴', '尼亚拔示巴', '拔示巴Metaverse', '尼亚', 
         '索罗', '索罗Metaverse', '米斯拉', '米斯拉Metaverse',
         '威廉', '威廉2', '艾莉尼', '艾莉尼0', '安克', '安克0']

for name in check:
    for eid, v in data['entries'].items():
        if v['comment'] == name:
            has_npc = '<npc' in v['content']
            m = None
            if has_npc:
                import re
                m = re.search(r'<npc[^>]*name="([^"]*)"', v['content'])
            print(f"[{eid}] comment='{name}' npc_name='{m.group(1) if m else 'N/A'}' content_len={len(v['content'])}")
