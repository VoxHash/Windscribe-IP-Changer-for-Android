# Changelog — Windscribe IP Changer for Android

## [Unreleased]
### Added
- Enhanced device detection and connection validation
- Improved IP address detection with multiple fallback methods
- Support for both Windscribe CLI and Android app detection
- Better error handling and user feedback

### Changed
- Improved device name extraction from ADB output
- Enhanced VPN status checking via Android system dumpsys

### Fixed
- Fixed broken shell command with pipe in `check_windscribe_installed()`
- Fixed incorrect device ID extraction in `get_connected_device()`
- Improved ADB connection validation logic

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
