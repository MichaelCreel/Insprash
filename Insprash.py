# Copyright 2025 Michael Creel

import os
import sys
import random
import requests
import google.generativeai as genai
import tkinter as tk
from tkinter import font as tkfont
from PIL import Image, ImageTk
from google.generativeai import types

DURATION = 7000 # Duration of splash in miliseconds
API_TIMEOUT = 2.5 # Duration for API Response
TEXT_RATIO = 0.65
GRAD_TOP = "#330c5a"
GRAD_BOTTOM = "#831764"
FALLBACK_TEXTS = [ #Fallbacks if Gemini API does not respond
    "Visualize. Inspire. Create.",
    "Never stop creating.",
    "Build for the world.",
    "Design your dreams.",
    "Unleash your creativity.",
    "Push your limits.",
    "Dare to innovate.",
    "Be bold. Be different.",
    "Make it happen.",
]

PROMPT = "Generate a short, inspiring sentence about creativity, productivity, etc. that nicely greets people when they login to their computer."
PROMPT = "Generate one single, short, inspiring sentence about creativity or productivity that nicely greets people when they login to their computer. Don't surround it with any characters or apply any formatting, only write the sentence."

def main():
    load_api_key()
    message = generate_text()
    splash(message)

#Store the API key for Gemini
def load_api_key():
    global GEMINI_API_KEY
    key=""
    with open("gemini_api_key", "r") as f:
        key=f.read().strip()
        genai.configure(api_key=key)
        GEMINI_API_KEY=key
        genai.configure(api_key=key)
    print("Loaded API Key")

#Gemini call to generate text
def generate_text():
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(PROMPT
            #PROMPT,
            #generation_config=types.GenerationConfig(
            #    temperature=0.7,
            #    max_output_tokens=60
            #)
        )
        return response.text.strip()
    except Exception as e:
        print(f"Error generating text: {e}")
        return random.choice(FALLBACK_TEXTS)

#Generates the splash screen
def splash(message):
    print(message)
    #Initialization
    root = tk.Tk()
    root.title("Inprash")
    root.attributes("-fullscreen", True)
    root.configure(background=GRAD_TOP)
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    #Gradient
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
    background = ImageTk.PhotoImage(gradient)
    background_label = tk.Label(root, image=background)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    #Font
    font_size = max(18, int(min(screen_width, screen_height) * 0.05))
    splash_font = tkfont.Font(family="Helvetica", size=font_size, weight="bold")

    #Message Setup
    text_label = tk.Label(
        root,
        text=message,
        font=splash_font,
        fg="white",
        bg=None,
        wraplength=int(screen_width * TEXT_RATIO),
        justify="center"
    )
    text_label.place(relx=0.5,rely=0.5, anchor="center")

    #Auto close
    root.after(DURATION, root.destroy)
    
    #Early close with escape
    root.bind("<Escape>", lambda e: root.destroy())

    root.background = background
    root.mainloop()

if __name__ == "__main__":
    print("Insprash Launching...")
    main()