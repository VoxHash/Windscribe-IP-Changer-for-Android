# Getting Started

Complete guide to setting up and using Windscribe IP Changer for Android.

## Overview

Windscribe IP Changer for Android is a Python script that automates IP address changes on Android devices by connecting to different Windscribe VPN servers via ADB.

## Setup Process

### 1. Install Dependencies

See [Installation](installation.md) for platform-specific steps.

### 2. Enable Developer Options

On your Android device:
1. Go to Settings → About Phone
2. Tap "Build Number" 7 times
3. Go back to Settings → Developer Options
4. Enable "USB Debugging"

### 3. Connect Device

**Physical Device:**
- Connect via USB cable
- Accept debugging prompt on device
- Verify: `adb devices`

**Emulator:**
- Start your emulator
- ADB should automatically detect it
- Verify: `adb devices`

### 4. Install Windscribe

Install Windscribe app on your Android device and log in.

### 5. Test Connection

```bash
python3 test_connection.py
```

## Basic Usage

```bash
# Change IP once
python3 windscribe_ip_changer.py

# Automatic rotation
python3 windscribe_ip_changer.py --rotate --count 10 --interval 300
```

## Next Steps

- [Usage Guide](usage.md) - Detailed usage instructions
- [Examples](examples/example-01.md) - Real-world examples
- [Configuration](configuration.md) - Customize settings
