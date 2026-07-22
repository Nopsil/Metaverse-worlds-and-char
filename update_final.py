import json

p = r'D:\ST\SillyTavern\data\default-user\characters\Metaverse-Final.json'
d = json.load(open(p, 'r', encoding='utf-8'))

fm = "【METAVERSE 命运观测终端】\n\n1.拔示巴  2.蕾娜  3.米姆  4.贝尔泽ブト  5.艾莉ニ\n\n输入数字后回车"

sp = "用户输入1-5时，回复该角色的开局编号列表并说'请选择编号'。用户再次选择后，以该角色身份开始叙述。绝对禁止跳步。"

d['first_mes'] = fm
d['data']['first_mes'] = fm
d['data']['system_prompt'] = sp

json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('OK')