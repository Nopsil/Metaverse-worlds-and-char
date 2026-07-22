import json

with open(r'C:\Users\nopsi\Desktop\metaverse工程\reborn_unpack\tavern-cards-state.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

ext = d.get('extensions', {})
th = ext.get('tavern_helper', {})
scripts = th.get('scripts', {})

print(f'scripts type: {type(scripts).__name__}')
if isinstance(scripts, dict):
    print(f'scripts keys ({len(scripts)}):')
    for k in list(scripts.keys())[:10]:
        v = scripts[k]
        if isinstance(v, str):
            print(f'  {k}: "{v[:80]}"')
        else:
            print(f'  {k}: {type(v).__name__}')
elif isinstance(scripts, list):
    print(f'scripts list ({len(scripts)} items), first item type: {type(scripts[0]).__name__}')
    if isinstance(scripts[0], str):
        print(f'  [0]: "{scripts[0][:80]}"')
    else:
        print(f'  [0] keys: {list(scripts[0].keys()) if isinstance(scripts[0], dict) else "?"}')