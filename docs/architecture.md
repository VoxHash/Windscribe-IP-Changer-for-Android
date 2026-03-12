# Architecture

How Windscribe IP Changer for Android works.

## Overview

The script uses ADB (Android Debug Bridge) to communicate with Android devices and control Windscribe VPN connections.

## Components

### 1. ADB Connection Management

- Auto-detects ADB executable
- Validates device connection
- Handles connection errors

### 2. Windscribe Detection

- Checks for Windscribe CLI (if available)
- Checks for Windscribe Android app
- Detects package name for app-based operations

### 3. IP Management

- Gets current IP address
- Connects to Windscribe servers
- Disconnects from current server
- Verifies new IP address

### 4. Server Selection

- Random server selection from available list
- Supports custom server configurations
- Fallback to default servers

## Flow Diagram

```
┌─────────────┐
│   Script    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│     ADB     │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Android    │
│   Device     │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Windscribe  │
│   (VPN)      │
└─────────────┘
```

## Process Flow

1. **Initialization**
   - Find ADB executable
   - Check device connection

2. **Detection**
   - Detect Windscribe installation
   - Get current IP and status

3. **Connection**
   - Disconnect from current server (if connected)
   - Connect to random server
   - Wait for connection to stabilize

4. **Verification**
   - Get new IP address
   - Verify connection status

## Error Handling

- ADB connection failures
- Windscribe not found
- Connection timeouts
- Invalid server locations

## See Also

- [Usage Guide](usage.md)
- [API Documentation](api.md)
