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
        d = json.loads(base64.b64decode(b64))['data']
        ext = d['extensions']
        
        scripts = ext.get('tavern_helper', {}).get('scripts', [])
        out = open(r'C:\Users\nopsi\Desktop\metaverse工程\reborn_scripts.json', 'w', encoding='utf-8')
        json.dump(scripts, out, ensure_ascii=False, indent=2)
        out.close()
        print(f'Saved {len(scripts)} tavern_helper scripts to reborn_scripts.json')
        
        # Also extract regex
        reg = ext.get('regex_scripts', [])
        if reg:
            out = open(r'C:\Users\nopsi\Desktop\metaverse工程\reborn_regex.json', 'w', encoding='utf-8')
            json.dump(reg, out, ensure_ascii=False, indent=2)
            out.close()
            print(f'Saved {len(reg)} regex_scripts to reborn_regex.json')
        
        break
    pos += 12 + length