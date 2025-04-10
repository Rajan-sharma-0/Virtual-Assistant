import tkinter as tk
from tkinter import ttk, scrolledtext, Canvas
import threading
import time
import math
from PIL import Image, ImageTk, ImageDraw
import os
import colorsys
import random

class ModernUI(tk.Canvas):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.configure(bg='#0A0A0A', highlightthickness=0)
        self.particles = []
        self.animate_particles()
        
    def create_particle(self):
        return {
            'x': random.randint(0, self.winfo_width()),
            'y': random.randint(0, self.winfo_height()),
            'size': random.randint(2, 4),
            'speed': random.uniform(0.5, 2),
            'angle': random.uniform(0, 2 * math.pi)
        }
        
    def animate_particles(self):
        self.delete('particle')
        
        for p in self.particles:
            p['y'] += math.sin(p['angle']) * p['speed']
            p['x'] += math.cos(p['angle']) * p['speed']
            
            if p['x'] < 0 or p['x'] > self.winfo_width() or \
               p['y'] < 0 or p['y'] > self.winfo_height():
                self.particles.remove(p)
                self.particles.append(self.create_particle())
                
            self.create_circle(p['x'], p['y'], p['size'], '#1A1A1A')
            
        self.after(50, self.animate_particles)
        
    def create_circle(self, x, y, r, color):
        self.create_oval(x-r, y-r, x+r, y+r, fill=color, outline='')

