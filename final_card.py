import json

p = r'C:\Users\nopsi\Desktop\metaverse工程\new_card\Metaverse-Final.json'

d = json.load(open(p, 'r', encoding='utf-8'))

fm = (
    '<div style="background:linear-gradient(160deg,#0a001a,#1a0030,#050520);padding:2px;border-radius:14px;font-family:sans-serif;color:#fff;max-width:600px;margin:0 auto;text-align:center;">'
    '<div style="font-size:2.2em;font-weight:900;background:linear-gradient(180deg,#ff6bcd,#c45cff,#6b8cff);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;margin:14px 0 4px;">CHUNITHM METAVERSE</div>'
    '<div style="color:#9080b0;font-size:.85em;letter-spacing:3px;margin-bottom:10px;">—— 命运观测终端 ——</div>'
    '<div style="display:flex;flex-direction:column;gap:8px;text-align:left;">'
    '<div style="background:rgba(255,107,205,.08);border:1px solid rgba(255,107,205,.3);border-radius:10px;padding:10px 14px;">🩸 <b style="color:#ff6bcd;">1 拔示巴</b> <span style="color:#b0a0c0;font-size:.78em;">1配种室 2圣堂独白 3米斯拉的微笑</span></div>'
    '<div style="background:rgba(140,200,255,.08);border:1px solid rgba(140,200,255,.3);border-radius:10px;padding:10px 14px;">🌙 <b style="color:#8eceff;">2 蕾娜</b> <span style="color:#b0a0c0;font-size:.78em;">1伊欧尼亚 2航程 3安特路亚 4战后</span></div>'
    '<div style="background:rgba(140,255,160,.08);border:1px solid rgba(140,255,160,.3);border-radius:10px;padding:10px 14px;">💉 <b style="color:#90ff90;">3 米姆</b> <span style="color:#b0a0c0;font-size:.78em;">1包扎 2觉醒 3药房 4旅路</span></div>'
    '<div style="background:rgba(255,190,100,.08);border:1px solid rgba(255,190,100,.3);border-radius:10px;padding:10px 14px;">👑 <b style="color:#ffcc66;">4 贝尔泽ブト</b> <span style="color:#b0a0c0;font-size:.78em;">1王座 2撤退 3负伤 4奇遇</span></div>'
    '<div style="background:rgba(170,140,255,.08);border:1px solid rgba(170,140,255,.3);border-radius:10px;padding:10px 14px;">🦋 <b style="color:#c0a0ff;">5 艾莉ニ</b> <span style="color:#b0a0c0;font-size:.78em;">1蓝蝶 2废墟 3童年</span></div>'
    '</div>'
    '<div style="margin-top:12px;padding:8px;border:1px dashed rgba(255,107,205,.3);border-radius:8px;color:#ff9dde;font-size:.85em;">输入 角色-开局（如 4-1 或 4-机械王座）</div>'
    '</div>'
)

sp = '你是命运观测终端。用户会用 角色编号-开局名/编号 选择场景。直接以该角色第一人称开始叙述。'

d['first_mes'] = fm
d['data']['first_mes'] = fm
d['data']['system_prompt'] = sp

json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

# Also copy to ST
import shutil
shutil.copy2(p, r'D:\ST\SillyTavern\data\default-user\characters\Metaverse-Final.json')

print('OK - 2000 chars HTML menu + system_prompt')