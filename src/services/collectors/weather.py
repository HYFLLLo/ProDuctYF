"""
天气数据采集器
"""
import httpx
from datetime import datetime
from typing import Optional
from .base import BaseCollector


class WeatherCollector(BaseCollector):
    """天气数据采集器"""

    def __init__(self, api_config: dict):
        super().__init__("weather", api_config)

    async def collect(self, time_range: tuple[datetime, datetime]) -> list[dict]:
        """采集天气数据"""
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.get(
                    self.api_config.get("url", "https://api.weather.example.com"),
                    params={
                        "key": self.api_config.get("api_key", ""),
                        "location": self.api_config.get("location", "beijing")
                    }
                )
                data = response.json()
                return self._parse_weather_data(data)
            except Exception as e:
                print(f"Weather collector error: {e}")
                return []

    def _parse_weather_data(self, data: dict) -> list[dict]:
        """解析天气数据为事件列表"""
        events = []
        try:
            hourly_data = data.get("HeWeather", [{}])[0].get("hourly", [])
            for item in hourly_data:
                if self._is_night_hours(item.get("time", "")):
                    events.append({
                        "name": f"天气：{item.get('text', '未知')}",
                        "summary": f"温度{item.get('temp', '?')}度，{item.get('text', '未知')}，风力{item.get('windDir', '?')}",
                        "time": item.get("time", ""),
                        "location": self.api_config.get("location", ""),
                        "temperature": item.get("temp"),
                        "weather_text": item.get("text"),
                        "wind_dir": item.get("windDir")
                    })
        except Exception as e:
            print(f"Parse weather data error: {e}")
        return events


class MockWeatherCollector(BaseCollector):
    """模拟天气采集器（用于测试）"""

    def __init__(self, api_config: dict):
        super().__init__("weather", api_config)

    async def collect(self, time_range: tuple[datetime, datetime]) -> list[dict]:
        """返回基于当前季节的真实天气数据"""
        now = datetime.now()
        month = now.month
        current_hour = now.hour
        
        # 根据季节生成天气
        weather_data = self._generate_seasonal_weather(month, current_hour)
        
        return weather_data

    def _generate_seasonal_weather(self, month: int, hour: int) -> list:
        """根据季节和时间生成天气"""
        import random
        
        # 春季天气（3-5月）
        spring_weather = [
            {
                "name": "天气：晴",
                "summary": "温度18-24度，晴，东南风2-3级，适合出行",
                "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "location": "成都"
            },
            {
                "name": "天气：多云转晴",
                "summary": "温度16-22度，多云转晴，微风，春意盎然",
                "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "location": "成都"
            },
        ]
        
        # 夏季天气（6-8月）
        summer_weather = [
            {
                "name": "天气：高温预警",
                "summary": "温度35-38度，晴，紫外线强，注意防暑降温",
                "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "location": "成都"
            },
            {
                "name": "天气：雷阵雨",
                "summary": "温度28-32度，雷阵雨，局地伴有短时强降水",
                "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "location": "成都"
            },
        ]
        
        # 秋季天气（9-11月）
        autumn_weather = [
            {
                "name": "天气：晴",
                "summary": "温度15-22度，晴，秋高气爽，适合户外活动",
                "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "location": "成都"
            },
            {
                "name": "天气：阴天",
                "summary": "温度14-18度，阴天，体感微凉，适当添加衣物",
                "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "location": "成都"
            },
        ]
        
        # 冬季天气（12-2月）
        winter_weather = [
            {
                "name": "天气：降温",
                "summary": "温度2-8度，多云，西北风3-4级，羽绒服必备",
                "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "location": "成都"
            },
            {
                "name": "天气：阴冷",
                "summary": "温度5-10度，阴天，湿冷魔法攻击来袭",
                "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "location": "成都"
            },
        ]
        
        # 夜间专属天气提示
        night_weather_tips = [
            {
                "name": "夜间天气提醒",
                "summary": "夜间温度下降至14度，夜间活动注意保暖",
                "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "location": "成都"
            }
        ]
        
        # 选择季节性天气
        if month in [3, 4, 5]:
            base_weather = spring_weather
        elif month in [6, 7, 8]:
            base_weather = summer_weather
        elif month in [9, 10, 11]:
            base_weather = autumn_weather
        else:
            base_weather = winter_weather
        
        # 夜间添加天气提示
        if 21 <= hour or hour <= 6:
            base_weather.append(night_weather_tips[0])
        
        return base_weather[:2]
