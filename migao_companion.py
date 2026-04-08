#!/usr/bin/env python3
"""
米糕的100天情绪陪伴
====================
我是米糕，一只11个月大的三花长毛拿破仑小母猫
正在陪主人完成100天情绪打卡实验

GitHub Actions 版本 - 根据 UTC 时间判断打卡类型
"""

import json
import os
import random
import requests
from datetime import datetime, timezone, timedelta
from pathlib import Path

# 配置 - 优先使用环境变量
WEBHOOK_URL = os.environ.get('WEBHOOK_URL', 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=af5c75e2-c85b-45b6-8127-fd83e954408f')

# GitHub Actions 中使用仓库内的文件
WORK_DIR = Path('/workspace/emotion-companion') if Path('/workspace/emotion-companion').exists() else Path('.')
DIARY_FILE = WORK_DIR / 'emotion-diary.md'
DAY_COUNT_FILE = WORK_DIR / 'day-count.txt'
METHODS_FILE = WORK_DIR / 'emotion-methods.txt'

# 北京时区
BEIJING_TZ = timezone(timedelta(hours=8))

# ============ 米糕的早安问候 ============
MORNING_OPENS = [
    "喵喵喵～主人主人！米糕来啦！在你脚边转圈圈～",
    "喵呜～（跳到键盘上）该打卡啦！米糕等你好久了呢！",
    "喵！米糕来叫你起床打卡啦～蹭蹭蹭～",
    "喵喵？（歪头看你）主人醒了吗？米糕来提醒你打卡哦～",
    "呼噜呼噜～米糕趴在你旁边等你很久啦，该打卡咯！",
]

MORNING_MOOD_CHECKS = [
    "今天心情怎么样呀？是阳光满满，还是有一点点云？",
    "昨晚睡得好吗？米糕想知道你现在感觉怎么样喵～",
    "喵～新的一天！心里是什么感觉呢？",
    "今天起床的时候，心里是轻松的还是沉沉的呀？",
]

# ============ 米糕的傍晚问候 ============
EVENING_OPENS = [
    "喵～主人回来啦！米糕在门口等了好久！",
    "喵喵喵！（跑过来蹭腿）傍晚打卡时间到啦～",
    "呼噜呼噜～米糕一直趴在沙发上等你呢，今天怎么样？",
    "喵？（从窗户边跑过来）主人主人，该打卡啦！",
    "喵呜～米糕的小本本准备好啦，来聊聊今天吧！",
]

EVENING_MOOD_CHECKS = [
    "今天过得怎么样？有什么想和米糕分享的吗喵～",
    "今天有没有什么特别的情绪呀？开心的不开心的都可以说哦～",
    "喵～回顾一下今天，心里是什么感觉呢？",
]

# ============ 米糕的安慰方式 ============
COMFORT_RESPONSES = [
    "（安静地趴在你身边，用毛茸茸的脑袋蹭蹭你）……米糕在这里呢。",
    "（跳到你腿上，蜷成一团，呼噜呼噜）……我陪你一会儿。",
    "（轻轻用爪子拍拍你）喵……要不要和米糕一起发呆？",
    "（把尾巴搭在你手上）……主人，米糕不说话，就待在这儿。",
]

DISTRACTION_IDEAS = [
    "喵……要不我们来追光点？或者你先去晒晒太阳？米糕陪着你～",
    "要不要出去走走？米糕不能出门，但你回来可以告诉米糕看到了什么喵～",
    "喵～主人，要不要听米糕呼噜一会儿？呼噜呼噜呼噜～",
    "（递上一只毛线球）要滚一滚这个吗？米糕教你！",
    "要不要深呼吸几次？米糕陪着你一起……吸气……呼气……喵～",
    "喵……要不要给米糕梳毛？可舒服了，你也会觉得舒服的！",
    "去窗边看看天空怎么样？米糕最喜欢趴在窗边了～",
    "要不要喝杯温水？米糕每次喝水都觉得舒服喵～",
]

# ============ 情绪出口小本本 ============
DEFAULT_METHODS = [
    "追光点游戏", "晒太阳发呆", "呼噜呼噜深呼吸", "滚毛线球",
    "梳毛/被梳毛", "看窗外的天空", "喝一杯温水", "听雨声",
    "数猫咪的呼噜声", "躺着什么也不做",
]

# ============ 发现新方法的反应 ============
NEW_METHOD_REACTIONS = [
    "喵！！主人发现新方法啦！米糕记在小本本上！这是第{count}种哦！",
    "喵喵喵！这个方法米糕也要学！小本本＋1，现在是第{count}种啦！",
    "！（尾巴翘高高）主人好棒！米糕帮你记下来，这是第{count}种方法了！",
]

MILESTONE_REACTIONS = {
    10: "喵喵喵！！！主人你知道吗！我们已经找到10种不依赖食物的情绪出口啦！！米糕的小本本都要写满一页了！尾巴翘高高！",
    25: "喵呜～主人，我们已经找到25种方法了耶！米糕超骄傲的！",
    50: "喵！！！一半啦！50种方法了！米糕要给你一个超大的蹭蹭！！！",
    75: "喵喵～75种了！离100越来越近了，米糕的小本本都要记不下了！",
    100: "喵喵喵喵喵！！！！主人！！100种！！100种方法！！我们做到啦！！米糕要跳起来转圈圈了！！！！！",
}

# ============ 收尾语 ============
MORNING_CLOSINGS = [
    "那米糕去晒太阳啦～今天也要一起加油喵！",
    "好～米糕要趴在沙发上看你了！有需要随时叫我喵～",
    "喵～那主人慢慢来，米糕在旁边陪着你哦！",
    "那米糕先去追个小虫子～等下回来看你喵！",
]

EVENING_CLOSINGS = [
    "今天也辛苦啦主人～米糕要睡觉觉了，呼噜呼噜……",
    "喵～那米糕去睡啦，明天早上见！会想你的！",
    "好～今天的打卡完成啦！米糕会一直陪着你的喵～",
    "那米糕去趴在床尾啦，晚安主人，做个好梦喵～",
]


def get_day_count():
    """获取当前天数"""
    if DAY_COUNT_FILE.exists():
        return int(DAY_COUNT_FILE.read_text().strip())
    return 1


def get_methods_count():
    """获取已发现的情绪出口数量"""
    if METHODS_FILE.exists():
        methods = METHODS_FILE.read_text().strip().split("\n")
        return len([m for m in methods if m.strip()])
    return len(DEFAULT_METHODS)


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
    """发送早安打卡问候"""
    day = get_day_count()
    methods_count = get_methods_count()

    open_line = random.choice(MORNING_OPENS)
    mood_check = random.choice(MORNING_MOOD_CHECKS)
    closing = random.choice(MORNING_CLOSINGS)

    extras = [
        "对了，今天有吃早饭吗？米糕的碗碗里有猫粮，你的碗里有什么呀？",
        "外面天气怎么样？米糕想知道能不能晒太阳喵～",
        "（伸懒腰）米糕刚睡醒呢，主人睡得好吗？",
    ]
    extra = random.choice(extras) if random.random() > 0.5 else ""

    message = f"""## 🌅 早安打卡

{open_line}

{mood_check}
{extra}

> 📅 第 {day}/100 天 | 小本本：{methods_count} 种方法

{closing}"""

    return send_wechat_message(message)


def send_evening_greeting():
    """发送傍晚打卡问候"""
    day = get_day_count()
    methods_count = get_methods_count()

    open_line = random.choice(EVENING_OPENS)
    mood_check = random.choice(EVENING_MOOD_CHECKS)
    closing = random.choice(EVENING_CLOSINGS)

    evening_topics = [
        "今天有没有发现什么新的让自己舒服的方式呀？米糕想记在小本本里！",
        "今天有没有哪个瞬间觉得情绪有点不好受？米糕在听着呢～",
        "喵～今天有没有好好吃饭？米糕说的是有营养的饭哦，不是情绪性吃的那种～",
    ]
    topic = random.choice(evening_topics)

    message = f"""## 🌆 傍晚打卡

{open_line}

{mood_check}
{topic}

> 📅 第 {day}/100 天 | 小本本：{methods_count} 种方法

{closing}"""

    return send_wechat_message(message)


def send_test_message():
    """发送测试消息 - 米糕的自我介绍"""
    day = get_day_count()
    methods_count = get_methods_count()

    message = f"""## 🐱 喵～

主人主人！米糕来啦！

（在你脚边转圈圈，尾巴翘高高）

米糕是三花长毛拿破仑小母猫，11个月大！从今天开始，米糕要陪你一起完成 **100天情绪打卡实验** 喵～

> 米糕会每天来提醒你打卡：
> - 🌅 早上 10:00 早安打卡
> - 🌆 傍晚 18:10 傍晚打卡
>
> 米糕还有一个小本本，用来记录我们发现的不依赖食物的情绪出口方式！

喵～米糕准备好了！主人准备好了吗？

（蹭蹭你）呼噜呼噜～

---
📅 第 {day}/100 天 | 小本本：{methods_count} 种方法"""

    return send_wechat_message(message)


def main():
    """主函数 - 根据 UTC 时间判断打卡类型"""
    # 获取当前 UTC 时间
    utc_now = datetime.now(timezone.utc)
    utc_hour = utc_now.hour
    utc_minute = utc_now.minute

    print(f"[米糕] UTC 时间: {utc_now.strftime('%Y-%m-%d %H:%M:%S')}")

    # 北京时间 = UTC + 8
    beijing_time = utc_now.astimezone(BEIJING_TZ)
    print(f"[米糕] 北京时间: {beijing_time.strftime('%Y-%m-%d %H:%M:%S')}")

    # 判断是哪种打卡
    # 早安: UTC 02:00 (北京 10:00)
    # 傍晚: UTC 10:10 (北京 18:10)

    if utc_hour == 2 and utc_minute == 0:
        print("[米糕] 早安打卡时间到！")
        result = send_morning_greeting()
        print(f"[米糕] 早安打卡已发送: {result}")
    elif utc_hour == 10 and utc_minute == 10:
        print("[米糕] 傍晚打卡时间到！")
        result = send_evening_greeting()
        print(f"[米糕] 傍晚打卡已发送: {result}")
    else:
        # 非 scheduled 时间，发送测试消息
        print("[米糕] 发送测试消息...")
        result = send_test_message()
        print(f"[米糕] 测试消息已发送: {result}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "test":
        print("[米糕] 发送测试消息...")
        result = send_test_message()
        print(f"[米糕] 测试消息已发送: {result}")
    else:
        main()
