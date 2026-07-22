#!/usr/bin/env python3
"""
审计电脑世界篇其他时期 + 地上真人篇 + 乐园事变角色
对照 Metaverse-New.json vs MD源文件
重点提取外貌/性格/衣着/武器/技能，只标记差异
"""

import json
import os
import re
from pathlib import Path

BASE = Path(r"C:/Users/nopsi/Desktop/metaverse工程")
JSON_PATH = BASE / "new_card" / "Metaverse-New.json"
MD_DIR = BASE / "metaverse_full_story"

# Character mapping: (md_filename, json_uid, json_comment, arc)
# None json_uid means no dedicated JSON entry
CHARACTERS = [
    # === Liberate期 ===
    ("MIR201", 55, "赫卡蒂", "Liberate期"),
    ("MIR202", 131, "阿尔忒弥斯", "Liberate期"),
    ("MIR203", 129, "塞蕾娜", "Liberate期"),
    ("serafita", 21, "塞拉菲塔", "Liberate期"),
    
    # === Observe期 ===
    ("MDA01", None, "MDA-01天狼星", "Observe期"),  # no dedicated JSON entry
    ("brillante", 71, "布里兰特", "Observe期"),
    ("grave", 73, "格拉维", "Observe期"),
    ("MDA21", None, "MDA-21", "Observe期"),  # no dedicated JSON entry
    
    # === Revive期 ===
    ("seele", 68, "塞蕾", "Revive期"),
    ("negal", 70, "尼加尔", "Revive期"),
    ("bergelmir", 74, "贝格尔米尔", "Revive期"),
    ("neo", 105, "NEO", "Revive期"),
    ("wiseman", 51, "WISEMAN", "Revive期"),
    ("dyan", 45, "迪安", "Revive期"),
    ("ciel", 59, "雪儿", "Revive期"),
    
    # === 地上真人篇 ===
    ("ahab", 41, "亚哈", "地上真人篇"),
    ("bathsheba", 25, "拔示巴", "地上真人篇"),
    ("lena", 24, "蕾娜", "地上真人篇"),
    ("izevel", 81, "伊泽维尔", "地上真人篇"),
    ("yona", 82, "约拿", "地上真人篇"),
    ("gideon", 83, "基德翁", "地上真人篇"),
    ("miliam", 84, "米利安姆", "地上真人篇"),
    ("saul", 85, "萨乌尔", "地上真人篇"),
    ("megit", 87, "米吉多", "地上真人篇"),
    ("mene", 88, "梅尼", "地上真人篇"),
    
    # === 乐园事变 ===
    ("kainan", 50, "凯南", "乐园事变"),
    ("mythra", 53, "米斯拉", "乐园事变"),
    ("nier", 54, "尼亚", "乐园事变"),
    ("solo", 90, "索罗", "乐园事变"),
    ("zargon", 57, "萨尔贡", "乐园事变"),
    ("dandy", 58, "丹迪", "乐园事变"),
    ("marduk", 94, "马尔杜克", "乐园事变"),
    ("eva", 95, "艾娃", "乐园事变"),
    ("elisha", 96, "艾莉夏", "乐园事变"),
    ("nadin", 97, "纳丁", "乐园事变"),
    ("durweg", 98, "德威格", "乐园事变"),
    ("anshal", 99, "安夏尔", "乐园事变"),
    ("estel", 100, "艾斯特尔", "乐园事变"),
    ("leya", 101, "蕾亚", "乐园事变"),
    ("wv", 102, "沃特", "乐园事变"),
    ("xevel", 103, "赛罗", "乐园事变"),  # also known as zevel
    ("rod", 104, "洛特", "乐园事变"),
]

