import os
import random
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

import requests


CITY = "杭州"
RECIPIENT_NAME = "灯芯"
MESSAGE_TITLE = "灯芯今日出门指南"
BIRTHDAY_MESSAGE_TITLE = "🎂 生日特别来信"
CONCLUSION_ANIMALS = (
    "🐷",
    "🐶",
    "🐱",
    "🐰",
    "🐼",
    "🐸",
    "🦊",
    "🐻",
)
REMINDER_FACES = (
    "(●'◡'●)",
    "(｡•̀ᴗ-)✧",
    "(๑•̀ㅂ•́)و✧",
    "(ง •̀_•́)ง",
    "(｡･ω･｡)ﾉ♡",
    "(๑˃̵ᴗ˂̵)و",
    "(❁´◡`❁)",
    "( •̀ ω •́ )✧",
)

SOLAR_TERM_MESSAGES = {
    (1, 5): "今天是小寒哦，天气寒冷，出门要注意保暖。",
    (1, 20): "今天是大寒哦，一年中最冷的时候到了，注意保暖。",
    (2, 4): "今天是立春哦，天气开始慢慢回暖，早晚温差仍要注意。",
    (2, 19): "今天是雨水哦，天气变化多，出门记得看好雨具。",
    (3, 5): "今天是惊蛰哦，春天的气息越来越明显啦。",
    (3, 20): "今天是春分哦，白天和夜晚开始变得一样长。",
    (4, 4): "今天是清明哦，天气转暖，出门注意踏青安全。",
    (4, 20): "今天是谷雨哦，春雨渐多，出门记得留意降雨。",
    (5, 5): "今天是立夏哦，天气开始变热，注意补水防晒。",
    (5, 21): "今天是小满哦，天气渐热，穿搭可以轻便一些。",
    (6, 5): "今天是芒种哦，天气闷热，出门注意防晒和补水。",
    (6, 21): "今天是夏至哦，白天最长，外出注意防晒降温。",
    (7, 7): "今天是小暑哦，天气开始炎热，记得防暑降温。",
    (7, 23): "今天是大暑哦，一年中最热的时候，注意防暑。",
    (8, 7): "今天是立秋哦，天气还可能炎热，早晚温差会慢慢变大。",
    (8, 23): "今天是处暑哦，暑气渐退，早晚出门可以留意温差。",
    (9, 7): "今天是白露哦，早晚开始转凉，记得适时添衣。",
    (9, 23): "今天是秋分哦，天气渐凉，早晚出门注意保暖。",
    (10, 8): "今天是寒露哦，天气明显转凉，出门记得添衣。",
    (10, 23): "今天是霜降哦，天气更冷了，注意保暖防寒。",
    (11, 7): "今天是立冬哦，冬天要来了。",
    (11, 22): "今天是小雪哦，天气渐冷，出门注意保暖和路滑。",
    (12, 7): "今天是大雪哦，天气寒冷，出门记得做好保暖。",
    (12, 21): "今天是冬至哦，白天变短，天气寒冷，注意保暖。",
}

HOLIDAY_MESSAGES = {
    (1, 1): "CC祝你元旦开心，新的一年顺顺利利！",
    (2, 14): "CC祝你情人节快乐，今天也要被温柔对待。",
    (3, 8): "CC祝你妇女节快乐，愿你每天都开心自在。",
    (5, 1): "CC祝你劳动节快乐，好好休息，玩得开心。",
    (6, 1): "CC祝你儿童节快乐，保持童心，天天开心。",
    (9, 10): "CC祝老师们节日快乐，也祝你今天心情舒畅。",
    (10, 1): "CC祝你国庆节快乐，假期平安开心。",
    (12, 25): "CC祝你圣诞快乐，愿今天有温暖和惊喜。",
}

FREEZING_CONCLUSIONS = (
    "CC得穿秋裤了，今天真的很冷，注意保暖",
    "你别把灯芯冻坏了，赶紧穿厚一点",
    "今天冷得不讲道理，灯芯要裹严实一点",
    "CC建议灯芯全副武装，别让冷风钻进来",
    "零度以下的天气太认真了，灯芯记得把自己捂暖",
    "今天出门先把灯芯包好，别让寒风占了便宜",
    "冷空气来势汹汹，灯芯要穿成一个暖呼呼的小团子",
    "今天不适合硬扛，灯芯请把厚衣服安排上",
    "外面冷到冒烟，灯芯要把帽子围巾都戴好",
    "CC申请把灯芯装进保温袋，出门一定要穿暖",
    "今天的风像开了冰冻模式，灯芯要穿厚实一点",
    "灯芯，外套拉链拉到顶，别给冷空气留门",
    "今天请把保暖放在第一位，灯芯不能着凉啦",
    "寒冷天气已上线，灯芯要带着暖意再出门",
    "CC提醒灯芯开启冬日防御，厚衣服穿起来",
)

