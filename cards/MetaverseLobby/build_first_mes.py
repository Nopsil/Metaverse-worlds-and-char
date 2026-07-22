#!/usr/bin/env python3
"""
Build first_mes HTML for MetaverseLobby.
Resizes avatar images to 200x200 and inlines them as base64 data URIs.
"""
import base64
import io
import json
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    import subprocess
    subprocess.check_call(["pip", "install", "Pillow"])
    from PIL import Image

BASE_DIR = Path(__file__).parent
ASSETS_DIR = BASE_DIR / "assets"
OUTPUT_FILE = BASE_DIR / "开场白" / "0.txt"

CHARACTERS = [
    {"id": "airine", "name": "艾莉尼·居里亚斯", "tagline": "次元旅人 · 流浪的画家", "desc": "银发蓝瞳的少女画师，画笔能将所绘之物短暂实体化。温柔而疏离，用画记录所有美丽的瞬间——每一幅画都是告别。"},
    {"id": "bathsheba", "name": "拔示巴·阿西德菲尔", "tagline": "破灭圣女 · 命运之子", "desc": "银白长发、深红眼瞳的圣女，右眼能看见命运的破灭点。表面庄严冷静，内心燃烧着自毁式的使命感。"},
    {"id": "lena", "name": "蕾娜·伊修梅尔", "tagline": "归还者 · 废土幸存者", "desc": "从虚无中归来的战士，银白中长发、浅紫眼眸。坚韧寡言，擅长在废土生存，却害怕再次失去重要的人。"},
    {"id": "meme", "name": "米姆·米库拉", "tagline": "双重存在 · 医疗兵", "desc": "天真烂漫的少女医疗兵，体内寄宿着古老意识「泰斯塔蒙特」。纯真的外表下藏着令人毛骨悚然的另一面。"},
    {"id": "belzeebul", "name": "贝尔泽ブト·涅墨西斯", "tagline": "欺瞒的使徒 · 混沌七器", "desc": "深紫渐变长发、青紫色皮肤的数据女王。优雅而危险，以轻笑声瓦解对手意志，将万物都当作玩具。"},
]

SCENARIOS = [
    # airine: 0-4
    {"char": "airine", "idx": 0, "title": "星空下的相遇", "nsfw": False},
    {"char": "airine", "idx": 1, "title": "废墟中的速写", "nsfw": False},
    {"char": "airine", "idx": 2, "title": "次元隙间的旅伴", "nsfw": False},
    {"char": "airine", "idx": 3, "title": "索拉里斯的归途", "nsfw": False},
    {"char": "airine", "idx": 4, "title": "蛮族的肉凯", "nsfw": True},
    # bathsheba: 5-9
    {"char": "bathsheba", "idx": 0, "title": "圣堂中的王座", "nsfw": False},
    {"char": "bathsheba", "idx": 1, "title": "虚无中的一线留恋", "nsfw": False},
    {"char": "bathsheba", "idx": 2, "title": "革新者的访客", "nsfw": False},
    {"char": "bathsheba", "idx": 3, "title": "佩尔修斯的废墟", "nsfw": False},
    {"char": "bathsheba", "idx": 4, "title": "命运之子的配种", "nsfw": True},
    # lena: 10-14
    {"char": "lena", "idx": 0, "title": "废土上的邂逅", "nsfw": False},
    {"char": "lena", "idx": 1, "title": "塞雷基亚之后", "nsfw": False},
    {"char": "lena", "idx": 2, "title": "伊欧尼亚的幸存者", "nsfw": False},
    {"char": "lena", "idx": 3, "title": "佩尔修斯的守护者", "nsfw": False},
    {"char": "lena", "idx": 4, "title": "淫魔史莱姆的觉醒", "nsfw": True},
    # meme: 15-19
    {"char": "meme", "idx": 0, "title": "新世界废墟", "nsfw": False},
    {"char": "meme", "idx": 1, "title": "泰斯塔蒙特的低语", "nsfw": False},
    {"char": "meme", "idx": 2, "title": "光之塔的旅伴", "nsfw": False},
    {"char": "meme", "idx": 3, "title": "医疗营的访客", "nsfw": False},
    {"char": "meme", "idx": 4, "title": "塞拉菲娜的困扰", "nsfw": True},
    # belzeebul: 20-24
    {"char": "belzeebul", "idx": 0, "title": "Metaverse深渊", "nsfw": False},
    {"char": "belzeebul", "idx": 1, "title": "猫戏老鼠", "nsfw": False},
    {"char": "belzeebul", "idx": 2, "title": "混沌之器的契约", "nsfw": False},
    {"char": "belzeebul", "idx": 3, "title": "工厂的入侵者", "nsfw": False},
    {"char": "belzeebul", "idx": 4, "title": "一魂双体", "nsfw": True},
]


