#!/bin/bash

# Build script for pka2xml
# Supports macOS and Linux

set -e  # Exit on error

echo "==================================="
echo "  PKT to XML Converter - Build"
echo "==================================="
echo ""

# Detect operating system
OS="$(uname -s)"
case "${OS}" in
    Linux*)     MACHINE=Linux;;
    Darwin*)    MACHINE=Mac;;
    *)          MACHINE="UNKNOWN:${OS}"
esac

echo "Detected system: $MACHINE"
echo ""

# Check if g++ is installed
if ! command -v g++ &> /dev/null; then
    echo "❌ Error: g++ not found!"
    echo ""
    if [ "$MACHINE" == "Mac" ]; then
        echo "On macOS, install Xcode Command Line Tools:"
        echo "  xcode-select --install"
    else
        echo "On Linux, install build-essential:"
        echo "  sudo apt-get install build-essential"
    fi
    exit 1
fi

echo "✅ g++ compiler found: $(g++ --version | head -n1)"
echo ""

# Configure paths based on system
if [ "$MACHINE" == "Mac" ]; then
    # macOS with Homebrew
    if [ -d "/opt/homebrew/include" ]; then
        # Apple Silicon (M1/M2)
        INCLUDE_PATH="/opt/homebrew/include"
        LIB_PATH="/opt/homebrew/lib"
    elif [ -d "/usr/local/include" ]; then
        # Intel Mac
        INCLUDE_PATH="/usr/local/include"
        LIB_PATH="/usr/local/lib"
    else
        echo "❌ Error: Homebrew not found!"
        echo ""
        echo "Install Homebrew and dependencies:"
        echo '  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
        echo "  brew install cryptopp re2"
        exit 1
    fi
elif [ "$MACHINE" == "Linux" ]; then
    # Linux
    INCLUDE_PATH="/usr/include"
    LIB_PATH="/usr/lib"

    # Check if libs are installed
    if [ ! -f "/usr/include/cryptopp/base64.h" ] && [ ! -f "/usr/local/include/cryptopp/base64.h" ]; then
        echo "❌ Error: CryptoPP not found!"
        echo ""
        echo "Install dependencies:"
        echo "  sudo apt-get install libcryptopp-dev libre2-dev zlib1g-dev"
        exit 1
    fi
else
    echo "❌ Unsupported operating system: $MACHINE"
    exit 1
fi

echo "📁 Include path: $INCLUDE_PATH"
echo "📁 Library path: $LIB_PATH"
echo ""

# Compile
echo "🔨 Compiling pka2xml..."
echo ""

COMPILE_CMD="g++ -std=c++17 -o pka2xml main.cpp -I${INCLUDE_PATH} -L${LIB_PATH} -lcryptopp -lz -lre2"

echo "Running: $COMPILE_CMD"
echo ""

if $COMPILE_CMD; then
    echo ""
    echo "✅ Compilation successful!"
    echo ""

    # Make executable
    chmod +x pka2xml

    # Test
    echo "📋 Testing binary..."
    if ./pka2xml 2>&1 | grep -q "usage:"; then
        echo "✅ Binary working correctly!"
    else
        ./pka2xml 2>&1 | head -n 5
    fi

    echo ""
    echo "==================================="
    echo "  Build completed successfully! ✨"
    echo "==================================="
    echo ""
    echo "Usage: ./pka2xml -d file.pkt output.xml"
    echo ""
else
    echo ""
    echo "❌ Compilation error!"
    echo ""
    echo "Check if all dependencies are installed:"
    if [ "$MACHINE" == "Mac" ]; then
        echo "  brew install cryptopp re2"
    else
        echo "  sudo apt-get install libcryptopp-dev libre2-dev zlib1g-dev"
    fi
    exit 1
fi
