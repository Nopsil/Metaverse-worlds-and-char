#!/usr/bin/env python3
"""Extract specific character entry contents for manual audit."""
import json

JSON_PATH = r"C:\Users\nopsi\Desktop\metaverse工程\card\CHUNITHM-Metaverse.json"

TARGETS = [
    "该隐", "艾克雷尔", "提亚马特", "远古之蓝", "泰斯塔蒙特",
    "凯南", "米吉多", "马尔库特的女神", "格兰雷斯", "拉托娜",
    "达因斯雷夫", "断绝的破坏神", "塞蕾", "迪安", "安歇尔",
    "NEO", "金恩", "雪儿", "斯托姆", "尼加尔", "贝格尔米尔",
    "天狼星", "轩辕十四", "修伯利斯", "布里兰特", "格拉维",
    "索尔娜", "塞拉菲娜", "塞夏特", "古龙", "混沌巨人",
    "奥米茄", "伊泽维尔", "约拿", "基德翁", "米利安姆",
    "萨乌尔", "布鲁斯坦因", "梅尼", "潘多拉", "利希德修茨",
    "WISEMAN", "狄安娜", "露娜", "阿雷斯", "贝尔泽布特",
    "厄里斯", "捷夫提", "提丰", "尤巴尔", "缇欧", "梅德",
]

with open(JSON_PATH, 'r', encoding='utf-8') as f:
    data = json.load(f)

entries = data['entries']
found = set()

for key, entry in entries.items():
    comment = entry.get('comment', '')
    display = entry.get('display_name', '')
    content = entry.get('content', '')
    uid = entry.get('uid')

    for target in TARGETS:
        if target in comment or target in display:
            if target in found:
                continue
            found.add(target)
            # Print summary
            series_match = None
            for line in content.split('\n'):
                if '系列:' in line or '系列：' in line:
                    series_match = line.strip()
                    break

            print(f"\n{'='*60}")
            print(f"UID={uid} | {display}")
            print(f"SERIES: {series_match}")
            print(f"CONTENT LENGTH: {len(content)} chars")
            print(f"FULL CONTENT:")
            print(content)
            print(f"---END---")
            break

print(f"\n\n找不到的: {set(TARGETS) - found}")
