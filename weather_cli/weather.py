import sys
import io
# 强制UTF-8编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import requests
from dotenv import load_dotenv
import os
from colorama import Fore, Style, init

# 初始化彩色终端
init(autoreset=True)
weather_icons = {
    "晴": "[晴]",
    "雨": "[雨]",
    "多云": "[云]",
    "雪": "[雪]"
}

# 加载环境变量
load_dotenv()
API_KEY = os.getenv("OWM_API_KEY") or "b900199c33bcfa88e2592cc8933ced90"  # 优先使用.env中的密钥

def get_weather_forecast(city, units='metric'):
    """获取5天天气预报数据"""
    base_url = "https://api.openweathermap.org/data/2.5/forecast"
    params = {
        "q": city,
        "appid": API_KEY,
        "units": units,
        "lang": "zh_cn",
        "cnt": 40  # 获取40条数据（5天）
    }
    
    try:
        response = requests.get(base_url, params=params, timeout=10)
        data = response.json()
        
        # 错误处理
        if data.get("cod") != "200":
            print(f"{Fore.RED}错误：{data.get('message', '未知错误')}")
            return None
            
        return data
    
    except Exception as e:
        print(f"{Fore.RED}请求失败：{e}")
        return None

def display_weather(data, units):
    """美化显示天气信息"""
    if not data:
        return
        
    city = data['city']['name']
    unit_symbol = "°C" if units == "metric" else "°F"
    
    print(f"\n{Fore.YELLOW}====== {city}天气预报 ======{Style.RESET_ALL}")
    
    # 按日期分组显示
    daily_data = {}
    for item in data['list']:
        date = item['dt_txt'].split()[0]  # 提取日期部分
        if date not in daily_data:
            daily_data[date] = []
        daily_data[date].append(item)
    
    # 显示每一天数据
    for date, items in daily_data.items():
        print(f"\n{Fore.CYAN}📅 {date}{Style.RESET_ALL}")
        for item in items[:3]:  # 每天显示3个时间点
            time = item['dt_txt'].split()[1][:5]
            weather = item['weather'][0]['description']
            temp = item['main']['temp']
            humidity = item['main']['humidity']
            
            # 根据天气类型设置颜色
            if '雨' in weather:
                weather_color = Fore.BLUE
            elif '晴' in weather:
                weather_color = Fore.YELLOW
            else:
                weather_color = Fore.WHITE
                
            print(f"⏰ {time} | {weather_color}{weather.ljust(6)} | "
                  f"🌡 {Fore.RED}{temp}{unit_symbol} | 💧 {humidity}%")

if __name__ == "__main__":
    print(f"{Fore.GREEN}=== 天气查询工具 ===")
    city = input("请输入城市名称（例如：北京）: ")
    unit = input("温度单位 (1)摄氏度 (2)华氏度: ").strip()
    
    # 获取并显示天气
    weather_data = get_weather_forecast(
        city,
        units="metric" if unit == "1" else "imperial"
    )
    
    if weather_data:
        display_weather(weather_data, "metric" if unit == "1" else "imperial")