BIRTHDAY_MONTH = 10
BIRTHDAY_DAY = 30
BIRTHDAY_PAGE_URL = "https://chench9527.github.io/-/"
LATITUDE = 30.2741
LONGITUDE = 120.1551
PUSHPLUS_URL = "https://www.pushplus.plus/send"
BEIJING_TIMEZONE = ZoneInfo("Asia/Shanghai")

WEATHER_NAMES = {
    0: "晴",
    1: "基本晴",
    2: "多云",
    3: "阴",
    45: "雾",
    48: "雾",
    51: "小毛毛雨",
    53: "毛毛雨",
    55: "大毛毛雨",
    56: "冻毛毛雨",
    57: "强冻毛毛雨",
    61: "小雨",
    63: "中雨",
    65: "大雨",
    66: "冻雨",
    67: "强冻雨",
    71: "小雪",
    73: "中雪",
    75: "大雪",
    77: "雪粒",
    80: "小阵雨",
    81: "阵雨",
    82: "强阵雨",
    85: "小阵雪",
    86: "强阵雪",
    95: "雷雨",
    96: "雷雨夹冰雹",
    99: "强雷雨夹冰雹",
}

WEATHER_ICONS = {
    0: "☀️",
    1: "🌤️",
    2: "⛅",
    3: "☁️",
    45: "🌫️",
    48: "🌫️",
    51: "🌦️",
    53: "🌦️",
    55: "🌧️",
    56: "🌧️",
    57: "🌧️",
    61: "🌧️",
    63: "🌧️",
    65: "🌧️",
    66: "🌧️",
    67: "🌧️",
    71: "❄️",
    73: "❄️",
    75: "❄️",
    77: "🌨️",
    80: "🌦️",
    81: "🌦️",
    82: "🌧️",
    85: "🌨️",
    86: "🌨️",
    95: "⛈️",
    96: "⛈️",
    99: "⛈️",
}

