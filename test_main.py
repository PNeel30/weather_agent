import unittest
from unittest.mock import Mock, patch

import requests

from main import WeatherAgent, fetch_weather


class FakeLLM:
    def __init__(self, response: str = "Default weather summary."):
        self.response = response
        self.prompts = []

    def predict(self, prompt: str) -> str:
        self.prompts.append(prompt)
        return self.response


class TestWeatherAgent(unittest.TestCase):
    def test_extract_city_uses_query_or_default(self):
        agent = WeatherAgent(llm=FakeLLM(), weather_api_key="test-key")

        self.assertEqual(
            agent.extract_city("What's the weather in New York?"),
            "New York",
        )
        self.assertEqual(
            agent.extract_city("What's the weather in New York today?"),
            "New York",
        )
        self.assertEqual(
            agent.extract_city("Is it raining in Tokyo right now?"),
            "Tokyo",
        )
        self.assertEqual(agent.extract_city("Tell me the weather"), "London")

    @patch.dict("os.environ", {}, clear=True)
    def test_missing_weather_api_key_raises_error(self):
        agent = WeatherAgent(llm=FakeLLM(), weather_api_key=None)

        with self.assertRaisesRegex(RuntimeError, "OPENWEATHER_API_KEY"):
            agent.get_weather("London")

    @patch("main.requests.get")
    def test_unknown_city_raises_helpful_error(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
            "404 Client Error"
        )
        mock_get.return_value = mock_response

        agent = WeatherAgent(llm=FakeLLM(), weather_api_key="test-key")

        with self.assertRaisesRegex(ValueError, "Try only the city name"):
            agent.get_weather("London today")

    @patch("main.requests.get")
    def test_fetch_weather_returns_llm_summary(self, mock_get):
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            "name": "London",
            "main": {"temp": 17},
            "weather": [{"description": "light rain"}],
        }
        mock_get.return_value = mock_response

        llm = FakeLLM("London is 17C with light rain.")
        result = fetch_weather(
            "What's the weather in London?",
            llm=llm,
            weather_api_key="test-key",
        )

        self.assertEqual(result, "London is 17C with light rain.")
        self.assertEqual(len(llm.prompts), 1)
        self.assertIn("temperature", llm.prompts[0])

        params = mock_get.call_args.kwargs["params"]
        self.assertEqual(params["q"], "London")
        self.assertEqual(params["appid"], "test-key")
        self.assertEqual(params["units"], "metric")


if __name__ == "__main__":
    unittest.main()
