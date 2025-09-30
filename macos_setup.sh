#!/bin/bash
#This script sets up Insprash for macOS systems.

echo "Insprash macOS Setup"
echo "=================="

# Check if Python is available
PYTHON_CMD=""
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo "ERROR: Python not found. Please install Python 3 from https://python.org or using Homebrew:"
    echo "  brew install python"
    exit 1
fi

echo "Found Python: $PYTHON_CMD"

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

# Create launcher script
cat <<EOF > LaunchInsprash.command
#!/bin/bash
cd "$(dirname "$0")"
$PYTHON_CMD Insprash.py
EOF

chmod +x LaunchInsprash.command
echo "Created LaunchInsprash.command"

# Try to add to login items using AppleScript
echo "Adding Insprash to Login Items..."
if osascript <<EOF
tell application "System Events"
    try
        make new login item at end with properties {path:"$(pwd)/LaunchInsprash.command", hidden:true}
        return "success"
    on error
        return "error"
    end try
end tell
EOF
then
    echo "Successfully added Insprash to Login Items."
else
    echo "WARNING: Could not automatically add to Login Items."
    echo "Manual steps:"
    echo "1. Open System Preferences > Users & Groups > Login Items"
    echo "2. Click the '+' button"
    echo "3. Navigate to and select: $(pwd)/LaunchInsprash.command"
fi

echo "Setup complete. Insprash should now run on user login."
echo "To test manually: ./LaunchInsprash.command"