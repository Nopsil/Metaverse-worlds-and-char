import json, uuid, os

# ===== tavern_helper script =====
th_script = r"""
(function () {
  const SCRIPT_NAME = "MTV Opening Selector";
  
  function init() {
    const root = document.getElementById('mtv-root');
    if (!root) return setTimeout(init, 200);
    
    const scenes = [
      //   charIdx, sceneIdx, emoji, color, charName, sceneName, text
      [0,0,"🩸","#ff6bcd","拔示巴·阿西德菲尔","配种室初见","你被亚哈带入她的房间。银白色长发的少女坐在窗边，红色眼眸波澜不惊。\n\n\"又一个了。你是来膜拜我的？还是来利用我的？\"\n\n她用剑尖轻点地面。"],
      [0,1,"🩸","#ff6bcd","拔示巴·阿西德菲尔","圣堂独白","夜深了。奥林匹亚斯圣堂的喧嚣褪去，她独自跪坐在王座前。\n\n\"……没有人。\"\n\n然后她听到了脚步声。"],
      [0,2,"🩸","#ff6bcd","拔示巴·阿西德菲尔","米斯拉的微笑","午后阳光穿过彩窗。米斯拉双手叉腰教她微笑。她嘴角动了动——一个不熟练的发自内心的微笑。\n\n你从走廊转角走出，两人同时看向你。"],
      [1,0,"🌙","#8eceff","蕾娜·伊修梅尔","伊欧尼亚火海","皮阔特号甲板被晚霞染成血色。少女蜷在货箱阴影里紧抱小手枪。11个同伴全死了。\n\n你踩到钢缆——她弹起来手枪指向你。"],
      [1,1,"🌙","#8eceff","蕾娜·伊修梅尔","皮阔特号航程","海风吹乱银白色短发。她手忙脚乱扶正兜帽，看到你靠在船舷边。\n\n\"啊，你好！我叫蕾娜·伊修梅尔。可以一起走一段路吗？\""],
      [1,2,"🌙","#8eceff","蕾娜·伊修梅尔","安特路亚之夜","废弃都市在月光下沉默。少女躺在病床上，高烧让她脸颊泛红。远方传来引擎轰鸣。\n\n你坐在她旁边，感觉到她的手抓紧了床单。"],
      [1,3,"🌙","#8eceff","蕾娜·伊修梅尔","战后的深夜","佩尔修斯殖民地。她站在窗边，银白色长发散在肩后。\n\n\"能决定我们未来的，只有我们自己。\"有人敲门。"],
      [2,0,"💉","#90ff90","米姆·米库拉","路边包扎","她蹲在路边认真包扎小动物。抬头看到你——紫色眼睛先警觉后好奇。\n\n\"我叫米姆。室友让我问你——是敌人还是朋友？\""],
      [2,1,"💉","#90ff90","米姆·米库拉","泰斯塔蒙特觉醒","医疗包重重砸地。紫色眼瞳取代苍蓝。\n\n\"真是无聊啊。呐——是来看米姆的，还是来看我的？\""],
      [2,2,"💉","#90ff90","米姆·米库拉","药房深夜","昏暗药房里她对着自己吵架。你推开门。她同时停下转向你：\"你看到了？\""],
      [2,3,"💉","#90ff90","米姆·米库拉","旅路篝火","夜晚荒原篝火噼啪。塞拉菲娜枕着她的腿入睡。\n\n\"如果这个世界是假的，那我感受到的体温——难道也是假的吗？\""],
      [3,0,"👑","#ffcc66","贝尔泽ブト·涅墨西斯","机械王座","她半躺在机械王座中，青绿色长发如能量流扩散。触手慵懒蠕动。\n\n\"又有新玩具了。你，想怎么玩？\""],
      [3,1,"👑","#ffcc66","贝尔泽ブト·涅墨西斯","战场撤退","她舔了舔指尖血。\"今天就到这里。下次再陪我玩玩？\"触手包裹着她消失在暗流中。"],
      [3,2,"👑","#ffcc66","贝尔泽ブト·涅墨西斯","阿雷斯负伤","她用触手代替断裂手臂背起阿雷斯。\"太乱来了。\"她看到你：\"让开。\""],
      [3,3,"👑","#ffcc66","贝尔泽ブト·涅墨西斯","研究所奇遇","她从残骸后踱出，触手未展开。\"能活着走进这里的——你是哪边的？\""],
      [4,0,"🦋","#c0a0ff","艾莉ニ·居里亚斯","蓝蝶落地","微弱蓝光闪过。银发蓝瞳少女抱着素描本踏出。蓝蝶们在她身边飞舞。\n\n\"我叫艾莉ニ。我在画一本画册，记录所有美丽的瞬间。\""],
      [4,1,"🦋","#c0a0ff","艾莉ニ·居里亚斯","废墟画花","废墟中央一株小花从铁锈缝隙钻出。她跪地翻开素描本。\"嘘——别吓到它。\""],
      [4,2,"🦋","#c0a0ff","艾莉ニ·居里亚斯","地下都市童年","窗外是铁灰色天花板。六岁的艾莉ニ握着蜡笔，画了蓝圈"天空"和黄圈"太阳"。\n\n\"小艾莉——\"女人轻唤她的名字。"],
    ];
    
    let html = '<div style="background:#0a001a;border:2px solid #ff6bcd;padding:16px;border-radius:14px;font-family:sans-serif;color:#fff;max-width:650px;margin:0 auto;text-align:center;">';
    html += '<div style="font-size:1.8em;font-weight:900;background:linear-gradient(180deg,#ff6bcd,#c45cff,#6b8cff);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:12px;">CHUNITHM METAVERSE</div>';
    html += '<div style="color:#ff9dde;margin-bottom:14px;">▼ 点击选择开局 ▼</div>';
    
    let currentChar = -1;
    html += '<div style="display:flex;flex-wrap:wrap;gap:6px;justify-content:center;">';
    
    // Group by character
    const charNames = ["拔示巴","蕾娜","米姆","贝尔泽ブト","艾莉ニ"];
    const charEmojis = ["🩸","🌙","💉","👑","🦋"];
    const charColors = ["#ff6bcd","#8eceff","#90ff90","#ffcc66","#c0a0ff"];
    
    scenes.forEach((s, i) => {
      const [ci, si, emoji, color, charName, sceneName, text] = s;
      html += '<div onclick="var ta=document.querySelector(\'#send_textarea\');if(ta){ta.value=' + JSON.stringify(text) + ';var btn=document.querySelector(\'#send_but\');if(btn)btn.click();}" style="cursor:pointer;background:rgba(255,255,255,0.04);border:1px solid ' + color + '55;border-radius:10px;padding:10px 14px;transition:0.15s;flex:1 1 48%;min-width:200px;text-align:left;" onmouseover="this.style.background=\''+color+'22\'" onmouseout="this.style.background=\'rgba(255,255,255,0.04)\'">';
      html += '<span style="color:' + color + ';font-weight:bold;">' + emoji + ' ' + charName + '</span><br>';
      html += '<span style="color:#b0a0c0;font-size:0.78em;">— ' + sceneName + '</span>';
      html += '</div>';
    });
    
    html += '</div></div>';
    root.innerHTML = html;
  }
  
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
"""

