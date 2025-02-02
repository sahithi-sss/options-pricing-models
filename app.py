import streamlit as st

st.set_page_config(
    page_title="Options Pricing Models",
    page_icon="📈",
    menu_items={"Get Help": None, "Report a Bug": None, "About": None}
)

st.markdown("""
    <style>
        [data-testid="collapsedControl"] {display: none}
        section[data-testid="stSidebar"] > div:first-child {display: none}
        .main > div:first-child {display: none}
    </style>
""", unsafe_allow_html=True)



def create_sidebar():
    st.sidebar.header("About Me")
    st.sidebar.markdown("**Sri Sahithi Sunkaranam**")
    st.sidebar.markdown("[LinkedIn](https://www.linkedin.com/in/sri-sahithi-sunkaranam)")
    st.sidebar.markdown("[GitHub](https://github.com/sahithi-sss)")

create_sidebar()

st.title("Options Pricing Models")

st.markdown("""
    <style>
        [data-testid="collapsedControl"] {display: none}
        section[data-testid="stSidebar"] > div:first-child {display: none}
        .main > div:first-child {display: none}
        button[kind="headerNoPadding"] {display: none}
        .st-emotion-cache-1dp5vir {display: none}
        [data-testid="stSidebarNav"] {display: none !important}
        .st-emotion-cache-16pwjcz {display: none}
    </style>
""", unsafe_allow_html=True)

# Create radio buttons for model selection
selected_model = st.radio(
    "Select an Options Pricing Model",
    ["Black-Scholes Model", "Binomial Options Pricing Model", "Trinomial Options Pricing Model"]
)

# Add a button to navigate to the selected model
if st.button("Show Model", use_container_width=True):
    if selected_model == "Black-Scholes Model":
        st.switch_page("pages/1_black-scholes-model.py")
    elif selected_model == "Binomial Options Pricing Model":
        st.switch_page("pages/2_binomial-model.py")
    elif selected_model == "Trinomial Options Pricing Model":
        st.switch_page("pages/3_trinomial-model.py")