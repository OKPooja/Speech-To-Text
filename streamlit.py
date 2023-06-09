# Libraries to be used ------------------------------------------------------------

import streamlit as st
import requests
import json
import os
import sounddevice as sd

# title and favicon ------------------------------------------------------------

st.set_page_config(
    page_title="Speech-to-Text Transcription App", page_icon="👄", layout="wide"
)

# App layout width -------------------------------------------------


def _max_width_():
    max_width_str = f"max-width: 1200px;"
    st.markdown(
        f"""
    <style>
    .reportview-container .main .block-container{{
        {max_width_str}
    }}
    </style>
    """,
        unsafe_allow_html=True,
    )


_max_width_()

# logo and header -------------------------------------------------

c30, c31, c32 = st.columns([2.5, 1, 3])

with c30:
    st.image("logo.png", width=350)
    st.header("")

with c32:
    st.title("")
    st.title("")
    st.caption("")
    st.caption("")
    st.caption("")
    st.caption("")
    st.caption("")
    st.caption("")

    st.write(
        "&nbsp &nbsp Made in [![this is an image link](https://i.imgur.com/iIOA6kU.png)](https://www.streamlit.io/)&nbsp, with :heart: by [@DataChaz](https://www.charlywargnier.com/) | [![this is an image link](https://i.imgur.com/thJhzOO.png)](https://www.buymeacoffee.com/cwar05)"
    )

st.text("")
st.markdown(
    f"""
                    The speech to text recognition is done via the [Facebook's Wav2Vec2 model.](https://huggingface.co/facebook/wav2vec2-large-960h)
                    """
)
st.text("")

# region Main

# multi navbar -------------------------------------------------


def main():
    pages = {
        "👾 Free mode (2MB per API call)": demo,
        "🤗 Full mode (with your API key)": API_key,
    }

    if "page" not in st.session_state:
        st.session_state.update(
            {
                # Default page
                "page": "Home",
            }
        )

    with st.sidebar:
        page = st.radio("Select your mode", tuple(pages.keys()))

    pages[page]()


# endregion main

# Free mode -------------------------------------------------


def demo():
    c1, c2, c3 = st.columns([1, 4, 1])
    with c2:
        with st.form(key="my_form"):
            duration = st.number_input("Recording Duration (in seconds)", value=5, min_value=1)
            submit_button = st.form_submit_button(label="Transcribe")

    if submit_button:
        audio = record_audio(duration)

        bytes_data = audio.tobytes()

        api_token = st.secrets["api_token"]

        headers = {"Authorization": f"Bearer {api_token}"}
        API_URL = "https://api-inference.huggingface.co/models/facebook/wav2vec2-base-960h"

        def query(data):
            response = requests.request("POST", API_URL, headers=headers, data=data)
            return json.loads(response.content.decode("utf-8"))

        data = query(bytes_data)

        values_view = data.values()
        value_iterator = iter(values_view)
        text_value = next(value_iterator)
        text_value = text_value.lower()

        st.success(text_value)

        c0, c1 = st.columns([2, 2])

        with c0:
            st.download_button(
                "Download the transcription",
                text_value,
                file_name=None,
                mime=None,
                key=None,
                help=None,
                on_click=None,
                args=None,
                kwargs=None,
            )


# Custom API key mode -------------------------------------------------


def API_key():
    c1, c2, c3 = st.columns([1, 4, 1])
    with c2:
        with st.form(key="my_form"):
            text_input = st.text_input("Enter your HuggingFace API key")
            duration = st.number_input("Recording Duration (in seconds)", value=5, min_value=1)
            submit_button = st.form_submit_button(label="Transcribe")

    if submit_button:
        try:
            audio = record_audio(duration)

            # Convert audio to bytes
            bytes_data = audio.tobytes()

            api_token = text_input

            headers = {"Authorization": f"Bearer {api_token}"}
            API_URL = "https://api-inference.huggingface.co/models/facebook/wav2vec2-base-960h"

            def query(data):
                response = requests.request("POST", API_URL, headers=headers, data=data)
                return json.loads(response.content.decode("utf-8"))

            data = query(bytes_data)

            values_view = data.values()
            value_iterator = iter(values_view)
            text_value = next(value_iterator)
            text_value = text_value.lower()

            st.success(text_value)

            c0, c1 = st.columns([2, 2])

            with c0:
                st.download_button(
                    "Download the transcription",
                    text_value,
                    file_name=None,
                    mime=None,
                    key=None,
                    help=None,
                    on_click=None,
                    args=None,
                    kwargs=None,
                )

        except ValueError:
            st.error("ValueError")


# Notes about the app -------------------------------------------------

with st.expander("ℹ️ - About this app", expanded=False):
    st.write(
        """     

-   The Free mode is limited to 2MB of the audio file. You can use your API key to transcribe audio files of up to 30MB!
-   The tool is still in Beta; don't hesitate to contact me at [![Gitter chat](https://badges.gitter.im/gitterHQ/gitter.png)](https://gitter.im/DataChaz/speech-to-text) if bugs or questions
-   This app is free. If it's helpful to you, you can [buy me a ☕](https://www.buymeacoffee.com/cwar05) to support my work
	    """
    )

    st.markdown("")

with st.expander("🔆 Coming soon!", expanded=False):
    st.write(
        """  
-   Add more embedding models
-   Add more languages
-   Allow for larger wave files to be reviewed (currently limited to 30 MB)

	    """
    )

    st.markdown("")


def record_audio(duration):
    sample_rate = 16000  
    channels = 1  

    # Record audio
    audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=channels)
    sd.wait()  

    return audio.flatten()  


if __name__ == "__main__":
    main()

