# python自动脚本
[![pyAutoScript](https://img.shields.io/badge/python-v3.x-blue)](https://github.com/ziitar/pyAutoScript) ![windows only](https://img.shields.io/badge/platform-windows-blue)

一个使用json配置自定义在window程序点击/滑动操作流程的python脚本。可以用于制作游戏脚本、连点器、抢购或其他需要重复的操作的批处理脚本。（部分windows程序可能截图黑屏导致图像无法识别）

## 内容列表

- [背景](#背景)
- [安装](#安装)
- [使用说明](#使用说明)
- [示例](#示例)
- [相关仓库](#相关仓库)
- [接下来需要做](#接下来需要做)
- [如何贡献](#如何贡献)
- [特别说明](#特别说明)
- [使用许可](#使用许可)

## 背景
大部分现有的开源脚本只能在特定的场景下使用，对于用户的一些自定义操作无法支持。本项目意在提供一个通用的可自定义的脚本流程，使用者无需关心python代码如何实现，只要会配置json以及会基本的流程逻辑思维（当然还需会安装python及依赖），便能轻松的编写自己的脚本。

## 安装
安装python v3.x [windows安装指引](https://docs.python.org/zh-cn/3/using/windows.html#)。在[release](https://github.com/ziitar/pyAutoScript/releases)下载项目代码或者git clone本项目代码，执行[pip install](https://docs.python.org/zh-cn/3/installing/index.html)。

## 使用说明

### 配置
根据 [config item 字段及说明](https://github.com/ziitar/pyAutoScript/blob/master/config/config.md) 配置自己的流程，将配置使用json保存在项目config下，将样品图片放入项目imgs下。

### 执行
使用系统管理员打开cmd 
cd 到此项目所在目录
```
  $ python .\main.py
```
根据提示选择要执行的脚本配置文件
根据提示选中脚本执行对象（windows 程序）

## 示例
config/config.json:
```json
  {
    "start": {
        "debug": true,
        "match": {
            "method": "TM_SQDIFF_NORMED",
            "sample": "start.jpg",
            "targetNum": 1,
            "rate": 0.1
        },
        "reject": {
            "sleep": 1,
            "retry": 2
        },
        "resolve": {
            "do": "click"
        },
        "click": {
            "positionBase": "center",
            "offset": [
                0,
                0
            ],
            "random": 35
        },
        "sleep": 4,
        "next": "step_2"
    },
    "step_2": {
        "debug": true,
        "match": {
            "method": "TM_SQDIFF_NORMED",
            "sample": "step_2.jpg",
            "targetNum": 1,
            "rate": 0.1
        },
        "click": {
            "positionBase": "center",
            "random": 40
        },
        "resolve": {
            "do": "click"
        },
        "sleep": 22,
        "next": "start"
    }
}
```
等效于 ![流程图](http://assets.processon.com/chart_image/625d21381e085306fa70ddff.png)

## 相关仓库

[SmartOnmyoji](https://github.com/aicezam/SmartOnmyoji)


## 接下来需要做

- [ ] match.sample支持数组
- [ ] 当match.sample为数组是提供或、且判定
- [ ] 支持拖动操作
- [ ] 拖动支持ease-in-out，模拟人手动拖动
- [ ] 支持键盘按键
- [ ] 支持文本输入
- [ ] 支持特征值图像匹配
- [x] sleep支持随机浮动
- [ ] 支持adb链接android手机执行脚本
- [ ] 测试用例

## 如何贡献
非常欢迎你的加入！[提一个 Issue](https://github.com/ziitar/pyAutoScript/issues/new)或者提交一个 Pull Request。
遵循 [Contributor Covenant](http://contributor-covenant.org/version/1/3/0/) 行为规范。

## 特别说明

本项目不提供config配置文件，
仅作学习用途，请勿用于其他非法途径！

## 使用许可
[MIT](LICENSE) © Richard Littauer
