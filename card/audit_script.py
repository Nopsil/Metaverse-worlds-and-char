#!/usr/bin/env python3
"""Knowledge boundary audit for CHUNITHM-Metaverse world book."""

import json
import re
import sys
from collections import defaultdict

JSON_PATH = r"C:\Users\nopsi\Desktop\metaverse工程\card\CHUNITHM-Metaverse.json"

# ─── Era definitions (character name → era/series) ───
ERA_MAP = {
    # 旧人类战争篇 (earliest, Earth)
    "艾克雷尔": "旧人类战争篇",
    "该隐": "旧人类战争篇",
    "达因斯雷夫": "旧人类战争篇",
    "提亚马特": "旧人类战争篇",
    "拉托娜": "旧人类战争篇",
    "格兰雷斯": "旧人类战争篇",
    "断绝的破坏神": "旧人类战争篇",

    # 电脑世界篇 - Liberate期
    "赫卡蒂": "Liberate期",
    "阿尔忒弥斯": "Liberate期",
    "塞蕾娜": "Liberate期",
    "远古之蓝": "Liberate期",
    "利希德修茨": "Liberate期",
    "提丰": "Liberate期",
    "WISEMAN": "Liberate期",
    "潘多拉": "Liberate期",

    # 电脑世界篇 - Observe期
    "天狼星": "Observe期",
    "轩辕十四": "Observe期",
    "修伯利斯": "Observe期",
    "厄里斯": "Observe期",
    "布里兰特": "Observe期",
    "格拉维": "Observe期",
    # TXR-梅尔维亚 not found in list

    # 电脑世界篇 - Reconnect期
    "狄安娜": "Reconnect期",
    "露娜": "Reconnect期",
    "塞拉菲塔": "Reconnect期",
    "阿雷斯": "Reconnect期",
    "捷夫提": "Reconnect期",
    "尤巴尔": "Reconnect期",  # Dr.三人组
    "缇欧": "Reconnect期",    # Dr.三人组
    "梅德": "Reconnect期",    # Dr.三人组
    "泰斯塔蒙特": "Reconnect期",
    "贝尔泽布特": "Reconnect期",

    # 电脑世界篇 - Revive期
    "安歇尔": "Revive期",
    "NEO": "Revive期",
    "金恩": "Revive期",
    "塞蕾": "Revive期",
    "雪儿": "Revive期",
    "斯托姆": "Revive期",
    "迪安": "Revive期",
    "尼加尔": "Revive期",
    "贝格尔米尔": "Revive期",

    # 新世界篇
    "米姆": "新世界篇",
    "塞拉菲娜": "新世界篇",
    "塞夏特": "新世界篇",
    "古龙": "新世界篇",
    "混沌巨人": "新世界篇",
    "索尔娜": "新世界篇",

    # 地上真人篇
    "奥米茄": "地上真人篇",
    "伊泽维尔": "地上真人篇",
    "约拿": "地上真人篇",
    "蕾娜": "地上真人篇",
    "基德翁": "地上真人篇",
    "米利安姆": "地上真人篇",
    "萨乌尔": "地上真人篇",
    "布鲁斯坦因": "地上真人篇",
    "米吉多": "地上真人篇",
    "亚哈": "地上真人篇",
    "拔示巴": "地上真人篇",
    "梅尼": "地上真人篇",
    "凯南": "地上真人篇",
    "艾尔": "地上真人篇",
    "米斯拉": "地上真人篇",
    "尼亚": "地上真人篇",
    "萨尔贡": "地上真人篇",
    "索罗": "地上真人篇",
    "丹迪": "地上真人篇",
    "泽法": "地上真人篇",
    "约基姆": "地上真人篇",
    "艾萨克": "地上真人篇",
    "米卡": "地上真人篇",
    "马尔杜克": "地上真人篇",
    "艾娃": "地上真人篇",
    "艾莉夏": "地上真人篇",
    "纳丁": "地上真人篇",
    "德威格": "地上真人篇",
    "安夏尔": "地上真人篇",
    "艾斯特尔": "地上真人篇",
    "蕾亚": "地上真人篇",
    "沃特": "地上真人篇",
    "赛罗": "地上真人篇",
    "洛特": "地上真人篇",
    "尼亚拔示巴": "地上真人篇",
    "索罗Metaverse": "地上真人篇",
    "米斯拉Metaverse": "地上真人篇",
    "拔示巴Metaverse": "地上真人篇",
    "艾比斯": "地上真人篇",
    "莉扎": "地上真人篇",
    "海凯": "地上真人篇",
    "马尔库特的女神": "地上真人篇",
    "觉醒者巴西安": "地上真人篇",
    "灾厄简": "地上真人篇",

    # 次元放浪记
    "威廉": "次元放浪记",
    "艾莉尼": "次元放浪记",
    "玛利亚": "次元放浪记",
    "林内": "次元放浪记",
    "拉维娜": "次元放浪记",
    "阿斯托尔": "次元放浪记",
    "艾弗雷特": "次元放浪记",
    "格雷": "次元放浪记",
    "希尔德": "次元放浪记",
    "安克": "次元放浪记",
    "海伯里昂": "次元放浪记",
    "毛毛": "次元放浪记",
    "皮埃尔": "次元放浪记",
    "利兹利斯威尔": "次元放浪记",
    "拉菲恩": "次元放浪记",
    "调谐者": "次元放浪记",
    "瓦尔马西亚的亡灵": "次元放浪记",
    "贝奈黛塔": "次元放浪记",
    "诺瓦": "次元放浪记",
    "拉尔瓦": "次元放浪记",
}

