#!/usr/bin/env python3
"""
深度对比：从JSON提取关键属性（发色/瞳色/衣着/武器/技能），
在MD文件中验证是否一致，标记差异。
"""

import json
import re
from pathlib import Path

BASE = Path(r"C:/Users/nopsi/Desktop/metaverse工程")
JSON_PATH = BASE / "new_card" / "Metaverse-New.json"
MD_DIR = BASE / "metaverse_full_story"

# Hair color patterns
HAIR_PATTERNS = {
    '金发': ['金发', '金色'],
    '银发': ['银发', '银色', '银白'],
    '白发': ['白发', '白色头发', '白髪'],
    '黑发': ['黑发', '黑色头发'],
    '红发': ['红发', '红色头发', '赤发'],
    '蓝发': ['蓝发', '蓝色头发'],
    '紫发': ['紫发', '紫色头发'],
    '粉发': ['粉发', '粉色头发'],
    '绿发': ['绿发', '绿色头发'],
    '灰发': ['灰发', '灰色头发'],
    '灰蓝发': ['灰蓝'],
}

EYE_PATTERNS = {
    '金瞳': ['金瞳', '金色眼', '金眼'],
    '红瞳': ['红瞳', '红色眼', '红眼', '赤瞳'],
    '蓝瞳': ['蓝瞳', '蓝色眼', '蓝眼'],
    '绿瞳': ['绿瞳', '绿色眼', '绿眼'],
    '紫瞳': ['紫瞳', '紫色眼', '紫眼'],
    '黄瞳': ['黄瞳', '黄色眼', '黄眼'],
    '黑瞳': ['黑瞳', '黑色眼', '黑眼'],
    '棕瞳': ['棕瞳', '棕色眼'],
}

CLOTHING_KEYWORDS = ['服', '衣', '披风', '斗篷', '长袍', '外套', '裙', '铠甲',
                     '制服', '装束', '手套', '靴', '翅膀', '机械翼', '装饰']

WEAPON_KEYWORDS = ['剑', '刀', '枪', '炮', '锤', '弓', '杖', '链锯', '镰刀',
                   '盾', '权杖', '手', '武器', '兵器', '拳']

