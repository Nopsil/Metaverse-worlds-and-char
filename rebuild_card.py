import json, struct, base64, zlib

# Rebuild card with all fixes
packed = open('C:/Users/nopsi/Desktop/metaverse工程/cardFIX/.backup/MetaverseLobby_v1_20260723_0103.png', 'rb').read()
pos = 8
while pos < len(packed):
    L = struct.unpack('>I', packed[pos:pos+4])[0]
    t = packed[pos+4:pos+8]
    d = packed[pos+8:pos+8+L]
    if t == b'tEXt' and (n := d.find(b'\x00')) > 0 and d[:n] == b'chara':
        card = json.loads(base64.b64decode(d[n+1:]))
        break
    pos += 12 + L

import uuid, os

# 1. Embed MVU Beta + zod schema scripts
uid_mvu = str(uuid.uuid4())
uid_zod = str(uuid.uuid4())

zod_content = """import { registerMvuSchema } from 'https://testingcf.jsdelivr.net/gh/StageDog/tavern_resource/dist/util/mvu_zod.js';
import { z } from 'https://testingcf.jsdelivr.net/gh/StageDog/tavern_resource/dist/util/zod.js';

const CharacterSchema = z.object({
  name: z.string().default(''),
  affection: z.number().min(0).max(100).default(0),
  relationship: z.string().default('陌生人'),
  mood: z.string().default(''),
  clothing: z.string().default(''),
  inner_thought: z.string().default(''),
  body_state: z.string().default('正常'),
  clothing_integrity: z.string().default('整齐'),
  pose: z.string().default('站立')
}).catchall(z.unknown());

const StatDataSchema = z.object({
  selected_character: z.string().default(''),
  selected_scenario: z.number().default(0),
  phase: z.string().default('lobby'),
  present_characters: z.string().default(''),
  characters: z.object({
    airine: CharacterSchema,
    bathsheba: CharacterSchema,
    lena: CharacterSchema,
    meme: CharacterSchema,
    belzeebul: CharacterSchema
  }).catchall(CharacterSchema)
}).catchall(z.unknown());

export const Schema = z.object({
  stat_data: StatDataSchema
}).catchall(z.unknown());

registerMvuSchema(Schema, { version: 1 });"""

# 2. Embed all 7 regex scripts
regex_dir = 'C:/Users/nopsi/Desktop/metaverse工程/remote-statusbar/regex-scripts'
regex_scripts = []
for f in sorted(os.listdir(regex_dir)):
    if f.endswith('.json'):
        regex_scripts.append(json.load(open(f'{regex_dir}/{f}', encoding='utf-8')))

# 3. Update card data
card['data']['extensions']['tavern_helper'] = {
    'scripts': {
        'MVU': {
            'type': 'script', 'enabled': True, 'name': 'MVU', 'id': uid_mvu,
            'content': "import 'https://testingcf.jsdelivr.net/gh/MagicalAstrogy/MagVarUpdate@beta/artifact/bundle.js';"
        },
        '变量结构': {
            'type': 'script', 'enabled': True, 'name': 'MetaverseLobby变量结构', 'id': uid_zod,
            'content': zod_content
        }
    },
    'variables': {}
}
card['data']['extensions']['regex_scripts'] = regex_scripts

# 4. Update alternate_greetings with JSONPatch init
chars = ['airine','bathsheba','lena','meme','belzeebul']
ags = card['data']['alternate_greetings']
for idx in range(1, 26):
    ci = (idx - 1) // 5
    si = (idx - 1) % 5
    char_id = chars[ci]
    ag = ags[idx - 1]
    # Add initvar at end of each greeting
    var_init = f"""\n\n<UpdateVariable>
<initvar>
selected_character: "{char_id}"
selected_scenario: {si}
phase: "playing"
characters:
  {char_id}:
    name: "{char_id}"
    affection: 0
    relationship: "陌生人"
    mood: ""
    clothing: ""
    inner_thought: ""
    body_state: "正常"
    clothing_integrity: "整齐"
    pose: "站立"
</initvar>
</UpdateVariable>"""
    # Remove old initvar/JSONPatch if present
    up_idx = ag.find('<UpdateVariable>')
    if up_idx > 0:
        ag = ag[:up_idx]
    ags[idx - 1] = ag + var_init

# 5. Pack back
new_json = json.dumps(card['data'], ensure_ascii=False, separators=(',', ':'))
new_b64 = base64.b64encode(new_json.encode('utf-8'))
new_chunk_data = b'chara\x00' + new_b64
new_chunk = struct.pack('>I', len(new_chunk_data)) + b'tEXt' + new_chunk_data + struct.pack('>I', zlib.crc32(b'tEXt' + new_chunk_data))
new_png = packed[:pos] + new_chunk + packed[pos+12+L:]

out = 'C:/Users/nopsi/Desktop/metaverse工程/cardFIX/MetaverseLobby-clean.png'
open(out, 'wb').write(new_png)

# 6. Download opening files locally for lobby
openings_dir = 'C:/Users/nopsi/Desktop/metaverse工程/cards/MetaverseLobby/开场白'
os.makedirs(openings_dir, exist_ok=True)
for idx, ag in enumerate(ags):
    with open(f'{openings_dir}/{idx+1}.txt', 'w', encoding='utf-8') as f:
        f.write(ag)

# 7. Verify
p2 = open(out, 'rb').read()
o = 8
while o < len(p2):
    L = struct.unpack('>I', p2[o:o+4])[0]
    t = p2[o+4:o+8]
    d = p2[o+8:o+8+L]
    if t == b'tEXt' and (n := d.find(b'\x00')) > 0 and d[:n] == b'chara':
        c2 = json.loads(base64.b64decode(d[n+1:]))
        break
    o += 12 + L
rs = c2['data']['extensions']['regex_scripts']
th = c2['data']['extensions']['tavern_helper']
ag_count = len(c2['data']['alternate_greetings'])
print(f'Card: {len(rs)} regexes | {len(th["scripts"])} scripts | {ag_count} greetings')
has_init = sum(1 for ag in ags if '<initvar>' in ag)
print(f'Greetings with initvar: {has_init}/25')
