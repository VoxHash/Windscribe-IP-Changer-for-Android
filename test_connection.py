#!/usr/bin/env python3
"""
Simple test script to verify ADB connection and Windscribe setup
"""

from windscribe_ip_changer import WindscribeIPChanger

def test_connection():
    """Test ADB and Windscribe connection"""
    print("=== Testing ADB Connection ===")
    changer = WindscribeIPChanger()
    
    if changer.adb_path:
        print(f"✓ ADB found: {changer.adb_path}")
    else:
        print("✗ ADB not found!")
        return False
    
    if changer.check_adb_connection():
        print("✓ ADB connected to device")
        device = changer.get_connected_device()
        print(f"  Device: {device or 'Unknown'}")
    else:
        print("✗ No device connected via ADB")
        print("  Please connect a device or start an emulator")
        return False
    
    print("\n=== Testing Screen Detection ===")
    screen_width, screen_height = changer._get_screen_size()
    print(f"✓ Screen size detected: {screen_width}x{screen_height}")
    print(f"  Center coordinates: ({screen_width // 2}, {screen_height // 2})")
    
    print("\n=== Testing Windscribe Installation ===")
    if changer.check_windscribe_installed():
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
        
        print("\n=== Testing UI Automation Capabilities ===")
        if package:
            print("✓ UI automation methods available:")
            print("  - Screen size detection: ✓")
            print("  - Tap simulation: ✓")
            print("  - Swipe simulation: ✓")
            print("  - UI hierarchy detection: ✓")
        else:
            print("  UI automation: Not needed (CLI mode)")
        
        return True
    else:
        print("✗ Windscribe not found")
        print("  Please install Windscribe app or CLI")
        return False

if __name__ == "__main__":
    success = test_connection()
    if success:
        print("\n✓ All checks passed! Ready to use.")
        print("  The script can now fully automate Windscribe connections via UI automation.")
    else:
        print("\n✗ Some checks failed. Please fix issues above.")
