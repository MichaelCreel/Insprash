#!/usr/bin/env python3

import os
import sys
import random
import google.generativeai as genai
import tkinter as tk
import threading
from PIL import Image, ImageTk, ImageDraw, ImageFont

DURATION = 15000 # Duration of splash screen in miliseconds
API_TIMEOUT = 10 # Duration for API Response in seconds
SHOW_ON_ALL_MONITORS = False # Set to True to show splash on all monitors
GRAD_TOP = "#330c5a" # Default top gradient, replaced by gradient_colors file
GRAD_BOTTOM = "#831764" # Default bottom gradient, replaced by gradient_colors file
FALLBACK_TEXTS = [] # Fallbacks if Gemini API does not respond. Received from fallback_lines file
USE_GEMINI = True # Whether to use Gemini for generation, set to False if gemini_api_key is empty
GEMINI_API_KEY = "" # API Key for calling Gemini API, loaded from gemini_api_key file
PROMPT = "Return 'Prompt not loaded'." # Prompt for Gemini API Key call, loaded from prompt file

root = None
background_label = None
screen_width = None
screen_height = None
font = None

# Manages the startup of the application
def main():
    initialize()
    splash("Loading...")

# Initializes necessary values for the application from local files
def initialize():
    load_api_key()
    global GRAD_TOP, GRAD_BOTTOM, FALLBACK_TEXTS

    # Initialize Gradient Colors
    try:
        with open(get_source_path("gradient_colors"), "r") as f:
            lines = f.readlines()
            if len(lines) >= 2:
                top_color = lines[0].strip()
                bottom_color = lines[1].strip()
                
                # Validate hex color format
                if is_valid_hex_color(top_color) and is_valid_hex_color(bottom_color):
                    GRAD_TOP = top_color
                    GRAD_BOTTOM = bottom_color
                else:
                    print(f"Invalid hex color format in gradient_colors file")
            else:
                print(f"gradient_colors file must contain at least 2 lines")
    except Exception as e:
        print(f"Error loading gradient colors: {e}")

    # Initialize Fallback Lines
    try:
        with open(get_source_path("fallback_lines"), "r") as f:
            lines = f.readlines()
            FALLBACK_TEXTS = [line.strip() for line in lines if line.strip()]
            if not FALLBACK_TEXTS:
                FALLBACK_TEXTS = ["Welcome! Let's create something amazing today."]
    except Exception as e:
        print(f"Error loading fallback lines: {e}")
        FALLBACK_TEXTS = ["Welcome! Let's create something amazing today."]

    # Initialize Prompt
    try:
        with open(get_source_path("prompt"), "r") as f:
            lines = f.readlines()
            global PROMPT
            prompt_content = "".join(lines).strip()
            
            # Validate prompt content
            if len(prompt_content) == 0:
                print("Warning: prompt file is empty, using default")
            elif len(prompt_content) > 2000:
                print("Warning: prompt file is very long, may cause API issues")
                PROMPT = prompt_content[:2000]  # Truncate if too long
            else:
                PROMPT = prompt_content
    except Exception as e:
        print(f"Error loading prompt: {e}")
    
    # Initialize Show on All Monitors
    try:
        with open(get_source_path("show_on_all_monitors"), "r") as f:
            line = f.read().strip()
            global SHOW_ON_ALL_MONITORS
            # Handle multiple boolean representations (case-insensitive)
            line_lower = line.lower()
            if line_lower in ["true", "1", "yes", "on", "enabled"]:
                SHOW_ON_ALL_MONITORS = True
            elif line_lower in ["false", "0", "no", "off", "disabled"]:
                SHOW_ON_ALL_MONITORS = False
            else:
                print(f"Invalid value in show_on_all_monitors: '{line}', using default: False")
                SHOW_ON_ALL_MONITORS = False
    except Exception as e:
        print(f"Error loading show_on_all_monitors: {e}")
        SHOW_ON_ALL_MONITORS = False

def update():
    def worker():
        message = generate_text()
        root.after(0, lambda: update_splash(message))
    threading.Thread(target=worker, daemon=True).start()

