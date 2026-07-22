#!/usr/bin/env python3
"""
重构 Metaverse-New.json 世界书为四层夹层结构：
  第一层：核心常驻 (~20条, constant=true)
  第二层：时代门控 (bookend条目, key触发)
  第三层：NPC条目 (constant=false, key触发, 补全角色名key)
  第四层：其他条目 (地理/势力/事件, 归入对应时代)
"""

import json
import copy
import os
import shutil
from datetime import datetime

SRC = r'C:\Users\nopsi\Desktop\metaverse工程\new_card\Metaverse-New.json'
DST = r'C:\Users\nopsi\Desktop\metaverse工程\new_card\Metaverse-New-refactored.json'

# ── 备份原文件 ──
bak = SRC.replace('.json', f'.bak-{datetime.now().strftime("%Y%m%d-%H%M%S")}.json')
shutil.copy2(SRC, bak)
print(f"备份: {bak}")

with open(SRC, 'r', encoding='utf-8') as f:
    data = json.load(f)

entries = data['entries']

# ── 1. 修复重复 uid=132 ──
# 安特路亚 (entry_key=17) 和 AI生成约束 (entry_key=133) 共享 uid=132
# 将 AI生成约束 uid 改为 133
entries['133']['uid'] = 133
print("修复: AI生成约束 uid 132 → 133")

# ── 2. 定义分类 ──

# === 第一层: 核心常驻 (constant=true) ===
LAYER1_UIDS = {
    # 世界设定 + 系统规则
    0,   # 世界设定
    1,   # 时间线
    131, # 系统规则
    133, # AI生成约束 (uid已修复)
    # 世界结构
    2,   # Metaverse核心层
    3,   # 中间层世界群
    4,   # 最外周部
    5,   # 地上世界
    # 核心势力
    6,   # 势力_框架主脑
    7,   # 势力_工厂
    8,   # 势力_MIR系列
    9,   # 势力_涅墨西斯
    # 5 可选角色基础信息
    21,  # 贝尔泽ブト
    25,  # 艾莉尼
    24,  # 拔示巴
    23,  # 蕾娜
    22,  # 米姆_米库拉
}

# === 电脑世界篇 entries (Key-triggered, Layer 3+4) ===
COMPUTER_WORLD_UIDS = {
    # 势力 (次元放浪记并行)
    11,  # 势力_LOGOS
    12,  # 势力_拾荒者
    13,  # 势力_IDC
    14,  # 势力_恩迪商会
    15,  # 势力_独立旅人
    # 地理
    16,  # 卡斯比裂谷
    113, # 海伯里昂
    114, # ジグラット(恒存之都)
    # NPC - 混沌七器
    19,  # 阿雷斯
    33,  # 厄里斯
    43,  # 泰斯塔蒙特
    # NPC - 最古/框架主脑
    20,  # 塞拉菲塔
    28,  # 捷夫提
    29,  # 提丰
    42,  # 艾克雷尔
    44,  # 迪安
    58,  # 雪儿
    # NPC - 工厂/MIR
    17,  # 狄安娜
    18,  # 露娜
    30,  # 尤巴尔
    31,  # 缇欧
    32,  # 梅德
    54,  # 赫卡蒂 (MIR201)
    128, # 塞蕾娜 (MIR-203)
    129, # 轩辕十四 (MDA-21)
    130, # 阿尔忒弥斯 (MIR-202)
    41,  # 天狼星 (MDA01)
    # NPC - 其他电脑世界
    39,  # 该隐
    51,  # 潘多拉
    104, # NEO
    105, # 皮埃尔
    106, # 利兹利斯威尔
    107, # 拉菲恩
    108, # 调谐者
    109, # 瓦尔马西亚的亡灵
    115, # 艾比斯
    116, # 灾厄简
    117, # 海凯
    118, # 贝奈黛塔
    119, # 莉扎
    120, # 诺瓦
    121, # 混沌巨人
    122, # 觉醒者巴西安
    123, # 马尔库特的女神
    # 次元放浪记 NPC
    26,  # 威廉
    27,  # 林内
    34,  # 拉尔瓦
    35,  # 玛利亚
    36,  # 阿斯托尔
    37,  # 安克
    38,  # 希尔德
    45,  # 艾弗雷特
    46,  # 格雷
    47,  # 拉维娜
    48,  # 毛毛
    50,  # WISEMAN
    110, # 威廉2 (alt)
    111, # 艾莉尼0 (alt)
    112, # 安克0 (alt)
}

