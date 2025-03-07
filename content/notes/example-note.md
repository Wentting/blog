---
title: 使用mkdocs进行技术文档编写
date: 2025-03-01
tags: [programmming, software]
description: A brief description of the example note.
reading_time: 3
---

### 1.准备工作
- 学习markdown 语法，写好文档必备
- 学习mkdocs 基本原理和规范，以便合理规划好建站导航
- 安装好python或安装好homebrew
### 2.安装mkdocs
###3.准备github工程
- 在该步骤，我们需要创建两个github工程。
- 一个是编写源文档的库，在该库下进行文档编写。
- 另一个是mkdocs编译后的部署仓库，博客的html仓库。
- 当我们编写好源文档库后，对源文档库执行mkdocs build命令进行编译，将编译后的site站点部署文档拷贝到github站点仓库。

### 具体操作
参考https://mkdocs-like-code.readthedocs.io/zh-cn/latest/get-started/deploy/

- 先推送，比如使用github desktop

- 之后在文件夹下面执行
`mkdocs gh-deploy`