# Get monitor information for multi-monitor and scaling support
def get_monitor_info():
    """Get information about all monitors and their scaling"""
    monitors = []
    
    try:
        # Try to get monitor info using tkinter (works on most systems)
        temp_root = tk.Tk()
        temp_root.withdraw()  # Hide the temporary window
        
        # Get primary monitor info
        primary_width = temp_root.winfo_screenwidth()
        primary_height = temp_root.winfo_screenheight()
        
        # Get DPI scaling factor
        dpi = temp_root.winfo_fpixels('1i')  # Pixels per inch
        scale_factor = dpi / 96.0  # 96 DPI is standard
        
        # Try to get actual screen dimensions (physical pixels)
        try:
            actual_width = temp_root.winfo_vrootwidth()
            actual_height = temp_root.winfo_vrootheight()
        except:
            actual_width = primary_width
            actual_height = primary_height
        
        temp_root.destroy()
        
        monitors.append({
            'x': 0,
            'y': 0, 
            'width': actual_width,
            'height': actual_height,
            'scale_factor': scale_factor,
            'is_primary': True
        })
        
    except Exception as e:
        print(f"Error getting monitor info: {e}")
        # Fallback to basic screen info
        monitors.append({
            'x': 0,
            'y': 0,
            'width': 1920,
            'height': 1080, 
            'scale_factor': 1.0,
            'is_primary': True
        })
    
    return monitors

# Create splash window for specific monitor
def create_splash_window(monitor_info):
    """Create a splash window positioned on a specific monitor"""
    window = tk.Toplevel() if 'root' in globals() and root else tk.Tk()
    window.title("Insprash")
    
    # Set window geometry for this monitor
    geometry = f"{monitor_info['width']}x{monitor_info['height']}+{monitor_info['x']}+{monitor_info['y']}"
    window.geometry(geometry)
    
    # Make fullscreen on this monitor
    window.attributes('-fullscreen', True)
    window.attributes('-topmost', True)
    window.configure(background=GRAD_TOP)
    window.config(cursor="none")
    
    return window

# Helper functions for multi-monitor support
def update_splash_on_window(window, message, width, height):
    # Update splash screen on a specific window - simplified for now
    pass

def update_all_windows(windows, message):
    # Update all splash windows with new message
    def worker():
        new_message = generate_text()
        # For now, just update the main window
        if root and root.winfo_exists():
            root.after(0, lambda: update_splash(new_message))
    threading.Thread(target=worker, daemon=True).start()

def close_all_windows(windows):
    # Close all splash windows
    for window in windows:
        try:
            if window.winfo_exists():
                window.destroy()
        except:
            pass

# Method for accessing local files
def get_source_path(filename):
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, filename)

# Validate hex color format
def is_valid_hex_color(color_string):
    """Check if string is a valid hex color (#RRGGBB or #RGB)"""
    if not color_string.startswith('#'):
        return False
    
    hex_part = color_string[1:]
    
    # Check for valid lengths (3 for #RGB, 6 for #RRGGBB)
    if len(hex_part) not in [3, 6]:
        return False
    
    # Check if all characters are valid hex digits
    try:
        int(hex_part, 16)
        return True
    except ValueError:
        return False

# Loads the API Key for Gemini API from local files
def load_api_key():
    global GEMINI_API_KEY, USE_GEMINI
    try:
        with open(get_source_path("gemini_api_key"), "r") as f:
            key = f.read().strip()
            if key == "null" or key == "" or key == "none":
                USE_GEMINI = False
                print("No API key provided, using fallback text only")
            else:
                USE_GEMINI = True
                genai.configure(api_key=key)
                GEMINI_API_KEY = key
                print("Loaded API Key")
    except FileNotFoundError:
        print("API key file not found, using fallback text only")
        USE_GEMINI = False
    except Exception as e:
        print(f"Error loading API key: {e}, using fallback text only")
        USE_GEMINI = False

# Call to Gemini API for text generation
def generate_text():
    result = {"text": None}
    timeout_triggered = threading.Event()

    def gemini_call():
        if timeout_triggered.is_set():
            return
        if USE_GEMINI:
            try:
                model = genai.GenerativeModel("gemini-2.0-flash-exp")
                response = model.generate_content(PROMPT)
                if not timeout_triggered.is_set():
                    result["text"] = response.text.strip()
            except Exception as e:
                print(f"Error during Gemini API call: {e}")
    
    def fallback():
        timeout_triggered.set()
        print("Gemini API Timeout, using fallback.")
        if FALLBACK_TEXTS:
            result["text"] = random.choice(FALLBACK_TEXTS)
        else:
            result["text"] = "Welcome! Let's create something amazing today."

    # Start Gemini call
    thread = threading.Thread(target=gemini_call)
    thread.start()

    # Start timer
    timer = threading.Timer(API_TIMEOUT, fallback)
    timer.start()

    # Check for result or timeout
    while result["text"] is None and not timeout_triggered.is_set():
        thread.join(timeout=0.1)

    timer.cancel()
    return result["text"]
            

