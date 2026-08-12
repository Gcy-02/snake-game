# 🐍 贪吃蛇

一个网页版贪吃蛇，带排行榜。

一开始我用 pygame 写了个终端版（`1613.py`），能玩，但总感觉差点意思——自己玩玩还行，没法发给别人看。后来改成网页版：Flask 做后端，Canvas 渲染游戏，分数存 SQLite，首页放了个 TOP10 排行榜，前三名有奖牌。

## 功能

- 方向键控制蛇，撞墙、撞到自己就结束
- 吃一个食物 +1 分，蛇变长
- 游戏结束可以输入名字把分数存进排行榜
- 首页显示 TOP10，前三名 🥇🥈🥉
- 玩的时候按 Q 退出、按 C 重开

## 技术栈

- Python + Flask：后端路由和分数 API
- 原生 JavaScript + Canvas：游戏逻辑
- SQLite：分数持久化
- CSS：深色主题界面

## 运行

```bash
pip install flask
python app.py
```

浏览器打开 http://localhost:5000

数据库是首次运行自动创建的，不用手动建表。

想玩 pygame 终端版的话：

```bash
pip install pygame
python 1613.py
```

## 目录结构

```
app.py              # Flask 后端：页面路由 + 分数 API
templates/
  index.html        # 首页：开始游戏 + 排行榜
  game.html         # 游戏页
static/
  js/game.js        # 游戏逻辑（Canvas）
  css/style.css     # 样式
1613.py             # 最初的 pygame 终端版
```

## 写在后面

这是我学 Python 和 Web 开发时的练手作品（2026-07 写的）。代码写得很朴素，没什么花活，但胜在简单、能跑、能玩。排行榜是全局共享的，和同学朋友一起玩的时候互相刷分还挺有意思。