STYLE_PROFILES = [
    {
        "name": "元气鼓励版",
        "tone": "energetic",
        "greeting": "早呀，灯芯！能量条已充满，先收下今天的天气情报。",
        "clothing_label": "元气穿搭",
        "conclusion_label": "今日元气出发站",
        "travel_label": "出发加油站",
        "closing": "带好装备，抬头挺胸，灯芯今天也会闪闪发光！",
    },
    {
        "name": "古风小笺",
        "tone": "ancient",
        "greeting": "灯芯安好，今朝杭州天色已为你探得。",
        "clothing_label": "添衣小笺",
        "conclusion_label": "今日出行小笺",
        "travel_label": "出行叮咛",
        "closing": "愿灯芯行路从容，所遇皆安，今日亦有好景相伴。",
    },
    {
        "name": "二次元播报风",
        "tone": "anime",
        "greeting": "早安，灯芯！今日天气副本加载完毕。",
        "clothing_label": "装备栏",
        "conclusion_label": "今日出行任务",
        "travel_label": "出行任务",
        "closing": "天气副本已解锁，灯芯带上好心情出发吧！",
    },
    {
        "name": "温柔陪伴版",
        "tone": "default",
        "greeting": "早上好，灯芯。慢慢醒来，先看看今天的天气。",
        "clothing_label": "穿衣小纸条",
        "conclusion_label": "今天出门小提醒",
        "travel_label": "出门小叮嘱",
        "closing": "不用着急，照顾好自己，再慢慢走进今天。",
    },
    {
        "name": "俏皮日常版",
        "tone": "default",
        "greeting": "灯芯灯芯，今天的天空又有新剧情啦。",
        "clothing_label": "穿搭小机灵",
        "conclusion_label": "今天出门别大意",
        "travel_label": "出门别大意",
        "closing": "天气负责变化，灯芯负责开心，分工明确！",
    },
    {
        "name": "晨间电台版",
        "tone": "default",
        "greeting": "早间频道准时开播，灯芯请收听今日天气。",
        "clothing_label": "今日穿搭",
        "conclusion_label": "今日出行播报",
        "travel_label": "通勤提示",
        "closing": "本次播报结束，愿灯芯拥有顺畅又明亮的一天。",
    },
    {
        "name": "天气侦察版",
        "tone": "default",
        "greeting": "报告灯芯，杭州天空状态已侦察完毕。",
        "clothing_label": "装备建议",
        "conclusion_label": "今日出门情报",
        "travel_label": "路况情报",
        "closing": "情报汇报完毕，灯芯可以安心执行今日计划。",
    },
    {
        "name": "贴心管家版",
        "tone": "default",
        "greeting": "早上好灯芯，天气管家来交今天的作业啦。",
        "clothing_label": "衣着安排",
        "conclusion_label": "今日出门安排",
        "travel_label": "出门清单",
        "closing": "该带的都提醒好啦，灯芯放心出门吧。",
    },
    {
        "name": "治愈松弛版",
        "tone": "default",
        "greeting": "早安，灯芯。先看看天空，再不慌不忙地开始一天。",
        "clothing_label": "舒服穿搭",
        "conclusion_label": "今天从容出门",
        "travel_label": "从容出门",
        "closing": "无论晴雨，都给自己留一点从容和好心情。",
    },
    {
        "name": "清爽简报版",
        "tone": "default",
        "greeting": "灯芯早，今日天气重点已经整理好了。",
        "clothing_label": "穿衣建议",
        "conclusion_label": "今日出行结论",
        "travel_label": "出行建议",
        "closing": "简报完毕，祝灯芯今日顺利。",
    },
    {
        "name": "冒险任务版",
        "tone": "anime",
        "greeting": "灯芯，今日地图已开启，天气任务请查收。",
        "clothing_label": "冒险装备",
        "conclusion_label": "今日行动指令",
        "travel_label": "行动提示",
        "closing": "装备确认完毕，灯芯向着今天的目标出发吧！",
    },
    {
        "name": "云朵来信版",
        "tone": "default",
        "greeting": "灯芯早呀，今天的云朵托我捎来一封天气信。",
        "clothing_label": "衣橱回信",
        "conclusion_label": "今日出门回信",
        "travel_label": "路上叮咛",
        "closing": "信读完啦，愿灯芯今天遇见温柔的风和好心情。",
    },
    {
        "name": "皇上奏报版",
        "tone": "imperial",
        "greeting": "启禀灯芯陛下，杭州今日天象已探明，特来呈报。",
        "clothing_label": "更衣奏报",
        "conclusion_label": "今日出巡奏报",
        "travel_label": "出巡叮嘱",
        "closing": "奏报完毕，愿陛下今日出行安稳，诸事顺遂，龙颜常悦。",
    },
    {
        "name": "灯芯总裁大人版",
        "tone": "ceo",
        "greeting": "早上好，灯芯总裁大人。今日杭州天气简报已整理完毕。",
        "clothing_label": "今日着装方案",
        "conclusion_label": "今日出行决策",
        "travel_label": "行程风险提示",
        "closing": "汇报完毕。请灯芯总裁大人从容出发，今天依旧稳稳掌控全场。",
    },
    {
        "name": "灯芯大王版",
        "tone": "imperial",
        "greeting": "灯芯大王早安！杭州今日天气情报已快马加鞭送到。",
        "clothing_label": "大王穿搭谕旨",
        "conclusion_label": "今日出门圣谕",
        "travel_label": "大王出门军令",
        "closing": "天气小事已安排妥当，祝灯芯大王今日出门威风又顺利！",
    },
]

