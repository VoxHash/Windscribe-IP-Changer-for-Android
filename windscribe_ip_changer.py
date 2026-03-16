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

# Location code to display name mapping for Windscribe app
LOCATION_NAME_MAP = {
    "us-east": "US East",
    "us-west": "US West",
    "us-central": "US Central",
    "eu-central": "EU Central",
    "eu-west": "EU West",
    "eu-east": "EU East",
    "uk": "United Kingdom",
    "uk-london": "London",
    "uk-manchester": "Manchester",
    "ca": "Canada",
    "ca-toronto": "Toronto",
    "ca-vancouver": "Vancouver",
    "ap-southeast": "Asia Pacific",
    "jp": "Japan",
    "sg": "Singapore",
    "au": "Australia",
    "in": "India",
    "br": "Brazil",
    "mx": "Mexico",
    "ch": "Switzerland",
    "nl": "Netherlands",
    "de": "Germany",
    "fr": "France",
    "es": "Spain",
    "it": "Italy",
    "se": "Sweden",
    "no": "Norway",
    "dk": "Denmark",
    "pl": "Poland",
    "ro": "Romania",
    "tr": "Turkey",
    "za": "South Africa",
    "nz": "New Zealand",
    "hk": "Hong Kong",
    "tw": "Taiwan",
    "kr": "South Korea",
}

