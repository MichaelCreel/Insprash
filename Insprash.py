#!/usr/bin/env python3

import os
import sys
import random
import google.generativeai as genai
import tkinter as tk
import threading
from PIL import Image, ImageTk, ImageDraw, ImageFont

DURATION = 20000 # Duration of splash screen in miliseconds
API_TIMEOUT = 10 # Duration for API Response in seconds
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
            GRAD_TOP = lines[0].strip()
            GRAD_BOTTOM = lines[1].strip()
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
            PROMPT="".join(lines).strip()
    except Exception as e:
        print(f"Error loading prompt: {e}")

def update():
    def worker():
        message = generate_text()
        root.after(0, lambda: update_splash(message))
    threading.Thread(target=worker, daemon=True).start()

# Method for accessing local files
def get_source_path(filename):
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, filename)

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

    # Initialization
    root = tk.Tk()
    root.title("Inprash")
    root.attributes("-fullscreen", True)
    root.configure(background=GRAD_TOP)
    root.config(cursor="none")
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    try:
        font_size = max(18, int(min(screen_width, screen_height) * 0.035))
        font = ImageFont.truetype(get_source_path("font.ttf"), font_size)
    except IOError:
        print("Font not found")
        font = ImageFont.load_default()
    
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

    # Text
    draw = ImageDraw.Draw(gradient)
    bbox = draw.textbbox((0, 0), message, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (screen_width - text_width) // 2
    y = (screen_height - text_height) //2
    draw.text((x,y), message, font=font, fill="white")

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