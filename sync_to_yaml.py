#!/usr/bin/env python3
"""
Sync expanded content from CHUNITHM-Metaverse.json back to YAML source files.

Handles:
- NPC entries with <npc> XML tags → YAML files in NPC/
- World settings, timeline → 世界观/世界设定.yaml, 时间线/时间线.yaml
- Geographic/势力 entries → 地理/*.yaml
- 系统规则, 扮演准则 → special handling
"""

import json
import os
import re
from pathlib import Path

JSON_PATH = r'C:\Users\nopsi\Desktop\metaverse工程\card\CHUNITHM-Metaverse.json'
YAML_ROOT = r'C:\Users\nopsi\Desktop\metaverse工程\backup\20260710_225819\世界书源文件'

# Load JSON
with open(JSON_PATH, 'r', encoding='utf-8') as f:
    data = json.load(f)

entries = data['entries']

# Build YAML file index: filename (no ext) -> full path
yaml_index = {}
for root, dirs, files in os.walk(YAML_ROOT):
    for fname in files:
        if fname.endswith('.yaml'):
            full = os.path.join(root, fname)
            basename = fname[:-5]  # remove .yaml
            yaml_index[basename] = full
            # Also index by just the character name part (after last _)
            # E.g. "电脑世界篇_贝尔泽布特" -> index by "贝尔泽布特" too
            # But be careful with names containing _
            parts = fname.rsplit('.', 1)[0]
            yaml_index[parts] = full

print(f"Total YAML files indexed: {len(yaml_index)}")

# Counters
synced = 0
skipped = 0
not_found = []

def parse_npc_content_to_yaml(content: str) -> str:
    """
    Extract content from <npc> tags and convert to clean YAML.
    Handles both YAML-like and markdown-style formats.
    """
    # Remove the outer "名称: xxx\n---\n" prefix if present
    content = re.sub(r'^名称:\s*.+\n---\n', '', content)
    
    # Extract <npc> tag content
    m = re.search(r'<npc[^>]*>(.*?)</npc>', content, re.DOTALL)
    if not m:
        return content  # No npc tags, return as-is
    
    inner = m.group(1).strip()
    
    # Convert markdown-style ## headers to YAML keys
    # ## 基本信息 → 基本信息:
    inner = re.sub(r'^##+\s+(.+?)\s*$', r'\1:', inner, flags=re.MULTILINE)
    
    # Convert markdown list items to YAML
    # - key: value →   key: value
    inner = re.sub(r'^- (.+?:)(.*)$', r'  \1\2', inner, flags=re.MULTILINE)
    # - value (no colon) →   - value
    inner = re.sub(r'^- (.+)$', r'  - \1', inner, flags=re.MULTILINE)
    
    return inner


def npc_comment_to_yaml_name(comment: str, yaml_index: dict) -> str:
    """
    Find the YAML filename that matches this NPC comment.
    YAML files are named like '电脑世界篇_贝尔泽ブト.yaml'
    Match by character name (after last _).
    """
    # Direct match (full filename without .yaml)
    if comment in yaml_index:
        return comment
    
    # Try matching by comment as suffix
    for name in yaml_index:
        if name.endswith('_' + comment):
            return name
    
    # Handle special cases with underscores in name
    # e.g. comment "米姆_米库拉" → filename "新世界篇_米姆_米库ラ"
    replaced = comment.replace('_', '_')
    for name in yaml_index:
        # Compare without the chapter prefix
        parts = name.split('_', 1)
        if len(parts) == 2 and parts[1] == comment:
            return name
    
    return None


def find_npc_yaml_file(comment: str) -> str:
    """Match an NPC comment to its YAML file in NPC/ directory."""
    # Build a mapping of character names to files
    npc_dir = os.path.join(YAML_ROOT, 'NPC')
    for fname in os.listdir(npc_dir):
        if not fname.endswith('.yaml'):
            continue
        basename = fname[:-5]
        # Extract character name (part after first _)
        parts = basename.split('_', 1)
        char_name = parts[1] if len(parts) > 1 else basename
        
        # Try matching
        if char_name == comment:
            return os.path.join(npc_dir, fname)
        # Handle comments like "米姆_米库拉" matching filename ending with "米姆_米库拉"
        if basename.endswith(comment) or basename.endswith(comment.replace('·', '_')):
            return os.path.join(npc_dir, fname)
    
    # Try matching comment as a substring of character name
    for fname in os.listdir(npc_dir):
        if not fname.endswith('.yaml'):
            continue
        basename = fname[:-5]
        parts = basename.split('_', 1)
        char_name = parts[1] if len(parts) > 1 else basename
        
        # Try different name transformations
        search_names = [
            comment,
            comment.replace('·', '_'),
            comment.replace('_', '·'),
        ]
        for sn in search_names:
            if char_name == sn:
                return os.path.join(npc_dir, fname)
    
    return None


def sync_entry(eid: str, entry: dict):
    """Sync a single JSON entry to its matching YAML file."""
    global synced, skipped, not_found
    
    comment = entry['comment']
    content = entry['content']
    yaml_path = None
    
    # --- Special entries ---
    if comment == '世界设定':
        yaml_path = os.path.join(YAML_ROOT, '世界观', '世界设定.yaml')
    elif comment == '时间线':
        yaml_path = os.path.join(YAML_ROOT, '时间线', '时间线.yaml')
    elif comment == '系统规则':
        # No matching YAML file
        print(f"  SKIP: No YAML file for '{comment}'")
        skipped += 1
        return
    elif comment == '扮演准则':
        yaml_path = os.path.join(YAML_ROOT, '扮演准则', '扮演准则.yaml')
    elif comment in ('Metaverse核心层', '中间层世界群', '最外周部', '地上世界',
                     '势力_框架主脑', '势力_工厂', '势力_MIR系列', '势力_涅墨西斯',
                     '势力_革新者', '势力_LOGOS', '势力_拾荒者', '势力_IDC',
                     '势力_恩迪商会', '势力_独立旅人'):
        yaml_path = os.path.join(YAML_ROOT, '地理', f'{comment}.yaml')
    elif comment in ('卡斯比裂谷', '安特路亚'):
        # These don't have matching YAML files
        print(f"  SKIP: No YAML file for geographic entry '{comment}'")
        skipped += 1
        return
    else:
        # --- NPC entries ---
        yaml_path = find_npc_yaml_file(comment)
    
    if yaml_path is None or not os.path.exists(yaml_path):
        print(f"  NOT FOUND: '{comment}' -> no matching YAML file")
        not_found.append(comment)
        return
    
    # Parse content
    if '<npc' in content:
        yaml_content = parse_npc_content_to_yaml(content)
    else:
        # Non-NPC content: strip leading "名称: xxx\n" if present
        yaml_content = re.sub(r'^名称:\s*.+\n', '', content).strip()
    
    # Write YAML
    with open(yaml_path, 'w', encoding='utf-8') as f:
        f.write(yaml_content)
    
    rel = os.path.relpath(yaml_path, YAML_ROOT)
    print(f"  SYNCED: '{comment}' -> {rel} ({len(yaml_content)} chars)")
    synced += 1


# Process all entries in order
print("\n=== Syncing entries ===\n")
for eid in sorted(entries.keys(), key=int):
    entry = entries[eid]
    sync_entry(eid, entry)

print(f"\n=== Summary ===")
print(f"Synced: {synced}")
print(f"Skipped (no YAML): {skipped}")
print(f"Not found: {len(not_found)}")
for nf in not_found:
    print(f"  - {nf}")