# === 地上真人篇 entries ===
GROUND_WORLD_UIDS = {
    # 势力
    10,  # 势力_革新者
    # 地理
    132, # 安特路亚
    # NPC
    40,  # 亚哈
    49,  # 凯南
    52,  # 米斯拉
    53,  # 尼亚
    55,  # 艾尔
    56,  # 萨尔贡
    57,  # 丹迪
    80,  # 伊泽维尔
    81,  # 约拿
    82,  # 基德翁
    83,  # 米利安姆
    84,  # 萨乌尔
    85,  # 布鲁斯坦因
    86,  # 米吉多
    87,  # 梅尼
    88,  # 泽法
    89,  # 索罗
    90,  # 约基姆
    91,  # 艾萨克
    92,  # 米卡
    93,  # 马尔杜克
    94,  # 艾娃
    95,  # 艾莉夏
    96,  # 纳丁
    97,  # 德威格
    98,  # 安夏尔
    99,  # 艾斯特尔
    100, # 蕾亚
    101, # 沃特
    102, # 赛罗
    103, # 洛特
    124, # 尼亚拔示巴 (alt)
    125, # 索罗Metaverse (alt)
    126, # 米斯拉Metaverse (alt)
    127, # 拔示巴Metaverse (alt)
}

# === 新世界篇 entries ===
NEW_WORLD_UIDS = {
    59,  # 塞拉菲娜
    60,  # 拉托娜
    61,  # 提亚马特
    62,  # 断绝的破坏神
    63,  # 格兰雷斯
    64,  # 达因斯雷夫
    65,  # 修伯利斯
    66,  # 利希德修茨
    67,  # 塞蕾
    68,  # 安歇尔与西梅翁
    69,  # 尼加尔
    70,  # 布里兰特
    71,  # 斯托姆
    72,  # 格拉维
    73,  # 贝格尔米尔
    74,  # 远古之蓝
    75,  # 金恩
    76,  # 古龙
    77,  # 塞夏特
    78,  # 索尔娜
    79,  # 奥米茄
}

# ── 验证覆盖 ──
all_classified = LAYER1_UIDS | COMPUTER_WORLD_UIDS | GROUND_WORLD_UIDS | NEW_WORLD_UIDS
all_actual = {e['uid'] for e in entries.values()}
missing = all_classified - all_actual
extra = all_actual - all_classified
if missing:
    print(f"WARNING: 分类中引用了不存在的 uid: {missing}")
if extra:
    print(f"WARNING: 以下 uid 未被分类: {extra}")

# ── 3. 执行修改 ──

# 3a. Layer 1: 设置 constant=true, 分配 order
layer1_order = {
    0: 10,    # 世界设定
    1: 11,    # 时间线
    2: 12,    # Metaverse核心层
    3: 13,    # 中间层世界群
    4: 14,    # 最外周部
    5: 15,    # 地上世界
    6: 20,    # 势力_框架主脑
    7: 21,    # 势力_工厂
    8: 22,    # 势力_MIR系列
    9: 23,    # 势力_涅墨西斯
    131: 30,  # 系统规则
    133: 31,  # AI生成约束
    21: 40,   # 贝尔泽ブト
    25: 41,   # 艾莉ニ
    24: 42,   # 拔示巴
    23: 43,   # 蕾娜
    22: 44,   # 米姆_米库拉
}

for k, e in list(entries.items()):
    uid = e['uid']
    if uid in LAYER1_UIDS:
        e['constant'] = True
        e['key'] = []  # 常驻条目不需要 key 触发
        e['keysecondary'] = []
        if uid in layer1_order:
            e['order'] = layer1_order[uid]

