# Changelog — Windscribe IP Changer for Android

## [Unreleased]
### Added
- **Multi-device support** - Manage multiple Android devices simultaneously with different VPN connections
- **Device selection** - `--device` argument to target specific device by ID
- **Device listing** - `--list-devices` argument to show all connected devices
- **Multi-device management** - `--multi-device` argument with JSON config for simultaneous connections
- **`manage_multiple_devices()` function** - Connect multiple devices to different locations at once
- **`list_devices()` method** - List all connected Android devices with status
- **`_build_adb_command()` helper** - Device-specific ADB command builder
- **Full UI automation for Windscribe Android app** - No GUI interaction required
- **Smart screen size detection** - Automatically adapts to different device screen sizes
- **UI automation helper methods** - `_tap()`, `_swipe()`, `_get_screen_size()`, `_get_ui_hierarchy()`
- **Complete automated connection flow** - Opens app, disconnects, selects location, connects automatically
- **Taps and text input automation** - Uses `adb shell input tap` and `adb shell input text` to interact with app UI
- **In-app IP changes** - Changes IP from inside the Windscribe app on each device (not external routing)
- **Location name mapping** - Comprehensive mapping of location codes to display names
- **Connection verification** - Verifies VPN connection after automation
- Enhanced device detection and connection validation
- Improved IP address detection with multiple fallback methods
- Support for both Windscribe CLI and Android app detection
- Better error handling and user feedback
- Improved package detection (supports `com.windscribe.vpn` and variants)
- Example multi-device configuration file (`multi_device_config.json.example`)

### Changed
- **All ADB commands now support device selection** - Uses `-s DEVICE_ID` when device is specified
- **Device auto-selection** - Automatically selects first available device if none specified (backward compatible)
- **Removed GUI requirement** - Fully automated via ADB shell commands
- **Enhanced disconnect function** - Now uses UI automation with multiple button position attempts
- Improved device name extraction from ADB output
- Enhanced VPN status checking via Android system dumpsys
- Connection process now fully automated without manual steps

### Fixed
- Fixed broken shell command with pipe in `check_windscribe_installed()`
- Fixed incorrect device ID extraction in `get_connected_device()`
- Improved ADB connection validation logic
- Fixed connection function that only opened app without actually connecting

## [0.1.0] - 2026-03-12
### Added
- Initial release
- ADB connection management
- Windscribe VPN IP rotation
- Support for Android devices and emulators
- Automatic IP rotation mode
- Configurable server locations
- Current IP and status checking
- Command-line interface with argparse
- Example usage scripts
- Connection test utility
