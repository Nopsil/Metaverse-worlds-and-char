import requests
import re
import time
from pathlib import Path
from urllib.parse import urljoin

# ========== 配置 ==========
PROXIES = {
    "http": "http://127.0.0.1:7890",
    "https": "http://127.0.0.1:7890",
}

base = "https://copel-popn.github.io"
sidebar_url = f"{base}/_sidebar.md"
output_root = Path("./metaverse_full_story")
output_root.mkdir(exist_ok=True)
image_root = output_root / "images"
image_root.mkdir(exist_ok=True)

# ========== 1. 获取侧边栏索引 ==========
print("📡 正在拉取侧边栏索引...")
try:
    sidebar = requests.get(sidebar_url, timeout=10, proxies=PROXIES).text
except Exception as e:
    print(f"❌ 无法连接到侧边栏: {e}")
    exit()

lines = sidebar.split('\n')

# 设定范围
start_keyword = "旧人类战争篇"
end_keyword = "次元放浪记——Cross the Verse"

start_idx = None
end_idx = None
for i, line in enumerate(lines):
    if start_keyword in line and start_idx is None:
        start_idx = i
    if end_keyword in line and i > (start_idx or 0):
        end_idx = i
        break

if start_idx is None or end_idx is None:
    print("❌ 未找到起止标记，请检查侧边栏是否包含这两个标题")
    exit()

# 提取区间内的 MD 链接
target_links = []
for line in lines[start_idx:end_idx + 1]:
    matches = re.findall(r'\((/metaverse/[^)]+\.md)\)', line)
    target_links.extend(matches)

full_urls = set([base + link for link in target_links])

# ========== 2. 手动补抓 Cross-the-Verse ==========
cross_urls = [
    "https://copel-popn.github.io/metaverse/Cross-the-Verse/william.md",
    "https://copel-popn.github.io/metaverse/Cross-the-Verse/william2.md",
    "https://copel-popn.github.io/metaverse/Cross-the-Verse/airine0.md",
    "https://copel-popn.github.io/metaverse/Cross-the-Verse/maria.md",
    "https://copel-popn.github.io/metaverse/Cross-the-Verse/airine.md",
    "https://copel-popn.github.io/metaverse/Cross-the-Verse/momo.md",
    "https://copel-popn.github.io/metaverse/Cross-the-Verse/rinne.md",
    "https://copel-popn.github.io/metaverse/Cross-the-Verse/lavina.md",
    "https://copel-popn.github.io/metaverse/Cross-the-Verse/astol.md",
    "https://copel-popn.github.io/metaverse/Cross-the-Verse/everett.md",
    "https://copel-popn.github.io/metaverse/Cross-the-Verse/gray.md",
    "https://copel-popn.github.io/metaverse/Cross-the-Verse/hillda.md",
    "https://copel-popn.github.io/metaverse/Cross-the-Verse/ankh.md",
    "https://copel-popn.github.io/metaverse/Cross-the-Verse/ankh0.md",
]
full_urls.update(cross_urls)

print(f"✅ 共锁定 {len(full_urls)} 个 MD 文件")

# ========== 3. 图片下载函数 ==========
def download_image(img_url, save_dir):
    try:
        # 增加流式传输并在大文件时防止超时
        resp = requests.get(img_url, timeout=15, proxies=PROXIES, stream=True)
        if resp.status_code == 200:
            filename = Path(img_url).name
            if not filename:
                filename = f"image_{int(time.time())}.png"
            
            save_path = save_dir / filename
            counter = 1
            while save_path.exists():
                stem = save_path.stem + f"_{counter}"
                save_path = save_path.with_name(stem + save_path.suffix)
                counter += 1
                
            # 安全写入二进制内容
            with open(save_path, "wb") as f:
                for chunk in resp.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"    🖼️ 下载图片: {filename}")
            return True
        else:
            print(f"    ⚠️ 图片下载失败: {img_url} (状态码 {resp.status_code})")
    except Exception as e:
        print(f"    ❌ 图片异常: {img_url} -> {e}")
    return False

# ========== 4. 主循环 ==========
print("⬇️ 开始批量下载 MD 和图片...")
for url in full_urls:
    try:
        resp = requests.get(url, timeout=10, proxies=PROXIES)
        if resp.status_code != 200:
            print(f"  ⚠️ MD 下载失败: {url} (状态码 {resp.status_code})")
            continue

        md_name = Path(url).name
        md_path = output_root / md_name
        md_path.write_text(resp.text, encoding='utf-8')
        print(f"  ✅ MD: {md_name}")

        # 🔍 【核心修正 1】：过滤图片标签中的空格、双引号以及 title 说明文字
        img_links = re.findall(r'!\[[^\]]*\]\(([^\s)]+)(?:\s+["\'][^"\']*["\'])?\)', resp.text)
        
        if img_links:
            role_name = md_name.replace('.md', '')
            role_img_dir = image_root / role_name
            role_img_dir.mkdir(exist_ok=True)
            for rel_url in img_links:
                # 🔍 【核心修正 2】：使用当前的具体 MD 地址（url）进行相对路径拼接
                abs_url = urljoin(url, rel_url)
                download_image(abs_url, role_img_dir)

        time.sleep(0.2)

    except Exception as e:
        print(f"  ❌ 处理 {url} 时发生异常: {e}")

print(f"\n🎉 全部完成！")
print(f"   📁 MD 文件保存在: {output_root.absolute()}")
print(f"   🖼️ 图片保存在: {image_root.absolute()}")