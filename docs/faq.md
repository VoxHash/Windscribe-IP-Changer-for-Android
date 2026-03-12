# FAQ

Frequently asked questions.

## General

### What is Windscribe IP Changer for Android?

A Python script that automates IP address changes on Android devices by connecting to different Windscribe VPN servers via ADB.

### Do I need root access?

No, root access is not required. The script uses ADB which works with developer mode enabled.

### Does it work with physical devices?

Yes, it works with both physical Android devices and emulators.

## Installation

### What Python version do I need?

Python 3.x is required. Python 3.7 or higher is recommended.

### Where can I get ADB?

- Linux: `apt-get install adb`
- macOS: `brew install android-platform-tools`
- Windows: Download from [Android Developer site](https://developer.android.com/studio/releases/platform-tools)

### Do I need Windscribe CLI or app?

Either works. The Android app is recommended as it's easier to install and configure.

## Usage

### How do I change IP once?

```bash
python3 windscribe_ip_changer.py
```

### How do I rotate IPs automatically?

```bash
python3 windscribe_ip_changer.py --rotate --count 10 --interval 300
```

### Can I use custom servers?

Yes, create a `servers.json` file and use `--servers servers.json`.

## Troubleshooting

### ADB says "no devices/emulators found"

1. Enable USB debugging on your device
2. Accept the debugging prompt
3. Check with `adb devices`

### Windscribe not found

Install Windscribe app from Google Play Store or install Windscribe CLI.

### Connection timeouts

Increase wait time with `--wait 10` or check your network connection.

## See Also

- [Troubleshooting](troubleshooting.md)
- [Usage Guide](usage.md)
- [Support](SUPPORT.md)