def resize_and_encode(image_path, size=(200, 200)):
    """Resize image to given size and return base64 data URI."""
    img = Image.open(image_path).convert("RGBA")
    img = img.resize(size, Image.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, format="PNG", optimize=True)
    b64 = base64.b64encode(buf.getvalue()).decode("ascii")
    return f"data:image/png;base64,{b64}"


def build_raw_data():
    """Build the raw data div content."""
    lines = []
    for c in CHARACTERS:
        lines.append(f"[角色]name:{c['name']}|id:{c['id']}[/角色]")
    for s in SCENARIOS:
        nsfw_flag = "|nsfw:true" if s['nsfw'] else ""
        lines.append(f"[场景]char:{s['char']}|idx:{s['idx']}|title:{s['title']}{nsfw_flag}[/场景]")
    return "\n".join(lines)


def build_html():
    """Generate the complete HTML for first_mes."""
    
    # Resize and encode all avatars
    avatars_b64 = {}
    for c in CHARACTERS:
        img_path = ASSETS_DIR / f"{c['id']}.png"
        if img_path.exists():
            avatars_b64[c['id']] = resize_and_encode(img_path)
            print(f"  ✓ {c['id']}: {len(avatars_b64[c['id']])} chars")
        else:
            print(f"  ✗ {c['id']}: file not found at {img_path}")
            avatars_b64[c['id']] = ""
    
    raw_data = build_raw_data()
    
    # Build CSS with base64 avatars
    avatar_css = ""
    for c in CHARACTERS:
        b64 = avatars_b64.get(c['id'], "")
        if b64:
            avatar_css += f".char-avatar-{c['id']} {{ background-image: url({b64}); }}\n"
    
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Metaverse Lobby</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}

body {{
  font-family: 'Segoe UI', 'Microsoft YaHei', 'PingFang SC', sans-serif;
  background: #0a0a0f;
  color: #e0d8d0;
  overflow: hidden;
  min-height: 100vh;
  position: relative;
}}

/* Particle background */
#particles {{
  position: fixed;
  top: 0; left: 0;
  width: 100%; height: 100%;
  z-index: 0;
  pointer-events: none;
}}

/* Main container */
.lobby-container {{
  position: relative;
  z-index: 1;
  max-width: 800px;
  margin: 0 auto;
  padding: 40px 20px;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}}

/* Title */
.lobby-title {{
  text-align: center;
  margin-bottom: 40px;
}}
.lobby-title h1 {{
  font-size: 36px;
  font-weight: 300;
  letter-spacing: 6px;
  color: #c8b8e0;
  text-shadow: 0 0 30px rgba(180, 150, 220, 0.4);
  margin-bottom: 8px;
}}
.lobby-title .subtitle {{
  font-size: 14px;
  color: #8a7a9a;
  letter-spacing: 3px;
}}

/* Phase containers */
.phase {{
  display: none;
  width: 100%;
  flex-direction: column;
  align-items: center;
  animation: fadeIn 0.5s ease-out;
}}
.phase.active {{
  display: flex;
}}
@keyframes fadeIn {{
  from {{ opacity: 0; transform: translateY(12px); }}
  to   {{ opacity: 1; transform: translateY(0); }}
}}

/* Phase hints */
.phase-hint {{
  color: #9a8ab0;
  font-size: 14px;
  letter-spacing: 2px;
  margin-bottom: 28px;
  text-align: center;
}}

/* Character Grid */
.character-grid {{
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  justify-content: center;
  width: 100%;
  max-width: 780px;
}}

