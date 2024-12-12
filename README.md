# 夸克网盘自动签到

借助 GitHub Actions 定时运行 Python 程序来实现签到功能



## 使用方法

### 一、Fork 本仓库

点击右上角的 Fork 按钮将本仓库 Fork 至自己的账号下。



### 二、手机抓包获取签到所需变量

可以用的抓包工具：[Reqable](https://reqable.com/zh-CN/) 

1. 使用手机客户端访问签到界面。
2. 对 https://drive-m.quark.cn/1/clouddrive/capacity/growth/info 请求进行抓包。
3. 记录下该 url 后面的参数：`kps`、`sign` 以及 `vcode`。



### 三、添加到环境变量

在仓库的 Settings → Secrets and variables → Actions 中，点击 New repository secret 来添加刚刚获取的三个参数。

其中 Name 需全部大写，即：`KPS`、`SIGN` 和 `VCODE`，Secret 则对应各自的值。



### 四、手动执行

若对配置是否成功心存疑虑，可在仓库的 Actions 里找到 daily auto sign-in 并点击 Run workflow 就能手动执行签到操作。



## 配置推送

本项目使用 [Server酱<sup>3</sup>](https://sc3.ft07.com/) 来进行推送消息。



### 配置步骤

在 [SendKey](https://sc3.ft07.com/sendkey) 页面获取 SendKey 后，将其添加至 Secrets 当中，Name 设置为 `SENDKEY` 。

