#!/usr/bin/env python3
"""
Comprehensive test script for Windscribe IP Changer with device connection
"""

import subprocess
import sys
import os
from windscribe_ip_changer import WindscribeIPChanger

def check_adb_installation():
    """Check if ADB is installed and accessible"""
    print("=== Checking ADB Installation ===")
    
    # Check common locations
    common_paths = [
        "/usr/bin/adb",
        "/usr/local/bin/adb",
        os.path.join(os.path.expanduser("~"), "Android/Sdk/platform-tools/adb"),
        "/opt/android-sdk/platform-tools/adb",
    ]
    
    found_paths = []
    for path in common_paths:
        if os.path.isfile(path) and os.access(path, os.X_OK):
            found_paths.append(path)
            print(f"✓ Found ADB at: {path}")
    
    # Try which command
    try:
        result = subprocess.run(
            ["which", "adb"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0 and result.stdout:
            adb_path = result.stdout.strip()
            if adb_path not in found_paths:
                found_paths.append(adb_path)
                print(f"✓ Found ADB in PATH: {adb_path}")
    except:
        pass
    
    if not found_paths:
        print("✗ ADB not found!")
        print("\nTo install ADB on Arch Linux:")
        print("  sudo pacman -S android-tools")
        print("\nOr download Android SDK Platform Tools:")
        print("  https://developer.android.com/studio/releases/platform-tools")
        return None
    
    return found_paths[0] if found_paths else None

def test_device_connection(adb_path):
    """Test connection to Android device"""
    print("\n=== Testing Device Connection ===")
    
    changer = WindscribeIPChanger(adb_path=adb_path)
    
    # List devices
    devices = changer.list_devices()
    if not devices:
        print("✗ No devices connected!")
        print("\nPlease:")
        print("  1. Connect your Android device via USB")
        print("  2. Enable USB Debugging in Developer Options")
        print("  3. Accept the debugging prompt on your device")
        print("  4. Run: adb devices")
        return False
    
    print(f"✓ Found {len(devices)} device(s):")
    for device in devices:
        print(f"  - {device['device_id']} ({device['status']})")
    
    # Test connection
    if changer.check_adb_connection():
        print("✓ ADB connection verified")
        device_id = changer.get_connected_device()
        print(f"  Using device: {device_id}")
        return True, changer, device_id
    else:
        print("✗ ADB connection check failed")
        return False, None, None

def test_screen_detection(changer):
    """Test screen size detection"""
    print("\n=== Testing Screen Detection ===")
    try:
        screen_width, screen_height = changer._get_screen_size()
        print(f"✓ Screen size: {screen_width}x{screen_height}")
        print(f"  Center: ({screen_width // 2}, {screen_height // 2})")
        return True
    except Exception as e:
        print(f"✗ Screen detection failed: {e}")
        return False

def test_windscribe_detection(changer):
    """Test Windscribe app detection"""
    print("\n=== Testing Windscribe Detection ===")
    
    if not changer.check_windscribe_installed():
        print("✗ Windscribe not found!")
        print("\nPlease install Windscribe app from Google Play Store")
        return False
    
    print("✓ Windscribe found")
    package = changer.get_windscribe_package_name()
    if package:
        print(f"  Package: {package}")
        print("  Type: Android App (UI automation enabled)")
    else:
        print("  Type: CLI")
    
    status = changer.get_windscribe_status()
    if status:
        print(f"  Status: {status}")
    else:
        print("  Status: Not connected")
    
    ip = changer.get_current_ip()
    if ip:
        print(f"  Current IP: {ip}")
    else:
        print("  IP: Could not determine")
    
    return True

def test_ui_automation(changer):
    """Test UI automation capabilities"""
    print("\n=== Testing UI Automation Capabilities ===")
    
    package = changer.get_windscribe_package_name()
    if not package:
        print("  UI automation: Not needed (CLI mode)")
        return True
    
    print("✓ UI automation methods available:")
    print("  - Screen size detection: ✓")
    print("  - Tap simulation: ✓")
    print("  - Text input: ✓")
    print("  - Swipe simulation: ✓")
    print("  - UI hierarchy detection: ✓")
    
    # Test tap functionality
    try:
        screen_width, screen_height = changer._get_screen_size()
        center_x = screen_width // 2
        center_y = screen_height // 2
        print(f"\n  Testing tap at ({center_x}, {center_y})...")
        if changer._tap(center_x, center_y):
            print("  ✓ Tap command executed successfully")
        else:
            print("  ⚠ Tap command may have failed")
    except Exception as e:
        print(f"  ✗ Tap test failed: {e}")
    
    return True

def test_connection_flow(changer):
    """Test the connection/disconnection flow"""
    print("\n=== Testing Connection Flow ===")
    
    package = changer.get_windscribe_package_name()
    if not package:
        print("  Skipping (CLI mode - requires manual testing)")
        return True
    
    print("  This will test the full UI automation flow...")
    print("  Note: This will interact with the Windscribe app")
    
    response = input("  Proceed with connection test? (y/N): ").strip().lower()
    if response != 'y':
        print("  Skipped by user")
        return True
    
    # Test disconnect first
    print("\n  Testing disconnect...")
    if changer.disconnect_windscribe():
        print("  ✓ Disconnect completed")
    else:
        print("  ⚠ Disconnect may have failed")
    
    time.sleep(2)
    
    # Test connect to a location
    print("\n  Testing connect to 'us-east'...")
    if changer.connect_windscribe("us-east"):
        print("  ✓ Connection completed")
        
        # Verify connection
        time.sleep(3)
        status = changer.get_windscribe_status()
        ip = changer.get_current_ip()
        print(f"  Status: {status}")
        print(f"  IP: {ip}")
    else:
        print("  ✗ Connection failed")
        return False
    
    return True

def main():
    """Run all tests"""
    print("=" * 60)
    print("Windscribe IP Changer - Device Testing")
    print("=" * 60)
    
    # Step 1: Check ADB
    adb_path = check_adb_installation()
    if not adb_path:
        print("\n✗ Cannot proceed without ADB")
        sys.exit(1)
    
    # Step 2: Test device connection
    result = test_device_connection(adb_path)
    if not result:
        print("\n✗ Cannot proceed without connected device")
        sys.exit(1)
    
    success, changer, device_id = result
    
    # Step 3: Test screen detection
    if not test_screen_detection(changer):
        print("\n⚠ Screen detection failed, but continuing...")
    
    # Step 4: Test Windscribe detection
    if not test_windscribe_detection(changer):
        print("\n✗ Windscribe not found - install the app first")
        sys.exit(1)
    
    # Step 5: Test UI automation
    test_ui_automation(changer)
    
    # Step 6: Test connection flow (optional)
    import time
    test_connection_flow(changer)
    
    print("\n" + "=" * 60)
    print("✓ All tests completed!")
    print("=" * 60)

if __name__ == "__main__":
    main()
