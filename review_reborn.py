import json

with open(r'C:\Users\nopsi\Desktop\metaverse工程\reborn_unpack\tavern-cards-state.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

ext = d.get('extensions', {})
th = ext.get('tavern_helper', {})

scripts = th.get('scripts', [])
print(f'=== tavern_helper.scripts: {len(scripts)} ===')
for i, s in enumerate(scripts):
    sn = s.get('scriptName', '?')
    val_len = len(s.get('value', ''))
    print(f'[{i}] {sn} (value: {val_len} chars)')

vars_data = th.get('variables', {})
print(f'\n=== tavern_helper.variables: {len(vars_data)} keys ===')
# Just show the keys, not values
if isinstance(vars_data, dict):
    for k in list(vars_data.keys())[:10]:
        v = vars_data[k]
        if isinstance(v, str):
            print(f'  {k}: {v[:80]}...' if len(v)>80 else f'  {k}: {v}')
        else:
            print(f'  {k}: {type(v).__name__}')