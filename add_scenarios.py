"""Add scenarios arrays to each character in App.vue"""
import re

app_vue_path = r"C:\Users\nopsi\Desktop\metaverse工程\tavern_helper_template\src\MetaverseLobby\界面\状态栏\App.vue"

with open(app_vue_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Scenario lists for each character
scenarios_map = {
    'airine': ["星空下的相遇", "废墟中的速写", "次元隙间的旅伴", "索拉里斯的归途", "[NSFW] 蛮族的肉凯"],
    'bathsheba': ["圣堂中的王座", "虚无中的一线留恋", "革新者的访客", "佩尔修斯的废墟", "[NSFW] 命运之子的配种"],
    'lena': ["废土上的邂逅", "塞雷基亚之后", "伊欧尼亚的幸存者", "佩尔修斯的守护者", "[NSFW] 淫魔史莱姆的觉醒"],
    'meme': ["新世界废墟", "泰斯塔蒙特的低语", "光之塔的旅伴", "医疗营的访客", "[NSFW] 塞拉菲娜的困扰"],
    'belzeebul': ["Metaverse深渊", "猫戏老鼠", "混沌之器的契约", "工厂的入侵者", "[NSFW] 一魂双体"],
}

# For each character, find the avatar line and add scenarios after it
for char_id, scenarios in scenarios_map.items():
    # Build the JS array string
    scenarios_str = ",\n    scenarios: " + str(scenarios) + "\n  "
    
    # Pattern: find the character's avatar line ending, followed by the next character or end
    # The character starts like: { id: 'airine', name: ...
    # The avatar line ends with: ',\n  { id: '...   (next character) or ',\n]; (end of array)
    
    # We need to add scenarios BEFORE the closing or before the next character
    # Find pattern: },\n  { id: '<char_id>'  ... avatar line ... ',\n  { id: '<next_id>'
    # OR for last char: ... avatar line ... ',\n];
    
    # Let's use a regex approach: find the avatar line for each character
    # The avatar line is: line with id: '<char_id>' ... then next line is avatar
    
    if char_id == 'belzeebul':
        # Last character - add scenarios before the closing brace before ];
        # Pattern: ...avatar...',\n]  OR  ...avatar...'\n  }\n];
        # Actually looking at the structure, each character ends with:
        #   avatar: '...',\n  }  (but for multi-char, it's inline)
        # The last one ends with ...]\n;\n...
        pattern = r"(  \{ id: 'belzeebul', name: '贝尔泽布特[^}]+avatar: 'data:image/png;base64,[^']+'\n)(  )"
    else:
        # Find avatar line of current char followed by next char's id
        pattern = r"(  \{ id: '" + char_id + r"',[^}]+avatar: 'data:image/[^']+'\n)(  )"
    
    # Simpler approach: find the avatar line and insert scenarios right after it
    # Each character's id line is followed by avatar on next line
    # We want to insert: ,\n    scenarios: [...]\n  after the avatar line
    
    # Pattern: find the block from "{ id: 'char_id'" through the end of avatar line
    # Then insert scenarios right before "  " that starts the next character or "]"
    
    # The avatar line ends with a huge base64 string ending in ', then newline
    # After that is either next char or ];
    
    # Let's find the exact pattern for each char:
    start_marker = f"  {{ id: '{char_id}',"
    
    # Find the position of this character in the content
    idx = content.find(start_marker)
    if idx == -1:
        print(f"ERROR: Could not find character {char_id}")
        continue
    
    # Find the end of this character's block
    # The end is either the start of next character or the end of the array
    
    # Find the avatar line start
    avatar_start = content.find("avatar: '", idx)
    if avatar_start == -1:
        print(f"ERROR: Could not find avatar for {char_id}")
        continue
    
    # Find the end of the avatar line (next newline after avatar_start)
    avatar_end = content.find("\n", avatar_start + 1)
    if avatar_end == -1:
        print(f"ERROR: Could not find end of avatar line for {char_id}")
        continue
    
    # Now check what's after the avatar line
    next_line_start = avatar_end + 1
    
    # The scenarios should be inserted right before the next character or ];
    # Insert scenarios_str after the avatar line
    
    before = content[:avatar_end + 1]  # up to and including the \n
    after = content[avatar_end + 1:]    # rest of file
    
    # Insert scenarios + comma on a new line RIGHT AFTER the avatar line,
    # but the avatar line already ends with ', so we need to place the scenarios on the next line
    # The character block structure is:
    #   { id: 'airine', name: '...', tagline: '...',
    #     avatar: 'data:image/png;base64,...',
    #   { id: 'bathsheba', ...  (next char on next line)
    
    # So we insert: "    scenarios: [...]\n" right after "avatar: '...',\n"
    insertion = f"    scenarios: {str(scenarios)},\n"
    content = before + insertion + after
    print(f"Added scenarios for {char_id}")

with open(app_vue_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Done! Updated App.vue with scenarios arrays.")
