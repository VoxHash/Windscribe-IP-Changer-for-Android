# Usage Guide

How to use Windscribe IP Changer for Android.

## Basic Usage

### Single IP Change

Change IP to a random Windscribe server:

```bash
python3 windscribe_ip_changer.py
```

### Automatic IP Rotation

Rotate IPs automatically:

```bash
python3 windscribe_ip_changer.py --rotate --count 10 --interval 300
```

## Command-Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--adb-path` | Path to ADB executable | Auto-detected |
| `--servers` | Path to JSON file with server list | Uses defaults |
| `--wait` | Seconds to wait after connecting | 5 |
| `--rotate` | Enable automatic IP rotation | False |
| `--count` | Number of rotations | 5 |
| `--interval` | Seconds between rotations | 300 |

## Examples

### Custom ADB Path

```bash
python3 windscribe_ip_changer.py --adb-path /custom/path/to/adb
```

### Custom Server List

```bash
python3 windscribe_ip_changer.py --servers servers.json
```

### Custom Wait Time

```bash
python3 windscribe_ip_changer.py --wait 10
```

### Full Example

```bash
python3 windscribe_ip_changer.py \
  --servers servers.json \
  --rotate \
  --count 20 \
  --interval 600 \
  --wait 8
```

## Using as a Python Module

```python
from windscribe_ip_changer import WindscribeIPChanger

changer = WindscribeIPChanger()
if changer.check_adb_connection():
    changer.change_ip(wait_time=5)
```

See [API Documentation](api.md) for more details.

## Next Steps

- [Examples](examples/example-01.md) - Real-world examples
- [Configuration](configuration.md) - Customize settings
- [CLI Reference](cli.md) - Complete CLI documentation
