import math
from scipy.stats import norm
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def black_scholes(S, K, T, r, sigma, option_type="call"):

    d1 = (math.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    
    if option_type == "call":
        # Call option price
        price = S * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2)
    elif option_type == "put":
        # Put option price
        price = K * math.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    else:
        raise ValueError("Invalid option type. Use 'call' or 'put'.")
    
    return price

def generate_heatmap(S_min, S_max, sigma_min, sigma_max):
    S_range = np.linspace(S_min, S_max, 50)
    sigma_range = np.linspace(sigma_min, sigma_max, 50)
    prices = np.zeros((len(S_range), len(sigma_range)))
    
    for i, S in enumerate(S_range):
        for j, sigma in enumerate(sigma_range):
            prices[i, j] = black_scholes(S, 100, 1, 0.05, sigma, "call")
    
    fig, ax = plt.subplots()
    c = ax.imshow(prices, aspect='auto', cmap="RdYlGn", origin='lower', 
                  extent=[sigma_range.min(), sigma_range.max(), S_range.min(), S_range.max()])
    fig.colorbar(c, ax=ax, label="Option Price")
    ax.set_xlabel("Volatility (σ)")
    ax.set_ylabel("Stock Price (S)")
    ax.set_title("Profitability Heatmap (Green = Profitable, Red = Loss)")
    st.pyplot(fig)

st.title("Black-Scholes Option Pricing Calculator")

# Sidebar for input parameters
S = st.sidebar.number_input("Current Stock Price (S)", min_value=0.0, value=100.0, step=1.0)
K = st.sidebar.number_input("Strike Price (K)", min_value=0.0, value=100.0, step=1.0)
T = st.sidebar.number_input("Time to Maturity (T in years)", min_value=0.01, value=1.0, step=0.01)
r = st.sidebar.number_input("Risk-Free Interest Rate (r as decimal)", min_value=0.0, value=0.05, step=0.01)
sigma = st.sidebar.number_input("Volatility (σ as decimal)", min_value=0.01, value=0.2, step=0.01)
option_type = st.sidebar.radio("Option Type", ("call", "put"))

price = black_scholes(S, K, T, r, sigma, option_type)
st.success(f"The {option_type} option price is: ${price:.2f}")

# Sidebar for heatmap configuration
st.sidebar.header("Heatmap Configuration")
S_min = st.sidebar.number_input("Min Stock Price (S_min)", min_value=0.0, value=50.0, step=1.0)
S_max = st.sidebar.number_input("Max Stock Price (S_max)", min_value=S_min+1, value=150.0, step=1.0)
sigma_min = st.sidebar.number_input("Min Volatility (σ_min)", min_value=0.01, value=0.1, step=0.01)
sigma_max = st.sidebar.number_input("Max Volatility (σ_max)", min_value=sigma_min+0.01, value=0.5, step=0.01)

generate_heatmap(S_min, S_max, sigma_min, sigma_max)
