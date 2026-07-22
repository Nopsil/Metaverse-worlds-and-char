import struct, base64, json, zlib, os, sys
from PIL import Image
import io

# Image paths
IMG_DIR = r'C:\Users\nopsi\Desktop\metaverse工程\card'
STATE_DIR = r'c:\Users\nopsi\Desktop\skill项目\new_card\cards'
OUT_DIR = r'c:\Users\nopsi\Desktop\skill项目\new_card'
TAVERN_DIR = r'D:\jiuguan\SillyTavern\data\default-user\characters'

cards = [
    {'name': 'bathsheba', 'img': '拔示巴.png', 'display': '拔示巴·阿西德菲尔'},
    {'name': 'lena', 'img': '蕾娜.png', 'display': '蕾娜·伊修梅尔'},
    {'name': 'meme', 'img': '米姆.jpg', 'display': '米姆·米库拉'},
    {'name': 'velzub', 'img': '贝尔泽布特.jpg', 'display': '贝尔泽ブト·涅墨西斯'},
    {'name': 'airine', 'img': '艾莉尼.png', 'display': '艾莉尼·居里亚斯'},
]

for card in cards:
    name = card['name']
    img_path = os.path.join(IMG_DIR, card['img'])
    state_path = os.path.join(STATE_DIR, name, 'tavern-cards-state.json')
    
    # Skip if state doesn't exist
    if not os.path.exists(state_path):
        print(f'{name}: state file not found, skipping')
        continue
    if not os.path.exists(img_path):
        print(f'{name}: image not found, skipping')
        continue
    
    # Load state
    with open(state_path, 'r', encoding='utf-8') as f:
        state = json.load(f)
    
    description = state.get('description', '')
    first_messages = state.get('first_messages', [])
    first_mes = first_messages[0] if first_messages else ''
    
    # Build SillyTavern chara JSON
    chara_data = {
        'data': {
            'name': card['display'],
            'description': description,
            'personality': '',
            'scenario': '',
            'first_mes': first_mes,
            'mes_example': '',
            'creator': 'Cline + User',
            'character_version': '2.0',
            'create_date': state.get('create_date', '2026-07-20T04:00:00.000Z'),
        }
    }
    
    chara_json = json.dumps(chara_data, ensure_ascii=False).encode('utf-8')
    chara_b64 = base64.b64encode(chara_json).decode('ascii')
    
    # Load image and convert to PNG
    img = Image.open(img_path).convert('RGBA')
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    png_bytes = buf.read()
    
    # Find IEND position
    iend = png_bytes.rfind(b'IEND')
    if iend < 0:
        print(f'{name}: no IEND in PNG, skipping')
        continue
    
    # Build tEXt chunk with chara data
    keyword = b'chara'
    chunk_data = keyword + b'\x00' + chara_b64.encode('ascii')
    chunk_len = len(chunk_data)
    crc = zlib.crc32(b'tEXt' + chunk_data) & 0xffffffff
    text_chunk = struct.pack('>I', chunk_len) + b'tEXt' + chunk_data + struct.pack('>I', crc)
    
    # Insert before IEND
    final = png_bytes[:iend] + text_chunk + png_bytes[iend:iend+12]
    
    # Save to new_card/
    out_path = os.path.join(OUT_DIR, f'{name}.png')
    with open(out_path, 'wb') as f:
        f.write(final)
    
    # Copy to tavern
    tavern_path = os.path.join(TAVERN_DIR, f'{name}.png')
    with open(tavern_path, 'wb') as f:
        f.write(final)
    
    chara_size = len(chara_json)
    print(f'{name}: {card["display"]} → {len(final)} bytes (chara {chara_size} bytes, {img.size[0]}x{img.size[1]})')

print('\nAll 5 PNG character cards generated!')
print(f'Output: {OUT_DIR}/')
print(f'Tavern: {TAVERN_DIR}/')