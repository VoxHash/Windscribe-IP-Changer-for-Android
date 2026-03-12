# CLI Reference

Complete command-line interface reference.

## Synopsis

```bash
python3 windscribe_ip_changer.py [OPTIONS]
```

## Options

### `--adb-path PATH`

Specify custom path to ADB executable.

```bash
python3 windscribe_ip_changer.py --adb-path /usr/local/bin/adb
```

### `--servers FILE`

Path to JSON file containing server list.

```bash
python3 windscribe_ip_changer.py --servers servers.json
```

### `--wait SECONDS`

Seconds to wait after connecting to VPN server. Default: 5

```bash
python3 windscribe_ip_changer.py --wait 10
```

### `--rotate`

Enable automatic IP rotation mode.

```bash
python3 windscribe_ip_changer.py --rotate
```

### `--count NUMBER`

Number of IP rotations to perform. Only used with `--rotate`. Default: 5

```bash
python3 windscribe_ip_changer.py --rotate --count 10
```

### `--interval SECONDS`

Seconds between each IP rotation. Only used with `--rotate`. Default: 300

```bash
python3 windscribe_ip_changer.py --rotate --interval 600
```

## Examples

### Basic Usage

```bash
python3 windscribe_ip_changer.py
```

### Rotation Mode

```bash
python3 windscribe_ip_changer.py --rotate --count 20 --interval 1800
```

### Custom Configuration

```bash
python3 windscribe_ip_changer.py \
  --adb-path ~/Android/Sdk/platform-tools/adb \
  --servers my-servers.json \
  --wait 8
```

## Exit Codes

- `0` - Success
- `1` - Error (ADB not found, no device connected, etc.)

## See Also

- [Usage Guide](usage.md)
- [Configuration](configuration.md)
