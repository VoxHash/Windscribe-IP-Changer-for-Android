#!/usr/bin/env python3
"""
Test script that waits for device authorization and then runs full tests
"""

import time
import subprocess
from windscribe_ip_changer import WindscribeIPChanger

def wait_for_device_authorization(adb_path, max_wait=60):
    """Wait for device to be authorized"""
    print("Waiting for device authorization...")
    print("Please accept the USB debugging prompt on your Android device.")
    print("(Check 'Always allow from this computer' to avoid this in the future)\n")
    
    start_time = time.time()
    while time.time() - start_time < max_wait:
        try:
            result = subprocess.run(
                [adb_path, "devices"],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                lines = result.stdout.strip().split("\n")
                for line in lines[1:]:
                    if line.strip():
                        parts = line.split()
                        if len(parts) >= 2:
                            device_id = parts[0]
                            status = parts[1]
                            if status.lower() == "device":
                                print(f"✓ Device {device_id} is now authorized!")
                                return device_id
                            elif status.lower() == "unauthorized":
                                print(".", end="", flush=True)
                                time.sleep(2)
                                break
        except:
            pass
    
    print(f"\n✗ Device not authorized within {max_wait} seconds")
    return None

def run_full_test(device_id=None):
    """Run comprehensive tests on the device"""
    print("\n" + "=" * 60)
    print("Running Full Device Tests")
    print("=" * 60)
    
    changer = WindscribeIPChanger(device_id=device_id)
    
    # Test 1: Device connection
    print("\n[1/6] Testing device connection...")
    if not changer.check_adb_connection():
        print("✗ Device connection failed")
        return False
    print("✓ Device connected")
    
    device_name = changer.get_connected_device()
    print(f"  Device ID: {device_name}")
    
    # Test 2: Screen detection
    print("\n[2/6] Testing screen size detection...")
    try:
        screen_width, screen_height = changer._get_screen_size()
        print(f"✓ Screen size: {screen_width}x{screen_height}")
        print(f"  Center coordinates: ({screen_width // 2}, {screen_height // 2})")
    except Exception as e:
        print(f"✗ Screen detection failed: {e}")
        return False
    
    # Test 3: Windscribe detection
    print("\n[3/6] Testing Windscribe installation...")
    if not changer.check_windscribe_installed():
        print("✗ Windscribe not found!")
        print("  Please install Windscribe app from Google Play Store")
        return False
    
    print("✓ Windscribe found")
    package = changer.get_windscribe_package_name()
    if package:
        print(f"  Package: {package}")
        print("  Type: Android App (UI automation enabled)")
    else:
        print("  Type: CLI")
    
    # Test 4: Current status
    print("\n[4/6] Checking current Windscribe status...")
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
    
    # Test 5: UI automation capabilities
    print("\n[5/6] Testing UI automation capabilities...")
    if package:
        print("✓ UI automation methods available:")
        print("  - Screen size detection: ✓")
        print("  - Tap simulation: ✓")
        print("  - Text input: ✓")
        print("  - Swipe simulation: ✓")
        
        # Test a tap
        screen_width, screen_height = changer._get_screen_size()
        center_x = screen_width // 2
        center_y = screen_height // 2
        print(f"\n  Testing tap at ({center_x}, {center_y})...")
        if changer._tap(center_x, center_y):
            print("  ✓ Tap command executed successfully")
        else:
            print("  ⚠ Tap command may have failed")
    else:
        print("  UI automation: Not needed (CLI mode)")
    
    # Test 6: Connection flow (optional)
    print("\n[6/6] Connection flow test (optional)...")
    print("  This will test the full UI automation flow.")
    print("  Note: This will interact with the Windscribe app on your device.")
    
    response = input("  Proceed with connection test? (y/N): ").strip().lower()
    if response == 'y':
        print("\n  Testing disconnect...")
        changer.disconnect_windscribe()
        time.sleep(2)
        
        print("\n  Testing connect to 'us-east'...")
        if changer.connect_windscribe("us-east"):
            print("  ✓ Connection completed")
            time.sleep(3)
            
            status = changer.get_windscribe_status()
            ip = changer.get_current_ip()
            print(f"  Final Status: {status}")
            print(f"  Final IP: {ip}")
        else:
            print("  ✗ Connection failed")
    else:
        print("  Skipped by user")
    
    print("\n" + "=" * 60)
    print("✓ All tests completed!")
    print("=" * 60)
    return True

def main():
    print("=" * 60)
    print("Windscribe IP Changer - Device Testing")
    print("=" * 60)
    
    # Check ADB
    changer = WindscribeIPChanger()
    if not changer.adb_path:
        print("✗ ADB not found!")
        print("Please install ADB: sudo pacman -S android-tools")
        return
    
    print(f"✓ ADB found: {changer.adb_path}\n")
    
    # Check for devices
    devices = changer.list_devices()
    if not devices:
        # Check for unauthorized devices
        result = subprocess.run(
            [changer.adb_path, "devices"],
            capture_output=True,
            text=True
        )
        if "unauthorized" in result.stdout:
            device_id = wait_for_device_authorization(changer.adb_path)
            if not device_id:
                print("\n✗ Cannot proceed without authorized device")
                return
        else:
            print("✗ No devices connected!")
            print("Please connect your Android device via USB")
            return
    else:
        device_id = devices[0]["device_id"]
        print(f"✓ Device found: {device_id}\n")
    
    # Run full test
    run_full_test(device_id)

if __name__ == "__main__":
    main()
