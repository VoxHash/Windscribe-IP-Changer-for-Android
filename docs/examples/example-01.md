# Example 01: Basic IP Change

Simple example of changing IP address once.

## Scenario

You want to change your Android device's IP address by connecting to a random Windscribe server.

## Steps

1. Ensure your Android device is connected via ADB:

```bash
adb devices
```

2. Run the script:

```bash
python3 windscribe_ip_changer.py
```

## Expected Output

```
Connected device: emulator-5554
Windscribe app detected: com.windscribe.android
Current IP: 192.168.1.100
Windscribe status: Not connected

Changing IP to US East...
Connected to Windscribe: Connected to us-east
New IP: 203.0.113.42
```

## Using Python API

```python
from windscribe_ip_changer import WindscribeIPChanger

changer = WindscribeIPChanger()
if changer.check_adb_connection():
    success = changer.change_ip(wait_time=5)
    if success:
        print("IP changed successfully!")
```

## Next Steps

- [Example 02: Automatic Rotation](example-02.md)
- [Usage Guide](../usage.md)
