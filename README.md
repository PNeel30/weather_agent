# Weather Agent

A small Streamlit app that answers weather questions for a city using the
OpenWeatherMap API and Google Gemini.

## Features

- Ask weather questions in natural language
- Fetch live weather data from OpenWeatherMap
- Turn raw API data into a short user-friendly summary with Gemini
- Use the app in Streamlit or from Python code

## Prerequisites

- Python 3.8+
- Google API key
- OpenWeatherMap API key

## Installation

1. Clone the repository.
2. Create and activate a virtual environment.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_google_api_key_here
OPENWEATHER_API_KEY=your_openweather_api_key_here
```

## Running the App

```bash
streamlit run app.py
```

Then open `http://localhost:8501`.

## Example Questions

- `What's the weather in London?`
- `Temperature in New York`
- `Is it raining in Tokyo?`

## Programmatic Usage

```python
from main import fetch_weather

answer = fetch_weather("What's the weather in Paris?")
print(answer)
```

## Project Structure

```text
weather_agent/
|-- app.py
|-- main.py
|-- requirements.txt
|-- test_main.py
```

## Testing

Run the unit tests with:

```bash
python -m unittest test_main.py
```
