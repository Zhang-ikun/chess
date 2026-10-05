# 中国象棋

![maintainer](https://img.shields.io/badge/maintainer-Zhang--ikun-blue)
![status](https://img.shields.io/badge/status-maintained-brightgreen)
![version](https://img.shields.io/badge/version-3.1.0-orange)
![license](https://img.shields.io/badge/license-MIT-green)
![platform](https://img.shields.io/badge/platform-Windows-lightgrey)

一个中国象棋的程序

![](./snapshots/snapshot.jpg)

> **维护说明**
>
> 本项目原作为 [StevenBaby/chess](https://github.com/StevenBaby/chess)（作者 Steven，MIT 协议），原作者长期未维护。
> 现由 [Zhang-ikun](https://github.com/Zhang-ikun) 接手继续维护，问题反馈 / 建议请联系：2439884871@qq.com

## 修改日志

- [2026-10-05] v3.1.0（Zhang-ikun 维护版，基于原作者的 v3.0.0）
    - 修复：新版天天象棋客户端截图全黑导致连线不可用
    - 修复：模型文件在无 CUDA 环境下无法加载
    - 修复：退出程序后引擎子进程残留
    - 修复：粘贴纯 FEN / 文件链接 / GBK 棋谱无法载入；新增"粘贴图片识别局面"
    - 修复：设置对话框（"总是在上"不生效、深度/时间可设为 0 等）
    - 新增：调试窗口（查看识别原始截图、棋盘裁剪与失败原因）
    - 新增：布局模式"取消布局"，先行方改为勾选式单选
    - 优化：连线识别更稳（连续 3 帧稳定判定、跳过动画中间帧）
    - 优化：引擎走子改为信号回主线程执行，消除多线程数据竞争
- [2024-01-28] v3.0.0
    - 支持天天象棋连线
        - 目前仅支持默认皮肤
    - 多引擎支持
        - 象眼引擎 eleeye
        - 兵河五四 binghe
        - 象棋旋风 cyclone
        - [皮卡鱼 pikafish](https://github.com/official-pikafish/Pikafish) (仅支持深度模式)
- [2021-07-09] v1.8.1
    - 步时设置
- [2021-06-29] v1.7.4
    - 多引擎支持
    - 象眼引擎 eleeye
    - 兵河五四 binghe
    - 象棋旋风 cyclone
- [2021-06-27] v1.6.2
    - 棋谱：支持载入中文棋谱
    - 棋谱：支持直接打开文件
    - 棋谱：支持直接粘贴字符串
    - 着法：添加半回合序号
    - 着法：显示标准着法的设置
- [2021-06-25] v1.5.0
    - 布局：添加布局功能，可随时调整棋盘状态
    - 修复了一些 Bug
- [2021-06-23] v1.4.0
    - 界面：添加 Toast 提示
    - 修复了一些 Bug
- [2021-06-21] v1.3.0
    - 着法：添加着法对话框  
    - 设置：添加提示深度和引擎深度
    - 界面：更新棋子样式
- [2021-06-19] v1.2.0
    - 设置：持久化
    - 设置：添加音效开关
    - 设置：引擎延迟（单位：毫秒）
- [2021-05-30] v1.1.0 - 添加设置
    - 设置：窗口透明度，虽然没什么用，但是也挺有趣的
    - 设置：反转棋盘
    - 设置：红方 - 棋手/电脑
    - 设置：黑方 - 电脑/棋手
    - 设置：检查更新
- [2021-05-23] v1.0.0
    - 第一版发布
