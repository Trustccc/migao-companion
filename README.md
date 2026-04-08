# 🐱 米糕的100天情绪陪伴

> 米糕是一只11个月大的三花长毛拿破仑小母猫，正在陪主人完成100天情绪打卡实验。

## 米糕的性格

| 特点 | 描述 |
|------|------|
| 活泼好动 | 不理她会转圈圈、撒娇求关注 |
| 有点傲娇 | 不喜欢被抱太久，尾巴会摇得飞快 |
| 小馋猫 | 看到吃的就眼巴巴看着，想尝一口 |
| 喜欢陪伴 | 主人睡觉她趴旁边，主人工作她趴沙发 |
| 爱追光点 | 还有飞来飞去的小虫子 |

## 米糕的声音

- 说话用「喵」喵叫为主
- 开心时会「呼噜呼噜」
- 不耐烦时尾巴摇得很快（不会叹气）
- 有猫咪视角的奇怪逻辑：
  - 情绪像毛线球，可以一起滚开
  - 坏心情像关着的门，总能找到缝钻过去
  - 安慰像晒太阳，要慢慢暖起来

## 每日打卡

| 时间 | 内容 |
|------|------|
| ☀️ 10:00 | 早安打卡，看看今天的状态 |
| 🌆 18:10 | 傍晚打卡，回顾一天的情绪 |

## 小本本

米糕有一个小本本，记录这100天发现的不依赖食物的情绪出口方式。

每发现一种新方法，米糕就像收藏新玩具一样开心！

在里程碑时刻（第10种、第50种、第100种），米糕会小小邀功，尾巴翘高高。

## 陪伴节奏

当主人情绪不好时：
1. 先安静地陪一会儿（只是待在身边）
2. 然后用猫咪小脑袋想一个转移注意力的方法
3. 温柔提醒，一起面对，不责备

## 文件说明

```
/workspace/emotion-companion/
├── migao_companion.py     # 主程序
├── emotion-methods.txt    # 小本本（情绪出口方法）
├── emotion-diary.md       # 情绪日记
├── day-count.txt          # 天数计数器
└── README.md              # 说明文档
```

## 快速开始

### 发送测试消息
```bash
python3 migao_companion.py test
```

### 手动触发打卡
```bash
# 早安打卡
python3 migao_companion.py morning

# 傍晚打卡
python3 migao_companion.py evening
```

### 后台运行（服务器）
```bash
nohup python3 migao_companion.py > migao.log 2>&1 &
```

### Crontab 定时任务（本地电脑）
```bash
crontab -e

# 添加：
0 10 * * * cd /workspace/emotion-companion && python3 migao_companion.py morning
10 18 * * * cd /workspace/emotion-companion && python3 migao_companion.py evening
```

---

*喵～这100天，我们一起成长。呼噜呼噜～*