def load_json():
    with open(JSON_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def extract_hair_eye(content):
    """Extract hair color and eye color from text."""
    hair = None
    eye = None
    
    # Check explicit labels first
    for label, patterns in [('发', HAIR_PATTERNS), ('瞳', EYE_PATTERNS)]:
        for color_name, patterns_list in patterns.items():
            for pat in patterns_list:
                # Check for "X发X瞳" or "X色X瞳" pattern
                if pat in content:
                    if label == '发':
                        hair = color_name
                    else:
                        eye = color_name
                    break
    
    # Look for hair+eye combined pattern: "X发X瞳" or "X色X瞳"
    m = re.search(r'(金|银|白|黑|红|蓝|紫|粉|绿|灰蓝|灰)发\s*(金|红|蓝|绿|紫|黄|黑|棕)瞳', content)
    if m:
        hair = m.group(1) + '发' if m.group(1) else hair
        eye = m.group(2) + '瞳' if m.group(2) else eye
    
    return hair, eye

def extract_clothing_weapon(content):
    """Extract clothing and weapon descriptions."""
    clothing = []
    weapon = []
    
    for line in content.split('\n'):
        line = line.strip()
        if any(kw in line for kw in CLOTHING_KEYWORDS):
            if len(line) > 5:
                clothing.append(line)
        if any(kw in line for kw in WEAPON_KEYWORDS):
            if len(line) > 3:
                weapon.append(line)
    
    return clothing[:5], weapon[:5]

def check_consistency(json_attrs, md_content, character_name):
    """Check if JSON attributes appear in MD content."""
    issues = []
    
    # Check hair color
    json_hair = json_attrs.get('hair')
    if json_hair:
        hair_terms = HAIR_PATTERNS.get(json_hair, [json_hair])
        found = any(term in md_content for term in hair_terms)
        if not found:
            issues.append(f"⚠️ 发色差异: JSON={json_hair}, MD中未找到对应描述")
    
    # Check eye color
    json_eye = json_attrs.get('eye')
    if json_eye:
        eye_terms = EYE_PATTERNS.get(json_eye, [json_eye])
        found = any(term in md_content for term in eye_terms)
        if not found:
            issues.append(f"⚠️ 瞳色差异: JSON={json_eye}, MD中未找到对应描述")
    
    # Check weapon terms
    json_weapon_terms = json_attrs.get('weapon_terms', [])
    for wt in json_weapon_terms:
        if wt not in md_content:
            issues.append(f"⚠️ 武器差异: JSON提到'{wt}', MD中未出现")
    
    # Check for conflicting hair/eye colors in MD
    for name, patterns in [('hair', HAIR_PATTERNS), ('eye', EYE_PATTERNS)]:
        json_val = json_attrs.get(name)
        if not json_val:
            continue
        for color_name, terms in patterns.items():
            if color_name == json_val:
                continue  # skip same color
            for term in terms:
                # Only flag if the conflicting color is in a description context
                desc_matches = [m for m in re.finditer(
                    rf'(?:发|髪|头发).*?{term}|{term}.*?(?:发|髪|头发)', md_content)]
                if desc_matches and name == 'hair':
                    issues.append(f"⚠️ 发色冲突可能: JSON={json_val}, MD中出现'{term}'")
                    break
    
    return issues

def main():
    json_data = load_json()
    
    # Character mapping
    CHAR_MAP = [
        ("MIR201", 55, "赫卡蒂"), ("MIR202", 131, "阿尔忒弥斯"), ("MIR203", 129, "塞蕾娜"),
        ("serafita", 21, "塞拉菲塔"),
        ("brillante", 71, "布里兰特"), ("grave", 73, "格拉维"),
        ("seele", 68, "塞蕾"), ("negal", 70, "尼加尔"), ("bergelmir", 74, "贝格尔米尔"),
        ("neo", 105, "NEO"), ("wiseman", 51, "WISEMAN"), ("dyan", 45, "迪安"),
        ("ciel", 59, "雪儿"),
        ("ahab", 41, "亚哈"), ("bathsheba", 25, "拔示巴"), ("lena", 24, "蕾娜"),
        ("izevel", 81, "伊泽维尔"), ("yona", 82, "约拿"), ("gideon", 83, "基德翁"),
        ("miliam", 84, "米利安姆"), ("saul", 85, "萨乌尔"), ("megit", 87, "米吉多"),
        ("mene", 88, "梅尼"),
        ("kainan", 50, "凯南"), ("mythra", 53, "米斯拉"), ("nier", 54, "尼亚"),
        ("solo", 90, "索罗"), ("zargon", 57, "萨尔贡"), ("dandy", 58, "丹迪"),
        ("marduk", 94, "马尔杜克"), ("eva", 95, "艾娃"), ("elisha", 96, "艾莉夏"),
        ("nadin", 97, "纳丁"), ("durweg", 98, "德威格"), ("anshal", 99, "安夏尔"),
        ("estel", 100, "艾斯特尔"), ("leya", 101, "蕾亚"), ("wv", 102, "沃特"),
        ("xevel", 103, "赛罗"), ("rod", 104, "洛特"),
    ]
    
    print("=" * 80)
    print("深度角色审计: 发色/瞳色/衣着/武器/技能 — JSON vs MD")
    print("=" * 80)
    
    results = []
    
    for md_name, json_uid, json_comment in CHAR_MAP:
        # Get JSON content
        entry = json_data['entries'].get(str(json_uid))
        if not entry:
            continue
        
        json_content = entry.get('content', '')
        
        # Extract JSON appearance section
        json_appearance = ""
        m = re.search(r'外貌特征:(.*?)(?=\n\S+:\s|\n</npc>|\Z)', json_content, re.DOTALL)
        if m:
            json_appearance = m.group(1).strip()
        
        # Extract hair/eye from JSON
        json_hair, json_eye = extract_hair_eye(json_appearance if json_appearance else json_content)
        
        # Extract weapon terms from JSON
        json_weapon_terms = []
        for weapon_kw in ['剑', '刀', '枪', '锤', '弓', '杖', '链锯', '镰刀', '盾', '权杖']:
            if weapon_kw in json_appearance:
                json_weapon_terms.append(weapon_kw)
        
        # Get JSON structured sections
        json_sections = {}
        for sec in ['性格', '武器', '技能', '装备', '战斗风格', '人格']:
            m2 = re.search(rf'{sec}:(.*?)(?=\n\S+:\s|\n</npc>|\Z)', json_content, re.DOTALL)
            if m2:
                json_sections[sec] = m2.group(1).strip()
        
        # Read MD file
        md_path = MD_DIR / f"{md_name}.md"
        md_content = ""
        if md_path.exists():
            with open(md_path, 'r', encoding='utf-8') as f:
                md_content = f.read()
        
        # Check consistency
        json_attrs = {
            'hair': json_hair,
            'eye': json_eye,
            'weapon_terms': json_weapon_terms,
        }
        issues = check_consistency(json_attrs, md_content, json_comment)
        
        # Extract MD header info
        md_header = {}
        for line in md_content.split('\n')[:30]:
            line = line.strip()
            for field in ['名称', '年龄', '职业', '身份', 'CV', '对应']:
                mh = re.search(rf'{field}[：:]\s*(.+?)(?:\||$)', line)
                if mh:
                    md_header[field] = mh.group(1).strip()
        
        results.append({
            'name': md_name,
            'comment': json_comment,
            'json_hair': json_hair,
            'json_eye': json_eye,
            'json_appearance': json_appearance[:200],
            'json_weapons': json_weapon_terms,
            'json_sections': json_sections,
            'issues': issues,
            'md_header': md_header,
            'md_size': len(md_content),
        })
        
        # Print
        status = "✅" if not issues else "⚠️"
        print(f"\n{status} {md_name} ({json_comment})")
        print(f"   JSON外貌: {json_hair or '?'} / {json_eye or '?'} | 武器: {', '.join(json_weapon_terms) if json_weapon_terms else '未明确'}")
        if json_appearance:
            print(f"   外貌概要: {json_appearance[:120]}...")
        
        if json_sections:
            for sk, sv in json_sections.items():
                print(f"   [{sk}]: {sv[:100]}{'...' if len(sv)>100 else ''}")
        
        if issues:
            for issue in issues:
                print(f"   {issue}")
        
        if md_header:
            print(f"   MD表头: 名称={md_header.get('名称', '?')}, 年龄={md_header.get('年龄', '?')}")
    
    # Summary
    total = len(results)
    has_issues = sum(1 for r in results if r['issues'])
    clean = total - has_issues
    
    print(f"\n{'='*60}")
    print(f"汇总: 共{total}个角色")
    print(f"  ✅ 无差异: {clean}")
    print(f"  ⚠️ 有差异: {has_issues}")
    
    # List characters with issues
    if has_issues:
        print(f"\n有差异的角色:")
        for r in results:
            if r['issues']:
                print(f"  - {r['name']} ({r['comment']}): {len(r['issues'])}个问题")
                for i in r['issues']:
                    print(f"      {i}")
    
    # Characters with extra structured sections worth noting
    has_extras = [r for r in results if len(r['json_sections']) > 0]
    print(f"\nJSON有额外结构化章节的角色 ({len(has_extras)}个):")
    for r in has_extras:
        sections_str = ', '.join(f"[{k}]" for k in r['json_sections'].keys())
        print(f"  {r['name']} ({r['comment']}): {sections_str}")

if __name__ == '__main__':
    main()
