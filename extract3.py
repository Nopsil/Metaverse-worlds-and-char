import struct, base64, json

with open(r'C:\Users\nopsi\Desktop\酒馆预设与角色卡\V1.51_2.png', 'rb') as f:
    data = f.read()

pos = 8
while pos < len(data):
    length = struct.unpack('>I', data[pos:pos+4])[0]
    ctype = data[pos+4:pos+8]
    cdata = data[pos+8:pos+8+length]
    
    if ctype == b'tEXt':
        null_pos = cdata.find(b'\x00')
        if null_pos == 5 and cdata[:5] == b'chara':
            raw_b64 = cdata[6:]
            pad = 4 - len(raw_b64) % 4
            if pad != 4:
                raw_b64 += b'=' * pad
            decoded = base64.b64decode(raw_b64)
            card = json.loads(decoded)
            
            fm = card['data']['first_mes']
            with open(r'C:\Users\nopsi\Desktop\metaverse工程\ref_fm.txt', 'w', encoding='utf-8') as out:
                out.write(f'LENGTH: {len(fm)}\n')
                out.write(fm)
            print(f'Written {len(fm)} chars to ref_fm.txt')
            break
    pos += 12 + length