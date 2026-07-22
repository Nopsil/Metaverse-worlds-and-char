import json

with open("C:/Users/nopsi/Desktop/metaverse工程/new_card/Metaverse-New.json", "r", encoding="utf-8") as f:
    data = json.load(f)

targets = ["厄里斯", "提丰", "梅德", "古龙", "索尔娜"]
for entry_id, entry in data["entries"].items():
    c = entry.get("comment", "")
    if c in targets:
        content = entry["content"]
        idx = content.find("背景设定")
        if idx > 0:
            before = content[max(0, idx-10):idx]
            nl = chr(10)
            print(f"{c}: before='{repr(before)}', has_newline={nl in before}")
        else:
            print(f"{c}: '背景设定' NOT FOUND")
