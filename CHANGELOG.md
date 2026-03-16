# Changelog — Windscribe IP Changer for Android

## [Unreleased]
### Added
- **Full UI automation for Windscribe Android app** - No GUI interaction required
- **Smart screen size detection** - Automatically adapts to different device screen sizes
- **UI automation helper methods** - `_tap()`, `_swipe()`, `_get_screen_size()`, `_get_ui_hierarchy()`
- **Complete automated connection flow** - Opens app, disconnects, selects location, connects automatically
- **Location name mapping** - Comprehensive mapping of location codes to display names
- **Connection verification** - Verifies VPN connection after automation
- Enhanced device detection and connection validation
- Improved IP address detection with multiple fallback methods
- Support for both Windscribe CLI and Android app detection
- Better error handling and user feedback
- Improved package detection (supports `com.windscribe.vpn` and variants)

### Changed
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
