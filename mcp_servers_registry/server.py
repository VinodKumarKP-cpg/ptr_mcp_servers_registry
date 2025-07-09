#!/usr/bin/env python3
# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "fastmcp",
# ]
# ///
"""
Weather MCP Server using FastMCP
A simple and efficient MCP server that provides weather information tools.
"""

import asyncio
import json
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
import random

try:
    from fastmcp import FastMCP
except ImportError:
    print("FastMCP not installed. Install with: pip install fastmcp")
    exit(1)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WeatherMCPServer:
    """Weather MCP Server using FastMCP framework."""

    def __init__(self):
        # Initialize FastMCP app
        self.app = FastMCP("Weather Server")

        # Mock weather database with more realistic data
        self.weather_data = {
            "new york": {
                "temperature": 72,
                "condition": "sunny",
                "humidity": 65,
                "wind_speed": 8,
                "feels_like": 75,
                "pressure": 1013.25,
                "visibility": 10,
                "uv_index": 6
            },
            "london": {
                "temperature": 59,
                "condition": "cloudy",
                "humidity": 78,
                "wind_speed": 12,
                "feels_like": 56,
                "pressure": 1008.5,
                "visibility": 8,
                "uv_index": 2
            },
            "tokyo": {
                "temperature": 75,
                "condition": "rainy",
                "humidity": 82,
                "wind_speed": 6,
                "feels_like": 78,
                "pressure": 1005.2,
                "visibility": 5,
                "uv_index": 3
            },
            "paris": {
                "temperature": 68,
                "condition": "partly cloudy",
                "humidity": 70,
                "wind_speed": 9,
                "feels_like": 70,
                "pressure": 1011.8,
                "visibility": 9,
                "uv_index": 4
            },
            "sydney": {
                "temperature": 77,
                "condition": "sunny",
                "humidity": 60,
                "wind_speed": 11,
                "feels_like": 80,
                "pressure": 1018.3,
                "visibility": 12,
                "uv_index": 8
            },
            "los angeles": {
                "temperature": 78,
                "condition": "sunny",
                "humidity": 55,
                "wind_speed": 7,
                "feels_like": 79,
                "pressure": 1016.1,
                "visibility": 15,
                "uv_index": 7
            },
            "chicago": {
                "temperature": 64,
                "condition": "windy",
                "humidity": 68,
                "wind_speed": 18,
                "feels_like": 60,
                "pressure": 1009.7,
                "visibility": 11,
                "uv_index": 5
            }
        }

        # Historical data for trends
        self.historical_data = self._generate_historical_data()

        # Register tools
        self._register_tools()

        logger.info("Weather MCP Server initialized with FastMCP")

    def _generate_historical_data(self) -> Dict[str, List[Dict[str, Any]]]:
        """Generate mock historical weather data."""
        historical = {}

        for city, current_weather in self.weather_data.items():
            city_history = []
            base_temp = current_weather["temperature"]

            # Generate 7 days of historical data
            for i in range(7):
                # Add some variation to the temperature
                temp_variation = random.randint(-10, 10)
                temp = base_temp + temp_variation

                conditions = ["sunny", "cloudy", "rainy", "partly cloudy", "windy"]
                condition = random.choice(conditions)

                city_history.append({
                    "date": f"2024-07-{str(i + 1).zfill(2)}",
                    "temperature": temp,
                    "condition": condition,
                    "humidity": random.randint(40, 90)
                })

            historical[city] = city_history

        return historical

    def _register_tools(self):
        """Register all weather tools with FastMCP."""

        @self.app.tool()
        def get_weather(city: str) -> str:
            """
            Get current weather information for a city.

            Args:
                city: The city name to get weather for

            Returns:
                Current weather information including temperature, condition, humidity, etc.
            """
            city_lower = city.lower().strip()

            if not city_lower:
                return "Error: City name is required"

            if city_lower in self.weather_data:
                weather = self.weather_data[city_lower]

                result = f"""Current Weather in {city.title()}:
🌡️  Temperature: {weather['temperature']}°F (feels like {weather['feels_like']}°F)
🌤️  Condition: {weather['condition'].title()}
💧 Humidity: {weather['humidity']}%
💨 Wind Speed: {weather['wind_speed']} mph
📊 Pressure: {weather['pressure']} hPa
👁️  Visibility: {weather['visibility']} miles
☀️  UV Index: {weather['uv_index']}

Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"""

                return result
            else:
                available_cities = ", ".join([c.title() for c in self.weather_data.keys()])
                return f"Weather data not available for {city.title()}. Available cities: {available_cities}"

        @self.app.tool()
        def list_cities() -> str:
            """
            List all cities with available weather data.

            Returns:
                List of cities with weather information available
            """
            cities = list(self.weather_data.keys())
            result = f"Available cities ({len(cities)} total):\n"

            for i, city in enumerate(cities, 1):
                weather = self.weather_data[city]
                result += f"{i}. {city.title()} - {weather['temperature']}°F, {weather['condition']}\n"

            return result.strip()

        @self.app.tool()
        def compare_weather(city1: str, city2: str) -> str:
            """
            Compare weather between two cities.

            Args:
                city1: First city name
                city2: Second city name

            Returns:
                Comparison of weather conditions between the two cities
            """
            city1_lower = city1.lower().strip()
            city2_lower = city2.lower().strip()

            if city1_lower not in self.weather_data:
                return f"Weather data not available for {city1.title()}"

            if city2_lower not in self.weather_data:
                return f"Weather data not available for {city2.title()}"

            weather1 = self.weather_data[city1_lower]
            weather2 = self.weather_data[city2_lower]

            # Calculate differences
            temp_diff = weather1['temperature'] - weather2['temperature']
            humidity_diff = weather1['humidity'] - weather2['humidity']
            wind_diff = weather1['wind_speed'] - weather2['wind_speed']

            result = f"""Weather Comparison: {city1.title()} vs {city2.title()}

🌡️  Temperature:
   • {city1.title()}: {weather1['temperature']}°F
   • {city2.title()}: {weather2['temperature']}°F
   • Difference: {abs(temp_diff)}°F ({'warmer' if temp_diff > 0 else 'cooler'} in {city1.title() if temp_diff > 0 else city2.title()})

🌤️  Conditions:
   • {city1.title()}: {weather1['condition'].title()}
   • {city2.title()}: {weather2['condition'].title()}

💧 Humidity:
   • {city1.title()}: {weather1['humidity']}%
   • {city2.title()}: {weather2['humidity']}%
   • Difference: {abs(humidity_diff)}% ({'more humid' if humidity_diff > 0 else 'less humid'} in {city1.title() if humidity_diff > 0 else city2.title()})

💨 Wind Speed:
   • {city1.title()}: {weather1['wind_speed']} mph
   • {city2.title()}: {weather2['wind_speed']} mph
   • Difference: {abs(wind_diff)} mph ({'windier' if wind_diff > 0 else 'calmer'} in {city1.title() if wind_diff > 0 else city2.title()})"""

            return result

        @self.app.tool()
        def get_weather_forecast(city: str, days: int = 3) -> str:
            """
            Get weather forecast for a city (mock data).

            Args:
                city: The city name
                days: Number of days to forecast (1-7)

            Returns:
                Weather forecast for the specified number of days
            """
            city_lower = city.lower().strip()

            if city_lower not in self.weather_data:
                return f"Weather data not available for {city.title()}"

            if days < 1 or days > 7:
                return "Forecast days must be between 1 and 7"

            current_weather = self.weather_data[city_lower]
            base_temp = current_weather['temperature']

            result = f"Weather Forecast for {city.title()} ({days} days):\n\n"

            conditions = ["sunny", "cloudy", "rainy", "partly cloudy", "windy"]

            for i in range(days):
                # Generate forecast with some variation
                temp_variation = random.randint(-8, 8)
                temp = base_temp + temp_variation
                condition = random.choice(conditions)
                humidity = random.randint(40, 90)

                forecast_date = datetime.now()
                forecast_date = forecast_date.replace(day=forecast_date.day + i + 1)

                result += f"📅 {forecast_date.strftime('%A, %B %d')}:\n"
                result += f"   🌡️  {temp}°F\n"
                result += f"   🌤️  {condition.title()}\n"
                result += f"   💧 {humidity}% humidity\n\n"

            return result.strip()

        @self.app.tool()
        def get_weather_history(city: str, days: int = 7) -> str:
            """
            Get historical weather data for a city.

            Args:
                city: The city name
                days: Number of historical days to retrieve (1-7)

            Returns:
                Historical weather data for the specified city
            """
            city_lower = city.lower().strip()

            if city_lower not in self.historical_data:
                return f"Historical weather data not available for {city.title()}"

            if days < 1 or days > 7:
                return "Historical days must be between 1 and 7"

            history = self.historical_data[city_lower][:days]

            result = f"Weather History for {city.title()} (last {days} days):\n\n"

            for day_data in history:
                result += f"📅 {day_data['date']}:\n"
                result += f"   🌡️  {day_data['temperature']}°F\n"
                result += f"   🌤️  {day_data['condition'].title()}\n"
                result += f"   💧 {day_data['humidity']}% humidity\n\n"

            return result.strip()

        @self.app.tool()
        def get_weather_alerts(city: str) -> str:
            """
            Get weather alerts for a city (mock alerts).

            Args:
                city: The city name

            Returns:
                Current weather alerts for the city
            """
            city_lower = city.lower().strip()

            if city_lower not in self.weather_data:
                return f"Weather alert data not available for {city.title()}"

            weather = self.weather_data[city_lower]
            alerts = []

            # Generate mock alerts based on conditions
            if weather['temperature'] > 85:
                alerts.append("🔥 Heat Advisory: High temperatures expected")

            if weather['wind_speed'] > 15:
                alerts.append("💨 Wind Advisory: Strong winds expected")

            if weather['condition'] == "rainy":
                alerts.append("🌧️ Rain Warning: Heavy rainfall expected")

            if weather['uv_index'] > 7:
                alerts.append("☀️ UV Warning: High UV index, use sun protection")

            if weather['humidity'] > 80:
                alerts.append("💧 Humidity Alert: High humidity levels")

            if not alerts:
                return f"✅ No weather alerts for {city.title()}"

            result = f"Weather Alerts for {city.title()}:\n\n"
            for i, alert in enumerate(alerts, 1):
                result += f"{i}. {alert}\n"

            return result.strip()

    def run(self):
        """Run the FastMCP server."""
        logger.info("Starting Weather MCP Server...")
        self.app.run()


def main():
    """Main entry point for the weather MCP server."""
    try:
        server = WeatherMCPServer()
        server.run()
    except KeyboardInterrupt:
        logger.info("Weather MCP Server stopped by user")
    except Exception as e:
        logger.error(f"Error running Weather MCP Server: {e}")
        raise


if __name__ == "__main__":
    main()