import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Page configuration
st.set_page_config(
    page_title="Binomial Options Pricing Model",
    page_icon="📈",
    menu_items={"Get Help": None, "Report a Bug": None, "About": None}
)

if st.sidebar.button("🏠 Home", use_container_width=True):
    st.switch_page("app.py")

def binomial_model(S, K, T, r, sigma, N, option_type="call"):
    dt = T / N  # Time step
    u = np.exp(sigma * np.sqrt(dt))  # Up factor
    d = 1 / u  # Down factor
    p = (np.exp(r * dt) - d) / (u - d)  # Risk-neutral probability
    
    stock_prices = np.zeros((N + 1, N + 1))
    option_values = np.zeros((N + 1, N + 1))
    
    for i in range(N + 1):
        for j in range(i + 1):
            stock_prices[j, i] = S * (u ** (i - j)) * (d ** j)
    
    if option_type == "call":
        option_values[:, N] = np.maximum(stock_prices[:, N] - K, 0)
    else:
        option_values[:, N] = np.maximum(K - stock_prices[:, N], 0)
    
    for i in range(N - 1, -1, -1):
        for j in range(i + 1):
            option_values[j, i] = np.exp(-r * dt) * (p * option_values[j, i + 1] + (1 - p) * option_values[j + 1, i + 1])
    
    return option_values[0, 0]

def generate_heatmap(S_min, S_max, sigma_min, sigma_max, K, T, r,sigma, N, option_type):
    S_range = np.linspace(S_min, S_max, 10)
    sigma_range = np.linspace(sigma_min, sigma_max, 10)
    prices = np.zeros((len(S_range), len(sigma_range)))
    
    for i, S_val in enumerate(S_range):
        for j, sigma_val in enumerate(sigma_range):
            prices[i, j] = binomial_model(S_val, K, T, r, sigma_val,N, option_type)

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(prices, yticklabels=np.round(S_range, 2), xticklabels=np.round(sigma_range, 2), annot=True, fmt=".2f", ax=ax)
    ax.set_xlabel("Volatility (σ)")
    ax.set_ylabel("Stock Price (S)")
    ax.set_title("Binomial Option Pricing Model")
    return fig

def create_sidebar():
    # Navigation
    selected_model = st.sidebar.selectbox(
        "Navigate to",
        ["Black Scholes Option Pricing Model", "Binomial Options Pricing Model", "Trinomial Options Pricing Model"],
        index=1
    )

    if selected_model == "Black Scholes Option Pricing Model":
        st.switch_page("pages/1_black-scholes-model.py")
    elif selected_model == "Trinomial Options Pricing Model":
        st.switch_page("pages/3_trinomial-model.py")

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

# Main content
st.title("Binomial Options Pricing Calculator")

st.markdown("""***The Binomial Options Pricing Model is a numerical method for valuing options by simulating different possible paths that the underlying asset price can take.***""")

# Get parameters from sidebar
params = create_sidebar()

# Calculate and display option price
price = binomial_model(
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
    float(params["K"]),
    float(params["T"]),
    float(params["r"]),
    float(params["sigma"]),  # Missing sigma argument added
    int(params["N"]),        # Ensure N is an integer
    params["option_type"]    # Add this missing argument
)
st.pyplot(fig)

# Additional information
st.markdown("""---""")
st.subheader(""" ***Assumptions of the Binomial Model*** """)

st.markdown(""" 
- **Discrete Time N:** The Binomial Model assumes the price of the underlying asset can only move up or down by a fixed factor in each time step.
- **Risk-Neutral Valuation:** It uses a risk-neutral measure to discount future payoffs.
- **No Arbitrage:** The model assumes no arbitrage opportunities exist in the market.
- **Constant Volatility:** The volatility of the underlying asset is assumed to remain constant over the option's life.
- **European and American Options:** The model can price both European and American options.
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