import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

class BlackScholesREPL:
    def __init__(self):
        # Default values
        self.S = 100.0  # Stock price
        self.K = 100.0  # Strike price
        self.T = 30.0   # Time to maturity (days)
        self.r = 5.0    # Interest rate (%)
        self.sigma = 20.0  # Volatility (%)
        self.option_type = "call"
        
        self.plot_params = {
            "Stock Price ($)": (lambda: self.S, 1, 1000),
            "Strike Price ($)": (lambda: self.K, 1, 1000),
            "Time to Maturity (Days)": (lambda: self.T, 1, 365),
            "Interest Rate (%)": (lambda: self.r, 1, 30),
            "Volatility (%)": (lambda: self.sigma, 1, 250),
            "Option Price ($)": (None, None, None)
        }
        
        self.commands = {
            'help': self.show_help,
            'show': self.show_current_values,
            'set': self.set_parameter,
            'calculate': self.calculate_price,
            'plot': self.create_3d_plot,
            'exit': self.exit_repl
        }

    def black_scholes(self, S, K, T, r, sigma, option_type="call"):
        T = T / 365.0  # Convert days to years
        r = r / 100.0  # Convert percentage to decimal
        sigma = sigma / 100.0  # Convert percentage to decimal
        
        d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        
        if option_type == "call":
            price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
        else:
            price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
        
        return price

    def show_help(self, *args):
        help_text = """
Black-Scholes Option Calculator Commands:
---------------------------------------
help                - Show this help message
show               - Display current parameter values
set <param> <value> - Set parameter value
                    Valid parameters: stock, strike, time, rate, vol, type
                    For type, use 'call' or 'put'
calculate          - Calculate option price with current parameters
plot x y          - Create 3D plot with specified x and y axes
                    Valid axes: stock, strike, time, rate, vol
exit               - Exit the calculator

Example usage:
-------------
set stock 100
set type put
calculate
plot stock vol
"""
        print(help_text)

    def show_current_values(self, *args):
        print("\nCurrent Parameters:")
        print(f"Stock Price: ${self.S:.2f}")
        print(f"Strike Price: ${self.K:.2f}")
        print(f"Time to Maturity: {self.T:.1f} days")
        print(f"Interest Rate: {self.r:.1f}%")
        print(f"Volatility: {self.sigma:.1f}%")
        print(f"Option Type: {self.option_type}")

    def set_parameter(self, *args):
        if len(args) < 2:
            print("Error: Please specify parameter and value")
            return

        param, value = args[0], args[1]
        try:
            if param == "stock":
                self.S = float(value)
            elif param == "strike":
                self.K = float(value)
            elif param == "time":
                self.T = float(value)
            elif param == "rate":
                self.r = float(value)
            elif param == "vol":
                self.sigma = float(value)
            elif param == "type":
                if value.lower() not in ["call", "put"]:
                    raise ValueError("Option type must be 'call' or 'put'")
                self.option_type = value.lower()
            else:
                print(f"Unknown parameter: {param}")
                return
            print(f"Set {param} to {value}")
        except ValueError as e:
            print(f"Error: Invalid value - {e}")

    def calculate_price(self, *args):
        try:
            price = self.black_scholes(
                self.S, self.K, self.T, self.r, self.sigma, self.option_type
            )
            print(f"\nOption Price: ${price:.2f}")
        except Exception as e:
            print(f"Error calculating price: {e}")

    def create_3d_plot(self, *args):
        if len(args) < 2:
            print("Error: Please specify x and y axes")
            return

        param_map = {
            "stock": "Stock Price ($)",
            "strike": "Strike Price ($)",
            "time": "Time to Maturity (Days)",
            "rate": "Interest Rate (%)",
            "vol": "Volatility (%)"
        }

        try:
            x_param = param_map[args[0]]
            y_param = param_map[args[1]]
        except KeyError:
            print("Invalid parameter. Use: stock, strike, time, rate, vol")
            return

        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')

        x_getter, x_min, x_max = self.plot_params[x_param]
        y_getter, y_min, y_max = self.plot_params[y_param]

        x_range = np.linspace(x_min, x_max, 30)
        y_range = np.linspace(y_min, y_max, 30)
        X, Y = np.meshgrid(x_range, y_range)

        Z = np.zeros_like(X)
        original_x = x_getter()
        original_y = y_getter()

        for i in range(len(x_range)):
            for j in range(len(y_range)):
                if x_param == "Stock Price ($)":
                    self.S = X[j, i]
                elif x_param == "Strike Price ($)":
                    self.K = X[j, i]
                elif x_param == "Time to Maturity (Days)":
                    self.T = X[j, i]
                elif x_param == "Interest Rate (%)":
                    self.r = X[j, i]
                elif x_param == "Volatility (%)":
                    self.sigma = X[j, i]

                if y_param == "Stock Price ($)":
                    self.S = Y[j, i]
                elif y_param == "Strike Price ($)":
                    self.K = Y[j, i]
                elif y_param == "Time to Maturity (Days)":
                    self.T = Y[j, i]
                elif y_param == "Interest Rate (%)":
                    self.r = Y[j, i]
                elif y_param == "Volatility (%)":
                    self.sigma = Y[j, i]

                Z[j, i] = self.black_scholes(
                    self.S, self.K, self.T, self.r, self.sigma, self.option_type
                )

        # Restore original values
        if x_param == "Stock Price ($)":
            self.S = original_x
        elif x_param == "Strike Price ($)":
            self.K = original_x
        elif x_param == "Time to Maturity (Days)":
            self.T = original_x
        elif x_param == "Interest Rate (%)":
            self.r = original_x
        elif x_param == "Volatility (%)":
            self.sigma = original_x

        if y_param == "Stock Price ($)":
            self.S = original_y
        elif y_param == "Strike Price ($)":
            self.K = original_y
        elif y_param == "Time to Maturity (Days)":
            self.T = original_y
        elif y_param == "Interest Rate (%)":
            self.r = original_y
        elif y_param == "Volatility (%)":
            self.sigma = original_y

        surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm)
        ax.set_xlabel(x_param)
        ax.set_ylabel(y_param)
        ax.set_zlabel('Option Price ($)')
        plt.colorbar(surf)
        plt.show()

    def exit_repl(self, *args):
        print("\nExiting Black-Scholes Calculator. Goodbye!")
        exit()

    def run(self):
        print("\nWelcome to the Black-Scholes Option Calculator!")
        print("Type 'help' for available commands.")
        
        while True:
            try:
                command = input("\n> ").strip().lower().split()
                if not command:
                    continue
                
                cmd = command[0]
                args = command[1:]
                
                if cmd in self.commands:
                    self.commands[cmd](*args)
                else:
                    print(f"Unknown command: {cmd}")
                    print("Type 'help' for available commands.")
            
            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except Exception as e:
                print(f"Error: {e}")

def main():
    calculator = BlackScholesREPL()
    calculator.run()

if __name__ == "__main__":
    main()