CLOTHING_ADVICE = {
    "default": {
        "very_hot": "短袖和轻薄衣物最合适。防晒衣、帽子也安排上。",
        "hot": "短袖或轻薄衣物就好，怕空调凉可带件薄外套。",
        "warm_cool": "白天穿薄长袖或短袖，早晚加件薄外套更稳妥。",
        "warm": "薄长袖或短袖都合适，轻便透气最舒服。",
        "cool": "长袖配薄外套刚刚好。早晚有点凉，别被温差偷偷拿捏。",
        "chilly": "卫衣或针织衫加外套，怕冷就再添一层。",
        "cold": "厚外套、毛衣和长裤该上场了，注意手脚保暖。",
        "very_cold": "羽绒服或厚棉服请到位，围巾手套也别落下。",
    },
    "energetic": {
        "very_hot": "轻薄短袖上阵，防晒装备拉满，清爽迎接今天！",
        "hot": "短袖轻装出发，空调房里备件薄外套就更稳啦。",
        "warm_cool": "短袖加薄外套，灵活切换，元气不掉线。",
        "warm": "轻便长袖或短袖都能打，舒服就是今日最佳搭配。",
        "cool": "长袖和薄外套组队出场，温差也拦不住好状态。",
        "chilly": "卫衣加外套，把暖意和元气一起穿上。",
        "cold": "厚外套、毛衣和长裤集合，暖暖出发更有能量。",
        "very_cold": "羽绒服、围巾、手套全员到齐，保暖战斗力拉满。",
    },
    "ancient": {
        "very_hot": "暑意正盛，宜着轻薄短衣，亦莫忘遮阳防晒。",
        "hot": "天气偏暖，宜着轻衫；若久居冷房，可备薄外衣。",
        "warm_cool": "昼暖晨凉，宜薄衫配外衣，随温增减。",
        "warm": "气候温和，薄衫轻衣皆宜，以舒适为上。",
        "cool": "晨夕微凉，宜着长袖薄褂，莫教温差扰身。",
        "chilly": "凉意渐浓，宜添卫衣或针织外衫，以护暖意。",
        "cold": "寒意在身，宜着厚衣长裤，手足亦需保暖。",
        "very_cold": "寒气甚重，厚棉羽衣、围巾手套皆不可少。",
    },
    "anime": {
        "very_hot": "高温关卡开启！装备轻薄短袖和防晒道具。",
        "hot": "轻装模式最合适，空调区域记得追加薄外套装备。",
        "warm_cool": "短袖加薄外套，昼夜温差切换时随时换装。",
        "warm": "轻便套装即可通关，舒适度优先加点。",
        "cool": "长袖与薄外套组队，成功抵御早晚温差攻击。",
        "chilly": "卫衣加外套是今日推荐装备，保暖属性别忘升级。",
        "cold": "厚外套和长裤请装备完毕，优先守住体温值。",
        "very_cold": "寒冷首领登场！羽绒服、围巾和手套全部装备。",
    },
    "imperial": {
        "very_hot": "今日暑气颇盛，请陛下着轻薄短衣，遮阳防晒亦不可少。",
        "hot": "天气偏暖，请陛下轻装即可；若入冷房，可备薄外衣。",
        "warm_cool": "昼暖晨凉，请陛下着薄衫，并备一件外衣随时添减。",
        "warm": "今日气候温和，请陛下着轻便衣衫，以舒适为宜。",
        "cool": "晨夕微凉，请陛下着长袖薄褂，谨防温差扰身。",
        "chilly": "凉意渐浓，请陛下添卫衣或针织外衫，莫要受寒。",
        "cold": "今日寒意明显，请陛下着厚衣长裤，并注意手足保暖。",
        "very_cold": "寒气甚重，请陛下披羽绒厚衣，围巾手套一并备齐。",
    },
    "ceo": {
        "very_hot": "建议选择轻薄短袖，防晒衣和遮阳装备列入今日必备清单。",
        "hot": "建议轻装出行；如需长时间待在空调房，请备一件薄外套。",
        "warm_cool": "建议短袖搭配薄外套，方便根据早晚温差灵活调整。",
        "warm": "轻便长袖或短袖均可，以舒适利落为今日着装重点。",
        "cool": "建议长袖搭配薄外套，兼顾体面与早晚保暖需求。",
        "chilly": "建议卫衣或针织衫搭配外套，避免低温影响今日状态。",
        "cold": "建议厚外套、毛衣和长裤，手足保暖也请纳入安排。",
        "very_cold": "建议羽绒服或厚棉服，并配齐围巾手套，保暖优先。",
    },
}

