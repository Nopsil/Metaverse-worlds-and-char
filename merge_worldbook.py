#!/usr/bin/env python3
"""
Merge 133 CHUNITHM-Metaverse world book entries into MetaverseLobby card.
Fixed: handle duplicate display names with parenthetical suffixes.
"""
import json
import os
import re

BASE = r"C:\Users\nopsi\Desktop\metaverse工程"
SOURCE = os.path.join(BASE, "cardFIX", "CHUNITHM-Metaverse.json")
LOBBY_DIR = os.path.join(BASE, "cards", "MetaverseLobby")
WORLDBOOK_DIR = os.path.join(LOBBY_DIR, "世界书")
STATE_FILE = os.path.join(LOBBY_DIR, "tavern-cards-state.json")

CLASSIFICATION = {
    "世界设定": ("世界观", "foundation"),
    "时间线": ("世界观", "foundation"),
    "Metaverse核心层": ("世界观", "foundation"),
    "中间层世界群": ("世界观", "foundation"),
    "最外周部": ("世界观", "foundation"),
    "地上世界": ("世界观", "foundation"),
    "势力_框架主脑": ("势力", "foundation"),
    "势力_工厂": ("势力", "foundation"),
    "势力_MIR系列": ("势力", "foundation"),
    "势力_涅墨西斯": ("势力", "foundation"),
    "势力_革新者": ("势力", "foundation"),
    "势力_LOGOS": ("势力", "foundation"),
    "势力_拾荒者": ("势力", "foundation"),
    "势力_IDC": ("势力", "foundation"),
    "势力_恩迪商会": ("势力", "foundation"),
    "势力_独立旅人": ("势力", "foundation"),
    "卡斯比裂谷": ("地理", "foundation"),
    "安特路亚": ("地理", "foundation"),
    "系统规则": ("规则", "presentation"),
}

def classify_entry(comment, display_name):
    if comment in CLASSIFICATION:
        return CLASSIFICATION[comment]
    return ("角色", "presentation")

def get_entry_name(comment, display_name):
    """
    Get manifest key name. For character entries, use display_name.
    For entries with parenthetical variants (e.g. Metaverse异体), keep the variant info.
    """
    if display_name:
        # Remove "(幼年)", "(晨风)", "(Metaverse异体)" etc - BUT keep as part of name
        # to differentiate from base versions
        name = display_name.strip()
        # For Metaverse alternate versions, keep the variant
        return name
    
    name = comment.replace("势力_", "")
    return name

def get_clean_filename(name):
    """Make a filesystem-safe filename."""
    name = re.sub(r'[<>:"/\\|?*]', '_', name)
    name = name.strip()
    if not name:
        name = "unnamed"
    return name

def get_category_dir(category, name):
    """Get subdirectory under 世界书/ for the entry."""
    if category == "角色":
        # Use first character of name as dir (or first meaningful word)
        # But for the known 5 lobby characters, keep them in their existing dirs
        base_name = name.split("·")[0].split("(")[0].strip()
        return os.path.join(category, get_clean_filename(base_name))
    return category

