#!/bin/bash
#This script sets up Insprash for Linux systems.

read -p "Paste Gemini API Key (Ctrl + Shift + V): " key
echo "$key" > gemini_api_key
echo "API Key Written."

cat <<EOF > Insprash.desktop
[Desktop Entry]
Name=Insprash
Exec=python3 $(pwd)/Insprash.py
Type=Application
Terminal=false
Icon=$(pwd)/icon.png
EOF

chmod +x Insprash.py
chmod +x Insprash.desktop
echo "Created Insprash.desktop"

mv Insprash.desktop ~/.config/autostart/Insprash.desktop
echo "Added Insprash to startup applications."