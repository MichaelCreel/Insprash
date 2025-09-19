#!/bin/bash

read -p "Paste Gemini API Key (Ctrl + Shift + V): " key
echo "$key" > gemini_api_key
echo "API Key Written."

cat <<EOF > LaunchInsprash.command
#!/bin/bash
cd "$(dirname "$0")"
python3 Insprash.py
EOF

chmod +x LaunchInsprash.command
echo "Created LaunchInsprash.command"

osascript <<EOF
tell application "System Events"
    make new login item at end with properties {path:"$(pwd)/LaunchInsprash.command", hidden:true}
end tell
EOF

echo "Added Insprash to Login Items."