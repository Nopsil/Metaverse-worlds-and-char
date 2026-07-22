import json, shutil, re

# Read the generated card JSON to get the HTML that's already in regex scripts
with open(r'C:\Users\nopsi\Desktop\metaverse工程\new_card\Metaverse-Final.json', 'r', encoding='utf-8') as f:
    card = json.load(f)

# Get the HTML from the regex script
regex_scripts = card.get('data', {}).get('extensions', {}).get('regex', [])
html = ''
for script in regex_scripts:
    if script.get('scriptName') == 'MTV Opening Select - Display':
        html = script.get('replaceString', '')
        break

if html:
    card['first_mes'] = html
    card['data']['first_mes'] = html
    
    paths = [
        r'C:\Users\nopsi\Desktop\metaverse工程\new_card\Metaverse-Final.json',
        r'D:\ST\SillyTavern\data\default-user\characters\Metaverse-Final.json'
    ]
    for p in paths:
        json.dump(card, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    
    print(f'HTML moved to first_mes: {len(html)} chars')
else:
    print('ERROR: HTML not found in regex scripts')