# ─── Forbidden knowledge by era ───
# Concepts with regex patterns to catch variations
FORBIDDEN = {
    "旧人类战争篇": [
        # Concepts that didn't exist yet
        (r"程序(?!.*(?:旧人类|废土|KHD|旧都市))", "程序(Metaverse生命体)"),
        (r"归还种", "归还种"),
        (r"涅墨西斯", "涅墨西斯"),
        (r"FREQ[-\s]?Vertex", "FREQ-Vertex"),
        (r"框架主脑", "框架主脑(他们死后才出现)"),
        (r"MIR[-\s]?(?:系列|201|202|203)", "MIR系列"),
        (r"MDA[-\s]?(?:系列|01|21)", "MDA系列"),
        (r"ES(?:计划|姐妹|-\d)", "ES计划"),
        (r"三贤者", "三贤者(工厂)"),
        (r"传送(?:门|坐标)", "传送门"),
        (r"真人(?!.*(?:旧人类|废土))", "真人(Artificial Humans)"),
        (r"Metaverse(?!.*(?:创世纪|建造|开发|设计))", "Metaverse后期概念"),
        (r"机械种", "机械种"),
        (r"VOX", "VOX管理终端"),
        (r"人类素体", "人类素体(MIR基础)"),
        (r"进化(?!.*(?:人类|生物))", "程序的进化"),
        (r"寿命(?!.*(?:人类|自然|生物))", "程序的寿命"),
        (r"乐园事变", "乐园事变"),
    ],
    "Liberate期": [
        (r"归还种", "归还种"),
        (r"真人(?!.*(?:制造|创造))", "真人(地上世界)"),
        (r"乐园事变", "乐园事变"),
        (r"Reconnect(?:期|篇)", "Reconnect期事件"),
        (r"Revive(?:期|篇)", "Revive期事件"),
        (r"新世界(?:篇|时代)", "新世界篇"),
        (r"圣遗物", "圣遗物"),
        (r"革新者", "革新者(真人组织)"),
        (r"拔示巴", "拔示巴"),
        (r"母体", "母体计划"),
        (r"地上(?:世界|复兴)", "地上世界"),
        (r"恩迪商会", "恩迪商会"),
        (r"LOGOS(?!.*(?:雏形|原始))", "LOGOS组织"),
    ],
    "Observe期": [
        (r"归还种", "归还种"),
        (r"真人", "真人"),
        (r"乐园事变", "乐园事变"),
        (r"Reconnect(?:期|篇)(?!.*(之前|历史|曾经))", "Reconnect期之后"),
        (r"Revive(?:期|篇)", "Revive期"),
        (r"新世界(?:篇|时代)", "新世界篇"),
        (r"圣遗物", "圣遗物"),
        (r"革新者", "革新者"),
        (r"地上(?:世界|复兴)", "地上世界"),
    ],
    "Reconnect期": [
        (r"Revive(?:期|篇)", "Revive期及之后"),
        (r"新世界(?:篇|时代)", "新世界篇"),
        (r"圣遗物", "圣遗物"),
        (r"乐园事变", "乐园事变"),
        (r"归还种", "归还种"),
        (r"革新者", "革新者"),
        (r"真人(?!.*(?:制造|创造|起源))", "真人(地上世界)"),
        (r"拔示巴(?!.*(?:战役))", "拔示巴(biblical除外)"),
        (r"米姆", "米姆·米库拉"),
        (r"索尔娜", "索尔娜"),
        (r"塞拉菲娜", "塞拉菲娜"),
    ],
    "Revive期": [
        (r"新世界(?:篇|时代)", "新世界篇"),
        (r"圣遗物", "圣遗物"),
        (r"米姆", "米姆·米库拉"),
        (r"索尔娜", "索尔娜"),
        (r"塞拉菲娜", "塞拉菲娜"),
        (r"塞夏特", "塞夏特"),
        (r"古龙", "古龙"),
        (r"乐园事变", "乐园事变"),
        (r"归还种", "归还种"),
    ],
    "新世界篇": [
        # Most concepts open, but specific restrictions
        (r"伊欧尼亚屠杀", "伊欧尼亚屠杀"),
        (r"拔示巴战役(?!.*(?:传说|传闻|据说))", "拔示巴战役详情"),
        (r"革新者分裂", "革新者分裂详情"),
        (r"归还种.*?(?:详情|具体|内幕)", "归还种详情"),
    ],
    "地上真人篇": [
        (r"Metaverse.*?(?:内部|神战|最古|核心层)", "Metaverse内部详情"),
        (r"FREQ[-\s]?Vertex", "FREQ-Vertex"),
        (r"框架主脑.*?(?:内部|权力|斗争|合议)", "框架主脑内部详情"),
        (r"艾克雷尔(?!.*(?:传说|创世|神话))", "艾克雷尔详情"),
        (r"提丰(?!.*(?:传说|历史))", "提丰详情"),
        (r"新世界(?:篇|时代)", "新世界篇"),
        (r"圣遗物", "圣遗物"),
        (r"混沌七器", "混沌七器详情"),
        (r"涅墨西斯(?!.*(?:传说|历史|曾经))", "涅墨西斯详情"),
        (r"MIR[-\s]?(?:系列|201|202|203|三姐妹)", "MIR系列详情"),
        (r"ES(?:计划|姐妹)(?!.*(?:制造|创造))", "ES计划详情"),
    ],
    "次元放浪记": [
        # Varied by character - mark as "needs manual review"
    ],
}