def main():
    print("Step 1: Reading source world book...")
    with open(SOURCE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    entries = data.get('entries', {})
    print(f"  Found {len(entries)} entries")
    
    with open(STATE_FILE, 'r', encoding='utf-8') as f:
        state = json.load(f)
    
    # Clean up all existing CHUNITHM-created directories first
    # (keep Lobby's original directories: airine, bathsheba, belzeebul, lena, meme)
    lobby_preserved_dirs = {'airine', 'bathsheba', 'belzeebul', 'lena', 'meme'}
    
    # Remove previously created character directories
    for cat in ['世界观', '势力', '地理', '规则', '角色']:
        cat_dir = os.path.join(WORLDBOOK_DIR, cat)
        if os.path.isdir(cat_dir):
            for sub in os.listdir(cat_dir):
                sub_path = os.path.join(cat_dir, sub)
                if os.path.isdir(sub_path) and sub.lower() not in lobby_preserved_dirs:
                    # Remove all .txt files in this directory (CHUNITHM entries)
                    for f in os.listdir(sub_path):
                        if f.endswith('.txt'):
                            os.remove(os.path.join(sub_path, f))
                    # Only remove empty dirs
                    if not os.listdir(sub_path):
                        os.rmdir(sub_path)
            # Remove standalone .txt files at category level
            for f in os.listdir(cat_dir):
                if f.endswith('.txt'):
                    fp = os.path.join(cat_dir, f)
                    if os.path.isfile(fp):
                        os.remove(fp)
    
    entry_manifest = {}
    
    # Track used manifest keys to detect duplicates
    used_keys = set()
    stats = {}
    
    print("\nStep 2: Creating entry files and building manifest...")
    
    for uid_str, entry in entries.items():
        comment = entry.get('comment', '')
        content = entry.get('content', '')
        keys = entry.get('keys', [])
        display_name = entry.get('display_name', '')
        
        # Skip 世界设定 (Lobby has its own version)
        if comment == "世界设定":
            print(f"  SKIP uid={entry.get('uid')}: 世界设定 (Lobby version exists)")
            continue
        
        category, part = classify_entry(comment, display_name)
        entry_name = get_entry_name(comment, display_name)
        
        # Handle duplicate manifest keys
        if entry_name in used_keys:
            # Add suffix based on comment or uid
            suffix = comment.replace("势力_", "")
            if suffix == entry_name:
                suffix = f"v{entry.get('uid')}"
            entry_name = f"{entry_name}({suffix})"
        used_keys.add(entry_name)
        
        # Build path
        cat_dir = get_category_dir(category, entry_name)
        safe_name = get_clean_filename(entry_name)
        filename = f"{safe_name}.txt"
        rel_path = f"世界书/{cat_dir}/{filename}"
        
        # Create directory
        full_dir = os.path.join(WORLDBOOK_DIR, cat_dir)
        os.makedirs(full_dir, exist_ok=True)
        
        # Write content file
        full_path = os.path.join(WORLDBOOK_DIR, cat_dir, filename)
        
        # Handle filename collisions
        counter = 1
        while os.path.exists(full_path):
            safe_count = f"{safe_name}_{counter}"
            filename = f"{safe_count}.txt"
            rel_path = f"世界书/{cat_dir}/{filename}"
            full_path = os.path.join(WORLDBOOK_DIR, cat_dir, filename)
            counter += 1
        
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Determine scope
        if category in ("世界观", "势力", "地理", "规则"):
            scope = "catalog"
        else:
            scope = "specific"
        
        # Build manifest leaf - ALL entries need abstract
        abstract = content[:100].replace('\n', ' ').strip()
        if len(content) > 100:
            abstract += "..."
        leaf = {
            "path": rel_path,
            "scope": scope,
            "part": part,
            "keywords": keys if keys else [],
            "abstract": abstract,
        }
        
        if category not in entry_manifest:
            entry_manifest[category] = {}
        entry_manifest[category][entry_name] = leaf
        
        if category not in stats:
            stats[category] = 0
        stats[category] += 1
    
    # Register Lobby existing entries
    print("\nStep 3: Registering existing Lobby entries...")
    
    lobby_manifests = {
        "世界观": {
            "Lobby世界设定": {
                "path": "世界书/世界观/世界设定.txt",
                "scope": "catalog",
                "part": "foundation",
                "keywords": ["Metaverse", "Lobby", "世界观"],
                "abstract": "Metaverse——一个由数据与意志编织的多元次元交汇之地..."
            }
        },
        "扮演准则": {
            "Lobby系统规则": {
                "path": "世界书/扮演准则/系统规则.yaml",
                "scope": "catalog",
                "part": "presentation",
                "keywords": ["系统规则", "扮演准则"],
                "abstract": "Lobby卡系统规则与扮演准则..."
            },
            "选择响应": {
                "path": "世界书/扮演准则/选择响应.yaml",
                "scope": "specific",
                "part": "presentation",
                "keywords": ["选择角色", "角色选择"],
                "abstract": "Lobby卡角色选择响应规则..."
            }
        },
        "角色": {
            "艾莉尼·居里亚斯(Lobby)": {
                "path": "世界书/角色/airine/基础信息.txt",
                "scope": "specific",
                "part": "presentation",
                "keywords": ["艾莉尼", "Airine", "居里亚斯"],
                "abstract": "艾莉尼·居里亚斯——次元旅人，流浪的画家，银发蓝瞳的少女..."
            },
            "艾莉尼场景": {
                "path": "世界书/角色/airine/场景.txt",
                "scope": "specific",
                "part": "presentation",
                "keywords": ["艾莉尼", "场景", "airine_scene"],
                "abstract": "艾莉尼角色场景设定..."
            },
            "艾莉尼开局": {
                "path": "世界书/角色/airine/开局引导.txt",
                "scope": "specific",
                "part": "presentation",
                "keywords": ["艾莉尼", "开局", "airine_start"],
                "abstract": "艾莉尼开局引导..."
            },
            "拔示巴·阿西德菲尔(Lobby)": {
                "path": "世界书/角色/bathsheba/基础信息.txt",
                "scope": "specific",
                "part": "presentation",
                "keywords": ["拔示巴", "阿西德菲尔", "Bathsheba"],
                "abstract": "拔示巴·阿西德菲尔——命运之子，唯一自然分娩诞生的真人..."
            },
            "拔示巴场景": {
                "path": "世界书/角色/bathsheba/场景.txt",
                "scope": "specific",
                "part": "presentation",
                "keywords": ["拔示巴", "场景", "bathsheba_scene"],
                "abstract": "拔示巴角色场景设定..."
            },
            "拔示巴开局": {
                "path": "世界书/角色/bathsheba/开局引导.txt",
                "scope": "specific",
                "part": "presentation",
                "keywords": ["拔示巴", "开局", "bathsheba_start"],
                "abstract": "拔示巴开局引导..."
            },
            "贝尔泽布特(Lobby)": {
                "path": "世界书/角色/belzeebul/基础信息.txt",
                "scope": "specific",
                "part": "presentation",
                "keywords": ["ベルゼブト", "Belzeebul", "贝泽ブ"],
                "abstract": "贝尔泽ブト·涅墨西斯——混沌七器之一..."
            },
            "贝尔泽布特场景": {
                "path": "世界书/角色/belzeebul/场景.txt",
                "scope": "specific",
                "part": "presentation",
                "keywords": ["ベルゼブト", "场景", "belzeebul_scene"],
                "abstract": "贝尔泽ブト角色场景设定..."
            },
            "贝尔泽布特开局": {
                "path": "世界书/角色/belzeebul/开局引导.txt",
                "scope": "specific",
                "part": "presentation",
                "keywords": ["ベルゼブト", "开局", "belzeebul_start"],
                "abstract": "贝尔泽ブト开局引导..."
            },
            "蕾娜·伊修梅尔(Lobby)": {
                "path": "世界书/角色/lena/基础信息.txt",
                "scope": "specific",
                "part": "presentation",
                "keywords": ["蕾娜", "伊修梅尔", "Lena"],
                "abstract": "蕾娜·伊修梅尔——归还种，MIR系列战士..."
            },
            "蕾娜场景": {
                "path": "世界书/角色/lena/场景.txt",
                "scope": "specific",
                "part": "presentation",
                "keywords": ["蕾娜", "场景", "lena_scene"],
                "abstract": "蕾娜角色场景设定..."
            },
            "蕾娜开局": {
                "path": "世界书/角色/lena/开局引导.txt",
                "scope": "specific",
                "part": "presentation",
                "keywords": ["蕾娜", "开局", "lena_start"],
                "abstract": "蕾娜开局引导..."
            },
            "米姆·米库拉(Lobby)": {
                "path": "世界书/角色/meme/基础信息.txt",
                "scope": "specific",
                "part": "presentation",
                "keywords": ["米姆", "米库拉", "Meme"],
                "abstract": "米姆·米库拉——被泰斯塔蒙特夺舍的新世界旅人..."
            },
            "米姆场景": {
                "path": "世界书/角色/meme/场景.txt",
                "scope": "specific",
                "part": "presentation",
                "keywords": ["米姆", "场景", "meme_scene"],
                "abstract": "米姆角色场景设定..."
            },
            "米姆开局": {
                "path": "世界书/角色/meme/开局引导.txt",
                "scope": "specific",
                "part": "presentation",
                "keywords": ["米姆", "开局", "meme_start"],
                "abstract": "米姆开局引导..."
            },
        },
        "MVU": {
            "[InitVar]请勿打开": {
                "path": "世界书/变量/initvar.yaml",
                "scope": "catalog",
                "part": "foundation",
                "keywords": [],
                "enabled": False,
                "abstract": "MVU初始化变量..."
            },
            "变量列表": {
                "path": "世界书/变量/变量列表.txt",
                "scope": "catalog",
                "part": "foundation",
                "keywords": [],
                "abstract": "MVU变量列表定义..."
            },
            "变量更新规则": {
                "path": "世界书/变量/变量更新规则.yaml",
                "scope": "catalog",
                "part": "foundation",
                "keywords": [],
                "abstract": "MVU变量更新规则..."
            },
            "变量输出格式": {
                "path": "世界书/变量/变量输出格式.txt",
                "scope": "catalog",
                "part": "foundation",
                "keywords": [],
                "abstract": "MVU变量输出格式..."
            },
        }
    }
    
    for category, entries_dict in lobby_manifests.items():
        if category not in entry_manifest:
            entry_manifest[category] = {}
        for name, leaf in entries_dict.items():
            entry_manifest[category][name] = leaf
    
    # Update state.json
    state['entryManifest'] = entry_manifest
    
    state['typeLists'] = {
        "before_char": ["世界观", "势力", "扮演准则", "地理"],
        "after_char": ["角色"],
        "depth": ["规则", "MVU"]
    }
    
    state['strategyThresholds'] = {
        "世界观": "Infinity",
        "势力": "Infinity", 
        "扮演准则": "Infinity",
        "地理": "Infinity",
        "角色": 0,
        "规则": 0,
        "MVU": "Infinity"
    }
    
    state['partOrder'] = {
        "世界观": ["foundation"],
        "势力": ["foundation"],
        "扮演准则": ["presentation"],
        "地理": ["foundation"],
        "角色": ["presentation"],
        "规则": ["presentation"],
        "MVU": ["foundation"]
    }
    
    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    
    print(f"\n=== Summary ===")
    for cat, count in sorted(stats.items()):
        print(f"  {cat}: {count} entries")
    
    total_new = sum(stats.values())
    print(f"\n  Total new CHUNITHM entries: {total_new}")
    lobby_count = sum(len(v) for v in lobby_manifests.values())
    print(f"  Lobby existing entries: {lobby_count}")
    
    total_manifest = sum(len(v) for v in entry_manifest.values())
    print(f"  Total manifest entries: {total_manifest}")
    print(f"  Categories: {list(entry_manifest.keys())}")

if __name__ == '__main__':
    main()
