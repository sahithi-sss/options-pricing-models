import tkinter as tk
from tkinter import ttk
from tkinter import messagebox  
import os
import subprocess
import sys

class OptionPricingGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Option Pricing Models")
        self.root.geometry("800x600")
        self.root.configure(bg='black')
        
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width/2) - (800/2)
        y = (screen_height/2) - (600/2)
        self.root.geometry(f'800x600+{int(x)}+{int(y)}')

        container = tk.Frame(root, bg='black')
        container.pack(fill='both', expand=True, padx=20, pady=20)
        
        intro_text = """Option pricing is a fundamental concept in financial mathematics that determines the fair value of financial derivatives. 
These mathematical models help traders and investors calculate theoretical values of options based on various factors like underlying asset price, 
strike price, time to expiration, volatility, and interest rates. Different models account for various market conditions and assumptions: 
Black-Scholes assumes log-normal distribution and constant volatility, Heston model incorporates stochastic volatility, 
while Monte Carlo methods use simulation for complex scenarios. Jump diffusion models account for sudden price movements, 
and tree models (binomial/trinomial) provide discrete-time approximations. Understanding these models is crucial for risk management 
and trading strategies in options markets."""
        
        title_label = tk.Label(
            container,
            text="Option Pricing Models",
            bg='black',
            fg='white',
            font=('Arial', 16, 'bold')
        )
        title_label.pack(pady=(0, 20))

        intro_label = tk.Label(
            container,
            text=intro_text,
            bg='black',
            fg='white',
            wraplength=700,
            justify="left",
            font=('Arial', 11)
        )
        intro_label.pack(pady=(0, 30))
        
        separator = ttk.Separator(container, orient='horizontal')
        separator.pack(fill='x', pady=20)

        self.models = {
            "Black Scholes Option Pricing Model": "black-scholes-option-pricing-model.py",
            "Binomial Options Pricing Model": "binomial-options-pricing-model.py",
            "Heston Stochastic Volatility Model": "heston-stochastic-volatility-model.py",
            "Merton Jump Diffusion Model": "merton-jump-diffusion-model.py",
            "Trinomial Tree Model": "trinomial-tree-model.py",
            "Monte Carlo Simulation": "monte-carlo-simulation.py"
        }
        
        links_frame = tk.Frame(container, bg='black')
        links_frame.pack(fill='x')
        
        for model_name, file_name in self.models.items():
            link = tk.Label(
                links_frame,
                text=model_name,
                bg='black',
                fg='white',
                cursor='hand2',
                font=('Arial', 12, 'underline')
            )
            link.pack(pady=8)
            
            link.bind('<Enter>', lambda e, l=link: l.configure(fg='blue'))
            link.bind('<Leave>', lambda e, l=link: l.configure(fg='white'))
            link.bind('<Button-1>', lambda e, f=file_name: self.execute_file(f))
    
    def execute_file(self, filename):
        try:
            file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
            
            if not os.path.exists(file_path):
                messagebox.showerror("Error", f"File not found: {filename}")
                return
                
            if sys.platform == 'win32':
                subprocess.Popen([sys.executable, file_path], creationflags=subprocess.CREATE_NEW_CONSOLE)
            else:  # For Unix-based systems
                subprocess.Popen([sys.executable, file_path])
                
        except Exception as e:
            messagebox.showerror("Error", f"Error executing file: {e}")

def main():
    root = tk.Tk()
    app = OptionPricingGUI(root)
    root.mainloop()

main()