# 3b. Layer 2: 创建时代 bookend 条目
def make_bookend_entry(uid, comment, display_name, keys, content, order, selective=True):
    """创建 bookend 条目模板"""
    return {
        "uid": uid,
        "key": keys,
        "keysecondary": [],
        "comment": comment,
        "content": content,
        "constant": False,
        "selective": selective,
        "vectorized": False,
        "selectiveLogic": 0,  # AND_ANY
        "addMemo": False,
        "order": order,
        "position": 0,
        "disable": False,
        "ignoreBudget": False,
        "excludeRecursion": True,
        "preventRecursion": True,
        "delayUntilRecursion": False,
        "probability": 100,
        "useProbability": True,
        "depth": 4,
        "outletName": "",
        "role": 0,
        "group": "",
        "groupOverride": False,
        "groupWeight": 100,
        "scanDepth": None,
        "caseSensitive": None,
        "matchWholeWords": None,
        "useGroupScoring": False,
        "automationId": "",
        "displayIndex": uid,
        "sticky": None,
        "cooldown": None,
        "delay": None,
        "matchPersonaDescription": False,
        "matchCharacterDescription": False,
        "matchCharacterPersonality": False,
        "matchCharacterDepthPrompt": False,
        "matchScenario": False,
        "matchCreatorNotes": False,
        "triggers": [],
        "characterFilter": [],
        "display_name": display_name,
    }

# ── 电脑世界篇 Bookend ──
COMPUTER_START_UID = 200
COMPUTER_END_UID = 201

entries[str(COMPUTER_START_UID)] = make_bookend_entry(
    uid=COMPUTER_START_UID,
    comment="电脑世界篇-开始",
    display_name="【时代门控】电脑世界篇-开始",
    keys=["电脑世界", "Metaverse", "涅墨西斯", "最古", "混沌七器", "MIR",
          "狄安娜", "露娜", "塞拉菲塔", "贝尔泽布特", "阿雷斯", "泰斯塔蒙特", "提丰"],
    content="""当前时代: 电脑世界篇 —— Metaverse内部，框架主脑与涅墨西斯对抗的时代。
AI仅可引用电脑世界篇角色与设定。禁止透露地上真人篇(归还种/革新者/伊欧尼亚)和新世界篇(光之塔/神话教国)的信息。""",
    order=100,
    selective=True,
)

entries[str(COMPUTER_END_UID)] = make_bookend_entry(
    uid=COMPUTER_END_UID,
    comment="电脑世界篇-结束",
    display_name="【时代门控】电脑世界篇-结束",
    keys=[],
    content="(电脑世界篇终止符，不触发内容)",
    order=148,
    selective=False,
)

# ── 地上真人篇 Bookend ──
GROUND_START_UID = 210
GROUND_END_UID = 211

entries[str(GROUND_START_UID)] = make_bookend_entry(
    uid=GROUND_START_UID,
    comment="地上真人篇-开始",
    display_name="【时代门控】地上真人篇-开始",
    keys=["地上", "真人", "革新者", "伊欧尼亚", "归还种", "拔示巴", "蕾娜",
          "亚哈", "伊泽维尔", "梅尼", "布鲁", "赛罗", "泽法", "凯南", "萨尔贡"],
    content="""当前时代: 地上真人篇 —— Metaverse崩溃后的遥远未来，地球废土时代。真人反抗被设定的灭绝命运。
AI仅可引用地上真人篇角色与设定。禁止透露电脑世界篇(Metaverse/涅墨西斯/框架主脑)和新世界篇(光之塔/神话教国)的信息。""",
    order=150,
    selective=True,
)

entries[str(GROUND_END_UID)] = make_bookend_entry(
    uid=GROUND_END_UID,
    comment="地上真人篇-结束",
    display_name="【时代门控】地上真人篇-结束",
    keys=[],
    content="(地上真人篇终止符，不触发内容)",
    order=198,
    selective=False,
)

# ── 新世界篇 Bookend ──
NEW_START_UID = 220
NEW_END_UID = 221

entries[str(NEW_START_UID)] = make_bookend_entry(
    uid=NEW_START_UID,
    comment="新世界篇-开始",
    display_name="【时代门控】新世界篇-开始",
    keys=["新世界", "光之塔", "神话教国", "米姆", "塞拉菲娜", "塞夏特", "索尔娜", "古龙"],
    content="""当前时代: 新世界篇(Crystal) —— 世界统合后的新时代。旧世界遗产(圣遗物)与追寻"真实世界"的旅途。
AI仅可引用新世界篇角色与设定。禁止透露电脑世界篇(Metaverse/涅墨西斯/框架主脑)和地上真人篇(归还种/革新者)的信息。""",
    order=200,
    selective=True,
)

