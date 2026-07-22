#!/usr/bin/env python3
"""Refined knowledge boundary audit - separates metadata from narrative, handles era-transcending characters."""

import json
import re

JSON_PATH = r"C:\Users\nopsi\Desktop\metaverse工程\card\CHUNITHM-Metaverse.json"

# Characters who naturally transcend eras (live through multiple periods)
TRANSCENDENT = {
    "远古之蓝": "从Liberate期存活至地上真人篇，以布鲁·斯坦因身份协助归还者",
    "马尔库特的女神": "最古之一，从艾克雷尔时代存活至今，知晓提丰和框架主脑历史",
    "拉尔瓦": "???", # need to check
}

# Knows future through possession (泰斯塔蒙特's memories in 米姆)
EXCEPTIONS = {
    "米姆·米库拉": "通过泰斯塔蒙特获得电脑世界篇知识，但地上真人篇完全不知",
}

# Series classification by comment keywords
def get_series(comment, content):
    """Determine series from entry metadata."""
    series_map = {
        "旧人类战争篇": ["该隐", "艾克雷尔", "达因斯雷夫", "提亚马特", "拉托娜", "格兰雷斯", "断绝的破坏神"],
        "Liberate期": ["赫卡蒂", "阿尔忒弥斯", "塞蕾娜", "远古之蓝", "利希德修茨", "WISEMAN", "潘多拉"],
        "Observe期": ["天狼星", "轩辕十四", "修伯利斯", "布里兰特", "格拉维"],
        "Reconnect期": ["狄安娜", "露娜", "塞拉菲塔", "阿雷斯", "捷夫提", "尤巴尔", "缇欧", "梅德", "泰斯塔蒙特", "贝尔泽布特", "厄里斯"],
        "Revive期": ["安歇尔", "NEO", "金恩", "塞蕾", "雪儿", "斯托姆", "迪安", "尼加尔", "贝格尔米尔"],
        "新世界篇": ["米姆", "索尔娜", "塞拉菲娜", "塞夏特", "古龙", "混沌巨人"],
        "地上真人篇": ["奥米茄", "伊泽维尔", "约拿", "蕾娜", "基德翁", "米利安姆", "萨乌尔", "布鲁斯坦因", "米吉多", "亚哈", "拔示巴", "梅尼", "凯南", "艾尔", "米斯拉", "尼亚", "萨尔贡", "索罗", "丹迪", "泽法", "约基姆", "艾萨克", "米卡", "马尔杜克", "艾娃", "艾莉夏", "纳丁", "德威格", "安夏尔", "艾斯特尔", "蕾亚", "沃特", "赛罗", "洛特", "尼亚拔示巴", "索罗Metaverse", "米斯拉Metaverse", "拔示巴Metaverse", "艾比斯", "莉扎", "海凯", "觉醒者巴西安", "灾厄简"],
    }

    # Check by comment (the most reliable)
    for series, names in series_map.items():
        for name in names:
            if name in comment:
                return series

    # Check content for series line
    for line in content.split('\n'):
        if '系列:' in line or '系列：' in line:
            for series, names in series_map.items():
                for name in names:
                    if name in line:
                        return series
    return "UNKNOWN"


# Define what's forbidden for each character (not era) - more granular
# Rules: character should not demonstrate knowledge of concepts/events/people that
#   belong to a time period AFTER their own
# Exceptions: 1) metadata lines ("系列: ...") 2) narrative foreshadowing "在遥远的未来"  
#   3) characters who naturally live long enough 4) explicit blindspot lists

