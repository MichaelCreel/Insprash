# Insprash

Insprash is a customizable splash screen that greets users at login with inspiring messages. It uses Google Gemini to generate greeting text. It supports custom fonts and gradient colors. It is designed to run on Windows, Mac, and Linux and is simple to install and set up.

## Dependencies
- Python, Tkinter, Google Gemini API
  - Windows:
    Install [Python 3](https://python.org)
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

### PROBLEMS ON WINDOWS: Insprash currently has issues on Windows and may not run

#### Manual Installation: 
1. Download Git Zip Folder
  - Click "Code" on this page (Dropdown Menu)
  - Click "Download ZIP"
  - Save to desired location
2. Extract .zip folder (IMPORTANT: The extracted folder makes the app work. Save it to somewhere it won't bother you)
  - Open the extracted folder
3. Run the setup script for your operating system

#### Terminal Installation: (Requires Git on Windows and Linux)
1. Get a Gemini API Key
  - Open [Google AI Studio](https://aistudio.google.com/apikey)
  - Sign in with your Google account
  - Click "Create API key"
  - Copy the API key when it generates
      If you are copying installation commands, leave the API tab open to recopy the API key during setup
2. Open a terminal
  - Windows:
    `Windows`
    Type "PowerShell"
    `Enter`
  - Mac:
    `Command + Space`
    Type "Terminal"
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
- Multi-monitor display can be changed by editing `show_on_all_monitors`
- Gemini has limited tokens on free API keys, so AI generation is limited
- Setup scripts will automatically put the app in startup applications and will not need to be done manually
- Free Gemini API Keys have limits on prompts that can be called and fallback texts will be used if prompts run out
- The splash screen will not display properly with mixed monitor fractional scaling, so the same scale must be used for proper display

## License

MIT License
