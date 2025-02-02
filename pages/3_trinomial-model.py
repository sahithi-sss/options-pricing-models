import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Page configuration
st.set_page_config(
    page_title="Trinomial Options Pricing Model",
    page_icon="📈",
    menu_items={"Get Help": None, "Report a Bug": None, "About": None}
)

if st.sidebar.button("🏠 Home", use_container_width=True):
    st.switch_page("app.py")

def trinomial_model(S, K, T, r, sigma, N, option_type="call"):
    dt = T / N  # Time step
    u = np.exp(sigma * np.sqrt(2 * dt))  # Up factor
    d = 1 / u  # Down factor
    m = 1  # Middle (no change)
    p_u = ((np.exp(r * dt / 2) - np.exp(-sigma * np.sqrt(dt / 2))) / (np.exp(sigma * np.sqrt(dt / 2)) - np.exp(-sigma * np.sqrt(dt / 2))))**2
    p_d = ((np.exp(sigma * np.sqrt(dt / 2)) - np.exp(r * dt / 2)) / (np.exp(sigma * np.sqrt(dt / 2)) - np.exp(-sigma * np.sqrt(dt / 2))))**2
    p_m = 1 - p_u - p_d  # Middle probability
    
    stock_prices = np.zeros((2 * N + 1, N + 1))
    option_values = np.zeros((2 * N + 1, N + 1))
    
    for i in range(2 * N + 1):
        stock_prices[i, N] = S * (u ** (i - N))
    
    if option_type == "call":
        option_values[:, N] = np.maximum(stock_prices[:, N] - K, 0)
    else:
        option_values[:, N] = np.maximum(K - stock_prices[:, N], 0)
    
    for j in range(N - 1, -1, -1):
        for i in range(1, 2 * j + 1):
            option_values[i, j] = np.exp(-r * dt) * (
                p_u * option_values[i + 1, j + 1] +
                p_m * option_values[i, j + 1] +
                p_d * option_values[i - 1, j + 1]
            )
    
    return option_values[N, 0]

def generate_heatmap(S_min, S_max, sigma_min, sigma_max, S, K, T, r, sigma, N, option_type):
    S_range = np.linspace(S_min, S_max, 10)
    sigma_range = np.linspace(sigma_min, sigma_max, 10)
    prices = np.zeros((len(S_range), len(sigma_range)))
    
    for i, S in enumerate(S_range):
        for j, sigma in enumerate(sigma_range):
            prices[i, j] = trinomial_model(S, K, T, r, sigma, N, option_type)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(prices, yticklabels=np.round(S_range, 2), xticklabels=np.round(sigma_range, 2), annot=True, fmt=".2f", ax=ax)
    ax.set_xlabel("Volatility (σ)")
    ax.set_ylabel("Stock Price (S)")
    ax.set_title("Trinomial Option Pricing Model")
    return fig

def create_sidebar():
    # Navigation
    selected_model = st.sidebar.selectbox(
        "Navigate to",
        ["Black Scholes Option Pricing Model", "Binomial Options Pricing Model", "Trinomial Options Pricing Model"],
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
    params["S"] = st.sidebar.number_input("Current Stock Price (S)", min_value=0.0, value=100.0)
    params["K"] = st.sidebar.number_input("Strike Price (K)", min_value=0.0, value=100.0)
    params["T"] = st.sidebar.number_input("Time to Maturity (T in years)", min_value=0.01, value=1.0)
    params["r"] = st.sidebar.number_input("Risk-Free Interest Rate (r as decimal)", min_value=0.0, value=0.05)
    params["sigma"] = st.sidebar.number_input("Volatility (σ as decimal)", min_value=0.01, value=0.2)
    params["N"] = int(st.sidebar.slider("Number of N in Tree", min_value=10, max_value=500, value=50))
    params["option_type"] = st.sidebar.radio("Option Type", ("call", "put"))

    # Heatmap Configuration
    st.sidebar.header("Heatmap Configuration")
    params["S_min"] = st.sidebar.number_input("Min Stock Price (S_min)", min_value=0.01, value=params["S"] * 0.8, step = 0.01)
    params["S_max"] = st.sidebar.number_input("Max Stock Price (S_max)", min_value=0.01, value=params["S"] * 1.2, step = 0.01)
    params["sigma_min"] = st.sidebar.number_input("Min Volatility (σ_min)", min_value=0.01, max_value=1.0, value = params["sigma"] *0.5, step = 0.01)
    params["sigma_max"] = st.sidebar.number_input("Max Volatility (σ_max)",  min_value=0.01, max_value=1.0, value = params["sigma"] *1.5, step = 0.01)

    return params

st.title("Trinomial Multi-Step Option Pricing Calculator")

st.markdown("""***The trinomial option pricing model is an option pricing model incorporating three possible values that an underlying asset can have in one time period. The three possible values the underlying asset can have in a time period may be greater than, the same as, or less than the current value.***""")

params = create_sidebar()

price = trinomial_model(
    float(params["S"]),
    float(params["K"]),
    float(params["T"]),
    float(params["r"]),
    float(params["sigma"]),
    int(params["N"]),  # Ensure N is an integer
    params["option_type"]
)

st.success(f"The {params['option_type']} option price(according to given input parameters) is: ${price:.2f}")

# Generate and display heatmap
fig = generate_heatmap(
    float(params["S_min"]),
    float(params["S_max"]),
    float(params["sigma_min"]),
    float(params["sigma_max"]),
    float(params["S"]),
    float(params["K"]),
    float(params["T"]),
    float(params["r"]),
    float(params["sigma"]),
    int(params["N"]),
    params["option_type"]
)
st.pyplot(fig)

st.markdown("""---""")
st.subheader(""" ***Assumptions of the Trinomial Model*** """)

st.markdown(""" 
- **Three Possible Movements:** The Trinomial Model assumes the underlying asset price can move up, down, or stay the same in each time step.
- **Risk-Neutral Valuation:** It uses a risk-neutral measure to discount future payoffs.
- **No Arbitrage:** The model assumes no arbitrage opportunities exist in the market.
- **Improved Stability:** The Trinomial Model is more stable than the Binomial Model, especially for large steps.
- **European and American Options:** The model can price both European and American options.
- **Constant volatility:** The volatility of the underlying asset is assumed to be constant throughout the option's life.
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