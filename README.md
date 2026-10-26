# Xiaoxiao · 书页与舞台

笑笑的中英文个人网站：作品、观演札记和舞台导演手记。静态 HTML、CSS、JavaScript，无框架、无构建依赖。

- 网站：https://soloxue.github.io/xiao-blog/
- GitHub：https://github.com/soloxue/xiao-blog
- 当前公开版：2026-10-26；6篇Works、9篇Notes、1篇Stage，共40个中英文内容与目录页面。

## 本地预览

```powershell
python -m http.server 8736 --bind 127.0.0.1
```

打开 http://127.0.0.1:8736/ 。静态资源使用相对路径，支持GitHub Pages的`/xiao-blog/`项目路径。

## 文件结构与语言

- `index.html`：英文首页；`index.cn.html`：中文首页。
- `works/`、`notes/`、`stage/`：栏目目录；栏目首页的中文版本为`index.cn.html`。
- 每篇内容独立目录：`index.html`为英文，`cn.html`为中文，配图使用同目录WebP。
- `styles.css`、`app.js`、`fonts/`：共用样式、交互和字体。
- `DESIGN.md`、`DESIGN_CN.md`：中英文设计规范；`AGENTS.md`：维护规则。
- 旧版`index.zh.html`、`works.html`等地址仅作跳转，不保存旧站内容。对应规则在`scripts/build-redirects.py`。

## 已确定的设计

首页Works与Notes各展示最近1篇大图和3条目录，再进入完整目录。整站框架上限1440px，Works正文约800px，部分插图可到980px；首页和详情页背景封面允许铺满窗口。

详情页使用按篇选图的响应式封面和少量强调色。顶部导航保持可见，语言切换固定为等宽的“中文丨En”。Works正文使用衬线字体，Notes正文使用IBM Plex Sans／思源黑体；中文Notes题名在各处统一使用霞鹜文楷。Stage正文保留衬线字体。

各栏目按目录顺序连接上一篇／下一篇，首尾是明确的静态状态；英文Beginning／Finis、中文开篇／终篇与花叶饰仅用于装饰，下方保留首尾说明。单篇Stage两侧均为静态状态。Footer只保留左侧版权。图片查看器支持切图、图序、原尺寸、说明、键盘、关闭和焦点恢复，正文照片的分组与尺寸不受影响。

## 检查

运行环境：Node.js用于原有引用审查；Python 3.10+用于维护。浏览器检查另需`playwright`；字体子集维护需`fonttools`和`brotli`，图片补录需`Pillow`。日常访问和Pages发布不需要这些工具。

```powershell
python scripts/check-site.py
node scripts/audit.cjs
python scripts/browser-check.py
```

浏览器检查优先使用本机Chrome／Edge，也可使用Playwright的Chromium；未安装浏览器时可按Playwright文档安装。检查会启动只绑定本机的临时服务器，并模拟`/xiao-blog/`路径。线上复核：

```powershell
python scripts/browser-check.py --base-url https://soloxue.github.io/xiao-blog/ --widths 390,1440
```

输出与截图保存在`previews/`，不提交。原有`verify-notes.py`与`verify-zh-font.py`入口已转向当前浏览器检查，避免继续验证旧版布局。`verify-theatre-archive.py`等专项检查需要本地补录底稿，不是干净克隆的必需检查。

## 内容维护

原文和照片顺序优先；中文保留作者原有的中英混写，英文提供完整英文编辑版。使用可靠英文名或罗马字，语言切换标签除外，不保留无必要汉字。日期沿用材料，不补造日期、场次或个人经历。

- 封面文件与桌面／手机焦点：`scripts/article_presentation.py`；强调色：`styles.css`的`[data-article]`规则。
- 相邻导航：`scripts/reading_navigation.py`读取各栏目目录。新增、重排后重新生成受影响页面的导航，校验首尾和双语链接。
- 历史六则札记：`scripts/theatre_notes_content.py`维护译文与段落安排；`build-theatre-notes.py`需要网站上级本地`朋友圈/`原始JPG。生成器不是部署步骤，不在公开仓库提供私有底稿。
- `source.txt`、`archive.json`、原始朋友圈目录、预览截图与机器检查结果保留本地，不进入发布提交。
- 更改中文题名时核对字体cmap；需要时从官方完整字体重建子集。朱雀仿宋与霞鹜文楷均随仓库保留OFL许可；Web字体子集用于网页展示，不作为桌面字体发布。

## GitHub Pages发布

Pages使用`main`分支根目录，保留`.nojekyll`；无需另建构建工作流。先完成检查，再以普通提交推送，不强推、不清除Git历史。GitHub的Pages部署成功后，再验证线上首页、双语详情、资源与旧网址跳转。

本版替换了之前站点的当前文件；旧提交仍保留，可通过`git revert <发布提交>`建立回退提交。保留原仓库的托管配置或CNAME，若新增这些配置，应先核对Pages设置。

## 版权与字体

网站署名为© 2026 Xiaoxiao。字体许可分别见`fonts/OFL-Zhuque.txt`、`fonts/OFL-LXGW-WenKai.txt`；正文依赖的Google Fonts在不可用时使用系统后备字体。公开访问不意味着本仓库另行授予作品和照片的转载许可。
