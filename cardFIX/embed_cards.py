"""Embed character card JSON into PNG for SillyTavern. Clean rewrite."""
import json, base64, struct, zlib, io
from pathlib import Path
from PIL import Image
import PIL.PngImagePlugin

CF = Path(__file__).parent

CARDS = {
    'airine.json':                'airine.png',
    'bathsheba-ashidefill.json':  '拔示巴.png',
    'lena-ishmel.json':           '蕾娜.png',
    'meme-mikura.json':           '米姆.jpg',
    'Belzeebul.json':             'velzub.jpg',
}


def make_card_png(json_path, img_path, output_path):
    """Create a SillyTavern PNG card with embedded JSON."""
    
    # Load card JSON
    with open(json_path, 'r', encoding='utf-8') as f:
        card = json.load(f)
    
    # Remove avatar reference (PNG IS the avatar)
    card['avatar'] = 'none'
    if 'data' in card:
        card['data']['avatar'] = 'none'
    
    # Load image
    img = Image.open(img_path)
    if img.mode not in ('RGB', 'RGBA'):
        img = img.convert('RGB')
    
    # Save as PNG with custom chunks
    # PIL's PngImagePlugin allows adding custom chunks via 'pnginfo'
    chara_b64 = base64.b64encode(
        json.dumps(card, ensure_ascii=False).encode('utf-8')
    )
    
    # Create PngInfo with chara text chunks
    pnginfo = PIL.PngImagePlugin.PngInfo()
    pnginfo.add_text('chara', chara_b64.decode('ascii'))
    pnginfo.add_text('ccv3', chara_b64.decode('ascii'))
    
    # Save
    img.save(output_path, format='PNG', pnginfo=pnginfo)
    return output_path.stat().st_size


def main():
    for json_file, img_file in CARDS.items():
        json_path = CF / json_file
        img_path = CF / img_file
        out_path = CF / json_file.replace('.json', '.png')
        
        if not json_path.exists():
            print(f"  ❌ {json_file}: JSON not found")
            continue
        if not img_path.exists():
            print(f"  ❌ {json_file}: image not found")
            continue
        
        size = make_card_png(json_path, img_path, out_path)
        print(f"  ✅ {out_path.name} ({size:,} bytes)")


if __name__ == '__main__':
    main()