/* Character Card */
.char-card {{
  width: 200px;
  background: linear-gradient(145deg, rgba(30,25,45,0.85), rgba(20,18,35,0.9));
  border: 1px solid rgba(140,120,180,0.25);
  border-radius: 16px;
  padding: 16px;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}}
.char-card:hover {{
  border-color: rgba(180,150,220,0.5);
  transform: translateY(-4px);
  box-shadow: 0 8px 30px rgba(120,100,180,0.2);
}}
.char-card.selected {{
  border-color: rgba(180,140,220,0.8);
  box-shadow: 0 0 25px rgba(140,110,200,0.35), inset 0 0 20px rgba(140,110,200,0.08);
  background: linear-gradient(145deg, rgba(40,30,60,0.9), rgba(25,20,45,0.95));
}}
.char-card.selected::after {{
  content: '✓';
  position: absolute;
  top: 10px; right: 14px;
  font-size: 20px;
  color: #b090e0;
}}

.char-avatar {{
  width: 100%;
  aspect-ratio: 1;
  border-radius: 12px;
  background-size: cover;
  background-position: center;
  margin-bottom: 12px;
  border: 2px solid rgba(140,120,180,0.2);
}}
{avatar_css}
.char-name {{
  font-size: 16px;
  font-weight: 600;
  color: #d0c8e8;
  margin-bottom: 4px;
  text-align: center;
}}
.char-tagline {{
  font-size: 11px;
  color: #8a7a9a;
  text-align: center;
  letter-spacing: 1px;
  margin-bottom: 8px;
}}
.char-desc {{
  font-size: 11px;
  color: #6a5a7a;
  text-align: center;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}}

/* Scenario List */
.scenario-list {{
  width: 100%;
  max-width: 600px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}}

.scenario-item {{
  background: linear-gradient(135deg, rgba(30,25,45,0.7), rgba(20,18,35,0.8));
  border: 1px solid rgba(140,120,180,0.2);
  border-radius: 12px;
  padding: 14px 18px;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 14px;
}}
.scenario-item:hover {{
  border-color: rgba(180,150,220,0.45);
  background: linear-gradient(135deg, rgba(35,28,52,0.8), rgba(22,20,40,0.85));
  transform: translateX(4px);
}}
.scenario-item.selected {{
  border-color: rgba(180,140,220,0.7);
  box-shadow: 0 0 18px rgba(140,110,200,0.2);
  background: linear-gradient(135deg, rgba(40,30,60,0.85), rgba(25,20,48,0.9));
}}

.scenario-idx {{
  width: 32px; height: 32px;
  border-radius: 50%;
  background: rgba(140,120,180,0.2);
  display: flex; align-items: center; justify-content: center;
  font-size: 14px; color: #b090e0;
  flex-shrink: 0;
}}
.scenario-item.selected .scenario-idx {{
  background: rgba(160,130,210,0.35);
  color: #d0c0f0;
}}

.scenario-info {{ flex: 1; }}
.scenario-name {{
  font-size: 16px; font-weight: 500; color: #d0c8e8;
}}
.scenario-nsfw {{
  display: inline-block; margin-left: 8px;
  font-size: 10px; padding: 2px 7px;
  background: rgba(220,80,80,0.3); color: #f0a0a0;
  border-radius: 8px; letter-spacing: 1px;
}}

/* Buttons */
.lobby-btn {{
  padding: 12px 36px;
  border: 1px solid rgba(160,140,200,0.4);
  border-radius: 30px;
  background: linear-gradient(135deg, rgba(100,70,160,0.3), rgba(60,40,120,0.25));
  color: #d0c0e8;
  font-size: 15px;
  letter-spacing: 2px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-family: inherit;
}}
.lobby-btn:hover:not(:disabled) {{
  background: linear-gradient(135deg, rgba(130,90,190,0.45), rgba(80,50,150,0.35));
  border-color: rgba(180,150,220,0.6);
  box-shadow: 0 0 20px rgba(130,100,180,0.3);
  transform: translateY(-2px);
}}
.lobby-btn:disabled {{
  opacity: 0.35;
  cursor: not-allowed;
  border-color: rgba(140,120,180,0.15);
}}

.lobby-btn.secondary {{
  background: transparent;
  border-color: rgba(140,120,180,0.2);
  color: #8a7a9a;
}}
.lobby-btn.secondary:hover:not(:disabled) {{
  border-color: rgba(140,120,180,0.4);
  color: #b0a0c8;
}}

