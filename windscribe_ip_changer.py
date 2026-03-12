#!/usr/bin/env python3
"""
Windscribe IP Changer for Android via ADB
This script connects to Android devices/emulators via ADB and changes IPs by
connecting to different Windscribe VPN servers.
"""

import subprocess
import json
import time
import random
import argparse
import sys
import os
from typing import Optional, List

# Default Windscribe server locations
DEFAULT_SERVERS = [
    {"name": "US East", "location": "us-east"},
    {"name": "US West", "location": "us-west"},
    {"name": "EU Central", "location": "eu-central"},
    {"name": "EU West", "location": "eu-west"},
    {"name": "Asia Pacific", "location": "ap-southeast"},
]

class WindscribeIPChanger:
    """Manages Windscribe VPN connections on Android via ADB."""
    
    def __init__(self, adb_path: Optional[str] = None):
        """Initialize the IP changer.
        
        Args:
            adb_path: Path to ADB executable (auto-detected if in PATH)
        """
        self.adb_path = adb_path or self._find_adb()
        self.current_server = None
        
    def _find_adb(self) -> Optional[str]:
        """Find ADB executable in PATH."""
        common_paths = [
            "/usr/bin/adb",
            "/usr/local/bin/adb",
            os.path.join(os.path.expanduser("~"), "Android/Sdk/platform-tools/adb"),
        ]
        for path in common_paths:
            if os.path.isfile(path) and os.access(path, os.X_OK):
                return path
        # Try to find via which
        try:
            result = subprocess.run(
                ["which", "adb"],
                capture_output=True,
                text=True,
                stderr=subprocess.PIPE
            )
            if result.returncode == 0 and result.stdout:
                return result.stdout.strip()
        except:
            pass
        return None
    
    def check_adb_connection(self) -> bool:
        """Check if ADB is connected to a device."""
        if not self.adb_path:
            print("Error: ADB not found. Please install ADB or specify path with --adb-path")
            return False
        
        try:
            result = subprocess.run(
                [self.adb_path, "devices"],
                capture_output=True,
                text=True,
                stderr=subprocess.PIPE
            )
            if result.returncode == 0:
                output = result.stdout.strip()
                # Check if any device is listed
                lines = output.split("\n")
                for line in lines[1:]:  # Skip header
                    if "device" in line.lower() or "emulator" in line.lower():
                        return True
            return False
        except Exception as e:
            print(f"Error checking ADB connection: {e}")
            return False
    
    def get_connected_device(self) -> Optional[str]:
        """Get the name of the connected device."""
        try:
            result = subprocess.run(
                [self.adb_path, "devices"],
                capture_output=True,
                text=True,
                stderr=subprocess.PIPE
            )
            if result.returncode == 0:
                lines = [line.strip() for line in result.stdout.strip().split("\n") if line.strip()]
                for line in lines:
                    # Skip header line
                    if "list of devices" in line.lower():
                        continue
                    if "device" in line.lower() or "emulator" in line.lower():
                        # Extract device ID (format: "device_id    device" or "emulator-5554    device")
                        parts = line.split()
                        if len(parts) >= 1:
                            return parts[0]  # Return device ID (first part)
                return None
        except Exception as e:
            print(f"Error getting device name: {e}")
            return None
    
    def check_windscribe_installed(self) -> bool:
        """Check if Windscribe is installed on the device (CLI or app)."""
        # Check for CLI first
        try:
            result = subprocess.run(
                [self.adb_path, "shell", "which", "windscribe"],
                capture_output=True,
                text=True,
                stderr=subprocess.PIPE
            )
            if result.returncode == 0:
                return True
        except:
            pass
        
        # Check for Android app package
        try:
            result = subprocess.run(
                [self.adb_path, "shell", "pm", "list", "packages"],
                capture_output=True,
                text=True,
                stderr=subprocess.PIPE
            )
            if result.returncode == 0 and "windscribe" in result.stdout.lower():
                return True
        except:
            pass
        
        return False
    
    def get_windscribe_package_name(self) -> Optional[str]:
        """Get Windscribe app package name."""
        try:
            result = subprocess.run(
                [self.adb_path, "shell", "pm", "list", "packages"],
                capture_output=True,
                text=True,
                stderr=subprocess.PIPE
            )
            if result.returncode == 0:
                for line in result.stdout.split("\n"):
                    if "windscribe" in line.lower():
                        # Extract package name (format: "package:com.windscribe.android")
                        if ":" in line:
                            return line.split(":")[1].strip()
            return None
        except:
            return None
    
    def get_windscribe_status(self) -> Optional[str]:
        """Get current Windscribe connection status."""
        # Try CLI first
        try:
            result = subprocess.run(
                [self.adb_path, "shell", "windscribe", "status"],
                capture_output=True,
                text=True,
                stderr=subprocess.PIPE
            )
            if result.returncode == 0:
                return result.stdout.strip()
        except:
            pass
        
        # Check VPN status via Android system
        try:
            result = subprocess.run(
                [self.adb_path, "shell", "dumpsys", "vpn"],
                capture_output=True,
                text=True,
                stderr=subprocess.PIPE
            )
            if result.returncode == 0:
                output = result.stdout.strip()
                if "windscribe" in output.lower():
                    # Parse VPN status
                    for line in output.split("\n"):
                        if "connected" in line.lower() or "connecting" in line.lower():
                            return line.strip()
                    return "VPN status found"
            return None
        except Exception as e:
            print(f"Error getting Windscribe status: {e}")
            return None
    
    def disconnect_windscribe(self) -> bool:
        """Disconnect from current Windscribe server."""
        # Try CLI first
        try:
            result = subprocess.run(
                [self.adb_path, "shell", "windscribe", "disconnect"],
                capture_output=True,
                text=True,
                stderr=subprocess.PIPE,
                timeout=30
            )
            if result.returncode == 0:
                print("Disconnected from Windscribe")
                return True
        except subprocess.TimeoutExpired:
            pass
        except:
            pass
        
        # Try via Android VPN disconnect
        try:
            # Disconnect VPN via settings
            result = subprocess.run(
                [self.adb_path, "shell", "svc", "vpn", "disconnect"],
                capture_output=True,
                text=True,
                stderr=subprocess.PIPE,
                timeout=30
            )
            if result.returncode == 0:
                print("Disconnected VPN")
                return True
        except:
            pass
        
        # Try via app UI automation (fallback)
        package = self.get_windscribe_package_name()
        if package:
            try:
                # Open Windscribe app
                subprocess.run(
                    [self.adb_path, "shell", "monkey", "-p", package, "-c", "android.intent.category.LAUNCHER", "1"],
                    capture_output=True,
                    timeout=5
                )
                time.sleep(2)
                # Try to find and click disconnect button
                # This is a simplified approach - may need adjustment based on actual UI
                subprocess.run(
                    [self.adb_path, "shell", "input", "keyevent", "KEYCODE_BACK"],
                    capture_output=True
                )
                print("Attempted disconnect via app")
                return True
            except:
                pass
        
        print("Failed to disconnect from Windscribe")
        return False
    
    def connect_windscribe(self, location: str) -> bool:
        """Connect to a Windscribe server at the specified location.
        
        Args:
            location: Windscribe server location (e.g., "us-east", "eu-west")
        """
        # Try CLI first
        try:
            result = subprocess.run(
                [self.adb_path, "shell", "windscribe", "connect", location],
                capture_output=True,
                text=True,
                stderr=subprocess.PIPE,
                timeout=60
            )
            if result.returncode == 0:
                output = result.stdout.strip()
                print(f"Connected to Windscribe: {output}")
                self.current_server = location
                return True
        except subprocess.TimeoutExpired:
            pass
        except:
            pass
        
        # For Android app, we need to use UI automation
        # This is a simplified approach - actual implementation may vary
        package = self.get_windscribe_package_name()
        if package:
            try:
                # Open Windscribe app
                subprocess.run(
                    [self.adb_path, "shell", "monkey", "-p", package, "-c", "android.intent.category.LAUNCHER", "1"],
                    capture_output=True,
                    timeout=5
                )
                time.sleep(3)  # Wait for app to open
                
                # Note: Actual UI automation would require more sophisticated approach
                # This is a placeholder - you may need to use uiautomator or similar tools
                print(f"Opened Windscribe app. Please manually connect to {location}")
                print("Note: Full UI automation requires additional setup")
                self.current_server = location
                return True
            except Exception as e:
                print(f"Error opening Windscribe app: {e}")
                return False
        
        print(f"Failed to connect to Windscribe location: {location}")
        return False
    
    def get_current_ip(self) -> Optional[str]:
        """Get current IP address from the device."""
        try:
            # Method 1: Get public IP via curl (if available)
            try:
                result = subprocess.run(
                    [self.adb_path, "shell", "curl", "-s", "https://api.ipify.org"],
                    capture_output=True,
                    text=True,
                    stderr=subprocess.PIPE,
                    timeout=10
                )
                if result.returncode == 0 and result.stdout.strip():
                    ip = result.stdout.strip()
                    if ip and "." in ip:
                        return ip
            except:
                pass
            
            # Method 2: Via network interface
            result = subprocess.run(
                [self.adb_path, "shell", "ip", "addr", "show"],
                capture_output=True,
                text=True,
                stderr=subprocess.PIPE
            )
            if result.returncode == 0:
                output = result.stdout.strip()
                # Look for VPN interface first
                for line in output.split("\n"):
                    if "tun0" in line or "ppp" in line:
                        # Get IP from VPN interface
                        if "inet " in line:
                            parts = line.split()
                            for part in parts:
                                if part.startswith(("10.", "172.", "192.168.")):
                                    return part.split("/")[0]
                # Fallback to any interface
                for line in output.split("\n"):
                    if "inet " in line:
                        parts = line.split()
                        for part in parts:
                            if part.startswith(("10.", "172.", "192.168.")):
                                return part.split("/")[0]
            
            # Method 3: Via Windscribe status
            status = self.get_windscribe_status()
            if status and "IP:" in status:
                parts = status.split("IP:")
                if len(parts) > 1:
                    ip_part = parts[1].strip().split()[0]
                    return ip_part
            
            return None
        except Exception as e:
            print(f"Error getting IP: {e}")
            return None
    
    def change_ip(self, servers: Optional[List[dict]] = None, wait_time: int = 5) -> bool:
        """Change IP by connecting to a random Windscribe server.
        
        Args:
            servers: List of server dictionaries (if None, uses defaults)
            wait_time: Seconds to wait after connecting
        """
        if not servers:
            servers = DEFAULT_SERVERS
        
        # Check prerequisites
        if not self.check_adb_connection():
            print("Error: No Android device connected via ADB")
            print("Please connect a device or start an emulator")
            return False
        
        device_name = self.get_connected_device()
        print(f"Connected device: {device_name or 'Unknown'}")
        
        # Check if Windscribe is installed
        if not self.check_windscribe_installed():
            print("Error: Windscribe not found on device")
            print("Please install Windscribe app from: https://windscribe.com")
            print("Or install Windscribe CLI if available")
            return False
        
        # Show installation type
        package = self.get_windscribe_package_name()
        if package:
            print(f"Windscribe app detected: {package}")
        else:
            print("Using Windscribe CLI")
        
        # Get current status
        current_ip = self.get_current_ip()
        print(f"Current IP: {current_ip or 'Unknown'}")
        
        current_status = self.get_windscribe_status()
        if current_status:
            print(f"Windscribe status: {current_status}")
        
        # Select random server
        available_locations = [s["location"] for s in servers]
        selected_server = random.choice(servers)
        selected_location = selected_server["location"]
        selected_name = selected_server["name"]
        
        print(f"\nChanging IP to {selected_name}...")
        
        # Disconnect if connected
        if self.current_server:
            print(f"Disconnecting from {self.current_server}...")
            self.disconnect_windscribe()
            time.sleep(2)  # Wait for disconnect to complete
        
        # Connect to new server
        success = self.connect_windscribe(selected_location)
        if success:
            time.sleep(wait_time)  # Wait for connection to stabilize
            
            # Verify new IP
            new_ip = self.get_current_ip()
            print(f"New IP: {new_ip or 'Unknown'}")
            return True
        else:
            print("Failed to change IP")
            return False
    
    def rotate_ips(self, count: int = 5, interval: int = 300, servers: Optional[List[dict]] = None):
        """Automatically rotate IPs at specified intervals.
        
        Args:
            count: Number of IP changes to perform
            interval: Seconds between each change
            servers: List of server dictionaries
        """
        print(f"Starting automatic IP rotation: {count} changes every {interval} seconds")
        for i in range(count):
            print(f"\n--- Rotation {i+1}/{count} ---")
            success = self.change_ip(servers, wait_time=5)
            if not success:
                print("Skipping this rotation due to error")
                continue
            if i < count - 1:  # Don't wait after last change
                print(f"Waiting {interval} seconds before next change...")
                time.sleep(interval)


