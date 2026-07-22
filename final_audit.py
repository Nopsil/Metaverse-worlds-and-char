#!/usr/bin/env python3
"""
Final direct comparison: JSON 外貌特征 vs MD 外貌特征
For all 40 target characters, extract both sections and compare key attributes.
"""

import json
import re
from pathlib import Path

BASE = Path(r"C:/Users/nopsi/Desktop/metaverse工程")
JSON_PATH = BASE / "new_card" / "Metaverse-New.json"
MD_DIR = BASE / "metaverse_full_story"

# Target characters
CHARS = [
    # Liberate期
    ("MIR201", 55, "赫卡蒂", "Liberate"), ("MIR202", 131, "阿尔忒弥斯", "Liberate"),
    ("MIR203", 129, "塞蕾娜", "Liberate"), ("serafita", 21, "塞拉菲塔", "Liberate"),
    # Observe期
    ("MDA01", None, "MDA-01天狼星", "Observe"), ("brillante", 71, "布里兰特", "Observe"),
    ("grave", 73, "格拉维", "Observe"), ("MDA21", None, "MDA-21轩辕十四", "Observe"),
    # Revive期
    ("seele", 68, "塞蕾", "Revive"), ("negal", 70, "尼加尔", "Revive"),
    ("bergelmir", 74, "贝格尔米尔", "Revive"), ("neo", 105, "NEO", "Revive"),
    ("wiseman", 51, "WISEMAN", "Revive"), ("dyan", 45, "迪安", "Revive"),
    ("ciel", 59, "雪儿", "Revive"),
    # 地上真人篇
    ("ahab", 41, "亚哈", "地上真人"), ("bathsheba", 25, "拔示巴", "地上真人"),
    ("lena", 24, "蕾娜", "地上真人"), ("izevel", 81, "伊泽维尔", "地上真人"),
    ("yona", 82, "约拿", "地上真人"), ("gideon", 83, "基德翁", "地上真人"),
    ("miliam", 84, "米利安姆", "地上真人"), ("saul", 85, "萨乌尔", "地上真人"),
    ("megit", 87, "米吉多", "地上真人"), ("mene", 88, "梅尼", "地上真人"),
    # 乐园事变
    ("kainan", 50, "凯南", "乐园事变"), ("mythra", 53, "米斯拉", "乐园事变"),
    ("nier", 54, "尼亚", "乐园事变"), ("solo", 90, "索罗", "乐园事变"),
    ("zargon", 57, "萨尔贡", "乐园事变"), ("dandy", 58, "丹迪", "乐园事变"),
    ("marduk", 94, "马尔杜克", "乐园事变"), ("eva", 95, "艾娃", "乐园事变"),
    ("elisha", 96, "艾莉夏", "乐园事变"), ("nadin", 97, "纳丁", "乐园事变"),
    ("durweg", 98, "德威格", "乐园事变"), ("anshal", 99, "安夏尔", "乐园事变"),
    ("estel", 100, "艾斯特尔", "乐园事变"), ("leya", 101, "蕾亚", "乐园事变"),
    ("wv", 102, "沃特", "乐园事变"), ("xevel", 103, "赛罗", "乐园事变"),
    ("rod", 104, "洛特", "乐园事变"),
]

