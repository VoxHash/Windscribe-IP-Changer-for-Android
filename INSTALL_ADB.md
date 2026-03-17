# Installing ADB for Testing

## Quick Install (Arch Linux)

```bash
sudo pacman -S android-tools
```

## Verify Installation

After installation, verify ADB is working:

```bash
adb version
adb devices
```

## Connect Your Android Device

1. **Enable Developer Options** on your Android device:
   - Go to Settings → About Phone
   - Tap "Build Number" 7 times
   - Go back to Settings → Developer Options

2. **Enable USB Debugging**:
   - In Developer Options, enable "USB Debugging"
   - Connect device via USB
   - Accept the debugging prompt on your device

3. **Verify Connection**:
   ```bash
   adb devices
   ```
   You should see your device listed.

## Run Tests

Once ADB is installed and device is connected:

```bash
python3 test_with_device.py
```

Or use the automated setup script:

```bash
./setup_and_test.sh
```
