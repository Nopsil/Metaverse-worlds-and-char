import json, os, re

# Load existing state
with open(r'c:\Users\nopsi\cards\CHUNITHM-Metaverse\tavern-cards-state.json', 'r', encoding='utf-8') as f:
    state = json.load(f)

# Change project name
state['projectName'] = 'Metaverse-New'
state['worldbookName'] = 'Metaverse-New'

# ── Organize NPCs by chapter ──
npc_entries = state['entryManifest'].get('NPC', {})

chapters = {}
for entry_name, entry in npc_entries.items():
    # Extract chapter from entry name like [地上真人篇]蕾娜
    match = re.match(r'^\[(.+?)\](.+)', entry_name)
    if match:
        chapter = match.group(1)
        char_name = match.group(2)
    else:
        chapter = '其他'
        char_name = entry_name

    if chapter not in chapters:
        chapters[chapter] = {}
    
    # Clean keywords: remove multi-character generic triggers, add character-specific ones
    keywords = entry.get('keywords', [])
    
    # Remove overly generic cross-chapter triggers
    generic_triggers = {
        '涅墨西斯', '框架主脑', '最古', 'ES计划', '归还者', '卫士',
        '革新者', '指导者', '混沌七器', '工厂', '三贤者', 'BOT',
        '拾荒者', 'IDC', 'EXILE', '归还种', '同伴', '战友'
    }
    cleaned_keywords = [k for k in keywords if k not in generic_triggers]
    
    # Only keep character-specific triggers
    # If all were removed, add the character name itself
    if not cleaned_keywords:
        cleaned_keywords = [char_name]
    
    # Also convert entry title to use character name
    new_entry_name = char_name
    
    # Fix trigger words for multi-character entries
    # Ensure each character has unique identifying triggers
    chapters[chapter][new_entry_name] = {
        'path': entry.get('path', ''),
        'keywords': cleaned_keywords,
        'uid': entry.get('uid', 0),
        'enabled': entry.get('enabled', True),
        'strategy': entry.get('strategy', {'type': 'constant'}),
        'position': entry.get('position', {'type': 'before_character_definition', 'order': 10})
    }

# ── Build new entry manifest ──
new_manifest = {}

# Keep 世界观 and 时间线 and 地理
for cat in ['世界观', '时间线', '地理']:
    if cat in state['entryManifest']:
        entries = state['entryManifest'][cat]
        # Fix entries in these categories too
        for name, entry in entries.items():
            # Clean generic triggers
            if 'keywords' in entry:
                entry['keywords'] = [k for k in entry['keywords'] if k not in {'涅墨西斯', '框架主脑', '最古', '归还者', '真人', '殖民地', '归还者', '同伴', '战友'}]
                if not entry['keywords']:
                    entry['keywords'] = [name]
        new_manifest[cat] = entries

# Add chapters as categories
for chapter, entries in sorted(chapters.items()):
    cat_name = f'{chapter}角色'
    new_manifest[cat_name] = entries

# ── Update chapter order ──
chapter_order = [
    '旧人类战争篇', '电脑世界篇', '地上真人篇', '地上新人篇',
    '乐园事变', '后日谈', '新世界篇', '次元放浪记',
    '外传', '其他'
]

new_type_lists = {
    'before_char': ['世界观', '时间线', '地理'],
    'after_char': [f'{ch}角色' for ch in chapter_order if f'{ch}角色' in new_manifest],
    'depth': []
}

new_strategy_thresholds = {
    '世界观': 'Infinity',
    '时间线': 'Infinity',
    '地理': {'region': {'threshold': 4, 'required': False}, 'scene': {'threshold': 4, 'required': False}, 'faction': {'threshold': 4, 'required': False}}
}

for chapter in chapter_order:
    cat = f'{chapter}角色'
    if cat in new_manifest:
        count = len(new_manifest[cat])
        new_strategy_thresholds[cat] = count

state['entryManifest'] = new_manifest
state['typeLists'] = new_type_lists
state['strategyThresholds'] = new_strategy_thresholds

# Remove depth_defaults that reference removed categories
state['depth_defaults'] = {'role': 'system', 'depth': 0}

# Make absolute paths relative (forge needs relative from project dir)
for cat, entries in state['entryManifest'].items():
    for name, entry in list(entries.items()):
        if entry.get('path'):
            # Convert to relative path from new_card/
            rel = entry['path'].replace(
                r'c:\Users\nopsi\cards\CHUNITHM-Metaverse\世界书',
                r'..\..\cards\CHUNITHM-Metaverse\世界书'
            ).replace('\\', '/')
            entry['path'] = rel

out_path = r'c:\Users\nopsi\Desktop\skill项目\new_card\tavern-cards-state.json'
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(state, f, ensure_ascii=False, indent=2)

# ── Print summary ──
print('=== 世界书条目重组织完成 ===\n')
total = 0
for cat in sorted(state['entryManifest'].keys()):
    entries = state['entryManifest'][cat]
    total += len(entries)
    print(f'【{cat}】 ({len(entries)} 条)')
    for name, entry in sorted(entries.items()):
        kw = entry.get('keywords', [])
        print(f'  • {name}  → 触发词: {", ".join(kw[:5])}')
    print()

print(f'总计: {total} 条目')
print(f'分类数: {len(state["entryManifest"])}')