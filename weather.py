import os

import requests


CITY = "杭州"
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


def build_message(daily: dict) -> str:
    values = {key: daily[key][0] for key in daily}
    weather_name = WEATHER_NAMES.get(values["weather_code"], "未知天气")
    sunrise = values["sunrise"].split("T", 1)[-1]
    sunset = values["sunset"].split("T", 1)[-1]

    return "\n".join(
        [
            f"## {CITY}今日天气",
            "",
            f"- 日期：{values['time']}",
            f"- 天气：{weather_name}",
            f"- 气温：{values['temperature_2m_min']} ~ {values['temperature_2m_max']}°C",
            f"- 降水概率：{values['precipitation_probability_max']}%",
            f"- 预计降水量：{values['precipitation_sum']} mm",
            f"- 最大风速：{values['wind_speed_10m_max']} km/h",
            f"- 紫外线指数：{values['uv_index_max']}",
            f"- 日出 / 日落：{sunrise} / {sunset}",
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
            "title": f"{CITY}今日天气",
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