def load_entries():
    with open(JSON_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data['entries']


def get_era(entry):
    """Determine era for a character entry."""
    comment = entry.get('comment', '')
    display = entry.get('display_name', '')

    # Skip system/setting entries
    setting_entries = [
        '世界设定', '时间线', 'Metaverse核心层', '中间层世界群', '最外周部',
        '地上世界', '势力_框架主脑', '势力_工厂', '势力_MIR系列', '势力_涅墨西斯',
        '势力_革新者', '势力_LOGOS', '势力_拾荒者', '势力_IDC', '势力_恩迪商会',
        '势力_独立旅人', '卡斯比裂谷', '系统规则', '安特路亚', 'ジグラット',
    ]
    if comment in setting_entries:
        return None

    # Match by comment
    for name, era in ERA_MAP.items():
        if name in comment:
            return era

    # Try display name
    for name, era in ERA_MAP.items():
        if name in display:
            return era

    return "UNKNOWN"


def normalize_text(text):
    """Remove formatting and normalize for searching."""
    # Remove markdown formatting
    text = re.sub(r'#+\s*', '', text)
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    text = re.sub(r'`[^`]+`', '', text)
    return text


def check_entry(entry, era):
    """Check a single entry for forbidden knowledge. Returns list of violations."""
    if era not in FORBIDDEN:
        return []

    content = entry.get('content', '')
    comment = entry.get('comment', '')
    display = entry.get('display_name', '')
    normalized = normalize_text(content)

    violations = []
    for pattern, concept in FORBIDDEN[era]:
        matches = re.finditer(pattern, normalized, re.IGNORECASE)
        for m in matches:
            matched_text = m.group(0).strip()
            # Get context (±40 chars)
            start = max(0, m.start() - 40)
            end = min(len(normalized), m.end() + 40)
            context = normalized[start:end].replace('\n', ' ')

            violations.append({
                'entry': f"{display} (uid={entry.get('uid')})",
                'concept': concept,
                'match': matched_text,
                'context': f"...{context}..."
            })

    return violations


def main():
    entries = load_entries()
    all_violations = defaultdict(list)

    character_count = 0
    unknown = []

    for key, entry in entries.items():
        era = get_era(entry)
        if era is None:
            continue

        if era == "UNKNOWN":
            unknown.append(f"uid={entry.get('uid')}, comment={entry.get('comment')}, display={entry.get('display_name')}")
            continue

        character_count += 1
        violations = check_entry(entry, era)
        if violations:
            all_violations[era].extend(violations)

    # Print results
    print(f"=== 知识边界审计报告 ===")
    print(f"总字符条目数: {character_count}")
    print(f"未知分组的条目: {len(unknown)}")
    if unknown:
        print("\n--- 未分类条目 ---")
        for u in unknown[:20]:
            print(f"  {u}")

    print(f"\n--- 违规汇总 ---")
    total_violations = 0
    for era in sorted(all_violations.keys()):
        vlist = all_violations[era]
        total_violations += len(vlist)
        print(f"\n## {era} ({len(vlist)}处违规)")
        # Group by concept
        by_concept = defaultdict(list)
        for v in vlist:
            by_concept[v['concept']].append(v)

        for concept, items in sorted(by_concept.items()):
            print(f"\n  [{concept}] ({len(items)}处)")
            for item in items[:5]:  # Show up to 5 per concept
                print(f"    - {item['entry']}: \"{item['match']}\"")
                print(f"      上下文: {item['context']}")
            if len(items) > 5:
                print(f"    ... 还有 {len(items)-5} 处")

    print(f"\n\n总违规数: {total_violations}")

    # Also save detailed report
    report_path = r"C:\Users\nopsi\Desktop\metaverse工程\card\audit_report.json"
    report = {
        'total_characters': character_count,
        'unknown': unknown,
        'violations_by_era': {
            era: vlist for era, vlist in all_violations.items()
        },
        'total_violations': total_violations
    }
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"\n详细报告已保存至: {report_path}")


if __name__ == '__main__':
    main()
