import os
from datetime import date

import requests


CITY = "杭州"
RECIPIENT_NAME = "灯芯"
MESSAGE_TITLE = f"{RECIPIENT_NAME}专属天气提醒"
LATITUDE = 30.2741
LONGITUDE = 120.1551
PUSHPLUS_URL = "https://www.pushplus.plus/send"

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

GREETINGS = [
    "早呀，灯芯！天气小秘书准时来敲门啦。",
    "灯芯早上好，今天的天气情报新鲜送达。",
    "叮咚，灯芯请查收今日份杭州天气。",
    "灯芯，起床先别急着冲出门，天气有话要说。",
    "早安，灯芯！今天出门穿什么，我帮你参谋好了。",
    "灯芯早呀，窗外的天气已经被我打探清楚啦。",
    "今日天气播报员上线：灯芯，请接收专属提醒。",
    "灯芯，新的一天开场啦，先看看天气怎么安排。",
    "早上好，灯芯！天气这点小心思，已经被我看穿啦。",
]

CLOSINGS = [
    "装备带齐再出发，愿灯芯今天一路顺顺当当。",
    "天气负责变化，灯芯负责开心，今天也要元气满满。",
    "照顾好自己再去忙，灯芯今天也会是状态很好的一天。",
    "出门记得检查钥匙、手机和天气装备，少一样都不行哦。",
    "今天的天气功课交完啦，灯芯放心出门吧。",
    "把提醒装进口袋，灯芯今天也要舒舒服服地过。",
    "愿天气配合，路途顺利，灯芯收获一个好心情。",
    "该带的带上，该防的防好，剩下的就交给好心情吧。",
    "天气提醒已送达，灯芯今天也要稳稳拿捏每一程。",
    "无论晴雨，记得给自己留一点从容，灯芯加油呀。",
    "今天也请好好吃饭、慢慢赶路，平安到达最重要。",
]

HEADLINES = [
    "灯芯灯芯，今日杭州天气播报来咯~",
    "灯芯请注意，今天的杭州天气情报到啦~",
    "灯芯专属早间天气站，现在开始播报~",
    "灯芯快看，杭州今天的天气安排好啦~",
    "灯芯的今日天气小纸条，请查收~",
    "灯芯早呀，杭州天气小喇叭开播啦~",
    "灯芯灯芯，新鲜出炉的天气提醒送到~",
]


def get_weather() -> dict:
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
            "forecast_days": 1,
            "temperature_unit": "celsius",
            "wind_speed_unit": "kmh",
            "timezone": "Asia/Shanghai",
        },
        timeout=20,
    )
    response.raise_for_status()
    return response.json()["daily"]


def build_clothing_advice(min_temp: float, max_temp: float) -> str:
    if max_temp >= 35:
        return "天气很热，短袖和轻薄透气的衣服最合适；防晒衣、帽子也安排上，别让太阳占便宜。"
    if max_temp >= 28:
        return "短袖或轻薄衣物就很舒服，室内空调偏凉的话，可以随手带件薄外套。"
    if max_temp >= 23:
        if min_temp < 18:
            return "白天可以穿薄长袖或短袖，早晚有点凉，带件薄外套更稳妥。"
        return "薄长袖或短袖都合适，选轻便透气的搭配，走动起来更舒服。"
    if max_temp >= 16:
        return "建议长袖配薄外套，早晚温差容易偷偷使坏，分层穿最方便。"
    if max_temp >= 10:
        return "卫衣、针织衫加外套比较合适，怕冷的话再添一层，别硬扛。"
    if max_temp >= 5:
        return "厚外套、毛衣和长裤该上场了，手脚容易冷的话记得注意保暖。"
    return "今天寒意认真营业，羽绒服或厚棉服请到位，围巾手套也别落下。"