def load_json():
    with open(JSON_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def extract_json_appearance(content):
    """Extract 外貌特征 section from JSON content."""
    m = re.search(r'外貌特征:\s*\n((?:\s+.*\n?)*?)(?=\n\S+:\s|\n</npc>|\Z)', content)
    if m:
        return m.group(1).strip()
    return ""

def extract_md_appearance(content):
    """Extract **外貌特征** section from MD content."""
    m = re.search(r'\*\*外貌特征\*\*[：:]\s*(.+?)(?:。|\n|$)', content)
    if m:
        return m.group(1).strip()
    # Try alternate format
    m = re.search(r'外貌特征:\s*\n((?:\s+.*\n?)*?)(?=\n##|\n\S+:\s|\Z)', content)
    if m:
        return m.group(1).strip()
    return ""

def parse_appearance(text):
    """Parse appearance text into structured attributes."""
    attrs = {}
    
    # Hair color
    hair_map = {
        '金发': ['金发', '金色头发', '金髪'], '银发': ['银发', '银白发', '银白', '银色'],
        '白发': ['白发', '白髪', '白色'], '黑发': ['黑发', '黑髪', '黑色', '乌黑'],
        '红发': ['红发', '赤发', '红色头发'], '蓝发': ['蓝发', '青色'],
        '紫发': ['紫发'], '粉发': ['粉发', '粉色'], '绿发': ['绿发'],
        '棕发': ['棕发', '茶发'], '灰蓝发': ['灰蓝'],
        '双马尾': ['双马尾'], '渐变': ['渐变'],
        '粉蓝渐变': ['粉蓝渐变'],
    }
    for color, patterns in hair_map.items():
        for pat in patterns:
            if pat in text:
                attrs['hair'] = color
                break
    
    # Eye color
    eye_map = {
        '红瞳': ['红瞳', '红色眼', '红眼', '赤瞳', '红色双眼'],
        '蓝瞳': ['蓝瞳', '蓝色眼', '蓝眼'], '绿瞳': ['绿瞳', '绿色眼', '绿眼'],
        '紫瞳': ['紫瞳', '紫色眼', '紫眼', '深紫色眼'],
        '黄瞳': ['黄瞳', '黄色眼', '黄眼', '金色眼眸'],
        '黑瞳': ['黑瞳', '黑色眼', '黑眼'], '金瞳': ['金瞳', '金色眼'],
        '粉瞳': ['粉瞳', '粉色眼'], '棕瞳': ['棕瞳', '棕色眼'],
        '浅紫/淡粉': ['浅紫色', '淡粉色'],
    }
    for color, patterns in eye_map.items():
        for pat in patterns:
            if pat in text:
                attrs['eye'] = color
                break
    
    # Weapon
    weapon_map = {
        '链锯': ['链锯'], '剑': ['剑'], '镰刀': ['镰刀', '大镰'],
        '枪/长枪': ['长枪', '光之长枪'], '枪械': ['枪械', '火器', '多管枪', '机关枪'],
        '锤': ['锤', '巨锤'], '弓': ['弓'], '杖/权杖': ['权杖', '法杖', '魔杖'],
        '刀': ['刀'], '盾': ['盾牌', '盾'], '矛': ['矛', '长矛'],
        '大剑': ['大剑', '巨剑'], '机械臂': ['机械臂'],
        '双刃枪': ['双刃枪', '双刃'], '手枪': ['手枪'],
    }
    weapons_found = []
    for w, patterns in weapon_map.items():
        for pat in patterns:
            if pat in text:
                weapons_found.append(w)
                break
    if weapons_found:
        attrs['weapon'] = '/'.join(weapons_found)
    
    # Gender
    if '女性' in text:
        attrs['gender'] = '女'
    elif '男性' in text:
        attrs['gender'] = '男'
    elif '中性' in text or '无性别' in text:
        attrs['gender'] = '中性'
    
    return attrs

def main():
    json_data = load_json()
    
    print("=" * 90)
    print("最终审计: JSON vs MD 外貌特征直接对比")
    print("=" * 90)
    
    results = []
    
    for md_name, json_uid, json_comment, arc in CHARS:
        json_app = ""
        md_app = ""
        
        # Get JSON
        if json_uid is not None:
            entry = json_data['entries'].get(str(json_uid))
            if entry:
                json_app = extract_json_appearance(entry.get('content', ''))
        
        # Get MD
        md_path = MD_DIR / f"{md_name}.md"
        if md_path.exists():
            with open(md_path, 'r', encoding='utf-8') as f:
                md_app = extract_md_appearance(f.read())
        
        json_parsed = parse_appearance(json_app)
        md_parsed = parse_appearance(md_app)
        
        diffs = []
        for attr in ['hair', 'eye', 'weapon', 'gender']:
            jv = json_parsed.get(attr)
            mv = md_parsed.get(attr)
            if jv and mv and jv != mv:
                diffs.append(f"{attr}: JSON={jv} vs MD={mv}")
            elif jv and not mv:
                diffs.append(f"{attr}: JSON有「{jv}」, MD未标注")
            elif mv and not jv:
                diffs.append(f"{attr}: MD有「{mv}」, JSON未标注")
        
        results.append({
            'name': md_name,
            'comment': json_comment,
            'arc': arc,
            'json_parsed': json_parsed,
            'md_parsed': md_parsed,
            'diffs': diffs,
            'json_app': json_app[:150],
            'md_app': md_app[:150],
        })
        
        if diffs:
            print(f"\n⚠️ [{arc}] {md_name} ({json_comment})")
            print(f"   JSON外貌: {json_app[:120]}")
            print(f"   MD外貌:   {md_app[:120]}")
            for d in diffs:
                print(f"   ➤ 差异: {d}")
        else:
            print(f"✅ [{arc}] {md_name} ({json_comment}) — 一致")
    
    # Summary
    total = len(results)
    has_diffs = [r for r in results if r['diffs']]
    clean = total - len(has_diffs)
    
    print(f"\n{'='*90}")
    print(f"汇总统计")
    print(f"{'='*90}")
    print(f"总角色数: {total}")
    print(f"✅ 无差异: {clean}")
    print(f"⚠️ 有差异: {len(has_diffs)}")
    
    if has_diffs:
        # Group by severity
        color_diffs = [r for r in has_diffs if any('hair' in d or 'eye' in d for d in r['diffs'])]
        weapon_diffs = [r for r in has_diffs if any('weapon' in d for d in r['diffs'])]
        gender_diffs = [r for r in has_diffs if any('gender' in d for d in r['diffs'])]
        
        print(f"\n🔴 严重差异 (发色/瞳色不匹配): {len(color_diffs)}个")
        for r in color_diffs:
            print(f"   {r['name']} ({r['comment']}): {', '.join(r['diffs'])}")
        
        print(f"\n🟡 武器差异: {len(weapon_diffs)}个")
        for r in weapon_diffs:
            weapon_diff = [d for d in r['diffs'] if 'weapon' in d]
            print(f"   {r['name']} ({r['comment']}): {', '.join(weapon_diff)}")
        
        print(f"\n🟢 性别差异: {len(gender_diffs)}个")
        for r in gender_diffs:
            gd = [d for d in r['diffs'] if 'gender' in d]
            print(f"   {r['name']} ({r['comment']}): {', '.join(gd)}")

if __name__ == '__main__':
    main()