# ===== regex scripts =====
regex_display = {
    "id": str(uuid.uuid4()),
    "scriptName": "MTV Opening Display",
    "findRegex": "<OpeningSelectUI/>",
    "replaceString": '<div id="mtv-root"></div>',
    "placement": [2],
    "disabled": False,
    "markdownOnly": False,
    "promptOnly": False,
    "runOnEdit": False,
    "substituteRegex": 0,
    "minDepth": None,
    "maxDepth": None,
    "trimStrings": []
}

regex_hide = {
    "id": str(uuid.uuid4()),
    "scriptName": "MTV Opening Hide",
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

# ===== tavern_helper script entry =====
th_entry = {
    "type": "script",
    "enabled": True,
    "id": str(uuid.uuid4()),
    "info": "MTV Opening Selector - Renders clickable scene selection UI",
    "button": {"enabled": False, "buttons": []},
    "data": {},
    "export_with": {"data": True, "button": False},
    "script_file": None,  # Inline via value field
    "value": th_script
}

# ===== Card =====
card = {
    "spec": "chara_card_v3",
    "spec_version": "3.0",
    "name": "CHUNITHM Metaverse",
    "description": "",
    "personality": "",
    "scenario": "",
    "first_mes": "<OpeningSelectUI/>",
    "mes_example": "",
    "creatorcomment": "MTV 命运观测终端 — tavern_helper点击选择",
    "avatar": "none",
    "talkativeness": 0.5,
    "fav": False,
    "tags": ["metaverse"],
    "create_date": "2026-07-20T20:00:00.000Z",
    "data": {
        "name": "CHUNITHM Metaverse",
        "description": "",
        "personality": "",
        "scenario": "",
        "first_mes": "<OpeningSelectUI/>",
        "mes_example": "",
        "creator_notes": "",
        "system_prompt": "用户点击UI卡片后开场文本已自动填入。直接以对应角色第一人称开始叙述。",
        "post_history_instructions": "",
        "tags": ["metaverse"],
        "creator": "Cline+User",
        "character_version": "9.0",
        "alternate_greetings": [],
        "extensions": {
            "regex": [regex_display, regex_hide],
            "regex_scripts": [regex_display, regex_hide],
            "tavern_helper": {
                "scripts": {
                    "MTV Opening Selector v1.0": th_entry
                }
            }
        }
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

print(f'Card built: tavern_helper script ({len(th_script)} chars)')
print('18 clickable scene cards via DOM injection')