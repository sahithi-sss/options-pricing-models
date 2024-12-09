    try:
            # Load image
            original_image = Image.open("b-img.jpg")
            original_image = original_image.resize((1600, 900), Image.LANCZOS)
            
            # Convert to PhotoImage
            self.bg_image = ImageTk.PhotoImage(original_image)
            
            # Create a canvas to hold the background image
            self.bg_canvas = tk.Canvas(self.root, width=1600, height=900, highlightthickness=0)
            self.bg_canvas.pack(fill=tk.BOTH, expand=True)
            
            # Add the background image to the canvas
            self.bg_canvas.create_image(0, 0, anchor=tk.NW, image=self.bg_image)
            
            # Move the background canvas to the bottom of the widget stack
            self.bg_canvas.lower()
        except Exception as e:
            print(f"Background image error: {e}")
            # Fallback to a solid color background
            self.root.configure(bg='#1c1c1c')
