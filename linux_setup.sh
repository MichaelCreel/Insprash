#!/bin/bash
#This script sets up Insprash for Linux systems.

echo "Insprash Linux Setup"
echo "=================="

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 not found. Please install Python 3:"
    echo "  Ubuntu/Debian: sudo apt install python3 python3-pip"
    echo "  CentOS/RHEL: sudo yum install python3 python3-pip"
    echo "  Arch: sudo pacman -S python python-pip"
    exit 1
fi

echo "Found Python 3: $(which python3)"

# Check if required files exist
required_files=("Insprash.py" "fallback_lines" "gradient_colors" "prompt" "font.ttf")
for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        echo "ERROR: Required file '$file' not found in current directory"
        exit 1
    fi
done

echo "All required files found"

echo "Generate a Gemini API Key at https://aistudio.google.com/apikey"
read -p "Paste Gemini API Key: (Leave blank to skip Gemini) " key
if [ -z "$key" ]; then
    key="none"
fi
echo "$key" > gemini_api_key
echo "API Key saved"

# Create desktop entry
cat <<EOF > Insprash.desktop
[Desktop Entry]
Name=Insprash
Exec=python3 $(pwd)/Insprash.py
Type=Application
Terminal=false
Icon=$(pwd)/icon.png
Path=$(pwd)
EOF

chmod +x Insprash.py
chmod +x Insprash.desktop
echo "Created Insprash.desktop"

# Ensure autostart directory exists
mkdir -p ~/.config/autostart

# Copy to autostart
cp Insprash.desktop ~/.config/autostart/Insprash.desktop
echo "Added Insprash to startup applications."

echo "Setup complete. Insprash should now run on user login."
echo "To test manually: python3 ./Insprash.py"