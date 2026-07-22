import os

path = r'D:\jiuguan\SillyTavern\public\index.html'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

clean = [line for line in lines if 'cocktail' not in line.lower()]
with open(path, 'w', encoding='utf-8') as f:
    f.writelines(clean)

print(f"Removed {len(lines) - len(clean)} cocktail lines from index.html")