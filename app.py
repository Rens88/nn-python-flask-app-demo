from pathlib import Path

import streamlit as st


APP_TITLE = "NOCNSF SSC Demo App"
STATIC_DIR = Path(__file__).parent / "static"
LOGO_PATH = STATIC_DIR / "images" / "teamnl_sport_science_centre_LOGO.png"


st.set_page_config(page_title=APP_TITLE, layout="centered")

st.title(APP_TITLE)
st.write("This sample now runs as a Streamlit app on Azure App Service.")

if LOGO_PATH.exists():
    st.image(str(LOGO_PATH), width=260)

with st.form("hello_form"):
    name = st.text_input("Could you please tell me your name?")
    submitted = st.form_submit_button("Say Hello")

if submitted:
    cleaned_name = name.strip()
    if cleaned_name:
        st.success(f"Hello {cleaned_name}! It is nice to meet you.")
    else:
        st.warning("Please enter a name before submitting.")
else:
    st.caption("Enter your name and submit the form to see the greeting.")