TRAVEL_ADVICE = {
    "default": {
        "thunder": "有雷雨风险，少在户外停留，避开空旷处和大树。",
        "snow": "可能有雪，路面湿滑，走慢些，驾车保持距离。",
        "rain": "雨伞务必带上，鞋子尽量选防滑耐湿的。",
        "rain_time": "通勤多留一点时间，别和雨点比赛。",
        "maybe_rain": "雨点有点跃跃欲试，包里塞把折叠伞。",
        "dry": "降雨打扰不大，按平常节奏出门就好。",
        "fog": "能见度偏低，过马路和驾车都多观察。",
        "strong_wind": "风较强，少骑车，留意高空坠物。",
        "wind": "风有点活泼，帽子拿稳，骑行注意侧风。",
        "uv": "紫外线偏强，记得防晒。",
    },
    "energetic": {
        "thunder": "雷雨关卡有点难，减少户外停留，安全值优先！",
        "snow": "雪天路滑，放慢脚步、拉开车距，稳稳通关。",
        "rain": "雨伞和防滑鞋就位，雨天也能元气出发。",
        "rain_time": "通勤多留一点时间，从容才是满分状态。",
        "maybe_rain": "带把折叠伞当后援，天气变化也不慌。",
        "dry": "降雨影响不大，放心开启今天的行程。",
        "fog": "雾气影响视线，放慢速度，多看一眼更安全。",
        "strong_wind": "大风能量偏高，少骑车并留意高空物品。",
        "wind": "风有点活泼，拿稳随身物品再出发。",
        "uv": "紫外线偏强，防晒装备记得上线。",
    },
    "ancient": {
        "thunder": "雷雨将至，宜少行户外，远离旷野与高木。",
        "snow": "或有飞雪，道路湿滑，行步驾车皆宜从缓。",
        "rain": "雨具当随身，鞋履宜防滑耐湿。",
        "rain_time": "路途可多留片刻，莫与风雨争急。",
        "maybe_rain": "云有雨意，随身备一柄折伞为妥。",
        "dry": "雨意不浓，照常出行即可。",
        "fog": "雾气朦胧，行路驾车须多加留神。",
        "strong_wind": "风势颇劲，宜少骑行，亦防高处落物。",
        "wind": "风意稍盛，随身物件需拿稳。",
        "uv": "日光稍烈，出门宜作防晒。",
    },
    "anime": {
        "thunder": "雷雨事件触发！减少户外行动，远离空旷区域。",
        "snow": "冰雪地图已开启，降低移动速度并保持安全距离。",
        "rain": "雨伞和防滑鞋请加入装备栏。",
        "rain_time": "为通勤任务预留时间，别和雨点正面对线。",
        "maybe_rain": "随机降雨事件可能触发，折叠伞请放入背包。",
        "dry": "降雨概率较低，今日出行任务可正常推进。",
        "fog": "视野范围下降，移动和驾驶时请提高警戒。",
        "strong_wind": "强风警报！减少骑行并注意高空物品。",
        "wind": "风力增益生效，帽子和轻便物品记得锁定。",
        "uv": "紫外线伤害偏高，请装备防晒道具。",
    },
    "imperial": {
        "thunder": "今日或有雷雨，请陛下减少户外停留，远离旷野高木。",
        "snow": "或有飞雪，道路湿滑，请陛下缓步慢行，车驾保持距离。",
        "rain": "今日有雨，请陛下携伞，鞋履宜防滑耐湿。",
        "rain_time": "出巡路上可多留片刻，莫与风雨争急。",
        "maybe_rain": "云有雨意，请陛下随身备一柄折伞。",
        "dry": "今日雨意不浓，陛下可照常出巡。",
        "fog": "雾气朦胧，请陛下行路驾车时多加留神。",
        "strong_wind": "风势颇劲，请陛下少骑行，并提防高处落物。",
        "wind": "今日风意稍盛，请陛下拿稳帽子与随身物件。",
        "uv": "日光稍烈，请陛下出门时做好防晒。",
    },
    "ceo": {
        "thunder": "雷雨风险较高，建议压缩户外行程，避开空旷处和高大树木。",
        "snow": "可能出现降雪和湿滑路面，请放慢行程并保持安全车距。",
        "rain": "今日有雨，请将雨伞和防滑鞋列入出行清单。",
        "rain_time": "建议为通勤预留额外时间，避免天气打乱行程节奏。",
        "maybe_rain": "存在降雨可能，建议随身携带折叠伞作为备用方案。",
        "dry": "降雨影响较低，今日行程可按原计划推进。",
        "fog": "能见度偏低，步行和驾车时请提高观察频率。",
        "strong_wind": "风力较强，建议减少骑行，并留意高空坠物风险。",
        "wind": "风力略高，请拿稳随身物品，骑行时注意侧风。",
        "uv": "紫外线偏强，请把防晒纳入出门前的必要步骤。",
    },
}


def get_beijing_today() -> str:
    return datetime.now(BEIJING_TIMEZONE).date().isoformat()


def get_beijing_now() -> datetime:
    return datetime.now(BEIJING_TIMEZONE)


def get_birthday_page_url() -> str:
    return BIRTHDAY_PAGE_URL


def is_birthday_moment(now: datetime) -> bool:
    return (
        now.month == BIRTHDAY_MONTH
        and now.day == BIRTHDAY_DAY
        and now.hour == 23
        and now.minute >= 20
    )


def build_birthday_message() -> str:
    page_url = get_birthday_page_url()
    return "\n".join(
        [
            "**生日特别来信**",
            "",
            "灯芯，生日快乐！",
            "一份特别任务已经准备完成，请在今天零点接取。",
            "",
            "任务名称：生日祝福行动",
            "任务状态：等待接取",
            "",
            f"[点击接取任务，打开生日祝福网页]({page_url})",
            "",
            "祝你新的一岁，平安顺利，天天开心。",
        ]
    )


