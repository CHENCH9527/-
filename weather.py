import os
from datetime import date, datetime
from zoneinfo import ZoneInfo

import requests


CITY = "杭州"
RECIPIENT_NAME = "灯芯"
MESSAGE_TITLE = f"{RECIPIENT_NAME}专属天气提醒"
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

STYLE_PROFILES = [
    {
        "name": "元气鼓励版",
        "tone": "energetic",
        "headline": "灯芯元气天气站",
        "greeting": "早呀，灯芯！能量条已充满，先收下今天的天气情报。",
        "clothing_label": "元气穿搭",
        "travel_label": "出发加油站",
        "closing": "带好装备，抬头挺胸，灯芯今天也会闪闪发光！",
    },
    {
        "name": "古风小笺",
        "tone": "ancient",
        "headline": "灯芯晴雨小笺",
        "greeting": "灯芯安好，今朝杭州天色已为你探得。",
        "clothing_label": "添衣小笺",
        "travel_label": "出行叮咛",
        "closing": "愿灯芯行路从容，所遇皆安，今日亦有好景相伴。",
    },
    {
        "name": "二次元播报风",
        "tone": "anime",
        "headline": "灯芯天气作战部",
        "greeting": "早安，灯芯！今日天气副本加载完毕。",
        "clothing_label": "装备栏",
        "travel_label": "出行任务",
        "closing": "天气副本已解锁，灯芯带上好心情出发吧！",
    },
    {
        "name": "温柔陪伴版",
        "tone": "default",
        "headline": "灯芯温柔晨报",
        "greeting": "早上好，灯芯。慢慢醒来，先看看今天的天气。",
        "clothing_label": "穿衣小纸条",
        "travel_label": "出门小叮嘱",
        "closing": "不用着急，照顾好自己，再慢慢走进今天。",
    },
    {
        "name": "俏皮日常版",
        "tone": "default",
        "headline": "灯芯天气小剧场",
        "greeting": "灯芯灯芯，今天的天空又有新剧情啦。",
        "clothing_label": "穿搭小机灵",
        "travel_label": "出门别大意",
        "closing": "天气负责变化，灯芯负责开心，分工明确！",
    },
    {
        "name": "晨间电台版",
        "tone": "default",
        "headline": "灯芯晨间电台",
        "greeting": "早间频道准时开播，灯芯请收听今日天气。",
        "clothing_label": "今日穿搭",
        "travel_label": "通勤提示",
        "closing": "本次播报结束，愿灯芯拥有顺畅又明亮的一天。",
    },
    {
        "name": "天气侦察版",
        "tone": "default",
        "headline": "灯芯气象侦察局",
        "greeting": "报告灯芯，杭州天空状态已侦察完毕。",
        "clothing_label": "装备建议",
        "travel_label": "路况情报",
        "closing": "情报汇报完毕，灯芯可以安心执行今日计划。",
    },
    {
        "name": "贴心管家版",
        "tone": "default",
        "headline": "灯芯天气管家",
        "greeting": "早上好灯芯，天气管家来交今天的作业啦。",
        "clothing_label": "衣着安排",
        "travel_label": "出门清单",
        "closing": "该带的都提醒好啦，灯芯放心出门吧。",
    },
    {
        "name": "治愈松弛版",
        "tone": "default",
        "headline": "灯芯慢慢天气",
        "greeting": "早安，灯芯。先看看天空，再不慌不忙地开始一天。",
        "clothing_label": "舒服穿搭",
        "travel_label": "从容出门",
        "closing": "无论晴雨，都给自己留一点从容和好心情。",
    },
    {
        "name": "清爽简报版",
        "tone": "default",
        "headline": "灯芯天气简报",
        "greeting": "灯芯早，今日天气重点已经整理好了。",
        "clothing_label": "穿衣建议",
        "travel_label": "出行建议",
        "closing": "简报完毕，祝灯芯今日顺利。",
    },
    {
        "name": "冒险任务版",
        "tone": "anime",
        "headline": "灯芯今日冒险指南",
        "greeting": "灯芯，今日地图已开启，天气任务请查收。",
        "clothing_label": "冒险装备",
        "travel_label": "行动提示",
        "closing": "装备确认完毕，灯芯向着今天的目标出发吧！",
    },
    {
        "name": "云朵来信版",
        "tone": "default",
        "headline": "写给灯芯的天空来信",
        "greeting": "灯芯早呀，今天的云朵托我捎来一封天气信。",
        "clothing_label": "衣橱回信",
        "travel_label": "路上叮咛",
        "closing": "信读完啦，愿灯芯今天遇见温柔的风和好心情。",
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
}


def get_beijing_today() -> str:
    return datetime.now(BEIJING_TIMEZONE).date().isoformat()


def get_weather() -> dict:
    forecast_date = get_beijing_today()
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
            "start_date": forecast_date,
            "end_date": forecast_date,
            "temperature_unit": "celsius",
            "wind_speed_unit": "kmh",
            "timezone": "Asia/Shanghai",
        },
        timeout=20,
    )
    response.raise_for_status()
    daily = response.json()["daily"]
    if not daily.get("time") or daily["time"][0] != forecast_date:
        raise RuntimeError(
            f"天气日期不匹配：请求 {forecast_date}，返回 {daily.get('time')}"
        )
    return daily


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


