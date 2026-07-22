import json

fm='''【METAVERSE 命运观测终端】

选择命运后直接说出你要进入的场景，例如"进入拔示巴的圣堂独白"。

🩸 拔示巴·阿西德菲尔
  → 配种室初见 / 圣堂独白 / 米斯拉的微笑

🌙 蕾娜·伊修梅尔  
  → 伊欧尼亚火海 / 皮阔特号航程 / 安特路亚之夜 / 战后的深夜

💉 米姆·米库拉
  → 路边包扎 / 泰斯塔蒙特觉醒 / 药房深夜 / 旅路篝火

👑 贝尔泽布特·涅墨西斯
  → 机械王座 / 战场撤退 / 阿雷斯负伤 / 研究所奇遇

🦋 艾莉尼·居里亚斯
  → 蓝蝶落地 / 废墟画花 / 地下都市童年'''

sp='''你是命运观测终端。用户会用自然语言选择开局场景（如"进入贝尔泽布特的机械王座"）。你必须以该角色的第一人称视角立即开始叙述。'''

p=r'D:\ST\SillyTavern\data\default-user\characters\Metaverse-Final.json'
d=json.load(open(p,'r',encoding='utf-8'))
d['first_mes']=fm
d['data']['first_mes']=fm
d['data']['system_prompt']=sp
json.dump(d,open(p,'w',encoding='utf-8'),ensure_ascii=False,indent=2)
print(f'first_mes={len(fm)}chars, system_prompt={len(sp)}chars')