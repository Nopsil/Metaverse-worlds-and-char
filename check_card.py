import json, os

p = r'C:\Users\nopsi\Desktop\metaverse工程\new_card\Metaverse-Showcase.json'
d = json.load(open(p, 'r', encoding='utf-8'))

wb = d['data']['character_book']
entries = wb['entries']
print(f'Entries: {len(entries)}')
print(f'data.first_mes: {len(d["data"]["first_mes"])} chars')
print(f'data.description: {len(d["data"]["description"])} chars')
print(f'data.system_prompt: {len(d["data"]["system_prompt"])} chars')

# Check for empty keys
empty_keys = [e['id'] for e in entries if len(e.get('keys', [])) == 0]
print(f'Entries with empty keys: {empty_keys}')

# Check required fields
missing = [e['id'] for e in entries if 'content' not in e or not e['content']]
print(f'Entries with empty content: {missing}')

print('OK' if not empty_keys and not missing else 'HAS ISSUES')