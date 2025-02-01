import streamlit as st

st.set_page_config(page_title="Options Pricing Models", page_icon="📈")

st.title("Options Pricing Models")

st.sidebar.header("About Me")
st.sidebar.markdown("**Sri Sahithi Sunkaranam**")
st.sidebar.markdown("[LinkedIn](https://www.linkedin.com/in/sri-sahithi-sunkaranam)")
st.sidebar.markdown("[GitHub](https://github.com/sahithi-sss)")

# Dropdown to select model
default_model = "Black-Scholes Model"
model = st.sidebar.selectbox("Select an Options Pricing Model", 
                            ["Black-Scholes Model", "Binomial Options Pricing Model", "Monte Carlo Simulation"],
                            index=0)  # Default selection

# Redirect to the respective page
if model == "Black-Scholes Model":
    st.switch_page("pages/black_scholes.py")
elif model == "Binomial Options Pricing Model":
    st.switch_page("pages/binomial.py")
elif model == "Monte Carlo Simulation":
    st.switch_page("pages/monte_carlo.py")
