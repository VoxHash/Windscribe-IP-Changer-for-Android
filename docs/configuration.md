# Configuration

How to configure Windscribe IP Changer for Android.

## Server Configuration

Create a custom server list by copying the example:

```bash
cp servers.json.example servers.json
```

Edit `servers.json`:

```json
[
  {
    "name": "US East",
    "location": "us-east"
  },
  {
    "name": "EU West",
    "location": "eu-west"
  }
]
```

Use it:

```bash
python3 windscribe_ip_changer.py --servers servers.json
```

## Available Locations

Common Windscribe server locations:

- `us-east`, `us-west` (United States)
- `eu-central`, `eu-west` (Europe)
- `ap-southeast`, `jp` (Asia Pacific)
- `sg` (Singapore)
- And more...

## ADB Path

If ADB is not in PATH, specify it:

```bash
python3 windscribe_ip_changer.py --adb-path /custom/path/to/adb
```

Common locations:
- Linux: `/usr/bin/adb`
- macOS: `/usr/local/bin/adb` or `~/Android/Sdk/platform-tools/adb`
- Windows: `C:\Users\YourName\AppData\Local\Android\Sdk\platform-tools\adb.exe`

## Environment Variables

Currently, configuration is done via command-line arguments. Future versions may support environment variables.

## See Also

- [Usage Guide](usage.md)
- [Examples](examples/example-01.md)
