import streamlit as st

try:
    from src.brand import (
        BASE_ORANGE,
        BASE_RED,
        TEAMNL_LOGO_SYMBOL,
        TEAMNL_LOGO_WORDMARK,
    )
except ModuleNotFoundError:
    from brand import (
        BASE_ORANGE,
        BASE_RED,
        TEAMNL_LOGO_SYMBOL,
        TEAMNL_LOGO_WORDMARK,
    )

st.set_page_config(
    page_title="TeamNL Sport Science Centre",
    layout="wide",
)

st.markdown(
    f"""
    <style>
      .stApp,
      [data-testid="stAppViewContainer"],
      [data-testid="stMain"],
      [data-testid="stMainBlockContainer"] {{
        background: var(--background-color);
      }}

      [data-testid="stHeader"] {{
        background: transparent;
      }}

      .brand-title {{
        color: var(--text-color);
        margin-bottom: 0.1rem;
        font-weight: 700;
      }}

      .brand-subtitle {{
        color: var(--text-color);
        font-size: 1rem;
        opacity: 0.85;
      }}

      div.stButton > button {{
        background-color: {BASE_ORANGE};
        color: white;
        border: 0;
      }}

      div.stButton > button:hover {{
        background-color: {BASE_RED};
        color: white;
      }}
    </style>
    """,
    unsafe_allow_html=True,
)

logo_wordmark_col, title_col = st.columns([2, 4])

with logo_wordmark_col:
    if TEAMNL_LOGO_WORDMARK.exists():
        st.image(str(TEAMNL_LOGO_WORDMARK), width=220)
    else:
        st.info(f"Missing logo file: {TEAMNL_LOGO_WORDMARK}")

with title_col:
    st.markdown('<h1 class="brand-title">Streamlit demo app</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="brand-subtitle">Dummy app for validating local development and Azure container deployment.</p>',
        unsafe_allow_html=True,
    )

with st.sidebar:
    if TEAMNL_LOGO_SYMBOL.exists():
        st.image(str(TEAMNL_LOGO_SYMBOL), width=95)
    else:
        st.info(f"Missing logo file: {TEAMNL_LOGO_SYMBOL}")

    st.header("Parameters")
    name = st.text_input("Name", placeholder="Ada Lovelace")
    submitted = st.button("Say hello")

if submitted:
    cleaned = name.strip()
    if cleaned:
        st.success(f"Hello, {cleaned}!")
    else:
        st.warning("Please enter a name.")

st.caption("For Azure App Service, the startup command runs Streamlit on port 8000.")
