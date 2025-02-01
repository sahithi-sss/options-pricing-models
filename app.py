import streamlit as st

st.set_page_config(
    page_title="Options Pricing Models",
    page_icon="📈",
    menu_items={"Get Help": None, "Report a Bug": None, "About": None}
)

def create_sidebar():
    st.sidebar.header("About Me")
    st.sidebar.markdown("**Sri Sahithi Sunkaranam**")
    st.sidebar.markdown("[LinkedIn](https://www.linkedin.com/in/sri-sahithi-sunkaranam)")
    st.sidebar.markdown("[GitHub](https://github.com/sahithi-sss)")

create_sidebar()

st.title("Options Pricing Models")

st.markdown("""
    <div style="text-align: center; font-size: 20px;">
        Options pricing models are mathematical frameworks used to determine the fair value of options contracts.
        These models help traders and investors make informed decisions based on market conditions.
    </div>
""", unsafe_allow_html=True)

# Create radio buttons for model selection
selected_model = st.radio(
    "Select an Options Pricing Model",
    ["Black-Scholes Model", "Binomial Options Pricing Model", "Monte Carlo Simulation"]
)

# Add a button to navigate to the selected model
if st.button("Show Model", use_container_width=True):
    if selected_model == "Black-Scholes Model":
        st.switch_page("pages/1_black-scholes-model.py")
    elif selected_model == "Binomial Options Pricing Model":
        st.switch_page("pages/2_binomial-model.py")
    elif selected_model == "Monte Carlo Simulation":
        st.switch_page("pages/3_monte-carlo-model.py")