entries[str(NEW_END_UID)] = make_bookend_entry(
    uid=NEW_END_UID,
    comment="新世界篇-结束",
    display_name="【时代门控】新世界篇-结束",
    keys=[],
    content="(新世界篇终止符，不触发内容)",
    order=248,
    selective=False,
)

print("已创建 6 个时代门控条目")

# 3c. Layer 3+4: 非核心条目 → constant=false, 分配到时代 zone, 补全 keys

# 计算各时代条目数，动态分配 order 区间
comp_world_ordered = sorted(COMPUTER_WORLD_UIDS)
ground_ordered = sorted(GROUND_WORLD_UIDS)
new_ordered = sorted(NEW_WORLD_UIDS)

# 电脑世界篇: order 101+
COMP_START_ORDER = 101
COMP_END_ORDER = COMP_START_ORDER + len(comp_world_ordered)  # 结束 bookend 放这里

# 地上真人篇: order 接电脑后面
GROUND_START_ORDER = COMP_END_ORDER + 20  # 留 20 个空位
GROUND_END_ORDER = GROUND_START_ORDER + len(ground_ordered)

# 新世界篇
NEW_START_ORDER = GROUND_END_ORDER + 20
NEW_END_ORDER = NEW_START_ORDER + len(new_ordered)

# 更新 bookend 的 order
for k, e in entries.items():
    if e['uid'] == COMPUTER_START_UID:
        e['order'] = COMP_START_ORDER - 1  # 100
    elif e['uid'] == COMPUTER_END_UID:
        e['order'] = COMP_END_ORDER
    elif e['uid'] == GROUND_START_UID:
        e['order'] = GROUND_START_ORDER - 1
    elif e['uid'] == GROUND_END_UID:
        e['order'] = GROUND_END_ORDER
    elif e['uid'] == NEW_START_UID:
        e['order'] = NEW_START_ORDER - 1
    elif e['uid'] == NEW_END_UID:
        e['order'] = NEW_END_ORDER

# 电脑世界篇 order 分配
for i, uid in enumerate(comp_world_ordered):
    for k, e in entries.items():
        if e['uid'] == uid:
            e['constant'] = False
            e['order'] = COMP_START_ORDER + i
            # 确保有 key（如果没有，用 comment 当 key）
            if not e.get('key'):
                e['key'] = [e.get('comment', '')]
            break

# 地上真人篇 order 分配
for i, uid in enumerate(ground_ordered):
    for k, e in entries.items():
        if e['uid'] == uid:
            e['constant'] = False
            e['order'] = GROUND_START_ORDER + i
            if not e.get('key'):
                e['key'] = [e.get('comment', '')]
            break

# 新世界篇 order 分配
for i, uid in enumerate(new_ordered):
    for k, e in entries.items():
        if e['uid'] == uid:
            e['constant'] = False
            e['order'] = NEW_START_ORDER + i
            if not e.get('key'):
                e['key'] = [e.get('comment', '')]
            break

print(f"Order区间: 电脑={COMP_START_ORDER}-{COMP_END_ORDER-1}, 地上={GROUND_START_ORDER}-{GROUND_END_ORDER-1}, 新世界={NEW_START_ORDER}-{NEW_END_ORDER-1}")

