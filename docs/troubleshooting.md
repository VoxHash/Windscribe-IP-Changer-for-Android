# Troubleshooting

Common issues and solutions.

## ADB Connection Issues

### Problem: No Android device connected via ADB

**Solutions:**
1. Check ADB is installed: `adb version`
2. Check device connection: `adb devices`
3. For physical devices:
   - Enable USB debugging
   - Enable developer mode
   - Connect via USB
   - Accept debugging prompt on device
4. For emulators:
   - Start your emulator
   - Ensure ADB can see it: `adb devices`
5. Restart ADB server:
   ```bash
   adb kill-server
   adb start-server
   ```

## Windscribe Not Found

### Problem: Windscribe not found on device

**Solutions:**
1. **For CLI:** Install Windscribe CLI from https://windscribe.com
2. **For Android app:** Install Windscribe app from Google Play Store
3. Verify installation:
   - CLI: `adb shell which windscribe`
   - App: `adb shell pm list packages | grep windscribe`
4. Ensure Windscribe is configured and logged in

## Connection Timeouts

### Problem: Connection timeouts or failures

**Solutions:**
1. Increase wait time: `--wait 10` or higher
2. Check network connection on device
3. Verify Windscribe account is active
4. Try different server locations
5. Check VPN permissions on device

## Permission Denied

### Problem: Permission errors when running ADB commands

**Solutions:**
1. Ensure ADB has proper permissions
2. On Linux, add user to `plugdev` group:
   ```bash
   sudo usermod -a $USER plugdev
   ```
3. Restart ADB server:
   ```bash
   adb kill-server
   adb start-server
   ```

## IP Detection Issues

### Problem: Cannot detect IP address

**Solutions:**
1. Check network interface: `adb shell ip addr show`
2. Verify VPN connection is active
3. Try using public IP service: `adb shell curl -s https://api.ipify.org`

## Still Having Issues?

- Check [FAQ](faq.md)
- Open an issue on GitHub
- Contact support: contact@voxhash.dev
