# MetaverseLobby 远程状态栏（方案 A）

## 架构

```
卡片 (MetaverseLobby.png)
  └─ 正则 01-大厅界面 → 替换 <MetaverseLobby已就绪>
       └─ replaceString = 轻量 <body><script> 加载远程 dist
            └─ jsDelivr: .../remote-statusbar/dist/index.html
```

## 文件结构

```
remote-statusbar/
├── dist/
│   └── index.html          ← webpack 构建产物，通过 jsDelivr 托管
└── README.md
```

## 卡片集成

将 `regex-scripts/` 下的 3 个 JSON 导入酒馆（扩展→正则→导入），按编号顺序：

| 文件 | 用途 | 状态 |
|------|------|------|
| `01-大厅界面-远程.json` | 加载 jsDelivr dist | **启用** |
| `02-大厅界面-本地.json` | 加载 localhost:5500 | **禁用**（开发时手动切换） |
| `03-AI隐藏占位符.json` | 对 AI 隐藏占位符 | **启用** |

## 本地开发

```bash
# 启动本地服务器
npx serve remote-statusbar/dist -p 5500

# 重建 dist（修改 Vue 源码后）
cd tavern_helper_template && pnpm build
cp dist/MetaverseLobby/界面/状态栏/index.html ../remote-statusbar/dist/

# 在酒馆中：禁用 01，启用 02（本地版）→ 刷新即可看到最新改动
```

## 发布

```bash
git add remote-statusbar/
git commit -m "release: update status bar dist"
git push
# jsDelivr 自动更新（约 1-5 分钟缓存刷新）
```

## jsDelivr URL

```
https://cdn.jsdelivr.net/gh/Nopsil/Metaverse-worlds-and-char@master/remote-statusbar/dist/index.html
```
