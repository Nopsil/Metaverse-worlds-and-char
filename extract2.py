import struct, base64, json, os

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
        
        # Regex replaceString (the HTML template)
        reg = ext.get('regex_scripts', [])
        if reg:
            html = reg[0].get('replaceString', '')
            out = os.path.join(os.path.dirname(__file__), 'reborn_regex.html')
            open(out, 'w', encoding='utf-8').write(html)
            print(f'Regex HTML saved: {out} ({len(html)} chars)')
        
        # Variables
        vars_data = ext.get('tavern_helper', {}).get('variables', {})
        out = os.path.join(os.path.dirname(__file__), 'reborn_vars.json')
        json.dump(vars_data, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
        print(f'Variables saved: {out}')
        
        break
    pos += 12 + length