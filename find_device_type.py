#!/usr/bin/env python3
"""Try different device type variants to find the correct one."""

import logging
from libdyson import get_device
from libdyson.const import DEVICE_TYPE_NAMES

# Suppress most logging
logging.basicConfig(level=logging.ERROR)

SERIAL = "8HR-US-UCA1194A"
CREDENTIAL = "mUi62la+PLB2YCZo44c7DLCTsonMlV8tOsJqRxPxh19W6G1dVzE9BCSQE+Jmp0ISwxH1Mu1k44TdvAuXAjSuaQ=="
HOST = "192.168.1.102"

# Try Hot+Cool variants based on the "527" base type
device_types_to_try = [
    "527",   # Base type
    "527E",  # European variant
    "527K",  # Asian variant  
    "527M",  # Middle East variant
    "455",   # Pure Hot+Cool Link (older model)
]

print(f"Serial: {SERIAL}")
print(f"Host: {HOST}\n")
print("Trying different device types...\n")

for device_type in device_types_to_try:
    device_name = DEVICE_TYPE_NAMES.get(device_type, "Unknown")
    print(f"Testing {device_type}: {device_name}...")
    
    try:
        device = get_device(SERIAL, CREDENTIAL, device_type)
        if device is None:
            print(f"  ✗ Unknown device type\n")
            continue
            
        device.connect(HOST)
        
        # If we get here, connection succeeded!
        print(f"  ✓ SUCCESS! Device type {device_type} works!")
        print(f"  Status topic: {device._status_topic}")
        print(f"  Is On: {device.is_on}")
        
        device.disconnect()
        print(f"\n🎉 Use device type: {device_type}\n")
        break
        
    except Exception as e:
        print(f"  ✗ Failed: {type(e).__name__}\n")
        continue
else:
    print("❌ None of the device types worked.")
    print("\nTroubleshooting:")
    print("1. Verify the device IP address is correct")
    print("2. Ensure the device is powered on and connected to Wi-Fi")
    print("3. Check that credentials are from the correct device")
    print("4. Try resetting the device's Wi-Fi connection")