def get_weather_icon(weather_code: int) -> str:
    if weather_code == 0:
        return "🌞"
    if weather_code in {1, 2}:
        return "⛅"
    if weather_code == 3:
        return "☁️"
    if weather_code in {45, 48}:
        return "🌫️"
    if weather_code in {71, 73, 75, 77, 85, 86}:
        return "❄️"
    if weather_code in {95, 96, 99}:
        return "⛈️"
    return "🌧️"


def get_daily_style(date_text: str) -> dict[str, str]:
    day_number = date.fromisoformat(date_text).toordinal()
    return STYLE_PROFILES[day_number % len(STYLE_PROFILES)]


def build_message(daily: dict) -> str:
    values = {key: daily[key][0] for key in daily}
    weather_name = WEATHER_NAMES.get(values["weather_code"], "未知天气")
    sunrise = values["sunrise"].split("T", 1)[-1]
    sunset = values["sunset"].split("T", 1)[-1]
    display_date = date.fromisoformat(values["time"]).strftime("%m月%d日")
    style = get_daily_style(values["time"])
    weather_icon = get_weather_icon(values["weather_code"])
    clothing_advice = build_clothing_advice(
        values["temperature_2m_min"],
        values["temperature_2m_max"],
        style["tone"],
    )
    travel_advice = build_travel_advice(
        values["weather_code"],
        values["precipitation_probability_max"],
        values["wind_speed_10m_max"],
        values["uv_index_max"],
        style["tone"],
    )

    return "\n".join(
        [
            f"**{weather_icon} {style['headline']}｜{display_date}**",
            "",
            style["greeting"],
            "",
            f"**{CITY} · {weather_name}**",
            (
                f"{values['temperature_2m_min']}°C ~ "
                f"{values['temperature_2m_max']}°C"
            ),
            (
                f"降雨 {values['precipitation_probability_max']}% ｜ "
                f"风速 {values['wind_speed_10m_max']} km/h"
            ),
            (
                f"紫外线 {values['uv_index_max']} ｜ "
                f"降水量 {values['precipitation_sum']} mm"
            ),
            "",
            f"👕 **{style['clothing_label']}**",
            clothing_advice,
            "",
            f"🚗 **{style['travel_label']}**",
            *[f"- {item}" for item in travel_advice],
            "",
            f"🌅 日出 {sunrise} ｜ 日落 {sunset}",
            "",
            style["closing"],
        ]
    )


def send_to_wechat(content: str) -> None:
    token = os.environ.get("PUSHPLUS_TOKEN")
    topic = os.environ.get("PUSHPLUS_TOPIC")
    if not token:
        raise RuntimeError("缺少环境变量 PUSHPLUS_TOKEN")

    payload = {
        "token": token,
        "title": MESSAGE_TITLE,
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
    message = build_message(get_weather())
    send_to_wechat(message)
    print(message)
    print("天气提醒已提交到 PushPlus。")