def audit_entry_manual(comment, display, content):
    """Manually identify real violations. Returns list of (issue, detail)."""
    issues = []
    series = get_series(comment, content)
    
    # Helper: check if a forbidden term appears in narrative (not metadata/foreshadowing/blindspot)
    def in_narrative(term, content):
        """Check if term appears in narrative text, excluding metadata lines and foreshadowing."""
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if term in line:
                # Skip metadata lines
                stripped = line.strip()
                if stripped.startswith('系列:') or stripped.startswith('系列：'):
                    continue
                if stripped.startswith('归属:') or stripped.startswith('归属：'):
                    continue
                # Skip explicit blindspot declarations  
                if '不知道' in line and term in line:
                    continue
                if '毫不知情' in line and term in line:
                    continue
                if '知识边界' in line:
                    continue
                # Skip narrative foreshadowing
                if '在遥远的未来' in line or '在遥远' in line:
                    continue
                if '后世' in line or '后来' in line:
                    continue
                # Skip "地上真人篇:" section headers in cross-era entries
                if stripped.startswith('地上真人篇') or stripped.startswith('新世界篇'):
                    continue
                if stripped.startswith('乐园事变时期'):
                    continue
                # Skip entry author descriptions of legacy/future (not character knowledge)
                if '遗产:' in stripped or '遗产：' in stripped:
                    continue
                if '后以' in stripped or '后成为' in stripped:
                    continue
                return True
        return False

    # For each character, define their specific forbidden terms
    if series == "旧人类战争篇":
        # Oldest era - should not know ANY later concepts as personal knowledge
        forbidden = [
            "归还种", "归还者",
            "FREQ-Vertex", "FREQ Vertex",
            "MIR-201", "MIR-202", "MIR-203", "MIR系列",
            "MDA-01", "MDA-21", "MDA系列",
            "ES计划", "ES姐妹",
            "三贤者",
            "VOX", 
            "人类素体",
            "乐园事变",
            "革新者",
        ]
        # But these are OK in specific contexts:
        # "真人" - 该隐's plan included "合成人类" → 真人 origin, OK
        # "Metaverse" - they CREATED it, OK
        # "框架主脑" - 艾克雷尔 created it, OK
        # "涅墨西斯" - 提亚马特's fragments spawned them, the ENTRY says this, not the character KNOWING it
        # "机械种" - 该隐's legacy, the entry says what happened after death, not character knowledge
        # "程序" - they existed in the original system
        for term in forbidden:
            if in_narrative(term, content):
                issues.append((f"禁止知道【{term}】", f"角色属于{series}，不应知道后来的概念"))

    elif series == "Liberate期":
        forbidden = [
            "归还种", "归还者",
            "乐园事变",
            "Revive期",
            "新世界篇", 
            "圣遗物",
            "革新者",
            "拔示巴战役",
        ]
        for term in forbidden:
            if in_narrative(term, content):
                issues.append((f"禁止知道【{term}】", f"角色属于{series}，不应知道后来的概念"))

    elif series == "Observe期":
        forbidden = [
            "归还种", "归还者",
            "乐园事变",
            "Revive期",
            "新世界篇",
            "圣遗物",
            "革新者",
        ]
        for term in forbidden:
            if in_narrative(term, content):
                issues.append((f"禁止知道【{term}】", f"角色属于{series}，不应知道后来的概念"))

    elif series == "Reconnect期":
        forbidden = [
            "Revive期",
            "新世界篇",
            "圣遗物",
            "乐园事变",
            "归还种", "归还者",
            "革新者",
            "米姆·米库拉", "米姆",
            "索尔娜",
            "塞拉菲娜",
        ]
        for term in forbidden:
            if in_narrative(term, content):
                issues.append((f"禁止知道【{term}】", f"角色属于{series}，不应知道后来的概念"))

    elif series == "Revive期":
        forbidden = [
            "新世界篇",
            "圣遗物",
            "米姆", "索尔娜", "塞拉菲娜", "塞夏特", "古龙",
            "乐园事变",
            "归还种", "归还者",
            "革新者",
        ]
        for term in forbidden:
            if in_narrative(term, content):
                issues.append((f"禁止知道【{term}】", f"角色属于{series}，不应知道后来的概念"))

    elif series == "新世界篇":
        # Special: check米姆's declared blindspots
        pass

    elif series == "地上真人篇":
        # Should not know Metaverse internal god-level details
        # But "最古" references and basic "Metaverse" are OK
        forbidden_detail = [
            "FREQ-Vertex", "FREQ Vertex",
            "MIR-201", "MIR-202", "MIR-203", 
            "混沌七器",
            "新世界篇",
            "圣遗物",
        ]
        for term in forbidden_detail:
            if in_narrative(term, content):
                issues.append((f"禁止知道【{term}】", f"角色属于{series}，不应知道Metaverse内部神战细节或未来概念"))

    return issues


def main():
    with open(JSON_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    entries = data['entries']
    all_issues = []

    # Skip system entries
    skip_uids = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 114, 131, 132}

    for key, entry in entries.items():
        uid = entry.get('uid')
        if uid in skip_uids:
            continue
            
        comment = entry.get('comment', '')
        display = entry.get('display_name', '')
        content = entry.get('content', '')

        issues = audit_entry_manual(comment, display, content)
        if issues:
            for issue, detail in issues:
                all_issues.append({
                    'uid': uid,
                    'display': display,
                    'comment': comment,
                    'series': get_series(comment, content),
                    'issue': issue,
                    'detail': detail,
                })

    # Print findings grouped by series
    from collections import defaultdict
    by_series = defaultdict(list)
    for i in all_issues:
        by_series[i['series']].append(i)

    print("=== 精炼版知识边界审计 ===")
    print(f"发现 {len(all_issues)} 处疑似真实违规\n")

    for series in sorted(by_series.keys()):
        items = by_series[series]
        print(f"\n## {series} ({len(items)}处)")
        for item in items:
            print(f"  UID={item['uid']} | {item['display']}")
            print(f"    {item['issue']}")

    # Save full report
    report_path = r"C:\Users\nopsi\Desktop\metaverse工程\card\refined_audit.json"
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(all_issues, f, ensure_ascii=False, indent=2)
    print(f"\n详细报告: {report_path}")


if __name__ == '__main__':
    main()
