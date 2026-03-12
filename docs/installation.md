# Installation

Platform-specific installation steps for Windscribe IP Changer for Android.

## Python 3.x

### Linux
```bash
sudo apt-get update
sudo apt-get install python3 python3-pip
```

### macOS
```bash
brew install python3
```

### Windows
Download from [python.org](https://www.python.org/downloads/)

## ADB (Android Debug Bridge)

### Linux
```bash
sudo apt-get install adb
# Or via Android SDK
sudo apt-get install android-tools-adb
```

### macOS
```bash
brew install android-platform-tools
```

### Windows
1. Download from [Android Developer site](https://developer.android.com/studio/releases/platform-tools)
2. Extract and add to PATH
3. Or install Android Studio (includes ADB)

## Windscribe

### Android App (Recommended)
1. Install from [Google Play Store](https://play.google.com/store/apps/details?id=com.windscribe.android)
2. Or download APK from [Windscribe website](https://windscribe.com)
3. Configure and log in

### CLI (Optional)
1. Download from [Windscribe website](https://windscribe.com)
2. Install and configure
3. Ensure it's in PATH

## Verify Installation

```bash
# Check Python
python3 --version

# Check ADB
adb version

# Check device connection
adb devices

# Test script
python3 test_connection.py
```

## Next Steps

- [Quick Start](quick-start.md)
- [Usage Guide](usage.md)
