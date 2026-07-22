import struct, base64, json

with open(r'C:\Users\nopsi\Desktop\酒馆预设与角色卡\Reborn_V1.5_.png', 'rb') as f:
    data = f.read()

pos = 8
while pos < len(data):
    length = struct.unpack('>I', data[pos:pos+4])[0]
    ctype = data[pos+4:pos+8]
    cdata = data[pos+8:pos+8+length]
    if ctype == b'tEXt' and cdata[:5] == b'chara\x00':
        b64 = cdata[6:]
        pad = 4 - len(b64) % 4
        if pad != 4:
            b64 += b'=' * pad
        card = json.loads(base64.b64decode(b64))
        d = card['data']
        ext = d['extensions']
        
        # ===== REGEX SCRIPTS =====
        reg = ext.get('regex_scripts', [])
        print(f'=== REGEX SCRIPTS: {len(reg)} ===')
        for i, r in enumerate(reg):
            find = r.get('findRegex', '')
            rep = r.get('replaceString', '')
            print(f'\n--- Regex {i}: findRegex={find} ---')
            print(f'replaceString ({len(rep)} chars):')
            print(rep[:3000])
        
        # ===== TAVERN HELPER SCRIPTS =====
        scripts = ext.get('tavern_helper', {}).get('scripts', [])
        print(f'\n\n=== TAVERN HELPER SCRIPTS: {len(scripts)} ===')
        for i, s in enumerate(scripts):
            print(f'\n--- Script {i} ---')
            for k, v in s.items():
                if isinstance(v, str) and len(v) < 500:
                    print(f'  {k}: {v}')
                elif isinstance(v, str):
                    print(f'  {k}: ({len(v)} chars) {v[:200]}...')
                else:
                    print(f'  {k}: {v}')
        
        break
    pos += 12 + length