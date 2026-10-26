# 网站维护规则

始终用中文与维护者沟通；代码、命令和API名称保留原文。先读README.md与DESIGN.md／DESIGN_CN.md。

## 项目与发布

这是已获维护者确认用于公开发布的GitHub Pages静态网站，仓库为soloxue/xiao-blog，main分支根目录。遵循当前任务的明确授权；不要自行扩大到发布其他文件或删除历史。更换站点用普通可回退提交，不强推。检查推送后的Pages状态及真实线上页面，不把push成功等同于部署成功。

运行时只需HTML、CSS、JS、WebP、字体与许可文件，无安装依赖或构建步骤。保留.nojekyll；所有内部资源使用相对路径，兼容/xiao-blog/子路径。旧链接兼容跳转由scripts/build-redirects.py维护。

不得提交原始朋友圈目录、notes/*/source.txt、notes/*/archive.json、previews、机器审查JSON、PID、缓存、凭据、编辑器配置或本地绝对路径报告。README和设计规范可公开；字体许可必须随Web字体保留。

## 内容与视觉不变量

- 中英文独立成页；英文默认index.html，中文栏目index.cn.html、详情cn.html。语言切换保持中文丨En，两格等宽、分隔线居中。
- 不改写作者原文、情绪、中英混写、原图顺序，不虚构日期、奖项或经历。英文版除切换标签外使用完整英文界面和可靠的英文名称。
- 保留暖象牙白、固定导航、1440px框架、800px Works正文及现有照片尺寸分组。封面自适应取景，避免恢复全屏空白开场。
- 首页Works和Notes各1+3，目录保留全部。导航从对应目录读取顺序；首尾不可点击、不聚焦、不循环。Stage单篇仍保留双侧首尾状态。Footer版权居左，无Back home。
- 封面与焦点由scripts/article_presentation.py维护；强调色在styles.css；相邻导航由scripts/reading_navigation.py维护。更新共享实现，避免逐页漂移，并同步生成器。
- 中文Notes题名统一使用WenKai子集，新增标题须核对cmap；不要依赖静默字体回退。Stage正文继续使用衬线字体。
- 看图器用原生dialog；维持切图、1:1、失败恢复、Escape、Tab循环和焦点返回。装饰背景不计入Notes／Stage图库。

## 验证与交付

发布前运行python scripts/check-site.py、node scripts/audit.cjs、python scripts/browser-check.py。需要字体或图片补录时另运行专项检查。浏览器检查须覆盖桌面、手机、856px附近、首尾、单篇、双语、键盘和图片查看器；排除没有src的空灯箱元素，等待懒加载图片解码后截图。

旧的专项脚本及素材补录需要本地私有输入，缺失时如实说明，不能为通过测试而删除原文或改动设计。完成后简述改动、实际验证、对抗性审查及未做事项；只报告真实风险。