def get_weather() -> dict:
    forecast_date = get_beijing_today()
    previous_date = (
        date.fromisoformat(forecast_date) - timedelta(days=1)
    ).isoformat()
    response = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": LATITUDE,
            "longitude": LONGITUDE,
            "daily": ",".join(
                [
                    "weather_code",
                    "temperature_2m_max",
                    "temperature_2m_min",
                    "precipitation_probability_max",
                    "precipitation_sum",
                    "wind_speed_10m_max",
                    "uv_index_max",
                    "sunrise",
                    "sunset",
                ]
            ),
            "hourly": "precipitation_probability,rain,weather_code",
            "start_date": previous_date,
            "end_date": forecast_date,
            "temperature_unit": "celsius",
            "wind_speed_unit": "kmh",
            "timezone": "Asia/Shanghai",
        },
        timeout=20,
    )
    response.raise_for_status()
    payload = response.json()
    daily = payload["daily"]
    if not daily.get("time") or daily["time"][-1] != forecast_date:
        raise RuntimeError(
            f"天气日期不匹配：请求 {forecast_date}，返回 {daily.get('time')}"
        )
    today_index = daily["time"].index(forecast_date)
    previous_index = today_index - 1
    today = {
        key: [values[today_index]]
        for key, values in daily.items()
    }
    if previous_index >= 0:
        today["previous_temperature_2m_max"] = [
            daily["temperature_2m_max"][previous_index]
        ]
        today["previous_temperature_2m_min"] = [
            daily["temperature_2m_min"][previous_index]
        ]
    hourly = payload.get("hourly", {})
    today["rain_periods"] = [
        build_rain_periods(
            hourly.get("time", []),
            hourly.get("precipitation_probability", []),
            hourly.get("rain", []),
            hourly.get("weather_code", []),
            forecast_date,
        )
    ]
    return today


def build_clothing_advice(
    min_temp: float, max_temp: float, tone: str = "default"
) -> str:
    if max_temp >= 35:
        category = "very_hot"
    elif max_temp >= 28:
        category = "hot"
    elif max_temp >= 23 and min_temp < 18:
        category = "warm_cool"
    elif max_temp >= 23:
        category = "warm"
    elif max_temp >= 16:
        category = "cool"
    elif max_temp >= 10:
        category = "chilly"
    elif max_temp >= 5:
        category = "cold"
    else:
        category = "very_cold"

    advice = CLOTHING_ADVICE.get(tone, CLOTHING_ADVICE["default"])
    return advice[category]


def build_rain_periods(
    times: list[str],
    probabilities: list[float],
    rain_amounts: list[float],
    weather_codes: list[int],
    forecast_date: str,
) -> str:
    rain_codes = {51, 53, 55, 56, 57, 61, 63, 65, 66, 67, 80, 81, 82}
    periods = []
    current = []

    def append_period() -> None:
        if not current:
            return
        start_time = current[0][0][11:16]
        last_hour = int(current[-1][0][11:13])
        end_time = f"{last_hour + 1:02d}:00"
        max_probability = max(item[1] for item in current)
        periods.append(
            f"{start_time}~{end_time}（最高概率{max_probability:.0f}%）"
        )

    for index, time_text in enumerate(times):
        if not time_text.startswith(forecast_date):
            continue
        probability = probabilities[index] or 0
        rain_amount = rain_amounts[index] or 0
        weather_code = weather_codes[index]
        likely_rain = (
            probability >= 60
            or rain_amount > 0
            or weather_code in rain_codes
        )
        if likely_rain:
            current.append((time_text, probability))
        else:
            append_period()
            current.clear()
    append_period()

    return "、".join(periods) if periods else "暂无明显降雨时段"


def build_travel_advice(
    weather_code: int,
    precipitation_probability: float,
    wind_speed: float,
    uv_index: float,
    tone: str = "default",
) -> list[str]:
    advice = []
    copy = TRAVEL_ADVICE.get(tone, TRAVEL_ADVICE["default"])
    rain_codes = {51, 53, 55, 56, 57, 61, 63, 65, 66, 67, 80, 81, 82}
    snow_codes = {71, 73, 75, 77, 85, 86}
    thunder_codes = {95, 96, 99}

    if weather_code in thunder_codes:
        advice.append(copy["thunder"])
    elif weather_code in snow_codes:
        advice.append(copy["snow"])
    elif weather_code in rain_codes or precipitation_probability >= 70:
        advice.append(copy["rain"])
        advice.append(copy["rain_time"])
    elif precipitation_probability >= 40:
        advice.append(copy["maybe_rain"])
    else:
        advice.append(copy["dry"])

    if weather_code in {45, 48}:
        advice.append(copy["fog"])
    if wind_speed >= 35:
        advice.append(copy["strong_wind"])
    elif wind_speed >= 25:
        advice.append(copy["wind"])
    if uv_index >= 6:
        advice.append(copy["uv"])

    return advice


