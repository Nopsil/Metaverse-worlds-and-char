import json, os, shutil

# Simple HTML menu with compact codes
fm = (
    '<div style="background:#0a001a;border:2px solid #ff6bcd;padding:16px;border-radius:14px;font:14px Segoe UI;color:#fff;max-width:600px;margin:0 auto;text-align:center;">'
    '<div style="font-size:1.8em;background:linear-gradient(180deg,#ff6bcd,#c45cff,#6b8cff);-webkit-background-clip:text;-webkit-text-fill-color:transparent;font-weight:900;margin-bottom:12px;">CHUNITHM METAVERSE</div>'
    '<div style="color:#ff9dde;margin-bottom:12px;font-size:0.9em;">选择你想进入的命运</div>'
    '<table style="width:100%;border-collapse:collapse;margin:0 auto;text-align:left;">'
    '<tr><td style="padding:6px 10px;border-bottom:1px solid #333"><span style="color:#ff6bcd;font-weight:bold;">1A</span></td><td style="padding:6px 10px;border-bottom:1px solid #333">🩸 拔示巴 — 配种室初见</td></tr>'
    '<tr><td style="padding:6px 10px;border-bottom:1px solid #333"><span style="color:#ff6bcd;font-weight:bold;">1B</span></td><td style="padding:6px 10px;border-bottom:1px solid #333">🩸 拔示巴 — 圣堂独白</td></tr>'
    '<tr><td style="padding:6px 10px;border-bottom:1px solid #333"><span style="color:#ff6bcd;font-weight:bold;">1C</span></td><td style="padding:6px 10px;border-bottom:1px solid #333">🩸 拔示巴 — 米斯拉的微笑</td></tr>'
    '<tr><td style="padding:6px 10px;border-bottom:1px solid #333"><span style="color:#8eceff;font-weight:bold;">2A</span></td><td style="padding:6px 10px;border-bottom:1px solid #333">🌙 蕾娜 — 伊欧尼亚火海</td></tr>'
    '<tr><td style="padding:6px 10px;border-bottom:1px solid #333"><span style="color:#8eceff;font-weight:bold;">2B</span></td><td style="padding:6px 10px;border-bottom:1px solid #333">🌙 蕾娜 — 皮阔特号航程</td></tr>'
    '<tr><td style="padding:6px 10px;border-bottom:1px solid #333"><span style="color:#8eceff;font-weight:bold;">2C</span></td><td style="padding:6px 10px;border-bottom:1px solid #333">🌙 蕾娜 — 安特路亚之夜</td></tr>'
    '<tr><td style="padding:6px 10px;border-bottom:1px solid #333"><span style="color:#8eceff;font-weight:bold;">2D</span></td><td style="padding:6px 10px;border-bottom:1px solid #333">🌙 蕾娜 — 战后的深夜</td></tr>'
    '<tr><td style="padding:6px 10px;border-bottom:1px solid #333"><span style="color:#90ff90;font-weight:bold;">3A</span></td><td style="padding:6px 10px;border-bottom:1px solid #333">💉 米姆 — 路边包扎</td></tr>'
    '<tr><td style="padding:6px 10px;border-bottom:1px solid #333"><span style="color:#90ff90;font-weight:bold;">3B</span></td><td style="padding:6px 10px;border-bottom:1px solid #333">💉 米姆 — 泰斯塔蒙特觉醒</td></tr>'
    '<tr><td style="padding:6px 10px;border-bottom:1px solid #333"><span style="color:#90ff90;font-weight:bold;">3C</span></td><td style="padding:6px 10px;border-bottom:1px solid #333">💉 米姆 — 药房深夜</td></tr>'
    '<tr><td style="padding:6px 10px;border-bottom:1px solid #333"><span style="color:#90ff90;font-weight:bold;">3D</span></td><td style="padding:6px 10px;border-bottom:1px solid #333">💉 米姆 — 旅路篝火</td></tr>'
    '<tr><td style="padding:6px 10px;border-bottom:1px solid #333"><span style="color:#ffcc66;font-weight:bold;">4A</span></td><td style="padding:6px 10px;border-bottom:1px solid #333">👑 贝尔泽ブト — 机械王座</td></tr>'
    '<tr><td style="padding:6px 10px;border-bottom:1px solid #333"><span style="color:#ffcc66;font-weight:bold;">4B</span></td><td style="padding:6px 10px;border-bottom:1px solid #333">👑 贝尔泽ブト — 战场撤退</td></tr>'
    '<tr><td style="padding:6px 10px;border-bottom:1px solid #333"><span style="color:#ffcc66;font-weight:bold;">4C</span></td><td style="padding:6px 10px;border-bottom:1px solid #333">👑 贝尔泽ブト — 阿雷斯负伤</td></tr>'
    '<tr><td style="padding:6px 10px;border-bottom:1px solid #333"><span style="color:#ffcc66;font-weight:bold;">4D</span></td><td style="padding:6px 10px;border-bottom:1px solid #333">👑 贝尔泽ブト — 研究所奇遇</td></tr>'
    '<tr><td style="padding:6px 10px;"><span style="color:#c0a0ff;font-weight:bold;">5A</span></td><td style="padding:6px 10px;">🦋 艾莉ニ — 蓝蝶落地</td></tr>'
    '<tr><td style="padding:6px 10px;"><span style="color:#c0a0ff;font-weight:bold;">5B</span></td><td style="padding:6px 10px;">🦋 艾莉ニ — 废墟画花</td></tr>'
    '<tr><td style="padding:6px 10px;"><span style="color:#c0a0ff;font-weight:bold;">5C</span></td><td style="padding:6px 10px;">🦋 艾莉ニ — 地下都市童年</td></tr>'
    '</table>'
    '<div style="margin-top:14px;padding:8px;border:1px dashed #ff6bcd;border-radius:8px;color:#ff9dde;font-size:0.85em;">在聊天框输入编号（如 4A）选择开局</div>'
    '</div>'
)

# System prompt
sp = '用户输入编号（如"4A"）选择开局后，立即以对应角色身份开始叙述。不允许跳过这个步骤。'

# Build card
card = {
    "spec": "chara_card_v3",
    "spec_version": "3.0",
    "name": "CHUNITHM Metaverse",
    "description": "",
    "personality": "",
    "scenario": "",
    "first_mes": fm,
    "mes_example": "",
    "avatar": "none",
    "talkativeness": 0.5,
    "fav": False,
    "tags": ["metaverse"],
    "create_date": "2026-07-20T19:10:00.000Z",
    "data": {
        "name": "CHUNITHM Metaverse",
        "description": "",
        "personality": "",
        "scenario": "",
        "first_mes": fm,
        "mes_example": "",
        "system_prompt": sp,
        "tags": ["metaverse"],
        "creator": "Cline+User",
        "character_version": "8.0",
        "alternate_greetings": []
    }
}

# Save
paths = [
    r'C:\Users\nopsi\Desktop\metaverse工程\new_card\Metaverse-Final.json',
    r'D:\ST\SillyTavern\data\default-user\characters\Metaverse-Final.json'
]

for p in paths:
    os.makedirs(os.path.dirname(p), exist_ok=True)
    json.dump(card, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

print(f'Card built: HTML table with 18 options')