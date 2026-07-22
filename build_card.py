import json, uuid

# ==============================================
# 1. Create the HTML selection UI
# ==============================================
html = """<div style="background:linear-gradient(160deg,#0a001a,#1a0030,#050520);border-radius:14px;padding:16px;font-family:sans-serif;color:#fff;max-width:600px;margin:0 auto;text-align:center;">
<div style="font-size:1.8em;font-weight:900;background:linear-gradient(180deg,#ff6bcd,#c45cff,#6b8cff);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;margin-bottom:2px;">CHUNITHM METAVERSE</div>
<div style="color:#9080b0;font-size:.8em;letter-spacing:3px;margin-bottom:12px;">—— 命运观测终端 ——</div>
<div style="color:#a090c0;font-size:.78em;margin-bottom:12px;">点击下方卡片选择开局，自动填入聊天框</div>
<div style="display:flex;flex-direction:column;gap:6px;text-align:left;" id="mtv-opts">
<div onclick="document.querySelector('#send_textarea').value='被亚哈带入她的房间。银白色长发的少女坐在窗边。\\n\\n\\\"又一个了。是来膜拜我的？还是来利用我的？\\\"\\n\\n她用剑尖轻点地面。';document.querySelector('#send_but')?.click()" style="cursor:pointer;background:rgba(255,107,205,.1);border:1px solid rgba(255,107,205,.3);border-radius:10px;padding:10px 14px;transition:.15s" onmouseover="this.style.background='rgba(255,107,205,.2)'" onmouseout="this.style.background='rgba(255,107,205,.1)'">🩸 <b style="color:#ff6bcd;">拔示巴 — 配种室初见</b></div>
<div onclick="document.querySelector('#send_textarea').value='夜深了。奥林匹亚斯圣堂的喧嚣褪去，她独自跪坐在王座前。\\n\\n\\\"……没有人。\\\"\\n\\n然后她听到了脚步声。';document.querySelector('#send_but')?.click()" style="cursor:pointer;background:rgba(255,107,205,.1);border:1px solid rgba(255,107,205,.3);border-radius:10px;padding:10px 14px;transition:.15s" onmouseover="this.style.background='rgba(255,107,205,.2)'" onmouseout="this.style.background='rgba(255,107,205,.1)'">🩸 <b style="color:#ff6bcd;">拔示巴 — 圣堂独白</b></div>
<div onclick="document.querySelector('#send_textarea').value='午后阳光穿过彩窗。米斯拉双手叉腰：\\\"嘴角这样——自然一点。\\\"她嘴角动了动——一个不熟练的发自内心的微笑。\\n\\n你从走廊转角走出，两人同时看向你。';document.querySelector('#send_but')?.click()" style="cursor:pointer;background:rgba(255,107,205,.1);border:1px solid rgba(255,107,205,.3);border-radius:10px;padding:10px 14px;transition:.15s" onmouseover="this.style.background='rgba(255,107,205,.2)'" onmouseout="this.style.background='rgba(255,107,205,.1)'">🩸 <b style="color:#ff6bcd;">拔示巴 — 米斯拉的微笑</b></div>
<div onclick="document.querySelector('#send_textarea').value='皮阔特号甲板被晚霞染成血色。少女蜷在货箱阴影里紧抱小手枪。11个同伴全死了。\\n\\n你踩到钢缆——她弹起来手枪指向你：\\\"你是谁？\\\"';document.querySelector('#send_but')?.click()" style="cursor:pointer;background:rgba(140,200,255,.1);border:1px solid rgba(140,200,255,.3);border-radius:10px;padding:10px 14px;transition:.15s" onmouseover="this.style.background='rgba(140,200,255,.2)'" onmouseout="this.style.background='rgba(140,200,255,.1)'">🌙 <b style="color:#8eceff;">蕾娜 — 伊欧尼亚火海</b></div>
<div onclick="document.querySelector('#send_textarea').value='海风吹乱银白色短发。她拉兜帽——兜帽边沿盖住了整张脸。\\n\\n扶正兜帽后看到你靠在船舷边。\\\"啊，你好！我叫蕾娜·伊修梅尔。可以一起走一段路吗？\\\"';document.querySelector('#send_but')?.click()" style="cursor:pointer;background:rgba(140,200,255,.1);border:1px solid rgba(140,200,255,.3);border-radius:10px;padding:10px 14px;transition:.15s" onmouseover="this.style.background='rgba(140,200,255,.2)'" onmouseout="this.style.background='rgba(140,200,255,.1)'">🌙 <b style="color:#8eceff;">蕾娜 — 皮阔特号航程</b></div>
<div onclick="document.querySelector('#send_textarea').value='废弃都市在月光下沉默。少女躺在病床上，高烧让她脸颊泛红。远方隐约传来引擎轰鸣。\\n\\n你坐在她旁边，感觉到她的手抓紧了床单。';document.querySelector('#send_but')?.click()" style="cursor:pointer;background:rgba(140,200,255,.1);border:1px solid rgba(140,200,255,.3);border-radius:10px;padding:10px 14px;transition:.15s" onmouseover="this.style.background='rgba(140,200,255,.2)'" onmouseout="this.style.background='rgba(140,200,255,.1)'">🌙 <b style="color:#8eceff;">蕾娜 — 安特路亚之夜</b></div>
<div onclick="document.querySelector('#send_textarea').value='佩尔修斯殖民地。蕾娜站在窗边，银白色长发散在肩后。\\n\\n\\\"能决定我们未来的，只有我们自己。\\\"有人敲门。';document.querySelector('#send_but')?.click()" style="cursor:pointer;background:rgba(140,200,255,.1);border:1px solid rgba(140,200,255,.3);border-radius:10px;padding:10px 14px;transition:.15s" onmouseover="this.style.background='rgba(140,200,255,.2)'" onmouseout="this.style.background='rgba(140,200,255,.1)'">🌙 <b style="color:#8eceff;">蕾娜 — 战后的深夜</b></div>
<div onclick="document.querySelector('#send_textarea').value='米姆蹲在路边认真包扎一只小动物。\\n\\n她抬头看到你，紫色眼睛先警觉后好奇。\\\"我叫米姆。\\\"她顿了顿侧头——\\\"我室友让我问你——是敌人还是朋友？\\\"';document.querySelector('#send_but')?.click()" style="cursor:pointer;background:rgba(140,255,160,.1);border:1px solid rgba(140,255,160,.3);border-radius:10px;padding:10px 14px;transition:.15s" onmouseover="this.style.background='rgba(140,255,160,.2)'" onmouseout="this.style.background='rgba(140,255,160,.1)'">💉 <b style="color:#90ff90;">米姆 — 路边包扎</b></div>
<div onclick="document.querySelector('#send_textarea').value='她突然停下。医疗包重重砸地。紫色眼瞳取代苍蓝。\\n\\n\\\"真是无聊啊。\\\"声音低了半个八度。\\\"呐——是来看米姆的，还是来看我的？\\\"';document.querySelector('#send_but')?.click()" style="cursor:pointer;background:rgba(140,255,160,.1);border:1px solid rgba(140,255,160,.3);border-radius:10px;padding:10px 14px;transition:.15s" onmouseover="this.style.background='rgba(140,255,160,.2)'" onmouseout="this.style.background='rgba(140,255,160,.1)'">💉 <b style="color:#90ff90;">米姆 — 泰斯塔蒙特觉醒</b></div>
<div onclick="document.querySelector('#send_textarea').value='昏暗药房里她对着自己吵架。你推开门。\\n\\n她同时停下转向你：\\\"你看到了？\\\"';document.querySelector('#send_but')?.click()" style="cursor:pointer;background:rgba(140,255,160,.1);border:1px solid rgba(140,255,160,.3);border-radius:10px;padding:10px 14px;transition:.15s" onmouseover="this.style.background='rgba(140,255,160,.2)'" onmouseout="this.style.background='rgba(140,255,160,.1)'">💉 <b style="color:#90ff90;">米姆 — 药房深夜</b></div>
<div onclick="document.querySelector('#send_textarea').value='夜晚荒原，篝火噼啪。塞拉菲娜枕着她的腿入睡。\\n\\n她轻抚巫女的头发：\\\"如果这个世界是假的，那我感受到的体温——难道也是假的吗？\\\"';document.querySelector('#send_but')?.click()" style="cursor:pointer;background:rgba(140,255,160,.1);border:1px solid rgba(140,255,160,.3);border-radius:10px;padding:10px 14px;transition:.15s" onmouseover="this.style.background='rgba(140,255,160,.2)'" onmouseout="this.style.background='rgba(140,255,160,.1)'">💉 <b style="color:#90ff90;">米姆 — 旅路篝火</b></div>
<div onclick="document.querySelector('#send_textarea').value='她半躺在机械王座中，青绿色长发如能量流扩散。触手慵懒蠕动。\\n\\n\\\"啊啦。又有新玩具自己送上门了。\\\"她抬起手，指尖凝聚蓝白色能量球。\\\"你，想怎么玩？\\\"';document.querySelector('#send_but')?.click()" style="cursor:pointer;background:rgba(255,190,100,.1);border:1px solid rgba(255,190,100,.3);border-radius:10px;padding:10px 14px;transition:.15s" onmouseover="this.style.background='rgba(255,190,100,.2)'" onmouseout="this.style.background='rgba(255,190,100,.1)'">👑 <b style="color:#ffcc66;">贝尔泽ブト — 机械王座</b></div>
<div onclick="document.querySelector('#send_textarea').value='她舔了舔指尖血。\\\"一点意思都没有。不过——那两个小女孩挺有趣，伤到我了哦。\\\"\\n\\n\\\"今天就到这里。下次再陪我玩玩？\\\"触手包裹着她消失在暗流中。';document.querySelector('#send_but')?.click()" style="cursor:pointer;background:rgba(255,190,100,.1);border:1px solid rgba(255,190,100,.3);border-radius:10px;padding:10px 14px;transition:.15s" onmouseover="this.style.background='rgba(255,190,100,.2)'" onmouseout="this.style.background='rgba(255,190,100,.1)'">👑 <b style="color:#ffcc66;">贝尔泽ブト — 战场撤退</b></div>
<div onclick="document.querySelector('#send_textarea').value='轰——光芒吞没阿雷斯大半个身体。\\n\\n她用触手代替断裂手臂将他背起。\\\"太乱来了。\\\"声音没有戏谑。她看到你：\\\"让开。\\\"';document.querySelector('#send_but')?.click()" style="cursor:pointer;background:rgba(255,190,100,.1);border:1px solid rgba(255,190,100,.3);border-radius:10px;padding:10px 14px;transition:.15s" onmouseover="this.style.background='rgba(255,190,100,.2)'" onmouseout="this.style.background='rgba(255,190,100,.1)'">👑 <b style="color:#ffcc66;">贝尔泽ブト — 阿雷斯负伤</b></div>
<div onclick="document.querySelector('#send_textarea').value='金属和臭氧的味道。她从残骸后踱出，触手未展开。\\n\\n\\\"能活着走进这里的——要么是涅墨西斯的人，要么是敌人。你是哪边的？\\\"';document.querySelector('#send_but')?.click()" style="cursor:pointer;background:rgba(255,190,100,.1);border:1px solid rgba(255,190,100,.3);border-radius:10px;padding:10px 14px;transition:.15s" onmouseover="this.style.background='rgba(255,190,100,.2)'" onmouseout="this.style.background='rgba(255,190,100,.1)'">👑 <b style="color:#ffcc66;">贝尔泽ブト — 研究所奇遇</b></div>
<div onclick="document.querySelector('#send_textarea').value='微弱蓝光闪过。银发蓝瞳少女抱着素描本从传送余波中踏出。\\n\\n\\\"我叫艾莉ニ。我在画一本画册，记录所有美丽的瞬间。\\\"蓝蝶绕你转了一圈。\\\"它好像很喜欢你。\\\"';document.querySelector('#send_but')?.click()" style="cursor:pointer;background:rgba(170,140,255,.1);border:1px solid rgba(170,140,255,.3);border-radius:10px;padding:10px 14px;transition:.15s" onmouseover="this.style.background='rgba(170,140,255,.2)'" onmouseout="this.style.background='rgba(170,140,255,.1)'">🦋 <b style="color:#c0a0ff;">艾莉ニ — 蓝蝶落地</b></div>
<div onclick="document.querySelector('#send_textarea').value='荒凉废墟中央，一株小花从铁锈缝隙钻出。\\n\\n她跪地翻开素描本。\\\"嘘——别吓到它。\\\"笔尖记录这朵在绝望中绽放的生命。';document.querySelector('#send_but')?.click()" style="cursor:pointer;background:rgba(170,140,255,.1);border:1px solid rgba(170,140,255,.3);border-radius:10px;padding:10px 14px;transition:.15s" onmouseover="this.style.background='rgba(170,140,255,.2)'" onmouseout="this.style.background='rgba(170,140,255,.1)'">🦋 <b style="color:#c0a0ff;">艾莉ニ — 废墟画花</b></div>
<div onclick="document.querySelector('#send_textarea').value='窗外不是天空，是铁灰色天花板。六岁的艾莉ニ握着蓝色蜡笔。一个蓝圈——\\\"天空\\\"。一个黄圈——\\\"太阳\\\"。\\n\\n\\\"小艾莉——\\\"一个女人轻唤她的名字。';document.querySelector('#send_but')?.click()" style="cursor:pointer;background:rgba(170,140,255,.1);border:1px solid rgba(170,140,255,.3);border-radius:10px;padding:10px 14px;transition:.15s" onmouseover="this.style.background='rgba(170,140,255,.2)'" onmouseout="this.style.background='rgba(170,140,255,.1)'">🦋 <b style="color:#c0a0ff;">艾莉ニ — 地下都市童年</b></div>
</div>
</div>"""

