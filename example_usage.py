#!/usr/bin/env python3
"""
Example usage of Windscribe IP Changer
Demonstrates various ways to use the IP changer script
"""

from windscribe_ip_changer import WindscribeIPChanger, manage_multiple_devices
import time
import json

def example_single_change():
    """Example: Change IP once"""
    print("=== Example 1: Single IP Change ===")
    changer = WindscribeIPChanger()
    
    if changer.check_adb_connection():
        changer.change_ip(wait_time=5)
    else:
        print("No device connected!")

def example_rotation():
    """Example: Rotate IPs automatically"""
    print("\n=== Example 2: Automatic IP Rotation ===")
    changer = WindscribeIPChanger()
    
    if changer.check_adb_connection():
        # Rotate 5 times, every 5 minutes
        changer.rotate_ips(count=5, interval=300)
    else:
        print("No device connected!")

def example_custom_servers():
    """Example: Use custom server list"""
    print("\n=== Example 3: Custom Servers ===")
    custom_servers = [
        {"name": "US East", "location": "us-east"},
        {"name": "EU West", "location": "eu-west"},
    ]
    
    changer = WindscribeIPChanger()
    
    if changer.check_adb_connection():
        changer.change_ip(servers=custom_servers, wait_time=5)
    else:
        print("No device connected!")

def example_status_check():
    """Example: Check current status"""
    print("\n=== Example 4: Status Check ===")
    changer = WindscribeIPChanger()
    
    if changer.check_adb_connection():
        device = changer.get_connected_device()
        print(f"Device: {device}")
        
        if changer.check_windscribe_installed():
            status = changer.get_windscribe_status()
            print(f"Windscribe Status: {status}")
            
            ip = changer.get_current_ip()
            print(f"Current IP: {ip}")
        else:
            print("Windscribe not installed!")
    else:
        print("No device connected!")

def example_ui_automation():
    """Example: Demonstrate UI automation capabilities"""
    print("\n=== Example 5: UI Automation Demo ===")
    changer = WindscribeIPChanger()
    
    if changer.check_adb_connection():
        package = changer.get_windscribe_package_name()
        if package:
            print(f"Windscribe app detected: {package}")
            screen_width, screen_height = changer._get_screen_size()
            print(f"Screen size: {screen_width}x{screen_height}")
            print("UI automation is fully enabled - no manual interaction needed!")
            print("The script changes IP from INSIDE the app using:")
            print("  - Taps (adb shell input tap) to navigate UI")
            print("  - Text input (adb shell input text) to search locations")
            print("  - Automatic connection flow:")
            print("    1. Open Windscribe app")
            print("    2. Navigate to location selection")
            print("    3. Search and select location")
            print("    4. Connect automatically")
            print("  - All operations happen from inside the app on the device")
        else:
            print("Using CLI mode (no UI automation needed)")
    else:
        print("No device connected!")

def example_specific_device():
    """Example: Target a specific device by ID"""
    print("\n=== Example 6: Specific Device ===")
    # List available devices first
    changer = WindscribeIPChanger()
    devices = changer.list_devices()
    
    if devices:
        print("Available devices:")
        for device in devices:
            print(f"  - {device['device_id']} ({device['status']})")
        
        # Use first device as example
        device_id = devices[0]['device_id']
        print(f"\nConnecting to device: {device_id}")
        
        device_changer = WindscribeIPChanger(device_id=device_id)
        if device_changer.check_adb_connection():
            device_changer.change_ip(wait_time=5)
        else:
            print(f"Device {device_id} not available")
    else:
        print("No devices connected!")

def example_multi_device():
    """Example: Manage multiple devices simultaneously"""
    print("\n=== Example 7: Multi-Device Management ===")
    
    # List available devices
    changer = WindscribeIPChanger()
    devices = changer.list_devices()
    
    if len(devices) < 2:
        print("Need at least 2 devices for this example")
        print(f"Currently connected: {len(devices)} device(s)")
        return
    
    # Create multi-device configuration
    device_configs = [
        {"device_id": devices[0]["device_id"], "location": "us-east"},
        {"device_id": devices[1]["device_id"], "location": "eu-west"},
    ]
    
    print(f"Connecting {len(device_configs)} devices to different locations:")
    for config in device_configs:
        print(f"  - {config['device_id']} → {config['location']}")
    
    # Manage multiple devices
    results = manage_multiple_devices(changer.adb_path, device_configs)
    
    print("\nResults:")
    for device_id, result in results.items():
        status = "✓ Success" if result.get("success") else "✗ Failed"
        print(f"  {device_id}: {status}")
        if result.get("ip"):
            print(f"    IP: {result['ip']}")

def example_list_devices():
    """Example: List all connected devices"""
    print("\n=== Example 8: List Devices ===")
    changer = WindscribeIPChanger()
    devices = changer.list_devices()
    
    if devices:
        print(f"Found {len(devices)} connected device(s):")
        for device in devices:
            print(f"  Device ID: {device['device_id']}")
            print(f"  Status: {device['status']}")
            
            # Check Windscribe on each device
            device_changer = WindscribeIPChanger(device_id=device['device_id'])
            if device_changer.check_windscribe_installed():
                package = device_changer.get_windscribe_package_name()
                print(f"  Windscribe: Installed ({package or 'CLI'})")
            else:
                print(f"  Windscribe: Not installed")
            print()
    else:
        print("No devices connected via ADB")

if __name__ == "__main__":
    # Run examples
    example_list_devices()
    example_status_check()
    example_ui_automation()
    example_specific_device()
    # Uncomment to run other examples:
    # example_single_change()
    # example_rotation()
    # example_custom_servers()
    # example_multi_device()  # Requires 2+ devices