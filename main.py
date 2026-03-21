import os
import re
from typing import Any, Optional

import requests
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))


def build_llm():
    google_api_key = os.getenv("GOOGLE_API_KEY")
    if not google_api_key:
        raise RuntimeError("GOOGLE_API_KEY is not set. Add it to your .env file.")

    from langchain_google_genai import ChatGoogleGenerativeAI

    return ChatGoogleGenerativeAI(
        model="models/gemini-2.0-flash",
        temperature=0.3,
        google_api_key=google_api_key,
    )


class WeatherAgent:
    def __init__(
        self,
        llm: Optional[Any] = None,
        weather_api_key: Optional[str] = None,
    ):
        self._llm = llm
        self.weather_api_key = weather_api_key

    @property
    def llm(self):
        if self._llm is None:
            self._llm = build_llm()
        return self._llm

    def run(self, query: str) -> str:
        city = self.extract_city(query)
        weather_data = self.get_weather(city)
        return self.summarize_weather(weather_data)

    def extract_city(self, query: str) -> str:
        match = re.search(
            r"\bin\s+([a-zA-Z\s]+?)(?:\s+(?:today|now|currently|right now|please)\b|[?.!,]|$)",
            query,
            re.IGNORECASE,
        )
        city = match.group(1).strip() if match else "London"
        city = re.sub(r"[^a-zA-Z\s]", "", city).strip()
        return city or "London"

    def get_weather(self, city: str) -> dict:
        url = f"https://wttr.in/{city}?format=j1"

        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            raise Exception("Weather API failed")

        return response.json()

    def summarize_weather(self, data: dict) -> str:
        current = data["current_condition"][0]

        temp = current["temp_C"]
        desc = current["weatherDesc"][0]["value"]

        return f"The temperature is {temp}°C with {desc}."

class AIAgentPipeline:
    def __init__(
        self,
        llm: Optional[Any] = None,
        weather_api_key: Optional[str] = None,
    ):
        self.weather_agent = WeatherAgent(
            llm=llm,
            weather_api_key=weather_api_key,
        )

    def run(self, query: str) -> str:
        return self.weather_agent.run(query)


def fetch_weather(
    query: str,
    llm: Optional[Any] = None,
    weather_api_key: Optional[str] = None,
) -> str:
    return AIAgentPipeline(llm=llm, weather_api_key=weather_api_key).run(query)
