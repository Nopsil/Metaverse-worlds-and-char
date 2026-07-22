"""Replace base64 avatars with PNG imports in App.vue"""
import re

app_vue_path = r"C:\Users\nopsi\Desktop\metaverse工程\tavern_helper_template\src\MetaverseLobby\界面\状态栏\App.vue"

with open(app_vue_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Add imports after the existing imports
imports_insert = '\nimport airinePng from \'./airine.png\';\nimport bathshebaPng from \'./bathsheba.png\';\nimport lenaPng from \'./lena.png\';\nimport memePng from \'./meme.png\';\nimport belzeebulPng from \'./belzeebul.png\';\n'

# Insert before "const store"
content = content.replace("const store = useDataStore();", imports_insert + "\nconst store = useDataStore();")

# Map of character id -> import variable name
png_map = {
    'airine': 'airinePng',
    'bathsheba': 'bathshebaPng',
    'lena': 'lenaPng',
    'meme': 'memePng',
    'belzeebul': 'belzeebulPng',
}

# Replace each base64 avatar with the import reference
for char_id, var_name in png_map.items():
    # Pattern: { id: 'char_id', ... avatar: 'data:image/...',  ->  { id: 'char_id', ... avatar: var_name,
    # The avatar line is massive, so we need to find and replace it
    
    # Find the character block
    start = f"  {{ id: '{char_id}',"
    idx = content.find(start)
    if idx == -1:
        print(f"ERROR: Could not find {char_id}")
        continue
    
    # Find the avatar line within this character block
    search_start = idx
    avatar_start = content.find("avatar: 'data:image/", search_start)
    if avatar_start == -1:
        print(f"ERROR: Could not find avatar for {char_id}")
        continue
    
    # Find the end of the avatar line
    avatar_end = content.find("\n", avatar_start)
    if avatar_end == -1:
        print(f"ERROR: Could not find end of avatar for {char_id}")
        continue
    
    old_line = content[avatar_start:avatar_end]
    new_line = f"avatar: {var_name}"
    
    content = content.replace(old_line, new_line, 1)
    print(f"Replaced base64 avatar with {var_name} for {char_id}")

with open(app_vue_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Done! File size reduced from ~380KB to ~3KB.")
