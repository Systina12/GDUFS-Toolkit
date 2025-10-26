# 项目暂时不可用，教务更新了，但是不知道为啥还是没有看平时成绩的功能。项目未来会不会更新取决于新教务有没有留查询api。
# 广外(GDUFS)工具箱

> 如果你只想在浏览器上查下平时成绩，并不想下载这个软件，请看我的另一个项目
>
> https://github.com/Systina12/GDUFS_grade_query_fix
>
> 这是一个修复平时成绩弹窗的油猴脚本，保留了原本的操作逻辑，非常简洁，没有任何其他特性

也许你和我一样，考完试后总想快一点知道成绩，但是广外的教务系统隔一会就要重新登录，于是考完试放松的时间就变成了输账号密码验证码戳戳戳的循环。

也许你也好奇过，为啥查不到平时成绩？外语外贸通是什么来的？是官方的吗？其实一切的问题都出在广外的教务系统上，本来应该点一下成绩数字就展开的平时成绩窗口，因为代码过于老旧，在新的浏览器上已经用不了了，可是，又有谁还在用IE？

所以这个项目诞生了。

**这是一个为广外学子设计的工具箱，旨在自动化实现教务上高频使用的功能**

[最新Release下载链接](https://github.com/Systina12/GDUFS-Toolkit/releases/latest)



**如果你发现了BUG或者使用途中出现了一些问题，请联系我或者发送issue。这对我真的很重要。**

## 功能

### 自动登录

利用 `ddddocr` 自动识别验证码，免去每次登录教务系统时手动输入账号、密码和验证码的繁琐步骤，让查询更加便捷高效。

### 详细成绩查询

教务系统的平时成绩查询依赖较旧的 JavaScript 特性，无法在现代浏览器中正常使用。本项目通过 `requests` 抓取相关数据，实现了平时成绩的自动查询，并以结构清晰的表格形式展示成绩。

### 课表查询

普普通通的功能，做了个比教务好看点的UI，按学年-学期查询课程表并显示，点击课程可以展示课程详情。



## 使用说明

### 直接食用

在这里下载打包好的最新版本[最新Release下载链接](https://github.com/Systina12/GDUFS-Toolkit/releases/latest)

**注意！**程序会在同一个目录下生成`config.json`用于存储配置和缓存

### 自行打包

##### 用git或者在仓库网页上下载代码到本地

```
git clone https://github.com/Systina12/GDUFS-Toolkit.git
```

##### 使用requirements.txt配置依赖并安装`PyInstaller`

```
pip install -r requirements.txt
pip install pyinstaller
```

如果你使用`uv`或者其他工具进行项目管理，请使用你的工具对应的命令

##### 修改`pack.spec`

将data里的路径改为你的`nicegui`和`common.onnx`所在目录

如果你使用虚拟环境，这两个路径应该是`.venv/Lib/site-package/nicegui`和`.venv/Lib/site-package/ddddocr/common/onnx`请自行查找

##### 使用`PyInstaller`打包

```
pyinstaller '.\pack.spec'
```

