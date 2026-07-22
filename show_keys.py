import json

with open(r'C:\Users\nopsi\Desktop\metaverse工程\reborn_unpack\tavern-cards-state.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

scripts = d['extensions']['tavern_helper']['scripts']

# Show structure of 封面助手 and 角色创建助手
for name in ['斗罗封面助手脚本 @1.5.1', '斗罗角色创建助手脚本 @1.5.1']:
    s = scripts.get(name, {})
    print(f'=== {name} ===')
    print(f'keys: {list(s.keys())}')
    for k, v in s.items():
        if isinstance(v, str):
            print(f'  {k}: ({len(v)} chars)')
            if k == 'value':
                print(f'  value first 500: {v[:500]}')
        else:
            print(f'  {k}: {v}')
    print()