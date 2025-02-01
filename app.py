import streamlit as st

st.set_page_config(page_title="Options Pricing Models", page_icon="📈",menu_items={"Get Help": None, "Report a Bug": None, "About": None})

st.sidebar.header("About Me")
st.sidebar.markdown("**Sri Sahithi Sunkaranam**")
st.sidebar.markdown("[LinkedIn](https://www.linkedin.com/in/sri-sahithi-sunkaranam)")
st.sidebar.markdown("[GitHub](https://github.com/sahithi-sss)")

st.title("Options Pricing Models")

st.markdown("""
    <div style="text-align: center; font-size: 20px;">
        Options pricing models are mathematical frameworks used to determine the fair value of options contracts.
        These models help traders and investors make informed decisions based on market conditions.
    </div>
""", unsafe_allow_html=True)

selected_model = st.selectbox("Select an Options Pricing Model", 
                            ["Black-Scholes Model", "Binomial Options Pricing Model", "Monte Carlo Simulation"],
                            index=0, key="main_dropdown")

# Redirect to the respective page
if selected_model == "Black-Scholes Model":
    st.switch_page("pages/black-scholes-model.py")
elif selected_model == "Binomial Options Pricing Model":
    st.switch_page("pages/binomial-model.py")
elif selected_model == "Monte Carlo Simulation":
    st.switch_page("pages/monte-carlo-model.py")