# ==============================================
# 2. Build the complete card
# ==============================================
sp = "用户点击UI卡片后，开场文本已自动填入聊天框。你看到该文本后，以对应角色的第一人称视角立即开始叙述。"

card = {
    "spec": "chara_card_v3",
    "spec_version": "3.0",
    "name": "CHUNITHM Metaverse",
    "description": "",
    "personality": "",
    "scenario": "",
    "first_mes": "<OpeningSelectUI/>",
    "mes_example": "",
    "creatorcomment": "Metaverse命运观测终端v6.0 — SillyTavern正则脚本前端选择器",
    "avatar": "none",
    "talkativeness": 0.5,
    "fav": False,
    "tags": ["metaverse"],
    "create_date": "2026-07-20T18:50:00.000Z",
    "data": {
        "name": "CHUNITHM Metaverse",
        "description": "",
        "personality": "",
        "scenario": "",
        "first_mes": "<OpeningSelectUI/>",
        "mes_example": "",
        "creator_notes": "",
        "system_prompt": sp,
        "post_history_instructions": "",
        "tags": ["metaverse"],
        "creator": "Cline+User",
        "character_version": "6.0",
        "alternate_greetings": [],
        "extensions": {
            "regex": [
                {
                    "id": str(uuid.uuid4()),
                    "scriptName": "MTV Opening Select - Display",
                    "findRegex": "<OpeningSelectUI/>",
                    "replaceString": html,
                    "placement": [2],
                    "disabled": False,
                    "markdownOnly": False,
                    "promptOnly": False,
                    "runOnEdit": False,
                    "substituteRegex": 0,
                    "minDepth": None,
                    "maxDepth": None,
                    "trimStrings": []
                },
                {
                    "id": str(uuid.uuid4()),
                    "scriptName": "MTV Opening Select - Hide",
                    "findRegex": "<OpeningSelectUI/>",
                    "replaceString": "",
                    "placement": [2],
                    "disabled": False,
                    "markdownOnly": False,
                    "promptOnly": True,
                    "runOnEdit": False,
                    "substituteRegex": 0,
                    "minDepth": None,
                    "maxDepth": None,
                    "trimStrings": []
                }
            ]
        }
    }
}

# ==============================================
# 3. Write to both locations
# ==============================================
import shutil, os

paths = [
    r'C:\Users\nopsi\Desktop\metaverse工程\new_card\Metaverse-Final.json',
    r'D:\ST\SillyTavern\data\default-user\characters\Metaverse-Final.json'
]

for p in paths:
    os.makedirs(os.path.dirname(p), exist_ok=True)
    json.dump(card, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

print(f'Card built: {len(html)} chars HTML, 2 regex scripts')
print('Saved to both locations')