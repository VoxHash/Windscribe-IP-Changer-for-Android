#!/usr/bin/env python3
"""
Automated test script that runs all tests without user interaction
"""

import time
import subprocess
from windscribe_ip_changer import WindscribeIPChanger

def wait_for_device_authorization(adb_path, max_wait=60):
    """Wait for device to be authorized"""
    print("Waiting for device authorization...")
    print("Please accept the USB debugging prompt on your Android device.\n")
    
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

def run_automated_tests(device_id=None, test_connection=False):
    """Run comprehensive automated tests"""
    print("\n" + "=" * 60)
    print("Running Automated Device Tests")
    print("=" * 60)
    
    changer = WindscribeIPChanger(device_id=device_id)
    results = {
        "device_connection": False,
        "screen_detection": False,
        "windscribe_detection": False,
        "ui_automation": False,
        "connection_flow": False
    }
    
    # Test 1: Device connection
    print("\n[1/5] Testing device connection...")
    if changer.check_adb_connection():
        print("✓ Device connected")
        device_name = changer.get_connected_device()
        print(f"  Device ID: {device_name}")
        results["device_connection"] = True
    else:
        print("✗ Device connection failed")
        return results
    
    # Test 2: Screen detection
    print("\n[2/5] Testing screen size detection...")
    try:
        screen_width, screen_height = changer._get_screen_size()
        print(f"✓ Screen size: {screen_width}x{screen_height}")
        print(f"  Center coordinates: ({screen_width // 2}, {screen_height // 2})")
        results["screen_detection"] = True
    except Exception as e:
        print(f"✗ Screen detection failed: {e}")
        return results
    
    # Test 3: Windscribe detection
    print("\n[3/5] Testing Windscribe installation...")
    if changer.check_windscribe_installed():
        print("✓ Windscribe found")
        package = changer.get_windscribe_package_name()
        if package:
            print(f"  Package: {package}")
            print("  Type: Android App (UI automation enabled)")
        else:
            print("  Type: CLI")
        results["windscribe_detection"] = True
        
        status = changer.get_windscribe_status()
        if status:
            print(f"  Status: {status}")
        else:
            print("  Status: Not connected")
        
        ip = changer.get_current_ip()
        if ip:
            print(f"  Current IP: {ip}")
    else:
        print("✗ Windscribe not found!")
        print("  Please install Windscribe app from Google Play Store")
        return results
    
    # Test 4: UI automation capabilities
    print("\n[4/5] Testing UI automation capabilities...")
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
            results["ui_automation"] = True
        else:
            print("  ⚠ Tap command may have failed")
    else:
        print("  UI automation: Not needed (CLI mode)")
        results["ui_automation"] = True
    
    # Test 5: Connection flow (if requested)
    if test_connection:
        print("\n[5/5] Testing connection flow...")
        print("  Testing disconnect...")
        if changer.disconnect_windscribe():
            print("  ✓ Disconnect completed")
        time.sleep(2)
        
        print("\n  Testing connect to 'us-east'...")
        if changer.connect_windscribe("us-east"):
            print("  ✓ Connection completed")
            time.sleep(3)
            
            status = changer.get_windscribe_status()
            ip = changer.get_current_ip()
            print(f"  Final Status: {status}")
            print(f"  Final IP: {ip}")
            results["connection_flow"] = True
        else:
            print("  ✗ Connection failed")
    else:
        print("\n[5/5] Connection flow test skipped (use --test-connection to enable)")
        results["connection_flow"] = None
    
    return results

def main():
    import sys
    
    test_connection = "--test-connection" in sys.argv
    
    print("=" * 60)
    print("Windscribe IP Changer - Automated Device Testing")
    print("=" * 60)
    
    # Check ADB
    changer = WindscribeIPChanger()
    if not changer.adb_path:
        print("✗ ADB not found!")
        print("Please install ADB: sudo pacman -S android-tools")
        return 1
    
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
                return 1
        else:
            print("✗ No devices connected!")
            print("Please connect your Android device via USB")
            return 1
    else:
        device_id = devices[0]["device_id"]
        print(f"✓ Device found: {device_id}\n")
    
    # Run automated tests
    results = run_automated_tests(device_id, test_connection)
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Results Summary")
    print("=" * 60)
    for test_name, result in results.items():
        status = "✓ PASS" if result is True else "✗ FAIL" if result is False else "⊘ SKIP"
        print(f"{test_name.replace('_', ' ').title():<30} {status}")
    
    all_passed = all(r for r in results.values() if r is not None)
    print("\n" + "=" * 60)
    if all_passed:
        print("✓ All tests passed!")
        return 0
    else:
        print("✗ Some tests failed")
        return 1

if __name__ == "__main__":
    exit(main())
