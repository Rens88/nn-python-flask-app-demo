import streamlit as st

st.set_page_config(
    page_title="Streamlit on Azure App Service",
    layout="centered",
)

st.title("Streamlit demo app")
st.write(
    "This is a simple greeting app to validate that Streamlit can run on Azure App Service. Greetings Rens"
)

with st.form("hello_form"):
    name = st.text_input("Your name", placeholder="Ada Lovelace")
    submitted = st.form_submit_button("Say hello")

if submitted:
    cleaned = name.strip()
    if cleaned:
        st.success(f"Hello, {cleaned}!")
    else:
        st.warning("Please enter a name.")

st.caption(
    "For Azure App Service, the startup command runs Streamlit on port 8000."
)
