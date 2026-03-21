import requests
import streamlit as st

from main import AIAgentPipeline

st.set_page_config(page_title="Weather Agent", page_icon="W")

st.title("Weather Agent")
st.caption("Powered by Neel Patel")

st.caption("Ask for the current weather in any city.")

pipeline = AIAgentPipeline()

query = st.text_input(
    "Ask a weather question:",
    placeholder="What's the weather in London?",
)

if query:
    with st.spinner("Checking the weather..."):
        try:
            answer = pipeline.run(query)
            st.markdown("**Answer:**")
            st.write(answer)
        except ValueError as exc:
            st.error(str(exc))
        except RuntimeError as exc:
            st.error(str(exc))
        except requests.exceptions.ConnectionError:
            st.error("Network error while contacting the weather service.")
        except requests.exceptions.HTTPError as exc:
            st.error(f"Weather API error: {exc}")
        except Exception as exc:
            st.error(str(exc))
