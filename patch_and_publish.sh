#!/bin/bash

# 脚本执行中如遇到错误，则终止
set -e

# 更新项目版本号，patch 版本升级
poetry version patch

# 发布到 Python 包管理平台
poetry publish --build

# 将所有更改添加到 git
git add .

# 提交更改，自动使用版本号作为 commit message
version=$(poetry version -s)
git commit -m "Release version $version"

# 推送更改到远程仓库
git push origin main