class VirtualAssistantUI:
    def __init__(self, root):
        # Initialize variables first
        self.is_listening = False
        self.assistant = None
        self.animation_speed = 50
        self.matrix_symbols = []
        
        # Update theme colors
        self.colors = {
            'bg_dark': '#121212',
            'bg_medium': '#1E1E1E',
            'bg_light': '#2D2D2D',
            'accent': '#00FF44',
            'text': '#E0E0E0',
            'highlight': '#00FF88'
        }
        
        # Then set up the window
        self.root = root
        self.root.title("ECHO ")
        self.root.geometry("1200x800")
        self.root.configure(bg=self.colors['bg_dark'])
        
        # Create UI elements
        self.matrix_canvas = self.create_matrix_background()
        self.container = self.create_glass_container()
        self.create_animated_header()
        self.create_voice_animation()
        self.animate_voice()
        self.create_audio_visualizer()
        self.create_enhanced_output()
        self.create_modern_controls()

    def create_matrix_background(self):
        canvas = tk.Canvas(self.root, bg='#0A0A0A', highlightthickness=0)
        canvas.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        # Initialize matrix symbols list
        self.matrix_symbols = []
        
        # Create initial symbols
        self.init_matrix_symbols(canvas)
        
        return canvas

    def init_matrix_symbols(self, canvas):
        """Initialize matrix symbols with the canvas parameter"""
        for i in range(50):
            x = random.randint(0, 1200)
            y = random.randint(0, 800)
            symbol = canvas.create_text(
                x, y,
                text=chr(random.randint(0x30A0, 0x30FF)),
                font=('Arial', 14),
                fill='#00FF00'
            )
            self.matrix_symbols.append({
                'symbol': symbol,
                'speed': random.uniform(1, 5),
                'canvas': canvas  # Store canvas reference
            })
        
        # Start animation after symbols are created
        self.animate_matrix()

    def animate_matrix(self):
        """Animate matrix symbols using stored canvas reference"""
        for symbol in self.matrix_symbols:
            canvas = symbol['canvas']  # Get canvas reference
            y = canvas.coords(symbol['symbol'])[1]
            if y > 800:
                canvas.coords(
                    symbol['symbol'],
                    random.randint(0, 1200),
                    0
                )
            else:
                canvas.move(
                    symbol['symbol'],
                    0,
                    symbol['speed']
                )
        self.root.after(50, self.animate_matrix)

    def create_glass_container(self):
        # Create main container
        container = tk.Frame(self.root, bg=self.colors['bg_medium'])
        container.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)
        
        # Create layered glass effect using canvas
        glass_overlay = tk.Canvas(
            container,
            bg=self.colors['bg_medium'],
            highlightthickness=0
        )
        glass_overlay.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        # Add subtle glass highlights
        for i in range(3):
            # Create gradient effect
            y_offset = i * 50
            glass_overlay.create_rectangle(
                0, y_offset,
                glass_overlay.winfo_reqwidth(), y_offset + 100,
                fill=f'#{30+i*10:02x}{30+i*10:02x}{30+i*10:02x}',
                outline='',
                stipple='gray50'  # Creates a transparent effect
            )
        
        # Add subtle border
        border = tk.Frame(
            container,
            bg=self.colors['bg_light'],
            highlightthickness=1,
            highlightbackground=self.colors['bg_light']
        )
        border.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        return container

    def create_animated_header(self):
        self.header = tk.Label(
            self.container,
            text="ECHO AI ASSISTANT",
            font=('Orbitron', 24, 'bold'),
            bg=self.colors['bg_medium'],
            fg=self.colors['accent']
        )
        self.header.place(relx=0.05, relwidth=0.9, relheight=0.02)
        self.animate_header_color()

    def create_audio_visualizer(self):
        self.viz_canvas = tk.Canvas(
            self.container,
            bg=self.colors['bg_medium'],
            highlightthickness=0,
            height=100
        )
        self.viz_canvas.place(relx=0.05, relwidth=0.9)
        
        # Create circular visualizer
        self.viz_elements = []
        center_x, center_y = 400, 50
        for i in range(32):
            angle = (2 * math.pi * i) / 32
            x = center_x + 30 * math.cos(angle)
            y = center_y + 30 * math.sin(angle)
            line = self.viz_canvas.create_line(
                center_x, center_y, x, y,
                fill=self.colors['accent'],
                width=2
            )
            self.viz_elements.append(line)
        
        self.animate_visualizer()

    def create_voice_animation(self):
        # Create animation container
        self.voice_frame = tk.Frame(
            self.container,
            bg=self.colors['bg_medium'],
            height=80
        )
        self.voice_frame.place(relx=0.25, rely=0.12, relwidth=0.5)
        
        # Create animation canvas
        self.voice_canvas = tk.Canvas(
            self.voice_frame,
            bg=self.colors['bg_medium'],
            highlightthickness=0,
            height=80
        )
        self.voice_canvas.pack(fill=tk.BOTH, expand=True)
        
        # Create voice bars
        self.voice_bars = []
        num_bars = 20
        bar_width = 8
        bar_spacing = 15
        
        for i in range(num_bars):
            x = (i * (bar_width + bar_spacing)) + 50
            bar = self.voice_canvas.create_line(
                x, 40, x, 40,  # Initial position (compressed)
                fill=self.colors['accent'],
                width=bar_width,
                capstyle=tk.ROUND
            )
            self.voice_bars.append({
                'shape': bar,
                'phase': i * (math.pi / 8),
                'frequency': random.uniform(2, 4)
            })

    def animate_voice(self):
        if self.is_listening:
            t = time.time()
            for bar in self.voice_bars:
                # Create complex wave pattern
                wave = math.sin(t * bar['frequency'] + bar['phase'])
                amplitude = 20 * abs(wave)  # Max height of 20 pixels
                
                # Get bar position
                x1, _, x2, _ = self.voice_canvas.coords(bar['shape'])
                
                # Update bar height
                self.voice_canvas.coords(
                    bar['shape'],
                    x1, 40 - amplitude,  # Top point
                    x2, 40 + amplitude   # Bottom point
                )
                
                # Update bar color based on amplitude
                intensity = int(127 + 128 * abs(wave))
                color = f'#{0:02x}{intensity:02x}{0:02x}'
                self.voice_canvas.itemconfig(bar['shape'], fill=color)
        else:
            # Reset bars to center when not listening
            for bar in self.voice_bars:
                x1, _, x2, _ = self.voice_canvas.coords(bar['shape'])
                self.voice_canvas.coords(bar['shape'], x1, 40, x2, 40)
                self.voice_canvas.itemconfig(bar['shape'], fill=self.colors['accent'])
        
        self.root.after(50, self.animate_voice)

    def create_enhanced_output(self):
        output_frame = tk.Frame(self.container, bg=self.colors['bg_medium'])
        output_frame.place(relx=0.05, rely=0.25, relwidth=0.9, relheight=0.6)
        
        # Modern title bar
        title_bar = tk.Frame(output_frame, bg=self.colors['bg_light'])
        title_bar.pack(fill=tk.X, pady=(0, 1))
        
        tk.Label(
            title_bar,
            text="⚡ Console Output",
            font=('JetBrains Mono', 10),
            bg=self.colors['bg_light'],
            fg=self.colors['accent']
        ).pack(side=tk.LEFT, padx=10, pady=5)
        
        # Enhanced output area
        self.output_area = scrolledtext.ScrolledText(
            output_frame,
            font=('JetBrains Mono', 11),
            bg=self.colors['bg_light'],
            fg=self.colors['accent'],
            insertbackground=self.colors['accent'],
            relief=tk.FLAT,
            pady=10,
            padx=10
        )
        self.output_area.pack(fill=tk.BOTH, expand=True)

    def create_modern_controls(self):
        control_frame = tk.Frame(self.container, bg=self.colors['bg_medium'])
        control_frame.place(relx=0.05, rely=0.88, relwidth=0.9, relheight=0.1)
        
        # Status indicator with pulse effect
        self.status_dot = tk.Canvas(
            control_frame,
            width=12,
            height=12,
            bg=self.colors['bg_medium'],
            highlightthickness=0
        )
        self.status_dot.pack(side=tk.LEFT, padx=5)
        self.status_indicator = self.status_dot.create_oval(
            2, 2, 10, 10,
            fill='#FF4444'
        )
        
        # Status label
        self.status_label = tk.Label(
            control_frame,
            text="Status: Ready",
            font=('JetBrains Mono', 11),
            bg=self.colors['bg_medium'],
            fg=self.colors['accent']
        )
        self.status_label.pack(side=tk.LEFT, padx=5)
        
        # Modern buttons with hover effects
        button_frame = tk.Frame(control_frame, bg=self.colors['bg_medium'])
        button_frame.pack(side=tk.RIGHT)
        
        self.start_button = self.create_hover_button(
            button_frame,
            "⏵ START",
            self.start_listening,
            self.colors['accent']
        )
        self.stop_button = self.create_hover_button(
            button_frame,
            "⏹ STOP",
            self.stop_listening,
            '#FF4444'
        )
        self.stop_button.configure(state='disabled')

    def create_hover_button(self, parent, text, command, color):
        frame = tk.Frame(parent, bg=self.colors['bg_medium'])
        frame.pack(side=tk.LEFT, padx=5)
        
        btn = tk.Canvas(
            frame,
            width=120,
            height=35,
            bg=self.colors['bg_medium'],
            highlightthickness=0
        )
        btn.pack()
        
        def draw_button(hover=False):
            btn.delete('all')
            if hover:
                # Glow effect
                btn.create_rectangle(
                    2, 2, 118, 33,
                    fill=self.colors['bg_light'],
                    outline=self.colors['accent'],
                    width=2
                )
            else:
                btn.create_rectangle(
                    2, 2, 118, 33,
                    fill=self.colors['bg_medium'],
                    outline=self.colors['accent'],
                    width=1
                )
            btn.create_text(
                60, 17,
                text=text,
                fill=self.colors['accent'],
                font=('JetBrains Mono', 11, 'bold')
            )
        
        draw_button()
        btn.bind('<Enter>', lambda e: draw_button(True))
        btn.bind('<Leave>', lambda e: draw_button(False))
        btn.bind('<Button-1>', lambda e: command())
        
        return btn

    def animate_header_color(self):
        colors = [self.colors['accent'], '#00CC00', '#009900', '#00CC00']
        def update_color(index=0):
            self.header.configure(fg=colors[index])
            self.root.after(500, update_color, (index + 1) % len(colors))
        update_color()

    def animate_visualizer(self):
        if self.is_listening:
            t = time.time() * 5
            center_x, center_y = 400, 50
            for i, line in enumerate(self.viz_elements):
                angle = (2 * math.pi * i) / 32
                length = 30 + 10 * math.sin(t + i * 0.2)
                x = center_x + length * math.cos(angle)
                y = center_y + length * math.sin(angle)
                self.viz_canvas.coords(
                    line,
                    center_x,
                    center_y,
                    x,
                    y
                )
        self.root.after(50, self.animate_visualizer)

    def set_assistant(self, assistant):
        self.assistant = assistant
    
    def start_listening(self):
        if not self.is_listening and self.assistant:
            self.is_listening = True
            self.status_label.config(text="Status: Listening...")
            self.update_output("Assistant started listening...")
            self.start_button.config(state='disabled')
            self.stop_button.config(state='normal')
            threading.Thread(target=self.assistant.run, daemon=True).start()

    def stop_listening(self):
        if self.is_listening and self.assistant:
            self.is_listening = False
            self.status_label.config(text="Status: Ready")
            self.update_output("Assistant stopped.")
            self.start_button.config(state='normal')
            self.stop_button.config(state='disabled')
            if self.assistant:
                self.assistant.stop()
    
    def update_output(self, message):
        timestamp = time.strftime("%H:%M:%S")
        self.output_area.insert(tk.END, f"[{timestamp}] {message}\n")
        self.output_area.see(tk.END)

def main():
    root = tk.Tk()
    app = VirtualAssistantUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()