import struct, base64, json

with open(r'C:\Users\nopsi\Desktop\酒馆预设与角色卡\Reborn_V1.5_.png', 'rb') as f:
    data = f.read()

pos = 8
while pos < len(data):
    length = struct.unpack('>I', data[pos:pos+4])[0]
    ctype = data[pos+4:pos+8]
    cdata = data[pos+8:pos+8+length]
    if ctype == b'tEXt':
        np = cdata.find(b'\x00')
        if np == 5 and cdata[:5] == b'chara':
            b64 = cdata[6:]
            pad = 4 - len(b64) % 4
            if pad != 4:
                b64 += b'=' * pad
            card = json.loads(base64.b64decode(b64))
            d = card['data']
            
            print('=== 基本信息 ===')
            print(f'名称: {d.get("name","")}')
            print(f'first_mes 长度: {len(d.get("first_mes",""))}')
            print(f'first_mes 内容: {repr(d.get("first_mes","")[:200])}')
            print(f'system_prompt 长度: {len(d.get("system_prompt",""))}')
            
            print('\n=== alternate_greetings ===')
            ags = d.get('alternate_greetings', [])
            print(f'数量: {len(ags)}')
            for i, a in enumerate(ags[:3]):
                print(f'  [{i}] 前100字: {a[:100]}')
            
            print('\n=== extensions 结构 ===')
            ext = d.get('extensions', {})
            print(f'顶层 keys: {list(ext.keys())}')
            
            # regex_scripts (legacy format)
            rs = ext.get('regex_scripts', {})
            if isinstance(rs, dict):
                print(f'regex_scripts (dict): {len(rs)} entries')
                for k, v in list(rs.items())[:5]:
                    print(f'  {k}: findRegex={v.get("findRegex","")[:60]}')
            elif isinstance(rs, list):
                print(f'regex_scripts (list): {len(rs)} entries')
            
            # tavern_helper
            th = ext.get('tavern_helper', {})
            print(f'tavern_helper keys: {list(th.keys())}')
            scripts = th.get('scripts', {})
            if isinstance(scripts, list):
                print(f'tavern_helper.scripts (list): {len(scripts)} items')
                for i, s in enumerate(scripts[:5]):
                    sn = s.get('scriptName', '?')
                    val = s.get('value', '')
                    print(f'  [{i}] {sn}: {val[:200]}...')
            else:
                print(f'tavern_helper.scripts keys: {list(scripts.keys())[:5]}')
            
            # worldbook
            cb = d.get('character_book', {})
            print(f'\n=== 世界书 ===')
            print(f'条目数: {len(cb.get("entries", []))}')
            
            # first message full content
            print('\n=== first_mes 完整内容 ===')
            print(d.get('first_mes', ''))
            
            # juqingtuijin
            jq = ext.get('juqingtuijin', {})
            print(f'\n=== juqingtuijin ===')
            print(f'keys: {list(jq.keys())[:5] if isinstance(jq, dict) else type(jq)}')
            break
    pos += 12 + length