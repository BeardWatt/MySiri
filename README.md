# MySiri

[TOC]

## 测试环境

| 环境           | 版本     |
| -------------- | -------- |
| macOS Catalina | 10.15.7  |
| PyCharm        | 2020.3.3 |
| Python         | 3.9      |

## 依赖包
见requirement.txt

```shell
# 安装依赖包
# pip3 install -r requirement.txt
# 或（建议）,可以自动忽略错误，安装成功的包
cat requirements.txt | xargs -n 1 pip3 install

# macOS还需要
pip3 install -r requirements_macOS.txt
```

pyobjc*包为macOS独占，macOS必须安装；其他平台不能安装，不影响软件功能使用。

## 运行方式

```shell
# cd 到源码的ui路径下
cd MySiri/package/ui

# 执行
python3 MainWindow.py
```

## 运行截图

- macOS

![Biser@macOS](README.assets/Biser@macOS.jpg)

- Ubuntu

![Biser@Pi](README.assets/Biser@Pi.png)

## 鸣谢
- 讯飞语音API提供语音支持
- 图灵机器人API提供反馈支持
- ImageMagick提供运行截图拼接支持
