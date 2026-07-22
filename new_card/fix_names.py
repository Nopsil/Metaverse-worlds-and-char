import json

wb = json.load(open(r'c:\Users\nopsi\Desktop\skill项目\new_card\Metaverse-New.json', encoding='utf-8'))
st = json.load(open(r'c:\Users\nopsi\Desktop\skill项目\new_card\tavern-cards-state.json', encoding='utf-8'))

# Build uid -> name map from state.json
uid_map = {}
for cat, entries in st['entryManifest'].items():
    for name, entry in entries.items():
        uid = entry.get('uid')
        if uid is not None:
            uid_map[uid] = name

print(f'State.json has {len(uid_map)} named entries')

# Now fix: apply display_name using uid
fixed = 0
for k, e in wb['entries'].items():
    uid = e.get('uid')
    if uid in uid_map:
        e['display_name'] = uid_map[uid]
        fixed += 1

json.dump(wb, open(r'c:\Users\nopsi\Desktop\skill项目\new_card\Metaverse-New.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print(f'Fixed {fixed}/{len(wb["entries"])} entries')

# Verify first 5
for k in list(wb['entries'].keys())[:5]:
    e = wb['entries'][k]
    print(f'  {k}: display_name={e.get("display_name","(none)")} comment={e.get("comment","")[:40]}')
print('Done')