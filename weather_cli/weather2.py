import requests

def get_weather(city):
    API_KEY = "b900199c33bcfa88e2592cc8933ced90"  # 替换成你刚才申请的密钥
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=zh_cn"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if data["cod"] != 200:
            print(f"错误：{data['message']}")
            return
        
        weather = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        
        print(f"\n{city}的天气：")
        print(f"- 天气状况: {weather}")
        print(f"- 温度: {temp}°C")
        print(f"- 湿度: {humidity}%")
    
    except Exception as e:
        print(f"发生错误: {e}")

if __name__ == "__main__":
    city = input("请输入城市名称（例如：北京）: ")
    get_weather(city)