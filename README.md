# Windscribe IP Changer for Android

[![License](https://img.shields.io/github/license/VoxHash/windscribe-ip-changer-android)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.x-blue)](https://www.python.org/)

> Python script to automatically change IP addresses on Android devices and emulators by connecting to different Windscribe VPN servers via ADB (Android Debug Bridge).

## ✨ Features

- ✅ Connects to Android devices/emulators via ADB
- ✅ **Fully automated UI automation** - No GUI interaction required
- ✅ Automatically changes IP by connecting to random Windscribe servers
- ✅ Supports both physical devices and Android emulators
- ✅ **Multi-device support** - Manage multiple devices simultaneously with different connections
- ✅ Configurable server locations
- ✅ Automatic IP rotation mode
- ✅ Current IP and status checking
- ✅ Works with Windscribe CLI or Android app
- ✅ Smart screen size detection and adaptive UI interaction

## 🧭 Table of Contents

- [Quick Start](#-quick-start)
- [Installation](#-installation)
- [Usage](#-usage)
- [Configuration](#-configuration)
- [Examples](#-examples)
- [Architecture](#-architecture)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)
- [License](#-license)

## 🚀 Quick Start

```bash
# 1) Clone repository
git clone https://github.com/VoxHash/windscribe-ip-changer-android.git
cd windscribe-ip-changer-android

# 2) Verify Python 3.x is installed
python3 --version

# 3) Verify ADB is installed and device is connected
adb devices

# 4) Run script
python3 windscribe_ip_changer.py
```

## 💿 Installation

See [docs/installation.md](docs/installation.md) for platform-specific steps.

### Prerequisites

1. **Python 3.x** installed
2. **ADB (Android Debug Bridge)** installed and configured
   - Linux: `apt-get install adb` or your package manager
   - macOS: `brew install android-platform-tools`
   - Windows: Download from [Android Developer site](https://developer.android.com/studio/releases/platform-tools)
3. **Windscribe** installed on Android device/emulator
   - Android app: Install from Google Play Store or APK
   - CLI: Install from https://windscribe.com (if available)

## 🛠 Usage

Basic usage here. Advanced usage in [docs/usage.md](docs/usage.md).

### Single IP Change

```bash
python3 windscribe_ip_changer.py
```

### Automatic IP Rotation

```bash
python3 windscribe_ip_changer.py --rotate --count 10 --interval 300
```

### Custom Server List

```bash
python3 windscribe_ip_changer.py --servers servers.json
```

### Single Device with Device ID

```bash
python3 windscribe_ip_changer.py --device emulator-5554
```

### List Connected Devices

```bash
python3 windscribe_ip_changer.py --list-devices
```

### Multi-Device Management

Connect multiple devices to different locations simultaneously:

```bash
python3 windscribe_ip_changer.py --multi-device multi_device_config.json
```

Example `multi_device_config.json`:
```json
[
  {
    "device_id": "emulator-5554",
    "location": "us-east"
  },
  {
    "device_id": "emulator-5556",
    "location": "eu-west"
  }
]
```

### All Options

```bash
python3 windscribe_ip_changer.py \
  --adb-path /custom/path/to/adb \
  --device emulator-5554 \
  --servers servers.json \
  --rotate \
  --count 20 \
  --interval 600 \
  --wait 8
```

## ⚙️ Configuration

| Option | Description | Default |
|--------|-------------|---------|
| `--adb-path` | Path to ADB executable | Auto-detected |
| `--device` | Specific device ID to target | Auto-select first device |
| `--list-devices` | List all connected devices and exit | - |
| `--multi-device` | Path to JSON file with multi-device config | - |
| `--servers` | Path to JSON file with server list | Uses defaults |
| `--wait` | Seconds to wait after connecting | 5 |
| `--rotate` | Enable automatic IP rotation | False |
| `--count` | Number of rotations | 5 |
| `--interval` | Seconds between rotations | 300 |

Full reference: [docs/configuration.md](docs/configuration.md)

## 📚 Examples

- Start here: [docs/examples/example-01.md](docs/examples/example-01.md)
- More: [docs/examples/](docs/examples/)

## 🧩 Architecture

The script works by:
1. Connecting to Android device/emulator via ADB
2. Checking if Windscribe is installed (CLI or app)
3. Getting current IP and Windscribe status
4. Disconnecting from current server (if connected) via UI automation
5. **Automatically navigating Windscribe app UI** to select location
6. Connecting to a random Windscribe server using ADB input commands
7. Verifying the new IP address

**UI Automation:** The script uses ADB shell commands (`input tap`, `input text`, etc.) to fully automate the Windscribe Android app without requiring any manual GUI interaction. It adapts to different screen sizes and handles UI variations automatically.

See [docs/architecture.md](docs/architecture.md) for details.

## 🗺 Roadmap

Planned milestones live in [ROADMAP.md](ROADMAP.md). For changes, see [CHANGELOG.md](CHANGELOG.md).

## 🤝 Contributing

We welcome PRs! Please read [CONTRIBUTING.md](CONTRIBUTING.md) and follow the PR template.

## 🔒 Security

Please report vulnerabilities via [SECURITY.md](SECURITY.md).

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

## 📞 Support

For issues, questions, or contributions, see [SUPPORT.md](SUPPORT.md).

---

**Note:** This script requires Windscribe to be installed and configured on your Android device or emulator. It uses ADB shell commands to interact with Windscribe via **fully automated UI automation** - no manual GUI interaction is required. Proper ADB setup is essential.