def build_outing_conclusion(
    weather_code: int,
    precipitation_probability: float,
    min_temp: float,
    max_temp: float,
    daily_min_temp: float,
    daily_max_temp: float,
    previous_min_temp=None,
    previous_max_temp=None,
) -> list[str]:
    rain_codes = {51, 53, 55, 56, 57, 61, 63, 65, 66, 67, 80, 81, 82}
    snow_codes = {71, 73, 75, 77, 85, 86}
    thunder_codes = {95, 96, 99}

    if max_temp <= 5:
        conclusion = random.choice(FREEZING_CONCLUSIONS)
    elif max_temp < 16 or min_temp < 8:
        conclusion = "今天偏冷，建议多穿一层"
    elif max_temp < 22 or min_temp < 14:
        conclusion = "今天有点凉，建议长袖搭配薄外套"
    elif max_temp >= 32:
        conclusion = "今天很热，建议穿轻薄透气的衣服"
    elif max_temp >= 28:
        conclusion = "今天有点热，建议选择轻薄穿搭"
    else:
        conclusion = "今天温度适中，按舒适穿搭出门即可"

    reminders = []
    if weather_code in thunder_codes or weather_code in rain_codes:
        reminders.append("今天有雨，记得带伞")
    elif precipitation_probability >= 70:
        reminders.append("今天降雨概率较高，记得带伞")
    if weather_code in snow_codes:
        reminders.append("可能有雪，注意路面湿滑")

    drops = []
    if previous_max_temp is not None:
        drops.append(previous_max_temp - daily_max_temp)
    if previous_min_temp is not None:
        drops.append(previous_min_temp - daily_min_temp)
    temperature_drop = max(drops, default=0)
    if temperature_drop >= 2:
        reminders.append(
            f"今天比昨天降温约 {temperature_drop:.1f}°C，CC特别提醒你注意保暖"
        )

    return [conclusion, *reminders]


def build_temperature_hint(min_temp: float, max_temp: float) -> str:
    if max_temp >= 28:
        return f"今日最高温度：{max_temp}°C"
    return ""


def build_wind_hint(wind_speed: float) -> str:
    wind_levels = (
        (118, 12),
        (103, 11),
        (89, 10),
        (75, 9),
        (62, 8),
        (50, 7),
        (39, 6),
    )
    for minimum_speed, wind_level in wind_levels:
        if wind_speed >= minimum_speed:
            return (
                f"风力达到{wind_level}级，出门注意防风，少骑车并留意高空坠物。"
            )
    return ""


def build_special_day_notes(date_text: str) -> list[str]:
    current_date = date.fromisoformat(date_text)
    key = (current_date.month, current_date.day)
    notes = []
    solar_term_message = SOLAR_TERM_MESSAGES.get(key)
    holiday_message = HOLIDAY_MESSAGES.get(key)
    if solar_term_message:
        notes.append(solar_term_message)
    if holiday_message:
        notes.append(holiday_message)
    return notes


def get_daily_style(date_text: str) -> dict[str, str]:
    run_number = os.environ.get("GITHUB_RUN_NUMBER")
    run_attempt = os.environ.get("GITHUB_RUN_ATTEMPT", "1")

    if run_number and run_number.isdigit() and run_attempt.isdigit():
        style_index = (int(run_number) - 1 + int(run_attempt) - 1) % len(
            STYLE_PROFILES
        )
    else:
        style_index = date.fromisoformat(date_text).toordinal() % len(STYLE_PROFILES)

    return STYLE_PROFILES[style_index]


def build_message_title(weather_code: int) -> str:
    icon = WEATHER_ICONS.get(weather_code, "🌤️")
    return f"{icon} {MESSAGE_TITLE}"


