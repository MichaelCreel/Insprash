# Insprash

Insprash is a customizable splash screen that greets users at login with inspiring messages. It uses Google Gemini to generate greeting text. It supports custom fonts and gradient colors. It is designed to run on Windows, Mac, and Linux and is simple to install and set up.

## Dependencies

- Python, Tkinter, Google Gemini API
  - Windows:
    Install Python 3 from [python.org](https://python.org)
    Check "Add Python to PATH" during installation
    ```cmd
    pip install google-generativeai pillow
    ```
  - Mac:
    ```bash
    brew install python
    pip3 install google-generativeai pillow
    ```
  - Linux:
    ```bash
    sudo apt update
    sudo apt install python3 python3-pip
    sudo apt install python3-tk
    pip3 install google-generativeai pillow
    ```
    If google-generativeai fails to install, try these:
    ```bash
    pipx install google-generativeai
    ```
    or
    ```bash
    pip install google-generativeai --break-system-packages
    ```

## Installation
1. Get a Gemini API Key
  - Open [https://aistudio.google.com/apikey](https://aistudio.google.com/apikey)
  - Sign in with your Google account
  - Click "Create API key"
  - Copy the API key when it generates
      If you are copying installation commands, leave the API tab open to recopy the API key during setup
2. Open a terminal
  - Windows:
    `Windows + X`
    Click PowerShell
  - Mac:
    `Command + Space`
    Type Terminal
    `Enter`
  - Linux:
    `Ctrl + Alt + T`
3. Clone the repository
  ```bash
  git clone https://github.com/MichaelCreel/Insprash
  ```
4. Open app directory
   ```bash
   cd Insprash
   ```
5. Run setup
   - Windows:
     ```cmd
     Set-ExecutionPolicy Bypass -Scope Process
     .\windows_setup.ps1
     ```
   - Mac:
     ```bash
     chmod +x macos_setup.sh
     ./macos_setup.sh
   - Linux:
     ```bash
     chmod +x linux_setup.sh
     ./linux_setup.sh
     ```

## Notes

- Font can be changed by replacing `font.ttf`
- Gradient colors can be changed by editing hexadecimal colors in `gradient_colors`
- Fallback lines can be changed by editing `fallback_lines`
- Gemini prompt can be changed by editing `prompt`
- Gemini has limited tokens on free API keys, so AI generation is limited
- Setup scripts will automatically put the app in startup applications and will not need to be done manually
- Insprash can be launched manually for testing by opening the directory and running Insprash.py with either `python Insprash.py` or `python3 Insprash.py`

## License

MIT License
