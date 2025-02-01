import math
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Page configuration
st.set_page_config(
    page_title="Monte Carlo Simulation",
    page_icon="📈",
    menu_items={"Get Help": None, "Report a Bug": None, "About": None}
)

if st.sidebar.button("🏠 Home", use_container_width=True):
    st.switch_page("app.py")

def monte_carlo_simulation(S, K, T, r, sigma, option_type="call", simulations=10000):
    dt = T
    # Simulate end-of-period stock prices
    Z = np.random.standard_normal(simulations)
    ST = S * np.exp((r - 0.5 * sigma ** 2) * dt + sigma * np.sqrt(dt) * Z)

    # Calculate payoffs
    if option_type == "call":
        payoffs = np.maximum(0, ST - K)
    else:
        payoffs = np.maximum(0, K - ST)

    # Discount payoffs to present value
    option_price = np.exp(-r * T) * np.mean(payoffs)
    
    return option_price

def generate_heatmap(S_min, S_max, sigma_min, sigma_max, K, T, r, option_type, simulations=10000):
    S_range = np.linspace(S_min, S_max, 50)
    sigma_range = np.linspace(sigma_min, sigma_max, 50)
    prices = np.zeros((len(S_range), len(sigma_range)))
    
    for i, S in enumerate(S_range):
        for j, sigma in enumerate(sigma_range):
            prices[i, j] = monte_carlo_simulation(S, K, T, r, sigma, option_type, simulations)

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
        index=2
    )

    if selected_model == "Black Scholes Option Pricing Model":
        st.switch_page("pages/1_black-scholes-model.py")
    elif selected_model == "Binomial Options Pricing Model":
        st.switch_page("pages/2_binomial-model.py")

    # Initialize parameters dictionary
    params = {}

    # Model Parameters
    st.sidebar.header("Model Parameters")
    params["S"] = st.sidebar.number_input("Current Stock Price (S)", min_value=0.0, value=100.0, step=1.0)
    params["K"] = st.sidebar.number_input("Strike Price (K)", min_value=0.0, value=100.0, step=1.0)
    params["T"] = st.sidebar.number_input("Time to Maturity (T in years)", min_value=0.01, value=1.0, step=0.01)
    params["r"] = st.sidebar.number_input("Risk-Free Interest Rate (r as decimal)", min_value=0.0, value=0.05, step=0.01)
    params["sigma"] = st.sidebar.number_input("Volatility (σ as decimal)", min_value=0.01, value=0.2, step=0.01)
    params["simulations"] = st.sidebar.slider("Number of Simulations", min_value=1000, max_value=50000, value=10000, step=1000)
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
st.title("Monte Carlo Option Pricing Calculator")

st.markdown("""***The Monte Carlo Simulation method estimates the price of options by simulating a large number of possible future stock price paths and averaging the payoffs.***""")

# Get parameters from sidebar
params = create_sidebar()

# Calculate and display option price
price = monte_carlo_simulation(
    params["S"],
    params["K"],
    params["T"],
    params["r"],
    params["sigma"],
    params["option_type"],
    params["simulations"]
)
st.success(f"The {params['option_type']} option price is: ${price:.2f}")

# Generate and display heatmap
fig = generate_heatmap(
    params["S_min"],
    params["S_max"],
    params["sigma_min"],
    params["sigma_max"],
    params["K"],
    params["T"],
    params["r"],
    params["option_type"],
    params["simulations"]
)
st.pyplot(fig)

# Additional information
st.markdown("""---""")
st.subheader(""" ***Assumptions of the Monte Carlo Simulation*** """)

st.markdown(""" 
- **Random Walk:** Assumes stock prices follow a stochastic process, often modeled as geometric Brownian motion.
- **Risk-Neutral Valuation:** Uses a risk-neutral framework to discount expected payoffs.
- **No Arbitrage:** Assumes markets are arbitrage-free.
- **Constant Parameters:** Assumes constant risk-free rate and volatility during the option's life.
""")

st.markdown("""---""")
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
