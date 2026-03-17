#!/bin/bash
# Setup and test script for Windscribe IP Changer

echo "============================================================"
echo "Windscribe IP Changer - Setup and Testing"
echo "============================================================"

# Check if ADB is installed
if command -v adb &> /dev/null; then
    echo "✓ ADB is already installed"
    ADB_PATH=$(which adb)
else
    echo "✗ ADB is not installed"
    echo ""
    echo "Installing ADB..."
    
    # Try to install via pacman (Arch Linux)
    if command -v pacman &> /dev/null; then
        echo "Installing android-tools via pacman..."
        sudo pacman -S --noconfirm android-tools
        if [ $? -eq 0 ]; then
            echo "✓ ADB installed successfully"
            ADB_PATH=$(which adb)
        else
            echo "✗ Installation failed. Please install manually:"
            echo "  sudo pacman -S android-tools"
            exit 1
        fi
    else
        echo "Please install ADB manually:"
        echo "  Arch Linux: sudo pacman -S android-tools"
        echo "  Ubuntu/Debian: sudo apt install android-tools-adb"
        echo "  Or download from: https://developer.android.com/studio/releases/platform-tools"
        exit 1
    fi
fi

echo ""
echo "ADB Path: $ADB_PATH"
echo ""

# Check for connected devices
echo "=== Checking for Connected Devices ==="
DEVICES=$(adb devices | grep -v "List" | grep "device" | wc -l)

if [ "$DEVICES" -eq 0 ]; then
    echo "✗ No devices connected!"
    echo ""
    echo "Please:"
    echo "  1. Connect your Android device via USB"
    echo "  2. Enable USB Debugging in Developer Options"
    echo "  3. Accept the debugging prompt on your device"
    echo ""
    echo "Then run: adb devices"
    echo ""
    read -p "Press Enter when device is connected, or Ctrl+C to exit..."
    DEVICES=$(adb devices | grep -v "List" | grep "device" | wc -l)
    if [ "$DEVICES" -eq 0 ]; then
        echo "✗ Still no devices found. Exiting."
        exit 1
    fi
fi

echo "✓ Found $DEVICES device(s)"
adb devices

echo ""
echo "=== Running Python Tests ==="
python3 test_with_device.py