def build_message(daily: dict) -> str:
    values = {key: daily[key][0] for key in daily}
    message_title = build_message_title(values["weather_code"])
    weather_name = WEATHER_NAMES.get(values["weather_code"], "未知天气")
    sunrise = values["sunrise"].split("T", 1)[-1]
    sunset = values["sunset"].split("T", 1)[-1]
    display_date = date.fromisoformat(values["time"]).strftime("%m月%d日")
    style = get_daily_style(values["time"])
    daily_min_temperature = values["temperature_2m_min"]
    clothing_advice = build_clothing_advice(
        daily_min_temperature,
        daily_min_temperature,
        style["tone"],
    )
    travel_advice = build_travel_advice(
        values["weather_code"],
        values["precipitation_probability_max"],
        values["wind_speed_10m_max"],
        values["uv_index_max"],
        style["tone"],
    )
    outing_conclusion = build_outing_conclusion(
        values["weather_code"],
        values["precipitation_probability_max"],
        daily_min_temperature,
        daily_min_temperature,
        values["temperature_2m_min"],
        values["temperature_2m_max"],
        values.get("previous_temperature_2m_min"),
        values.get("previous_temperature_2m_max"),
    )
    if outing_conclusion:
        outing_conclusion[0] = (
            f"{outing_conclusion[0]}。{clothing_advice}"
        )
    temperature_hint = build_temperature_hint(
        values["temperature_2m_min"],
        values["temperature_2m_max"],
    )
    wind_hint = build_wind_hint(values["wind_speed_10m_max"])
    special_day_notes = build_special_day_notes(values["time"])
    key_reminder = (
        travel_advice[0]
        if travel_advice
        else "留意天气变化，按需调整出行安排。"
    )
    title_face = random.choice(REMINDER_FACES)
    conclusion_animal = random.choice(CONCLUSION_ANIMALS)
    conclusion_lines = [f"• {item}" for item in outing_conclusion]
    if conclusion_lines:
        conclusion_lines[-1] += f"{conclusion_animal}。"

    return "  \n".join(
        [
            f"**{message_title} {title_face}** 📅 {display_date}",
            "",
            style["greeting"],
            *special_day_notes,
            "",
            (
                f"今天温度：{values['temperature_2m_min']}°C ~ "
                f"{values['temperature_2m_max']}°C · {weather_name}"
            ),
            f"今日最低温度：{values['temperature_2m_min']}°C",
            *([temperature_hint] if temperature_hint else []),
            *([wind_hint] if wind_hint else []),
            "",
            f"{style['conclusion_label']}：",
            *conclusion_lines,
            "",
            f"**{CITY}**",
            (
                f"体感参考：{values['temperature_2m_min']}°C ~ "
                f"{values['temperature_2m_max']}°C"
            ),
            f"降雨概率：{values['precipitation_probability_max']}%",
            f"降雨时段：{values['rain_periods']}",
            f"降水量：{values['precipitation_sum']} mm",
            f"风速：{values['wind_speed_10m_max']} km/h",
            f"紫外线：{values['uv_index_max']}",
            "",
            f"🚗 **{style['travel_label']}**",
            *[f"• {item}" for item in travel_advice],
            "",
            f"🌅 日出 {sunrise} ｜ 日落 {sunset}",
            "",
            f"今日提醒：{key_reminder}",
            "",
            style["closing"],
        ]
    )


def send_to_wechat(content: str, title: str = MESSAGE_TITLE) -> None:
    token = os.environ.get("PUSHPLUS_TOKEN")
    topic = os.environ.get("PUSHPLUS_TOPIC")
    if not token:
        raise RuntimeError("缺少环境变量 PUSHPLUS_TOKEN")

    payload = {
        "token": token,
        "title": title,
        "content": content,
        "template": "markdown",
    }
    if topic:
        payload["topic"] = topic

    response = requests.post(
        PUSHPLUS_URL,
        json=payload,
        timeout=20,
    )
    response.raise_for_status()
    result = response.json()
    if result.get("code") != 200:
        raise RuntimeError(f"PushPlus 推送失败：{result}")


if __name__ == "__main__":
    now = get_beijing_now()
    message_kind = os.environ.get("MESSAGE_KIND", "auto")

    if message_kind == "birthday" or (
        message_kind == "auto" and is_birthday_moment(now)
    ):
        message = build_birthday_message()
        send_to_wechat(message, BIRTHDAY_MESSAGE_TITLE)
        print(message)
        print("生日特别来信已提交到 PushPlus。")
    elif message_kind == "weather" or (
        message_kind == "auto" and now.hour == 6 and now.minute >= 10
    ):
        daily = get_weather()
        message = build_message(daily)
        send_to_wechat(message, build_message_title(daily["weather_code"][0]))
        print(message)
        print("天气提醒已提交到 PushPlus。")
    else:
        print(
            f"北京时间 {now:%Y-%m-%d %H:%M} 无需发送消息；"
            "如需手动测试，请设置 MESSAGE_KIND=weather 或 birthday。"
        )
