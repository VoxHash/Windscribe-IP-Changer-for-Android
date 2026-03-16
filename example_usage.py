#!/usr/bin/env python3
"""
Example usage of Windscribe IP Changer
Demonstrates various ways to use the IP changer script
"""

from windscribe_ip_changer import WindscribeIPChanger
import time

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
            print("The script will automatically:")
            print("  - Open Windscribe app")
            print("  - Navigate to location selection")
            print("  - Search and select location")
            print("  - Connect automatically")
        else:
            print("Using CLI mode (no UI automation needed)")
    else:
        print("No device connected!")

if __name__ == "__main__":
    # Run examples
    example_status_check()
    example_ui_automation()
    example_single_change()
    # Uncomment to run other examples:
    # example_rotation()
    # example_custom_servers()