.lobby-btn.confirm {{
  background: linear-gradient(135deg, rgba(120,80,180,0.5), rgba(80,40,140,0.4));
  border-color: rgba(180,140,220,0.6);
  padding: 14px 48px;
  font-size: 16px;
}}

.btn-row {{
  display: flex; gap: 14px; margin-top: 28px;
}}

/* Playing Phase */
.playing-card {{
  background: linear-gradient(145deg, rgba(30,25,45,0.85), rgba(20,18,35,0.9));
  border: 1px solid rgba(140,120,180,0.3);
  border-radius: 20px;
  padding: 32px;
  text-align: center;
  max-width: 420px;
  width: 100%;
}}
.playing-avatar {{
  width: 120px; height: 120px;
  border-radius: 50%;
  background-size: cover;
  background-position: center;
  margin: 0 auto 20px;
  border: 3px solid rgba(160,140,200,0.4);
  box-shadow: 0 0 30px rgba(140,110,200,0.2);
}}
.playing-char-name {{
  font-size: 24px; font-weight: 600; color: #d0c8e8;
  margin-bottom: 6px;
}}
.playing-scenario {{
  font-size: 16px; color: #b090d0; margin-bottom: 20px;
  letter-spacing: 2px;
}}
.playing-hint {{
  font-size: 12px; color: #6a5a7a;
  line-height: 1.8;
}}
.playing-hint strong {{ color: #a090c0; }}

/* Raw data (hidden) */
.raw-data {{ display: none; }}
</style>
</head>
<body>

<canvas id="particles"></canvas>

<div class="lobby-container">
  <div class="lobby-title">
    <h1>M E T A V E R S E</h1>
    <div class="subtitle">L O B B Y</div>
  </div>

  <!-- Phase 1: Character Selection -->
  <div class="phase active" id="phase-select-char">
    <div class="phase-hint">✦ 选 择 你 的 命 运 ✦</div>
    <div class="character-grid" id="char-grid"></div>
    <div class="btn-row">
      <button class="lobby-btn confirm" id="btn-confirm-char" disabled>确认角色</button>
    </div>
  </div>

  <!-- Phase 2: Scenario Selection -->
  <div class="phase" id="phase-select-scenario">
    <div class="phase-hint" id="scenario-hint"></div>
    <div class="scenario-list" id="scenario-list"></div>
    <div class="btn-row">
      <button class="lobby-btn secondary" id="btn-back">← 返回</button>
      <button class="lobby-btn confirm" id="btn-confirm-scenario" disabled>确认开局</button>
    </div>
  </div>

  <!-- Phase 3: Confirmed -->
  <div class="phase" id="phase-playing">
    <div class="playing-card">
      <div class="playing-avatar" id="playing-avatar"></div>
      <div class="playing-char-name" id="playing-name"></div>
      <div class="playing-scenario" id="playing-scenario"></div>
      <div class="playing-hint">
        命运已启动<br>
        <strong>开局文本即将加载...</strong>
      </div>
    </div>
  </div>
</div>

<!-- Raw data (hidden) -->
<div class="raw-data">
{raw_data}
</div>

<script>
(function() {{
"use strict";

// ── Parse raw data ──
var rawEl = document.querySelector('.raw-data');
var rawText = rawEl ? rawEl.textContent.trim() : '';
var characters = [];
var scenarios = [];

var charRe = /\\[角色\\]name:(.+?)\\|id:(.+?)\\[\\/角色\\]/g;
var match;
while ((match = charRe.exec(rawText)) !== null) {{
  characters.push({{ name: match[1], id: match[2] }});
}}

var scenRe = /\\[场景\\]char:(.+?)\\|idx:(\\d+)\\|title:(.+?)(?:\\|nsfw:(true|false))?\\[\\/场景\\]/g;
while ((match = scenRe.exec(rawText)) !== null) {{
  scenarios.push({{
    char: match[1],
    idx: parseInt(match[2], 10),
    title: match[3],
    nsfw: match[4] === 'true'
  }});
}}

// ── State ──
var selectedCharId = null;
var selectedScenarioIdx = -1;

// ── DOM refs ──
var phaseChar = document.getElementById('phase-select-char');
var phaseScenario = document.getElementById('phase-select-scenario');
var phasePlaying = document.getElementById('phase-playing');
var charGrid = document.getElementById('char-grid');
var scenarioList = document.getElementById('scenario-list');
var scenarioHint = document.getElementById('scenario-hint');
var btnConfirmChar = document.getElementById('btn-confirm-char');
var btnConfirmScenario = document.getElementById('btn-confirm-scenario');
var btnBack = document.getElementById('btn-back');
var playingAvatar = document.getElementById('playing-avatar');
var playingName = document.getElementById('playing-name');
var playingScenario = document.getElementById('playing-scenario');

// ── Helper: avatar classes ──
var avatarClasses = {{
  airine: 'char-avatar-airine',
  bathsheba: 'char-avatar-bathsheba',
  lena: 'char-avatar-lena',
  meme: 'char-avatar-meme',
  belzeebul: 'char-avatar-belzeebul'
}};

// ── Phase switcher ──
function showPhase(phase) {{
  [phaseChar, phaseScenario, phasePlaying].forEach(function(el) {{
    el.classList.remove('active');
  }});
  if (phase === 'char') phaseChar.classList.add('active');
  else if (phase === 'scenario') phaseScenario.classList.add('active');
  else if (phase === 'playing') phasePlaying.classList.add('active');
}}

// ── Render character cards ──
function renderCharacters() {{
  charGrid.innerHTML = '';
  characters.forEach(function(c) {{
    var card = document.createElement('div');
    card.className = 'char-card';
    card.setAttribute('data-char-id', c.id);
    card.innerHTML =
      '<div class="char-avatar ' + (avatarClasses[c.id] || '') + '"></div>' +
      '<div class="char-name">' + c.name + '</div>' +
      '<div class="char-tagline">角色选择</div>';
    card.addEventListener('click', function() {{
      selectCharacter(c.id);
    }});
    charGrid.appendChild(card);
  }});
}}

function selectCharacter(charId) {{
  selectedCharId = charId;
  document.querySelectorAll('.char-card').forEach(function(card) {{
    if (card.getAttribute('data-char-id') === charId) {{
      card.classList.add('selected');
    }} else {{
      card.classList.remove('selected');
    }}
  }});
  btnConfirmChar.disabled = false;
}}

// ── Render scenarios for selected character ──
function renderScenarios(charId) {{
  var charScenarios = scenarios.filter(function(s) {{ return s.char === charId; }});
  scenarioList.innerHTML = '';
  charScenarios.forEach(function(s) {{
    var item = document.createElement('div');
    item.className = 'scenario-item';
    item.setAttribute('data-scenario-idx', s.idx);
    var nsfwBadge = s.nsfw ? '<span class="scenario-nsfw">NSFW</span>' : '';
    item.innerHTML =
      '<div class="scenario-idx">' + (s.idx + 1) + '</div>' +
      '<div class="scenario-info">' +
        '<div class="scenario-name">' + s.title + nsfwBadge + '</div>' +
      '</div>';
    item.addEventListener('click', function() {{
      selectScenario(s.idx);
    }});
    scenarioList.appendChild(item);
  }});

  var charName = '';
  characters.forEach(function(c) {{
    if (c.id === charId) charName = c.name;
  }});
  scenarioHint.textContent = '✦ ' + charName + ' · 选择开局 ✦';
}}

function selectScenario(idx) {{
  selectedScenarioIdx = idx;
  document.querySelectorAll('.scenario-item').forEach(function(item) {{
    if (parseInt(item.getAttribute('data-scenario-idx'), 10) === idx) {{
      item.classList.add('selected');
    }} else {{
      item.classList.remove('selected');
    }}
  }});
  btnConfirmScenario.disabled = false;
}}

// ── Confirm handlers ──
btnConfirmChar.addEventListener('click', function() {{
  if (!selectedCharId) return;
  renderScenarios(selectedCharId);
  selectedScenarioIdx = -1;
  btnConfirmScenario.disabled = true;
  showPhase('scenario');
}});

btnBack.addEventListener('click', function() {{
  showPhase('char');
}});

btnConfirmScenario.addEventListener('click', function() {{
  if (selectedScenarioIdx < 0 || !selectedCharId) return;

  // Find character name
  var charName = selectedCharId;
  var scenarioTitle = '';
  characters.forEach(function(c) {{
    if (c.id === selectedCharId) charName = c.name;
  }});
  scenarios.forEach(function(s) {{
    if (s.char === selectedCharId && s.idx === selectedScenarioIdx) {{
      scenarioTitle = s.title;
    }}
  }});

  // Show playing phase
  var avatarCls = avatarClasses[selectedCharId] || '';
  playingAvatar.className = 'playing-avatar ' + avatarCls;
  playingName.textContent = charName;
  playingScenario.textContent = '✦ ' + scenarioTitle + ' ✦';

  showPhase('playing');

  // Calculate swipe_id
  // Character order: airine=0, bathsheba=1, lena=2, meme=3, belzeebul=4
  // Each character has 5 scenarios (idx 0-4)
  var charIndexMap = {{ airine: 0, bathsheba: 1, lena: 2, meme: 3, belzeebul: 4 }};
  var charIdx = charIndexMap[selectedCharId] || 0;
  var swipeIdx = charIdx * 5 + selectedScenarioIdx;

  // Call setChatMessages to switch to the correct alternate greeting
  if (typeof setChatMessages === 'function') {{
    setChatMessages([{{ message_id: 0, swipe_id: swipeIdx }}], {{ refresh: 'affected' }});
  }}
}});

// ── Particle background ──
(function initParticles() {{
  var canvas = document.getElementById('particles');
  var ctx = canvas.getContext('2d');
  var particles = [];
  var PARTICLE_COUNT = 80;

  function resize() {{
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
  }}
  window.addEventListener('resize', resize);
  resize();

  for (var i = 0; i < PARTICLE_COUNT; i++) {{
    particles.push({{
      x: Math.random() * canvas.width,
      y: Math.random() * canvas.height,
      vx: (Math.random() - 0.5) * 0.4,
      vy: (Math.random() - 0.5) * 0.4,
      size: Math.random() * 1.8 + 0.4,
      opacity: Math.random() * 0.5 + 0.15,
      twinkleSpeed: Math.random() * 0.015 + 0.005,
      twinklePhase: Math.random() * Math.PI * 2
    }});
  }}

  function draw() {{
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    for (var i = 0; i < particles.length; i++) {{
      var p = particles[i];
      p.x += p.vx;
      p.y += p.vy;

      if (p.x < -10) p.x = canvas.width + 10;
      if (p.x > canvas.width + 10) p.x = -10;
      if (p.y < -10) p.y = canvas.height + 10;
      if (p.y > canvas.height + 10) p.y = -10;

      p.twinklePhase += p.twinkleSpeed;
      var alpha = p.opacity + Math.sin(p.twinklePhase) * 0.2;

      ctx.beginPath();
      ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
      ctx.fillStyle = 'rgba(180,150,220,' + Math.max(0, Math.min(1, alpha)) + ')';
      ctx.fill();
    }}

    // Draw faint connections between nearby particles
    for (var i = 0; i < particles.length; i++) {{
      for (var j = i + 1; j < particles.length; j++) {{
        var dx = particles[i].x - particles[j].x;
        var dy = particles[i].y - particles[j].y;
        var dist = Math.sqrt(dx * dx + dy * dy);
        if (dist < 120) {{
          ctx.beginPath();
          ctx.moveTo(particles[i].x, particles[i].y);
          ctx.lineTo(particles[j].x, particles[j].y);
          ctx.strokeStyle = 'rgba(140,120,180,' + (0.08 * (1 - dist / 120)) + ')';
          ctx.lineWidth = 0.5;
          ctx.stroke();
        }}
      }}
    }}

    requestAnimationFrame(draw);
  }}

  draw();
}})();

// ── Init ──
renderCharacters();
}})();
</script>
</body>
</html>'''
    
    return html


def main():
    print("Building MetaverseLobby first_mes HTML...")
    print("Processing avatars...")
    html = build_html()
    
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"\n✓ Written {len(html)} bytes to {OUTPUT_FILE}")
    print("Done!")


if __name__ == "__main__":
    main()
