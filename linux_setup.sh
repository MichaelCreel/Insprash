#!/bin/bash
#This script sets up Insprash for Linux systems.

echo "Generate a Gemini API Key at https://aistudio.google.com/apikey"
read -p "Paste Gemini API Key: (Leave blank to skip Gemini) " key
echo "$key" > gemini_api_key
echo "API Key Written."

cat <<EOF > Insprash.desktop
[Desktop Entry]
Name=Insprash
Exec=$(pwd)/Insprash.py
Type=Application
Terminal=false
Icon=$(pwd)/icon.png
EOF

chmod +x Insprash.py
chmod +x Insprash.desktop
echo "Created Insprash.desktop"

mv Insprash.desktop ~/.config/autostart/Insprash.desktop
echo "Added Insprash to startup applications."

echo "Setup complete. Insprash should now run on user login."