def build_travel_advice(
    weather_code: int,
    precipitation_probability: float,
    wind_speed: float,
    uv_index: float,
) -> list[str]:
    advice = []
    rain_codes = {51, 53, 55, 56, 57, 61, 63, 65, 66, 67, 80, 81, 82}
    snow_codes = {71, 73, 75, 77, 85, 86}
    thunder_codes = {95, 96, 99}

    if weather_code in thunder_codes:
        advice.append("有雷雨风险，尽量减少长时间户外活动，避开空旷处和高大树木。")
    elif weather_code in snow_codes:
        advice.append("可能有雪，路面容易湿滑，走路放慢一点，驾车注意保持车距。")
    elif weather_code in rain_codes or precipitation_probability >= 70:
        advice.append("雨伞务必带上，鞋子尽量选防滑耐湿的，通勤给自己多留一点时间。")
    elif precipitation_probability >= 40:
        advice.append("降雨有点跃跃欲试，包里塞把折叠伞，免得回家时和雨点赛跑。")
    else:
        advice.append("降雨打扰的可能不大，按平常节奏出门就好。")

    if weather_code in {45, 48}:
        advice.append("能见度可能偏低，过马路和驾车都要多观察，别赶得太急。")
    if wind_speed >= 35:
        advice.append("风比较强，少骑车、远离临时搭建物，也要留意高空坠物。")
    elif wind_speed >= 25:
        advice.append("风有点活泼，帽子和轻便物品要拿稳，骑行注意侧风。")
    if uv_index >= 6:
        advice.append("紫外线偏强，防晒霜、遮阳帽或太阳伞选一样带上。")

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


def get_daily_style(date_text: str) -> tuple[str, str, str]:
    day_number = date.fromisoformat(date_text).toordinal()
    headline = HEADLINES[(day_number * 3) % len(HEADLINES)]
    greeting = GREETINGS[day_number % len(GREETINGS)]
    closing = CLOSINGS[(day_number * 5) % len(CLOSINGS)]
    return headline, greeting, closing


def build_message(daily: dict) -> str:
    values = {key: daily[key][0] for key in daily}
    weather_name = WEATHER_NAMES.get(values["weather_code"], "未知天气")
    sunrise = values["sunrise"].split("T", 1)[-1]
    sunset = values["sunset"].split("T", 1)[-1]
    headline, greeting, closing = get_daily_style(values["time"])
    weather_icon = get_weather_icon(values["weather_code"])
    clothing_advice = build_clothing_advice(
        values["temperature_2m_min"], values["temperature_2m_max"]
    )
    travel_advice = build_travel_advice(
        values["weather_code"],
        values["precipitation_probability_max"],
        values["wind_speed_10m_max"],
        values["uv_index_max"],
    )

    return "\n".join(
        [
            f"## {weather_icon} {headline}",
            "",
            greeting,
            (
                f"{CITY}今天 **{weather_name}，"
                f"{values['temperature_2m_min']}°C ~ "
                f"{values['temperature_2m_max']}°C**。"
            ),
            (
                f"降雨概率 {values['precipitation_probability_max']}%，"
                f"最大风速 {values['wind_speed_10m_max']} km/h，"
                f"紫外线指数 {values['uv_index_max']}。"
            ),
            "",
            f"👕 **穿衣小纸条：** 灯芯，{clothing_advice}",
            "",
            f"🚗 **出门小叮嘱：** 灯芯，{' '.join(travel_advice)}",
            "",
            f"🌅 日出 {sunrise}，日落 {sunset}。预计降水量 {values['precipitation_sum']} mm。",
            "",
            closing,
        ]
    )


def send_to_wechat(content: str) -> None:
    token = os.environ.get("PUSHPLUS_TOKEN")
    if not token:
        raise RuntimeError("缺少环境变量 PUSHPLUS_TOKEN")

    response = requests.post(
        PUSHPLUS_URL,
        json={
            "token": token,
            "title": MESSAGE_TITLE,
            "content": content,
            "template": "markdown",
        },
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
