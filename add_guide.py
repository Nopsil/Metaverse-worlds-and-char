import json

p = r'D:\ST\SillyTavern\data\default-user\characters\Metaverse-Final.json'
d = json.load(open(p, 'r', encoding='utf-8'))

ags = d['data']['alternate_greetings']
guide = '【METAVERSE 命运观测终端】\n\n点击聊天窗口上方角色名旁边的"备选开场白"按钮（小钟表图标），从18条开局中选择一个即可直接进入剧情，无需等待API。\n\n🩸 拔示巴[3] | 🌙 蕾娜[4] | 💉 米姆[4] | 👑 贝尔泽ブト[4] | 🦋 艾莉尼[3]'
ags.insert(0, guide)

json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print(f'OK, alt_greetings = {len(ags)} 条')