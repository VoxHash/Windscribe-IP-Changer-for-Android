# Example 02: Automatic IP Rotation

Example of automatically rotating IP addresses at intervals.

## Scenario

You want to automatically change IP addresses every 10 minutes for 1 hour (6 rotations).

## Steps

1. Ensure your Android device is connected:

```bash
adb devices
```

2. Run with rotation mode:

```bash
python3 windscribe_ip_changer.py --rotate --count 6 --interval 600
```

## Expected Output

```
Starting automatic IP rotation: 6 changes every 600 seconds
Connected device: emulator-5554
Windscribe app detected: com.windscribe.android

--- Rotation 1/6 ---
Current IP: 192.168.1.100
Changing IP to EU West...
Connected to Windscribe: Connected to eu-west
New IP: 198.51.100.23
Waiting 600 seconds before next change...

--- Rotation 2/6 ---
...
```

## Using Python API

```python
from windscribe_ip_changer import WindscribeIPChanger

changer = WindscribeIPChanger()
if changer.check_adb_connection():
    changer.rotate_ips(count=6, interval=600)
```

## Custom Server List

Use a custom server list:

```bash
python3 windscribe_ip_changer.py \
  --servers servers.json \
  --rotate \
  --count 6 \
  --interval 600
```

## Next Steps

- [Example 01: Basic IP Change](example-01.md)
- [Configuration](../configuration.md)