def main():
    parser = argparse.ArgumentParser(
        description="Change Windscribe IP on Android via ADB",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "--adb-path",
        type=str,
        default=None,
        help="Path to ADB executable (auto-detected if not specified)"
    )
    parser.add_argument(
        "--servers",
        type=str,
        default=None,
        help="Path to JSON file with server list (uses defaults if not specified)"
    )
    parser.add_argument(
        "--wait",
        type=int,
        default=5,
        help="Seconds to wait after connecting (default: 5)"
    )
    parser.add_argument(
        "--rotate",
        action="store_true",
        help="Enable automatic IP rotation mode"
    )
    parser.add_argument(
        "--count",
        type=int,
        default=5,
        help="Number of rotations (default: 5)"
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=300,
        help="Seconds between rotations (default: 300)"
    )
    
    args = parser.parse_args()
    
    # Load custom servers if provided
    servers = None
    if args.servers:
        try:
            with open(args.servers, "r") as f:
                servers = json.load(f)
        except Exception as e:
            print(f"Error loading servers file: {e}")
            return
    
    # Initialize IP changer
    changer = WindscribeIPChanger(adb_path=args.adb_path)
    
    # Validate ADB path
    if not changer.adb_path:
        print("Error: ADB not found. Please install ADB or specify path with --adb-path")
        sys.exit(1)
    
    if args.rotate:
        # Automatic rotation mode
        changer.rotate_ips(
            count=args.count,
            interval=args.interval,
            servers=servers
        )
    else:
        # Single IP change
        changer.change_ip(servers=servers, wait_time=args.wait)


if __name__ == "__main__":
    main()
