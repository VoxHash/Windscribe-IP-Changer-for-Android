# API Documentation

Python API reference for Windscribe IP Changer for Android.

## WindscribeIPChanger

Main class for managing Windscribe VPN connections.

### `__init__(adb_path=None)`

Initialize the IP changer.

**Parameters:**
- `adb_path` (str, optional): Path to ADB executable. Auto-detected if not specified.

**Example:**
```python
changer = WindscribeIPChanger()
```

### `check_adb_connection() -> bool`

Check if ADB is connected to a device.

**Returns:** `bool` - True if device is connected

**Example:**
```python
if changer.check_adb_connection():
    print("Device connected")
```

### `get_connected_device() -> Optional[str]`

Get the name/ID of the connected device.

**Returns:** `Optional[str]` - Device ID or None

### `check_windscribe_installed() -> bool`

Check if Windscribe is installed (CLI or app).

**Returns:** `bool` - True if Windscribe is found

### `get_windscribe_package_name() -> Optional[str]`

Get Windscribe Android app package name.

**Returns:** `Optional[str]` - Package name or None

### `get_windscribe_status() -> Optional[str]`

Get current Windscribe connection status.

**Returns:** `Optional[str]` - Status string or None

### `disconnect_windscribe() -> bool`

Disconnect from current Windscribe server.

**Returns:** `bool` - True if successful

### `connect_windscribe(location: str) -> bool`

Connect to a Windscribe server at the specified location.

**Parameters:**
- `location` (str): Server location (e.g., "us-east", "eu-west")

**Returns:** `bool` - True if successful

### `get_current_ip() -> Optional[str]`

Get current IP address from the device.

**Returns:** `Optional[str]` - IP address or None

### `change_ip(servers=None, wait_time=5) -> bool`

Change IP by connecting to a random Windscribe server.

**Parameters:**
- `servers` (List[dict], optional): List of server dictionaries
- `wait_time` (int): Seconds to wait after connecting

**Returns:** `bool` - True if successful

### `rotate_ips(count=5, interval=300, servers=None)`

Automatically rotate IPs at specified intervals.

**Parameters:**
- `count` (int): Number of IP changes to perform
- `interval` (int): Seconds between each change
- `servers` (List[dict], optional): List of server dictionaries

## Example Usage

```python
from windscribe_ip_changer import WindscribeIPChanger

# Initialize
changer = WindscribeIPChanger()

# Check connection
if changer.check_adb_connection():
    device = changer.get_connected_device()
    print(f"Connected to: {device}")
    
    # Change IP
    if changer.change_ip(wait_time=5):
        new_ip = changer.get_current_ip()
        print(f"New IP: {new_ip}")
```

## See Also

- [Usage Guide](usage.md)
- [Examples](examples/example-01.md)