def load_json():
    with open(JSON_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def extract_json_section(content, section_name):
    """Extract a named section from JSON content text."""
    # Pattern: "section_name:\n  lines" or "section_name: text"
    patterns = [
        rf'{section_name}:\s*\n(\s+(?:.|\n)*?)(?=\n\S|\Z)',
        rf'{section_name}:\s*(.+?)(?:\n|$)',
    ]
    for pat in patterns:
        m = re.search(pat, content)
        if m:
            return m.group(1).strip()
    return None

def extract_json_character_data(content):
    """Extract structured sections from JSON character content."""
    sections = {}
    section_names = ['外貌特征', '性格', '衣着', '武器', '技能', '装备', '战斗风格', 
                     '基本信息', '背景设定', '人格', 'characteristics']
    
    # Try to find all labeled sections
    for name in section_names:
        val = extract_json_section(content, name)
        if val:
            sections[name] = val
    
    # Also try to capture everything between 外貌特征 and next major section
    return sections

def read_md_file(md_name):
    """Read MD file content."""
    md_path = MD_DIR / f"{md_name}.md"
    if md_path.exists():
        with open(md_path, 'r', encoding='utf-8') as f:
            return f.read()
    return None

def extract_md_appearance(md_content):
    """Extract appearance-related info from MD narrative."""
    appearance_keywords = ['发', '瞳', '眼', '色', '白', '黑', '金', '银', '红', 
                           '蓝', '绿', '紫', '装', '服', '衣', '披风', '斗篷',
                           '手套', '靴', '翅膀', '身体', '外貌', '容貌']
    lines = md_content.split('\n')
    relevant = []
    for line in lines:
        line_clean = line.strip()
        if not line_clean:
            continue
        if any(kw in line_clean for kw in appearance_keywords):
            # Skip pure narrative action lines
            if any(skip in line_clean for skip in ['展开', '发射', '攻击', '战斗', '炮', '枪口']):
                if not any(d in line_clean for d in ['头发', '瞳', '眼', '穿着', '服装', '身披', '携带']):
                    continue
            if len(line_clean) > 15 and len(line_clean) < 300:
                relevant.append(line_clean)
    return relevant[:15]

def extract_md_personality(md_content):
    """Extract personality-related info from MD narrative."""
    personality_keywords = ['性格', '温柔', '冷酷', '坚定', '善良', '残酷', '冷静',
                            '热心', '冷漠', '傲慢', '谦虚', '勇敢', '胆小', '忠诚',
                            '冷静', '理性', '感情', '意志', '信念', '决心', '优しい',
                            '慈爱', '正义', '温柔', '守护', '使命']
    lines = md_content.split('\n')
    relevant = []
    for line in lines:
        line_clean = line.strip()
        if len(line_clean) > 10 and any(kw in line_clean for kw in personality_keywords):
            relevant.append(line_clean)
    return relevant[:15]

def compare_character(md_name, json_uid, json_comment, arc, json_data):
    """Compare a single character between JSON and MD."""
    result = {
        'md_name': md_name,
        'json_comment': json_comment,
        'arc': arc,
        'json_uid': json_uid,
        'json_sections': {},
        'md_exists': False,
        'md_size': 0,
        'differences': [],
        'json_only_details': [],  # things in JSON not easily found in MD
    }
    
    # Get JSON data
    if json_uid is not None:
        entry = json_data['entries'].get(str(json_uid))
        if entry:
            content = entry.get('content', '')
            result['json_sections'] = extract_json_character_data(content)
            result['json_content_preview'] = content[:2000]
    
    # Read MD file
    md_content = read_md_file(md_name)
    if md_content:
        result['md_exists'] = True
        result['md_size'] = len(md_content)
        result['md_appearance_lines'] = extract_md_appearance(md_content)
        result['md_personality_lines'] = extract_md_personality(md_content)
        result['md_first_200'] = md_content[:200]
    
    # Check for additional MD files (metaverse variants, etc.)
    variants = []
    for suffix in ['_metaverse', '2']:
        variant_md = MD_DIR / f"{md_name}{suffix}.md"
        if variant_md.exists():
            variants.append(f"{md_name}{suffix}.md")
    if variants:
        result['variants'] = variants
    
    return result

def main():
    json_data = load_json()
    
    results = []
    for md_name, json_uid, json_comment, arc in CHARACTERS:
        r = compare_character(md_name, json_uid, json_comment, arc, json_data)
        results.append(r)
    
    # === REPORT ===
    report_lines = []
    report_lines.append("=" * 80)
    report_lines.append("角色审计报告 — 电脑世界篇(Liberate/Observe/Revive) + 地上真人篇 + 乐园事变")
    report_lines.append("对照源: Metaverse-New.json")
    report_lines.append("=" * 80)
    
    for arc_name in ["Liberate期", "Observe期", "Revive期", "地上真人篇", "乐园事变"]:
        arc_results = [r for r in results if r['arc'] == arc_name]
        report_lines.append(f"\n{'='*60}")
        report_lines.append(f"## {arc_name} ({len(arc_results)}个角色)")
        report_lines.append(f"{'='*60}")
        
        for r in arc_results:
            report_lines.append(f"\n--- {r['md_name']} ({r['json_comment']}) ---")
            
            if not r['md_exists']:
                report_lines.append(f"  ❌ MD文件不存在: {r['md_name']}.md")
                continue
            
            report_lines.append(f"  MD文件: {r['md_name']}.md ({r['md_size']} bytes)")
            if r.get('variants'):
                report_lines.append(f"  变体文件: {', '.join(r['variants'])}")
            
            if r['json_uid'] is None:
                report_lines.append(f"  ⚠️ JSON中无独立条目（仅在势力/组织条目中被提及）")
                report_lines.append(f"  MD开头: {r.get('md_first_200', 'N/A')[:150]}...")
                continue
            
            sections = r['json_sections']
            if not sections:
                report_lines.append(f"  ⚠️ JSON中未找到结构化章节（外貌/性格等）")
            else:
                for sec_name, sec_val in sections.items():
                    report_lines.append(f"  [{sec_name}]: {sec_val[:200]}{'...' if len(sec_val)>200 else ''}")
            
            report_lines.append(f"  MD外貌相关行数: {len(r.get('md_appearance_lines', []))}")
            report_lines.append(f"  MD性格相关行数: {len(r.get('md_personality_lines', []))}")
    
    # Summary statistics
    report_lines.append(f"\n{'='*60}")
    report_lines.append("统计汇总")
    report_lines.append(f"{'='*60}")
    total = len(results)
    has_json = sum(1 for r in results if r['json_uid'] is not None)
    no_json = sum(1 for r in results if r['json_uid'] is None)
    has_md = sum(1 for r in results if r['md_exists'])
    has_sections = sum(1 for r in results if r['json_sections'])
    report_lines.append(f"总角色数: {total}")
    report_lines.append(f"JSON有独立条目: {has_json}")
    report_lines.append(f"JSON无独立条目: {no_json} (MDA01/MDA21)")
    report_lines.append(f"MD文件存在: {has_md}")
    report_lines.append(f"MD文件缺失: {total - has_md}")
    report_lines.append(f"JSON有结构化章节(外貌/性格): {has_sections}")
    
    # Print to stdout
    print('\n'.join(report_lines))
    
    # Save report
    report_path = BASE / "audit_report.txt"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report_lines))
    print(f"\n报告已保存: {report_path}")
    
    return results

if __name__ == '__main__':
    main()