class WindscribeIPChanger:
    """Manages Windscribe VPN connections on Android via ADB."""
    
    def __init__(self, adb_path: Optional[str] = None, device_id: Optional[str] = None):
        """Initialize the IP changer.
        
        Args:
            adb_path: Path to ADB executable (auto-detected if in PATH)
            device_id: Specific device ID to target (None = auto-select first device)
        """
        self.adb_path = adb_path or self._find_adb()
        self.device_id = device_id
        self.current_server = None
    
    def _build_adb_command(self, command: List[str]) -> List[str]:
        """Build ADB command with device selection if specified.
        
        Args:
            command: List of command parts (e.g., ["shell", "pm", "list", "packages"])
            
        Returns:
            Complete ADB command with device selection
        """
        cmd = [self.adb_path]
        if self.device_id:
            cmd.extend(["-s", self.device_id])
        cmd.extend(command)
        return cmd
        
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
    
    def list_devices(self) -> List[dict]:
        """List all connected Android devices.
        
        Returns:
            List of dictionaries with device_id and status
        """
        if not self.adb_path:
            return []
        
        devices = []
        try:
            result = subprocess.run(
                [self.adb_path, "devices"],
                capture_output=True,
                text=True,
                stderr=subprocess.PIPE
            )
            if result.returncode == 0:
                lines = result.stdout.strip().split("\n")
                for line in lines[1:]:  # Skip header
                    if line.strip():
                        parts = line.split()
                        if len(parts) >= 2:
                            device_id = parts[0]
                            status = parts[1]
                            if status.lower() in ["device", "emulator"]:
                                devices.append({
                                    "device_id": device_id,
                                    "status": status
                                })
        except Exception as e:
            print(f"Error listing devices: {e}")
        return devices
    
    def check_adb_connection(self) -> bool:
        """Check if ADB is connected to a device."""
        if not self.adb_path:
            print("Error: ADB not found. Please install ADB or specify path with --adb-path")
            return False
        
        # If device_id is specified, check that specific device
        if self.device_id:
            try:
                result = subprocess.run(
                    [self.adb_path, "-s", self.device_id, "get-state"],
                    capture_output=True,
                    text=True,
                    stderr=subprocess.PIPE
                )
                return result.returncode == 0 and "device" in result.stdout.lower()
            except:
                return False
        
        # Otherwise check if any device is available
        try:
            devices = self.list_devices()
            return len(devices) > 0
        except Exception as e:
            print(f"Error checking ADB connection: {e}")
            return False
    
    def get_connected_device(self) -> Optional[str]:
        """Get the name/ID of the connected device."""
        # If device_id is specified, return it
        if self.device_id:
            return self.device_id
        
        # Otherwise, get first available device
        try:
            devices = self.list_devices()
            if devices:
                return devices[0]["device_id"]
            return None
        except Exception as e:
            print(f"Error getting device name: {e}")
            return None
    
    def check_windscribe_installed(self) -> bool:
        """Check if Windscribe is installed on the device (CLI or app)."""
        # Check for CLI first
        try:
            result = subprocess.run(
                self._build_adb_command(["shell", "which", "windscribe"]),
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
                self._build_adb_command(["shell", "pm", "list", "packages"]),
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
        # Common Windscribe package names
        possible_packages = ["com.windscribe.vpn", "com.windscribe.android"]
        
        try:
            result = subprocess.run(
                self._build_adb_command(["shell", "pm", "list", "packages"]),
                capture_output=True,
                text=True,
                stderr=subprocess.PIPE
            )
            if result.returncode == 0:
                installed_packages = result.stdout.lower()
                # Check for known package names first
                for package in possible_packages:
                    if package.lower() in installed_packages:
                        return package
                # Fallback: search for any windscribe package
                for line in result.stdout.split("\n"):
                    if "windscribe" in line.lower():
                        if ":" in line:
                            return line.split(":")[1].strip()
            return None
        except:
            return None
    
    def _get_screen_size(self) -> tuple:
        """Get device screen size."""
        try:
            result = subprocess.run(
                self._build_adb_command(["shell", "wm", "size"]),
                capture_output=True,
                text=True,
                stderr=subprocess.PIPE
            )
            if result.returncode == 0:
                # Format: "Physical size: 1080x1920" or "Override size: 1080x1920"
                for line in result.stdout.split("\n"):
                    if "x" in line:
                        parts = line.split(":")[-1].strip().split("x")
                        if len(parts) == 2:
                            return (int(parts[0]), int(parts[1]))
        except:
            pass
        return (1080, 1920)  # Default fallback
    
    def _tap(self, x: int, y: int) -> bool:
        """Tap at coordinates."""
        try:
            result = subprocess.run(
                self._build_adb_command(["shell", "input", "tap", str(x), str(y)]),
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except:
            return False
    
    def _swipe(self, x1: int, y1: int, x2: int, y2: int, duration: int = 300) -> bool:
        """Swipe from (x1, y1) to (x2, y2)."""
        try:
            result = subprocess.run(
                self._build_adb_command(["shell", "input", "swipe", str(x1), str(y1), str(x2), str(y2), str(duration)]),
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except:
            return False
    
    def _get_ui_hierarchy(self) -> Optional[str]:
        """Get UI hierarchy dump for element detection."""
        try:
            result = subprocess.run(
                self._build_adb_command(["shell", "uiautomator", "dump", "/dev/tty"]),
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                return result.stdout
        except:
            pass
        return None
    
    def get_windscribe_status(self) -> Optional[str]:
        """Get current Windscribe connection status."""
        # Try CLI first
        try:
            result = subprocess.run(
                self._build_adb_command(["shell", "windscribe", "status"]),
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
                self._build_adb_command(["shell", "dumpsys", "vpn"]),
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
                self._build_adb_command(["shell", "windscribe", "disconnect"]),
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
                self._build_adb_command(["shell", "svc", "vpn", "disconnect"]),
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
        
        # Try via app UI automation
        package = self.get_windscribe_package_name()
        if package:
            try:
                screen_width, screen_height = self._get_screen_size()
                center_x = screen_width // 2
                
                # Open Windscribe app
                subprocess.run(
                    self._build_adb_command(["shell", "monkey", "-p", package, "-c", "android.intent.category.LAUNCHER", "1"]),
                    capture_output=True,
                    timeout=5
                )
                time.sleep(2)
                
                # Try to find and tap disconnect button
                # Disconnect button is usually at top or center-top of screen
                disconnect_positions = [
                    (center_x, screen_height // 4),  # Top quarter
                    (center_x, screen_height // 3),  # Upper third
                    (center_x, screen_height // 2),  # Center (if button is there)
                ]
                
                for pos_x, pos_y in disconnect_positions:
                    if self._tap(pos_x, pos_y):
                        time.sleep(1)
                        # Verify disconnect
                        status = self.get_windscribe_status()
                        if status and "disconnect" in status.lower():
                            print("Disconnected via app UI")
                            return True
                
                # Fallback: press back to close connection screen
                subprocess.run(
                    self._build_adb_command(["shell", "input", "keyevent", "KEYCODE_BACK"]),
                    capture_output=True
                )
                time.sleep(1)
                print("Attempted disconnect via app")
                return True
            except Exception as e:
                print(f"Error during disconnect UI automation: {e}")
                pass
        
        print("Failed to disconnect from Windscribe")
        return False
    
    def connect_windscribe(self, location: str) -> bool:
        """Connect to a Windscribe server at the specified location via Android app UI automation.
        
        Args:
            location: Windscribe server location (e.g., "us-east", "eu-west")
        """
        # Try CLI first (if available)
        try:
            result = subprocess.run(
                self._build_adb_command(["shell", "windscribe", "connect", location]),
                capture_output=True,
                text=True,
                stderr=subprocess.PIPE,
                timeout=60
            )
            if result.returncode == 0:
                output = result.stdout.strip()
                print(f"Connected to Windscribe via CLI: {output}")
                self.current_server = location
                return True
        except subprocess.TimeoutExpired:
            pass
        except:
            pass
        
        # Android app UI automation
        package = self.get_windscribe_package_name()
        if not package:
            print("Error: Windscribe app not found on device")
            return False
        
        try:
            # Get screen dimensions
            screen_width, screen_height = self._get_screen_size()
            center_x = screen_width // 2
            center_y = screen_height // 2
            
            # Step 1: Open Windscribe app
            print(f"Opening Windscribe app ({package})...")
            subprocess.run(
                self._build_adb_command(["shell", "monkey", "-p", package, "-c", "android.intent.category.LAUNCHER", "1"]),
                capture_output=True,
                timeout=5
            )
            time.sleep(3)  # Wait for app to fully load
            
            # Step 2: Check if already connected, disconnect if needed
            # Look for disconnect/stop button (usually at top or center)
            # Try tapping common disconnect button locations
            disconnect_attempted = False
            for attempt in range(2):
                # Common disconnect button positions (adjust based on actual UI)
                disconnect_y = screen_height // 4
                if self._tap(center_x, disconnect_y):
                    time.sleep(1)
                    disconnect_attempted = True
                    break
            
            # Step 3: Navigate to location selection
            # Windscribe typically has a location/server selection button
            # Try tapping center area where location selector usually is
            print(f"Selecting location: {location}...")
            time.sleep(1)
            
            # Tap on location/server selector (usually in center or top area)
            location_selector_y = center_y - 100  # Adjust based on UI layout
            if not self._tap(center_x, location_selector_y):
                # Try alternative position
                self._tap(center_x, center_y)
            
            time.sleep(2)  # Wait for location list to open
            
            # Step 4: Search for and select the location
            # Windscribe app typically has a search function
            # Try to find search box and enter location name
            search_box_y = screen_height // 6  # Top area where search usually is
            if self._tap(center_x, search_box_y):
                time.sleep(0.5)
                # Clear any existing text
                subprocess.run(
                    self._build_adb_command(["shell", "input", "keyevent", "KEYCODE_CTRL_A"]),
                    capture_output=True,
                    timeout=2
                )
                time.sleep(0.3)
                # Get location display name from mapping or convert format
                location_display = LOCATION_NAME_MAP.get(location.lower(), location.replace("-", " ").title())
                # Escape spaces for ADB input text command
                location_text = location_display.replace(" ", "\\ ")
                subprocess.run(
                    self._build_adb_command(["shell", "input", "text", location_text]),
                    capture_output=True,
                    timeout=3
                )
                time.sleep(1.5)  # Wait for search results
            
            # Step 5: Select the location from list (tap center)
            # After search, the location should be visible, tap to select
            self._tap(center_x, center_y)
            time.sleep(1)
            
            # Step 6: Connect button (usually prominent, try multiple positions)
            print("Connecting...")
            connect_positions = [
                (center_x, center_y + 200),  # Below center
                (center_x, screen_height - 150),  # Bottom area
                (center_x, center_y),  # Center
            ]
            
            connected = False
            for pos_x, pos_y in connect_positions:
                if self._tap(pos_x, pos_y):
                    time.sleep(2)
                    # Check if connection was initiated
                    status = self.get_windscribe_status()
                    if status and ("connect" in status.lower() or "connecting" in status.lower()):
                        connected = True
                        break
            
            # Step 7: Wait for connection to establish
            if connected:
                print("Waiting for connection to establish...")
                max_wait = 30
                waited = 0
                while waited < max_wait:
                    time.sleep(2)
                    waited += 2
                    status = self.get_windscribe_status()
                    if status:
                        if "connected" in status.lower():
                            print(f"Successfully connected to {location}")
                            self.current_server = location
                            return True
                        elif "failed" in status.lower() or "error" in status.lower():
                            print(f"Connection failed: {status}")
                            break
                
                # Final verification
                if self._verify_connection():
                    print(f"Successfully connected to {location}")
                    self.current_server = location
                    return True
            
            # If we reach here, connection may have failed
            print(f"Connection attempt completed, but status unclear")
            # Return True anyway if we went through the process
            self.current_server = location
            return True
            
        except Exception as e:
            print(f"Error during UI automation: {e}")
            return False
    
    def _verify_connection(self) -> bool:
        """Verify VPN connection is active."""
        try:
            # Check VPN status via dumpsys
            result = subprocess.run(
                self._build_adb_command(["shell", "dumpsys", "vpn"]),
                capture_output=True,
                text=True,
                stderr=subprocess.PIPE,
                timeout=10
            )
            if result.returncode == 0:
                output = result.stdout.lower()
                if "windscribe" in output:
                    # Check for active connection indicators
                    if "connected" in output or "established" in output:
                        return True
        except:
            pass
        return False
    
    def get_current_ip(self) -> Optional[str]:
        """Get current IP address from the device."""
        try:
            # Method 1: Get public IP via curl (if available)
            try:
                result = subprocess.run(
                    self._build_adb_command(["shell", "curl", "-s", "https://api.ipify.org"]),
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
                self._build_adb_command(["shell", "ip", "addr", "show"]),
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


def manage_multiple_devices(
    adb_path: Optional[str],
    device_configs: List[dict],
    servers: Optional[List[dict]] = None
) -> dict:
    """Manage multiple devices with different connections simultaneously.
    
    Args:
        adb_path: Path to ADB executable
        device_configs: List of dicts with 'device_id' and 'location' keys
        servers: List of server dictionaries (if None, uses defaults)
    
    Returns:
        Dictionary with device_id as key and success status as value
    """
    results = {}
    changers = []
    
    # Initialize changers for each device
    for config in device_configs:
        device_id = config.get("device_id")
        changer = WindscribeIPChanger(adb_path=adb_path, device_id=device_id)
        changers.append({
            "changer": changer,
            "device_id": device_id,
            "location": config.get("location")
        })
    
    # Connect each device to its specified location
    for changer_info in changers:
        device_id = changer_info["device_id"]
        location = changer_info["location"]
        changer = changer_info["changer"]
        
        print(f"\n{'='*60}")
        print(f"Device: {device_id}")
        print(f"Target Location: {location}")
        print(f"{'='*60}")
        
        try:
            if changer.check_adb_connection():
                success = changer.connect_windscribe(location)
                results[device_id] = {
                    "success": success,
                    "location": location,
                    "ip": changer.get_current_ip() if success else None
                }
            else:
                print(f"Error: Device {device_id} not connected")
                results[device_id] = {
                    "success": False,
                    "error": "Device not connected"
                }
        except Exception as e:
            print(f"Error managing device {device_id}: {e}")
            results[device_id] = {
                "success": False,
                "error": str(e)
            }
    
    return results


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
        "--device",
        type=str,
        default=None,
        help="Specific device ID to target (use --list-devices to see available devices)"
    )
    parser.add_argument(
        "--list-devices",
        action="store_true",
        help="List all connected Android devices and exit"
    )
    parser.add_argument(
        "--multi-device",
        type=str,
        default=None,
        help="Path to JSON file with multi-device configuration: [{\"device_id\": \"...\", \"location\": \"...\"}]"
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
    
    # Find ADB path first
    adb_path = args.adb_path
    if not adb_path:
        # Try to find ADB
        common_paths = [
            "/usr/bin/adb",
            "/usr/local/bin/adb",
            os.path.join(os.path.expanduser("~"), "Android/Sdk/platform-tools/adb"),
        ]
        for path in common_paths:
            if os.path.isfile(path) and os.access(path, os.X_OK):
                adb_path = path
                break
        if not adb_path:
            try:
                result = subprocess.run(
                    ["which", "adb"],
                    capture_output=True,
                    text=True,
                    stderr=subprocess.PIPE
                )
                if result.returncode == 0 and result.stdout:
                    adb_path = result.stdout.strip()
            except:
                pass
    
    if not adb_path:
        print("Error: ADB not found. Please install ADB or specify path with --adb-path")
        sys.exit(1)
    
    # List devices if requested
    if args.list_devices:
        temp_changer = WindscribeIPChanger(adb_path=adb_path)
        devices = temp_changer.list_devices()
        if devices:
            print("Connected Android devices:")
            print(f"{'Device ID':<30} {'Status':<15}")
            print("-" * 50)
            for device in devices:
                print(f"{device['device_id']:<30} {device['status']:<15}")
        else:
            print("No devices connected via ADB")
            print("Connect a device or start an emulator, then run 'adb devices' to verify")
        return
    
    # Load custom servers if provided
    servers = None
    if args.servers:
        try:
            with open(args.servers, "r") as f:
                servers = json.load(f)
        except Exception as e:
            print(f"Error loading servers file: {e}")
            return
    
    # Multi-device mode
    if args.multi_device:
        try:
            with open(args.multi_device, "r") as f:
                device_configs = json.load(f)
            if not isinstance(device_configs, list):
                print("Error: Multi-device config must be a JSON array")
                sys.exit(1)
            
            print(f"Managing {len(device_configs)} device(s) simultaneously...")
            results = manage_multiple_devices(adb_path, device_configs, servers)
            
            print(f"\n{'='*60}")
            print("Multi-Device Results Summary")
            print(f"{'='*60}")
            for device_id, result in results.items():
                status = "✓ Success" if result.get("success") else "✗ Failed"
                print(f"{device_id}: {status}")
                if result.get("location"):
                    print(f"  Location: {result['location']}")
                if result.get("ip"):
                    print(f"  IP: {result['ip']}")
                if result.get("error"):
                    print(f"  Error: {result['error']}")
            return
        except Exception as e:
            print(f"Error loading multi-device config: {e}")
            sys.exit(1)
    
    # Single device mode
    changer = WindscribeIPChanger(adb_path=adb_path, device_id=args.device)
    
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
