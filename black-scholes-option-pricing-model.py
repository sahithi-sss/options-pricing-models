import tkinter as tk
from tkinter import ttk
import numpy as np
import math
from scipy.stats import norm
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
from PIL import Image, ImageTk
from tkinter import *


class BlackScholesGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Black-Scholes Option Calculator")
        self.root.geometry("1600x900")
        
        # Set dark theme
        self.root.configure(bg='black')
        self.style = ttk.Style()
        self.style.configure('TFrame', background='black')
        self.style.configure('TLabel', background='black', foreground='white', font=('Arial', 12))
        self.style.configure('TRadiobutton', background='black', foreground='white', font=('Arial', 12))
        
        # Custom style for entry widgets
        self.style.configure('Custom.TEntry', 
                              background='white', 
                              foreground='black', 
                              fieldbackground='white')
        self.style.map('Custom.TEntry', 
                       background=[('readonly', 'white')], 
                       fieldbackground=[('readonly', 'white')])

        # Create main frames
        self.sidebar = ttk.Frame(root, padding="10", style='TFrame')
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        
        self.text_panel = ttk.Frame(root, padding="10", style='TFrame')
        self.text_panel.pack(side=tk.LEFT, fill=tk.Y)
        
        self.main_panel = ttk.Frame(root, padding="10", style='TFrame')
        self.main_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Initialize parameters
        self.S = tk.DoubleVar(value=100)  # Stock price
        self.K = tk.DoubleVar(value=100)  # Strike price
        self.T = tk.DoubleVar(value=30)   # Time to maturity
        self.r = tk.DoubleVar(value=5)    # Interest rate
        self.sigma = tk.DoubleVar(value=20)  # Volatility
        self.option_type = tk.StringVar(value="call")

        # Variables for plot axes selection
        self.plot_params = {
            "Stock Price ($)": (self.S, 1, 1000),
            "Strike Price ($)": (self.K, 1, 1000),
            "Time to Maturity (Days)": (self.T, 1, 365),
            "Interest Rate (%)": (self.r, 1, 30),
            "Volatility (%)": (self.sigma, 1, 250),
            "Option Price ($)": (None, None, None)  # Special case for calculated value
        }
        
        self.x_axis = tk.StringVar(value="Stock Price ($)")
        self.y_axis = tk.StringVar(value="Volatility (%)")
        self.z_axis = tk.StringVar(value="Option Price ($)")

        self.create_sidebar()
        self.create_text_panel()
        self.create_main_panel()
        
        # Initial calculation and plot
        self.update_price()
        
    def create_text_panel(self):
        # Detailed explanation with mathematical formula
        info_text = """Black-Scholes Option Pricing Model

The Black-Scholes formula calculates the theoretical price of European-style options, considering multiple key financial parameters.

Formula:
C = S * N(d1) - K * e^(-rT) * N(d2)  [Call Option]
P = K * e^(-rT) * N(-d2) - S * N(-d1)  [Put Option]

Where:
• S = Current stock price
• K = Option strike price
• T = Time to expiration (in years)
• r = Risk-free interest rate
• σ (sigma) = Stock price volatility
• N() = Cumulative standard normal distribution
• e = Mathematical constant (approximately 2.71828)

Calculation Parameters:
d1 = [ln(S/K) + (r + σ²/2)T] / (σ√T)
d2 = d1 - σ√T

Key Model Assumptions:
- Stock prices follow geometric Brownian motion
- No transaction costs or taxes
- Constant risk-free interest rate
- No dividends during option's life
- European-style option (exercisable only at expiration)

Developed by Fischer Black, Myron Scholes, and Robert Merton in the early 1970s, this groundbreaking model revolutionized financial derivatives pricing by providing a mathematical framework to determine theoretical option values."""
        
        info_label = ttk.Label(
            self.text_panel,
            text=info_text,
            style='TLabel',
            justify=tk.LEFT,
            wraplength=400,
            font=('Arial', 12)
        )
        info_label.pack(anchor='w', padx=10)

    def create_sidebar(self):
        # Stock Price Entry
        stock_frame = ttk.Frame(self.sidebar, style='TFrame')
        stock_frame.pack(pady=10)
        ttk.Label(stock_frame, text="Stock Price ($)", style='TLabel').pack(side=tk.LEFT, padx=(0,5))
        stock_entry = ttk.Entry(stock_frame, textvariable=self.S, width=10, style='Custom.TEntry')
        stock_entry.pack(side=tk.LEFT)

        # Strike Price Entry
        strike_frame = ttk.Frame(self.sidebar, style='TFrame')
        strike_frame.pack(pady=10)
        ttk.Label(strike_frame, text="Strike Price ($)", style='TLabel').pack(side=tk.LEFT, padx=(0,5))
        strike_entry = ttk.Entry(strike_frame, textvariable=self.K, width=10, style='Custom.TEntry')
        strike_entry.pack(side=tk.LEFT)

        # Time to Maturity Slider
        time_frame = ttk.Frame(self.sidebar, style='TFrame')
        time_frame.pack(pady=10)
        ttk.Label(time_frame, text="Time to Maturity (Days)", style='TLabel').pack()
        time_slider = tk.Scale(
            time_frame,
            from_=1,
            to=365,
            variable=self.T,
            orient=tk.HORIZONTAL,
            command=self.schedule_update,
            length=200,
            resolution=0.5,
            bg='#2b2b2b',
            fg='white',
            highlightthickness=0,
            troughcolor='#404040'
        )
        time_slider.pack()

        # Interest Rate Slider
        rate_frame = ttk.Frame(self.sidebar, style='TFrame')
        rate_frame.pack(pady=10)
        ttk.Label(rate_frame, text="Interest Rate (%)", style='TLabel').pack()
        rate_slider = tk.Scale(
            rate_frame,
            from_=1,
            to=30,
            variable=self.r,
            orient=tk.HORIZONTAL,
            command=self.schedule_update,
            length=200,
            resolution=0.5,
            bg='#2b2b2b',
            fg='white',
            highlightthickness=0,
            troughcolor='#404040'
        )
        rate_slider.pack()

        # Volatility Slider
        vol_frame = ttk.Frame(self.sidebar, style='TFrame')
        vol_frame.pack(pady=10)
        ttk.Label(vol_frame, text="Volatility (%)", style='TLabel').pack()
        vol_slider = tk.Scale(
            vol_frame,
            from_=1,
            to=250,
            variable=self.sigma,
            orient=tk.HORIZONTAL,
            command=self.schedule_update,
            length=200,
            resolution=0.5,
            bg='#2b2b2b',
            fg='white',
            highlightthickness=0,
            troughcolor='#404040'
        )
        vol_slider.pack()

        # Option type toggle
        option_frame = ttk.Frame(self.sidebar, style='TFrame')
        option_frame.pack(pady=20)
        
        ttk.Radiobutton(
            option_frame,
            text="Call Option",
            variable=self.option_type,
            value="call",
            command=self.schedule_update,
            style='TRadiobutton'
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Radiobutton(
            option_frame,
            text="Put Option",
            variable=self.option_type,
            value="put",
            command=self.schedule_update,
            style='TRadiobutton'
        ).pack(side=tk.LEFT, padx=5)

        # Axis selection dropdowns
        axis_frame = ttk.Frame(self.sidebar, style='TFrame')
        axis_frame.pack(pady=20)
        
        ttk.Label(axis_frame, text="3D Plot Axes", style='TLabel').pack()
        
        x_frame = ttk.Frame(axis_frame, style='TFrame')
        x_frame.pack(pady=5)
        ttk.Label(x_frame, text="X-axis:", style='TLabel').pack(side=tk.LEFT)
        x_dropdown = ttk.Combobox(x_frame, textvariable=self.x_axis, values=list(self.plot_params.keys()))
        x_dropdown.pack(side=tk.LEFT)
        x_dropdown.bind('<<ComboboxSelected>>', self.schedule_update)

        y_frame = ttk.Frame(axis_frame, style='TFrame')
        y_frame.pack(pady=5)
        ttk.Label(y_frame, text="Y-axis:", style='TLabel').pack(side=tk.LEFT)
        y_dropdown = ttk.Combobox(y_frame, textvariable=self.y_axis, values=list(self.plot_params.keys()))
        y_dropdown.pack(side=tk.LEFT)
        y_dropdown.bind('<<ComboboxSelected>>', self.schedule_update)

        z_frame = ttk.Frame(axis_frame, style='TFrame')
        z_frame.pack(pady=5)
        ttk.Label(z_frame, text="Z-axis:", style='TLabel').pack(side=tk.LEFT)
        z_dropdown = ttk.Combobox(z_frame, textvariable=self.z_axis, values=list(self.plot_params.keys()))
        z_dropdown.pack(side=tk.LEFT)
        z_dropdown.bind('<<ComboboxSelected>>', self.schedule_update)

        # Add Go button
        go_frame = ttk.Frame(self.sidebar, style='TFrame')
        go_frame.pack(pady=20)
        go_button = tk.Button(
            go_frame, 
            text="Refresh", 
            command=self.manual_update,
            bg='#4CAF50',
            fg='white',
            font=('Arial', 12)
        )
        go_button.pack()

    def create_main_panel(self):
        # Price display
        self.price_label = ttk.Label(
            self.main_panel,
            text="Option Price: $0.00",
            font=('Arial', 20, 'bold'),
            style='TLabel'
        )
        self.price_label.pack(pady=20)

        # Create figure for 3D plot with dark theme
        self.fig = plt.Figure(figsize=(8, 6), facecolor='black')
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.main_panel)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Add navigation toolbar for graph interaction
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.main_panel)
        self.toolbar.update()
        self.toolbar.pack(side=tk.BOTTOM, fill=tk.X)

    def manual_update(self):
        self.update_price(force_update=True)

    def black_scholes(self, S, K, T, r, sigma, option_type="call"):
        T = T / 365.0  # Convert days to years
        r = r / 100.0  # Convert percentage to decimal
        sigma = sigma / 100.0  # Convert percentage to decimal
        
        d1 = (math.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * math.sqrt(T))
        d2 = d1 - sigma * math.sqrt(T)
        
        if option_type == "call":
            price = S * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2)
        else:
            price = K * math.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
        
        return price

    def schedule_update(self, *args):
        if hasattr(self, '_update_job'):
            self.root.after_cancel(self._update_job)
        self._update_job = self.root.after(100, self.update_price)

    def update_price(self, force_update=False):
        try:
            price = self.black_scholes(
                self.S.get(),
                self.K.get(),
                self.T.get(),
                self.r.get(),
                self.sigma.get(),
                self.option_type.get()
            )
            self.price_label.config(text=f"Option Price: ${price:.2f}")
            if force_update or not hasattr(self, 'last_price'):
                self.update_plot()
            self.last_price = price
        except Exception as e:
            print(f"Error calculating price: {e}")

    def update_plot(self):
        try:
            self.fig.clear()
            ax = self.fig.add_subplot(111, projection='3d')
            ax.set_facecolor('black')
            self.fig.patch.set_facecolor('black')

            x_param = self.x_axis.get()
            y_param = self.y_axis.get()
            z_param = self.z_axis.get()
            
            if len({x_param, y_param, z_param}) < 3:
                return  # Don't update if parameters are not unique

            x_var, x_min, x_max = self.plot_params[x_param]
            y_var, y_min, y_max = self.plot_params[y_param]

            x_range = np.linspace(x_min, x_max, 30)
            y_range = np.linspace(y_min, y_max, 30)
            X, Y = np.meshgrid(x_range, y_range)

            Z = np.zeros_like(X)
            for i in range(len(x_range)):
                for j in range(len(y_range)):
                    x_curr = x_var.get()
                    y_curr = y_var.get()
                    
                    x_var.set(X[j, i])
                    y_var.set(Y[j, i])
                    
                    if z_param == "Option Price ($)":
                        Z[j, i] = self.black_scholes(
                            self.S.get(),
                            self.K.get(),
                            self.T.get(),
                            self.r.get(),
                            self.sigma.get(),
                            self.option_type.get()
                        )
                    else:
                        z_var, _, _ = self.plot_params[z_param]
                        Z[j, i] = z_var.get()
                    
                    x_var.set(x_curr)
                    y_var.set(y_curr)

            surf = ax.plot_surface(
                X, Y, Z,
                cmap=cm.coolwarm,
                linewidth=0,
                antialiased=True
            )

            ax.set_xlabel(x_param, color='white')
            ax.set_ylabel(y_param, color='white')
            ax.set_zlabel(z_param, color='white')
            
            ax.tick_params(axis='x', colors='white')
            ax.tick_params(axis='y', colors='white')
            ax.tick_params(axis='z', colors='white')
            
            colorbar = self.fig.colorbar(surf)
            colorbar.ax.yaxis.set_tick_params(color='white')
            plt.setp(plt.getp(colorbar.ax.axes, 'yticklabels'), color='white')
            
            self.canvas.draw()
        except Exception as e:
            print(f"Error updating plot: {e}")
            

def main():
    root = tk.Tk()
    app = BlackScholesGUI(root)
    #bg = PhotoImage(file = "img.jpeg") 
    #label1 = Label( root, image = bg)
    #label1.place(x = 0, y = 0) 
    root.mainloop()

if __name__ == "__main__":
    main()