import struct, json, base64, zlib

with open(r'C:\Users\nopsi\Desktop\酒馆预设与角色卡\V1.51_2.png', 'rb') as f:
    data = f.read()

# Find tEXt chunks
pos = 8  # skip PNG signature
while pos < len(data):
    length = struct.unpack('>I', data[pos:pos+4])[0]
    chunk_type = data[pos+4:pos+8].decode('ascii', errors='ignore')
    chunk_data = data[pos+8:pos+8+length]
    
    if chunk_type == 'tEXt':
        # parse keyword\nvalue
        parts = chunk_data.split(b'\x00', 1)
        if len(parts) == 2:
            keyword = parts[0].decode('ascii', errors='ignore')
            value = parts[1]
            if keyword == 'chara':
                # Base64 decode
                try:
                    # pad if needed
                    pad = len(value) % 4
                    if pad:
                        value += b'=' * (4 - pad)
                    card_json = base64.b64decode(value)
                    card = json.loads(card_json)
                    print('NAME:', card.get('data', {}).get('name', ''))
                    fm = card.get('data', {}).get('first_mes', '')
                    print('FIRST_MES LEN:', len(fm))
                    print('=== FIRST_MES START ===')
                    print(fm[:1500])
                    print('=== FIRST_MES END ===')
                    
                    syn = card.get('system_prompt', '')
                    print('SYSTEM_PROMPT LEN:', len(syn))
                    print('=== SYSTEM_PROMPT START ===')
                    print(syn[:800])
                except Exception as e:
                    print(f'Error: {e}')
    pos += 12 + length
    pos += (4 - (pos % 4)) % 4  # crc