# Generates the splash screen
def splash(message):
    global root, background_label, screen_width, screen_height, font

    # Get monitor information
    monitors = get_monitor_info()
    primary_monitor = next((m for m in monitors if m['is_primary']), monitors[0])
    
    if SHOW_ON_ALL_MONITORS and len(monitors) > 1:
        # Show on all monitors (create multiple windows)
        windows = []
        for i, monitor in enumerate(monitors):
            if i == 0:
                # First window becomes the main root
                root = create_splash_window(monitor)
                windows.append(root)
            else:
                # Additional windows
                window = create_splash_window(monitor)
                windows.append(window)
        
        # Use primary monitor for sizing calculations
        screen_width = primary_monitor['width']
        screen_height = primary_monitor['height'] 
        scale_factor = primary_monitor['scale_factor']
        
        # Setup font and display on all windows
        base_font_size = int(min(screen_width, screen_height) * 0.035)
        font_size = max(18, int(base_font_size / scale_factor))
        
        try:
            font = ImageFont.truetype(get_source_path("font.ttf"), font_size)
        except IOError:
            print("Font not found")
            font = ImageFont.load_default()
        
        # Update splash on all windows
        for i, window in enumerate(windows):
            # Each window needs its own background label
            current_monitor = monitors[i] if i < len(monitors) else monitors[0]
            update_splash_on_window(window, message, current_monitor['width'], current_monitor['height'])
        
        # Schedule updates and auto-close for all windows
        root.after(100, lambda: update_all_windows(windows, message))
        root.after(DURATION, lambda: close_all_windows(windows))
        
        # Bind escape to close all windows
        for window in windows:
            window.bind("<Escape>", lambda e: close_all_windows(windows))
            
    else:
        # Show only on primary monitor (original behavior)
        root = create_splash_window(primary_monitor)
        
        # Store actual dimensions and scaling
        screen_width = primary_monitor['width']
        screen_height = primary_monitor['height']
        scale_factor = primary_monitor['scale_factor']
        
        # Calculate font size with proper scaling
        base_font_size = int(min(screen_width, screen_height) * 0.035)
        font_size = max(18, int(base_font_size / scale_factor))
        
        try:
            font = ImageFont.truetype(get_source_path("font.ttf"), font_size)
        except IOError:
            print("Font not found")
            font = ImageFont.load_default()
        
        print(f"Monitor: {screen_width}x{screen_height}, Scale: {scale_factor:.2f}, Font: {font_size}")
        
        # Update the splash screen
        update_splash(message)

        # Call update
        root.after(100, update)

        # Auto close
        root.after(DURATION, root.destroy)

        # Early close with escape
        root.bind("<Escape>", lambda e: root.destroy())
    
    root.mainloop()

# Update the splash screen
def update_splash(message):
    global root, background_label, screen_width, screen_height, font

    # Gradient
    gradient = Image.new("RGB", (1, screen_height), GRAD_TOP)
    top_rgb = tuple(int(GRAD_TOP[i:i+2], 16) for i in (1, 3, 5))
    bottom_rgb = tuple(int(GRAD_BOTTOM[i:i+2], 16) for i in (1, 3, 5))
    for y in range(screen_height):
        t = y / screen_height
        r = int(top_rgb[0] + (bottom_rgb[0] - top_rgb[0]) * t)
        g = int(top_rgb[1] + (bottom_rgb[1] - top_rgb[1]) * t)
        b = int(top_rgb[2] + (bottom_rgb[2] - top_rgb[2]) * t)
        gradient.putpixel((0, y), (r, g, b))

    gradient = gradient.resize((screen_width, screen_height))

    # Text with improved positioning for scaling
    draw = ImageDraw.Draw(gradient)
    
    # Get text dimensions using proper measurement
    bbox = draw.textbbox((0, 0), message, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    # Calculate center position with pixel-perfect alignment
    x = (screen_width - text_width) // 2
    y = (screen_height - text_height) // 2
    
    # Ensure coordinates are integers to prevent sub-pixel rendering issues
    x = int(round(x))
    y = int(round(y))
    
    draw.text((x, y), message, font=font, fill="white")

    # Convert to Tk Image
    background = ImageTk.PhotoImage(gradient)
    if background_label is None:
        background_label = tk.Label(root, image=background)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        background_label.image = background
    else:
        background_label.configure(image=background)
        background_label.image = background

if __name__ == "__main__":
    print("Insprash Launching...")
    main()