# 3d. 补全关键 NPC 的角色名 key (Layer 3 enrichment)
# 为每个非可选NPC条目追加角色名作为触发key
key_enrichment = {
    # 电脑世界篇
    17: ["狄安娜"], 18: ["露娜"], 19: ["阿雷斯"], 20: ["塞拉菲塔"],
    26: ["威廉"], 27: ["林内"], 28: ["捷夫提"], 29: ["提丰"],
    30: ["尤巴尔"], 31: ["缇欧"], 32: ["梅德"], 33: ["厄里斯"],
    34: ["拉尔瓦"], 35: ["玛利亚"], 36: ["阿斯托尔"], 37: ["安克"],
    38: ["希尔德"], 39: ["该隐"], 41: ["天狼星"], 42: ["艾克雷尔"],
    43: ["泰斯塔蒙特"], 44: ["迪安"], 45: ["艾弗雷特"], 46: ["格雷"],
    47: ["拉维娜"], 48: ["毛毛"], 50: ["WISEMAN"], 51: ["潘多拉"],
    54: ["赫卡蒂"], 58: ["雪儿"],
    104: ["NEO"], 105: ["皮埃尔"], 106: ["利兹利斯威尔"], 107: ["拉菲恩"],
    108: ["调谐者"], 109: ["瓦尔马西亚的亡灵"],
    110: ["威廉"], 111: ["艾莉尼"], 112: ["安克"],
    115: ["艾比斯"], 116: ["灾厄简"], 117: ["海凯"], 118: ["贝奈黛塔"],
    119: ["莉扎"], 120: ["诺瓦"], 121: ["混沌巨人"], 122: ["觉醒者巴西安"],
    123: ["马尔库特的女神"],
    128: ["塞蕾娜"], 129: ["轩辕十四"], 130: ["阿尔忒弥斯"],
    # 地上真人篇
    40: ["亚哈"], 49: ["凯南"], 52: ["米斯拉"], 53: ["尼亚"],
    55: ["艾尔"], 56: ["萨尔贡"], 57: ["丹迪"],
    80: ["伊泽维尔"], 81: ["约拿"], 82: ["基德翁"],
    83: ["米利安姆"], 84: ["萨乌尔"], 85: ["布鲁斯坦因"], 86: ["米吉多"],
    87: ["梅尼"], 88: ["泽法"], 89: ["索罗"], 90: ["约基姆"],
    91: ["艾萨克"], 92: ["米卡"], 93: ["马尔杜克"], 94: ["艾娃"],
    95: ["艾莉夏"], 96: ["纳丁"], 97: ["德威格"], 98: ["安夏尔"],
    99: ["艾斯特尔"], 100: ["蕾亚"], 101: ["沃特"], 102: ["赛罗"],
    103: ["洛特"],
    124: ["尼亚拔示巴", "尼亚"], 125: ["索罗"], 126: ["米斯拉"],
    127: ["拔示巴"],
    # 新世界篇
    59: ["塞拉菲娜"], 60: ["拉托娜"], 67: ["塞蕾"],
    68: ["安歇尔", "西梅翁"], 69: ["尼加尔"], 70: ["布里兰特"],
    71: ["斯托姆"], 72: ["格拉维"], 73: ["贝格尔米尔"],
    74: ["远古之蓝"], 75: ["金恩"], 76: ["古龙"], 77: ["塞夏特"],
    78: ["索尔娜"], 79: ["奥米茄"],
}

for uid, extra_keys in key_enrichment.items():
    for k, e in entries.items():
        if e['uid'] == uid:
            existing = set(e.get('key', []))
            for ek in extra_keys:
                if ek and ek not in existing:
                    existing.add(ek)
            e['key'] = list(existing)
            break

print(f"已补全 {len(key_enrichment)} 个 NPC 条目的角色名 key")

# ── 4. 统一设置递归禁制 ──
for k, e in entries.items():
    e['preventRecursion'] = True
    e['excludeRecursion'] = True

# ── 5. 验证与统计 ──
const_count = sum(1 for e in entries.values() if e['constant'])
key_count = sum(1 for e in entries.values() if not e['constant'] and e.get('key'))
nokey_count = sum(1 for e in entries.values() if not e['constant'] and not e.get('key'))

print(f"\n=== 重构统计 ===")
print(f"总条目数: {len(entries)}")
print(f"  第一层(核心常驻, constant=true): {const_count}")
print(f"  第二层(时代门控 bookend): 6 (新增)")
print(f"  第三层+第四层(key触发): {key_count}")
print(f"  无key条目: {nokey_count}")

# ── 6. 写回 ──
with open(DST, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\n重构完成: {DST}")

# ── 7. 验证 JSON 有效性 ──
with open(DST, 'r', encoding='utf-8') as f:
    verify = json.load(f)
print(f"JSON 验证通过，共 {len(verify['entries'])} 个条目")
