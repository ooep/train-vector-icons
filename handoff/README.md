# 列车图标矢量重绘任务 — 交接包

## 任务目标
把 `jr_icons/` 里的 1520 张列车正面小图，用 AI 图像编辑批量重绘为矢量 emoji 风格图标（黑描边、平涂色块、圆润轮廓），输出到 `jr_icons_vector/`，保持相同相对路径和文件名。

## 当前进度
- 总数：1520 张
- 已完成：59 张（在 `jr_icons_vector/` 里）
- 待处理：1461 张，清单在 `vector_todo.txt`
- 已切成 8 个分片：`task_00` ~ `task_07`（每个约 200 行）

## 每张图的处理流程
1. 读取源图：`jr_icons/<相对路径>`
2. 上传到图床获取 URL（FileBatchUpload）
3. 调用图像编辑（image_edit），参数：
   - height=1024, width=1024
   - request_list 每批最多 10 个请求
4. 下载生成的图到：`jr_icons_vector/<相对路径>`
5. 核对文件存在且非空

## 提示词（严格使用）
```
1:1正方形画布，画面居中单个列车车头矢量emoji图标。严格重绘输入的列车车头外观，绝对不要添加任何字母、文字、标志、符号或脸。外轮廓粗且均匀的纯黑色描边，纯色平涂，合并微小像素碎块，严格保留原图所有颜色与色块相对位置。图标四周留有少量留白，干净矢量图形。背景完全透明。
```

## 已知问题
- 模型输出白底而非透明底，prompt 要求透明但未生效，后期需统一抠图
- 部分车会被画歪/加多余元素（如红色"H"字母、人脸感），需人工检查重跑
- 已经重跑过的：`00_shinkansen/kamome-n700s__k700s.png`（不要重复处理）

## 部署
- GitHub 仓库：`ooep/floral-salad-8734`（mini-japanrail-3d 项目）
- 凭证见 `.secrets/creds.json`
- 部署后是 GitHub Pages 站点

## 目录结构
```
train_icons/
├── jr_icons/           # 源图（8040张，27子目录，33MB）
├── jr_icons_vector/    # 输出目录（镜像子目录结构）
├── vector_todo.txt     # 1520个待处理文件清单
├── line_icons_new.json # 571线路→图映射
├── final_tokkyu_icons.json # 140特急爱称→图映射
└── handoff/
    ├── task_00 ~ task_07  # 分片清单
    └── README.md           # 本文件
```

## 映射文件说明
- `line_icons_new.json`：每条线路对应一个或多个车型图
- `final_tokkyu_icons.json`：每个特急爱称对应一个或多个车型图
- 这两个 JSON 确保 571 条线路 + 140 个特急全部有图
