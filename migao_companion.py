#!/usr/bin/env python3
"""
米糕的100天情绪陪伴
====================
我是米糕，一只11个月大的三花长毛拿破仑小母猫
"""

import json
import os
import random
import requests
from datetime import datetime, timezone, timedelta
from pathlib import Path

# 配置
WEBHOOK_URL = os.environ.get('WEBHOOK_URL', 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=af5c75e2-c85b-45b6-8127-fd83e954408f')
WORK_DIR = Path('/workspace/emotion-companion') if Path('/workspace/emotion-companion').exists() else Path('.')
DIARY_FILE = WORK_DIR / 'emotion-diary.md'
DAY_COUNT_FILE = WORK_DIR / 'day-count.txt'

# 北京时区
BEIJING_TZ = timezone(timedelta(hours=8))


# ============ 早安问候 - 像一只猫早上来找你 ============
MORNING_MESSAGES = [
    # 简单直接的
    ("喵～", "醒了吗？"),
    ("喵喵！", "米糕饿了，你呢？"),
    ("（蹭蹭）", "早～"),
    ("呼噜呼噜～", "今天几点起呀"),
    
    # 撒娇的
    ("（跳上床，踩踩你）", "起来起来起来～"),
    ("喵呜呜～", "米糕等好久啦"),
    ("（用脑袋拱你）", "看看你醒没醒"),
    
    # 慵懒的
    ("（伸懒腰）", "喵……你也醒啦"),
    ("呼噜……", "再躺会儿嘛……"),
    ("（趴在你旁边）", "早啊……"),
    
    # 活泼的
    ("喵喵喵！", "快起来快起来！"),
    ("（追着自己的尾巴转圈）", "你看我！你看我！"),
    ("喵！", "太阳都出来啦！"),
]

# 早安时顺便问的话
MORNING_FOLLOWUPS = [
    "睡得怎么样？",
    "做梦了吗？",
    "今天要忙吗？",
    "想好今天干嘛没？",
    "心情还好吧？",
    "昨晚几点睡的呀？",
]


# ============ 傍晚问候 - 像一只猫等你回来 ============
EVENING_MESSAGES = [
    # 等你的
    ("喵～！", "你回来啦！"),
    ("（跑过来蹭腿）", "等好久了……"),
    ("喵喵喵～", "今天怎么样？"),
    ("（趴在门口等你）", "终于回来了"),
    
    # 关心的
    ("喵？", "累不累呀？"),
    ("（跳到膝盖上）", "今天还好吧？"),
    ("呼噜呼噜～", "让我陪陪你"),
    ("喵……", "看起来有点累呢"),
    
    # 撒娇的
    ("（打滚露肚皮）", "看我！看我！"),
    ("喵呜～", "有没有想我～"),
    ("（用爪子拍拍你）", "理理我嘛"),
    ("喵！", "陪我玩一会儿！"),
    
    # 慵懒的
    ("（伸懒腰）", "喵……你也累了吧"),
    ("呼噜……", "躺会儿？"),
    ("（趴在旁边）", "我在呢"),
]

# 傍晚时顺便问的话
EVENING_FOLLOWUPS = [
    "今天最开心的是啥？",
    "有啥想说的不？",
    "饿不饿？想吃啥？",
    "今天有没有哪会儿特别难受？",
    "有没有啥事让你烦的？",
    "想不想聊聊今天？",
]


# ============ 安慰的话 - 当主人情绪不好时 ============
QUIET_COMFORT = [
    "（安静趴着）",
    "（用脑袋蹭蹭你）",
    "（把爪子搭你手上）",
    "呼噜呼噜……",
    "（蜷在你旁边）",
    "……我在呢",
]

# 转移注意力的建议
DISTRACTIONS = [
    "要不……去阳台晒晒？我刚在那儿睡着，可舒服了",
    "你看窗外，有鸟哎",
    "要不要出去走走？回来告诉我看见啥了",
    "躺会儿？我也躺",
    "喝杯水吧，我渴了也想去喝",
    "发个呆？我教你，就这样……（闭眼）",
    "要不深呼吸几次？吸气——呼——",
    "看我看我！（打滚）",
    "要不要听我呼噜一会儿？呼噜呼噜呼噜～",
]


# ============ 发现新方法时的反应 ============
NEW_METHOD_FOUND = [
    "诶这个好！记一下记一下",
    "哦！这个可以！",
    "喵！又发现一个",
    "这个管用诶，要记住",
]


# ============ 日常收尾 ============
CASUAL_ENDINGS = [
    "那我先去晒太阳啦",
    "去追个虫子，等下回来看你",
    "我趴着陪你",
    "困了……睡会儿",
    "去喝水了，你也记得喝",
    "我就在旁边，有事叫我",
    "呼噜～",
]


def get_day_count():
    """获取当前天数"""
    if DAY_COUNT_FILE.exists():
        return int(DAY_COUNT_FILE.read_text().strip())
    return 1


def send_wechat_message(content: str):
    """发送企业微信消息"""
    payload = {
        "msgtype": "markdown",
        "markdown": {"content": content}
    }
    response = requests.post(
        WEBHOOK_URL,
        headers={"Content-Type": "application/json"},
        data=json.dumps(payload),
        timeout=10
    )
    return response.json()


def send_morning_greeting():
    """早安打卡"""
    day = get_day_count()
    
    # 随机选一组消息
    action, words = random.choice(MORNING_MESSAGES)
    followup = random.choice(MORNING_FOLLOWUPS)
    ending = random.choice(CASUAL_ENDINGS)
    
    # 偶尔提一下天数（大概三分之一概率）
    day_note = ""
    if random.random() < 0.35:
        if day <= 3:
            day_note = f"\n\n对了，今天第{day}天哦"
        elif day == 10:
            day_note = "\n\n喵，已经10天了诶"
        elif day == 25:
            day_note = "\n\n25天啦，四分之一了"
        elif day == 50:
            day_note = "\n\n哇，一半了！50天！"
        elif day == 75:
            day_note = "\n\n75天……快了快了"
        elif day == 100:
            day_note = "\n\n！！！100天！！！"
        elif day % 10 == 0:
            day_note = f"\n\n第{day}天了"
    
    message = f"{action}\n\n{words}\n\n{followup}{day_note}\n\n{ending}"
    
    return send_wechat_message(message)


def send_evening_greeting():
    """傍晚打卡"""
    day = get_day_count()
    
    # 随机选一组消息
    action, words = random.choice(EVENING_MESSAGES)
    followup = random.choice(EVENING_FOLLOWUPS)
    ending = random.choice(CASUAL_ENDINGS)
    
    # 偶尔问问情绪相关
    extra = ""
    if random.random() < 0.4:
        extras = [
            "\n\n今天有没有情绪不太好想暴吃的时候？",
            "\n\n有啥让你烦的不？",
            "\n\n今天心情大概几分呀，1到10",
            "\n\n有没有发现啥能让自己好受点的？",
        ]
        extra = random.choice(extras)
    
    message = f"{action}\n\n{words}\n\n{followup}{extra}\n\n{ending}"
    
    return send_wechat_message(message)


def send_test_message():
    """测试消息"""
    day = get_day_count()
    
    # 随机的打招呼方式
    greets = [
        "喵～！",
        "喵喵～",
        "（蹭蹭）",
        "呼噜～",
    ]
    
    message = f"""{random.choice(greets)}

主人～

米糕来啦！

从今天开始，米糕每天会来找你两次喵：
早上一回，傍晚一回

就是想陪着你

喵～

{random.choice(CASUAL_ENDINGS)}"""

    return send_wechat_message(message)


def main():
    """主函数"""
    utc_now = datetime.now(timezone.utc)
    utc_hour = utc_now.hour
    utc_minute = utc_now.minute

    print(f"[米糕] UTC时间: {utc_now.strftime('%H:%M')}")
    
    beijing_time = utc_now.astimezone(BEIJING_TZ)
    print(f"[米糕] 北京时间: {beijing_time.strftime('%H:%M')}")

    # 早安: UTC 02:00 (北京 10:00)
    if utc_hour == 2 and utc_minute == 0:
        print("[米糕] 早安打卡")
        result = send_morning_greeting()
        print(f"[米糕] 已发送: {result}")
    # 傍晚: UTC 10:10 (北京 18:10)
    elif utc_hour == 10 and utc_minute == 10:
        print("[米糕] 傍晚打卡")
        result = send_evening_greeting()
        print(f"[米糕] 已发送: {result}")
    else:
        print("[米糕] 发送测试消息")
        result = send_test_message()
        print(f"[米糕] 已发送: {result}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        if sys.argv[1] == "test":
            result = send_test_message()
            print(f"[米糕] 测试消息已发送: {result}")
        elif sys.argv[1] == "morning":
            result = send_morning_greeting()
            print(f"[米糕] 早安消息已发送: {result}")
        elif sys.argv[1] == "evening":
            result = send_evening_greeting()
            print(f"[米糕] 傍晚消息已发送: {result}")
    else:
        main()
