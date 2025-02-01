import math
from scipy.stats import norm
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Page configuration
st.set_page_config(
    page_title="Black-Scholes Model",
    page_icon="📈",
    menu_items={"Get Help": None, "Report a Bug": None, "About": None}
)

if st.sidebar.button("🏠 Home", use_container_width=True):
    st.switch_page("app.py")

def black_scholes(S, K, T, r, sigma, option_type="call"):
    d1 = (math.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    
    if option_type == "call":
        price = S * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2)
    else:
        price = K * math.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    
    return price

def generate_heatmap(S_min, S_max, sigma_min, sigma_max):
    S_range = np.linspace(S_min, S_max, 50)
    sigma_range = np.linspace(sigma_min, sigma_max, 50)
    prices = np.zeros((len(S_range), len(sigma_range)))
    
    for i, S in enumerate(S_range):
        for j, sigma in enumerate(sigma_range):
            prices[i, j] = black_scholes(S, 100, 1, 0.05, sigma, "call")
    
    fig, ax = plt.subplots(figsize=(10, 6))
    c = ax.imshow(
        prices,
        aspect='auto',
        cmap="RdYlGn",
        origin='lower',
        extent=[sigma_range.min(), sigma_range.max(), S_range.min(), S_range.max()]
    )
    plt.colorbar(c, ax=ax, label="Option Price")
    ax.set_xlabel("Volatility (σ)")
    ax.set_ylabel("Stock Price (S)")
    ax.set_title("Profitability Heatmap (Green = Profitable, Red = Loss)")
    return fig

def create_sidebar():
    # Navigation
    selected_model = st.sidebar.selectbox(
        "Navigate to",
        ["Black Scholes Option Pricing Model", "Binomial Options Pricing Model", "Monte Carlo Simulation"],
        index=0
    )

    if selected_model == "Binomial Options Pricing Model":
        st.switch_page("pages/2_binomial-model.py")
    elif selected_model == "Monte Carlo Simulation":
        st.switch_page("pages/3_monte-carlo-model.py")

    # Initialize parameters dictionary
    params = {}

    # Model Parameters
    st.sidebar.header("Model Parameters")
    params["S"] = st.sidebar.number_input("Current Stock Price (S)", min_value=0.0, value=100.0, step=1.0)
    params["K"] = st.sidebar.number_input("Strike Price (K)", min_value=0.0, value=100.0, step=1.0)
    params["T"] = st.sidebar.number_input("Time to Maturity (T in years)", min_value=0.01, value=1.0, step=0.01)
    params["r"] = st.sidebar.number_input("Risk-Free Interest Rate (r as decimal)", min_value=0.0, value=0.05, step=0.01)
    params["sigma"] = st.sidebar.number_input("Volatility (σ as decimal)", min_value=0.01, value=0.2, step=0.01)
    params["option_type"] = st.sidebar.radio("Option Type", ("call", "put"))

    # Heatmap Configuration
    st.sidebar.header("Heatmap Configuration")
    params["S_min"] = st.sidebar.number_input("Min Stock Price (S_min)", min_value=0.0, value=50.0, step=1.0)
    S_max_min = params["S_min"] + 1  # Calculate minimum value for S_max
    params["S_max"] = st.sidebar.number_input("Max Stock Price (S_max)", min_value=S_max_min, value=150.0, step=1.0)
    params["sigma_min"] = st.sidebar.number_input("Min Volatility (σ_min)", min_value=0.01, value=0.1, step=0.01)
    sigma_max_min = params["sigma_min"] + 0.01  # Calculate minimum value for sigma_max
    params["sigma_max"] = st.sidebar.number_input("Max Volatility (σ_max)", min_value=sigma_max_min, value=0.5, step=0.01)

    return params

# Main content
st.title("Black-Scholes Option Pricing Calculator")

st.markdown("""***The Black-Scholes option pricing model is a mathematical model used to determine the theoretical price of European-style options. 
    The model assumes a constant volatility and interest rate and is widely used in financial markets.***""")

# Get parameters from sidebar
params = create_sidebar()

# Calculate and display option price
price = black_scholes(
    params["S"],
    params["K"],
    params["T"],
    params["r"],
    params["sigma"],
    params["option_type"]
)
st.success(f"The {params['option_type']} option price is: ${price:.2f}")

# Generate and display heatmap
fig = generate_heatmap(
    params["S_min"],
    params["S_max"],
    params["sigma_min"],
    params["sigma_max"]
)
st.pyplot(fig)

# Additional information
st.markdown("""---""")
st.markdown("""***The Black-Scholes-Merton (BSM) model is used for the valuation of stock options. The BSM model is used to determine the fair prices of stock options based on six variables: volatility, type, underlying stock price, strike price, time, and risk-free rate.***""")

# Display formulas
st.image("images\BS-call-img.png", caption="Formula for calculating Black-Scholes options pricing")
if params["option_type"] == "put":
    st.image("images\BS-put-img.png", caption="Formula for calculating Black-Scholes PUT options pricing")

st.subheader(""" ***Assumptions of the Black-Scholes-Merton Model*** """)

st.markdown(""" 
- **Lognormal distribution:** The Black-Scholes-Merton model assumes that stock prices follow a lognormal distribution based on the principle that asset prices cannot take a negative value; they are bounded by zero.
- **No dividends:** The BSM model assumes that the stocks do not pay any dividends or returns.
- **Expiration date:** The model assumes that the options can only be exercised on their expiration or maturity date. Hence, it does not accurately price American options. It is extensively used in the European options market.
- **Random walk:** The stock market is highly volatile, and hence, a state of random walk is assumed as the market direction can never truly be predicted.
- **Frictionless market:** No transaction costs, including commission and brokerage, are assumed in the BSM model.
- **Risk-free interest rate:** The interest rates are assumed to be constant, hence making the underlying asset a risk-free one.
""")

st.markdown("---")  # Adds a horizontal line
st.markdown("""
**About Me**  
Sri Sahithi Sunkaranam | [LinkedIn](https://www.linkedin.com/in/sri-sahithi-sunkaranam) | [GitHub](https://github.com/sahithi-sss)
""")

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