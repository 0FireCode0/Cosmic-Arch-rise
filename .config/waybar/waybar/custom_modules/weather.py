#!/usr/bin/env python3
import json
import requests
from datetime import datetime

# Константы
WEATHER_URL = "https://wttr.in/vologda?format=j1"
LANG = "ru"  # Язык для погодных данных

# Соответствие кодов погоды иконкам (можно расширить по need)
WEATHER_CODES = {
    '113': ' ',  # Sunny
    '116': '󰖕 ',  # Partly cloudy
    '119': '󰖐 ',  # Cloudy
    '122': '󰖐 ',  # Overcast
    '143': '󰖑 ',  # Fog
    '176': '󰼳 ',  # Light rain showers
    '179': '󰼳 ',  # Light sleet showers
    '182': '󰼳 ',  # Light sleet
    '185': '󰼳 ',  # Light sleet
    '200': ' ',  # Thundery showers
    '227': '󰖘 ',  # Light snow
    '230': '󰼶 ',  # Heavy snow
    '248': '󰖑 ',  # Fog
    '260': '󰖑 ',  # Fog
    '263': '󰼳 ',  # Light rain showers
    '266': '󰼳 ',  # Light rain
    '281': '󰼵 ',  # Light sleet
    '284': '󰼵 ',  # Light sleet
    '293': '󰼳 ',  # Light rain
    '296': '󰼳 ',  # Light rain
    '299': ' ',  # Heavy rain showers
    '302': ' ',  # Heavy rain
    '305': ' ',  # Heavy rain showers
    '308': ' ',  # Heavy rain
    '311': '󰼵 ',  # Light sleet
    '314': '󰼵 ',  # Light sleet
    '317': '󰼵 ',  # Light sleet
    '320': '󰼴 ',  # Light snow showers
    '323': '󰼴 ',  # Light snow showers
    '326': '󰼴 ',  # Light snow showers
    '329': '󰼶 ',  # Heavy snow
    '332': '󰼶 ',  # Heavy snow
    '335': '󰼶 ',  # Heavy snow showers
    '338': '󰼶 ',  # Heavy snow
    '350': '󰼵 ',  # Light sleet
    '353': '󰼳 ',  # Light rain showers
    '356': ' ',  # Heavy rain showers
    '359': ' ',  # Heavy rain
    '362': '󰼵 ',  # Light sleet showers
    '365': '󰼵 ',  # Light sleet showers
    '368': '󰼴 ',  # Light snow showers
    '371': '󰼶 ',  # Heavy snow showers
    '374': '󰼵 ',  # Light sleet showers
    '377': '󰼵 ',  # Light sleet
    '386': ' ',  # Thundery showers
    '389': ' ',  # Thundery heavy rain
    '392': ' ',  # Thundery snow showers
    '395': '󰼶 '   # Heavy snow showers
}

def get_weather_data():
    try:
        # Запрос данных с учетом языка
        response = requests.get(f"{WEATHER_URL}&lang={LANG}")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Ошибка запроса: {e}")
        return None

def format_time(time_str):
    """Форматирование времени в читаемый вид."""
    return time_str.replace("00", "").zfill(2)

def format_chances(hour):
    """Форматирование вероятностей осадков."""
    chances = {
        "chanceoffog": "Туман",
        "chanceoffrost": "Иней",
        "chanceofovercast": "Облачно",
        "chanceofrain": "Дождь",
        "chanceofsnow": "Снег",
        "chanceofsunshine": "Солнечно",
        "chanceofthunder": "Гроза",
        "chanceofwindy": "Ветрено"
    }
    conditions = []
    for event, desc in chances.items():
        if int(hour.get(event, 0)) > 0:
            conditions.append(f"{desc} {hour[event]}%")
    return ", ".join(conditions)

def main():
    weather_data = get_weather_data()
    if not weather_data:
        # Возвращаем ошибку в Waybar
        error_output = {
            "text": "❌ Ошибка",
            "tooltip": "Не удалось получить данные о погоде"
        }
        print(json.dumps(error_output))
        return

    current_condition = weather_data['current_condition'][0]
    area = weather_data['nearest_area'][0]

    # Текущая погода для основного вывода
    weather_code = current_condition['weatherCode']
    icon = WEATHER_CODES.get(weather_code, '?')
    temp = current_condition['temp_C']
    feels_like = current_condition['FeelsLikeC']

    # Формируем текст для waybar
    data = {
        'text': f"{icon} {temp}°C",
        'tooltip': f"<b>Текущая погода в {area['areaName'][0]['value']}</b>\n"
                  f"Состояние: {current_condition['lang_ru'][0]['value']}\n"
                  f"Температура: {temp}°C (ощущается как {feels_like}°C)\n"
                  f"Влажность: {current_condition['humidity']}%\n"
                  f"Ветер: {current_condition['windspeedKmph']} км/ч\n"
                  f"Давление: {current_condition['pressure']} hPa\n\n"
                  f"<b>Прогноз на ближайшие 24 часа:</b>\n"
    }

    # Добавляем прогноз по часам на ближайшие 24 часа
    today = weather_data['weather'][0]
    for hour in today['hourly']:
        hour_time = format_time(hour['time'])
        # Пропускаем прошедшие часы
        if int(hour_time) < datetime.now().hour - 2:
            continue
        hour_icon = WEATHER_CODES.get(hour['weatherCode'], '?')
        hour_temp = hour['FeelsLikeC']
        hour_desc = hour['lang_ru'][0]['value']
        hour_chances = format_chances(hour)
        if int(hour_time) < 21:
            data['tooltip'] += f"{hour_time}:00 {hour_icon} {hour_temp}°C, {hour_desc}, {hour_chances}\n"
        else: data['tooltip'] += f"{hour_time}:00 {hour_icon} {hour_temp}°C, {hour_desc}, {hour_chances}"

    print(json.dumps(data))

if __name__ == "__main__":
    main()
