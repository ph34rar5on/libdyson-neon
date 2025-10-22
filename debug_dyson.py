#!/usr/bin/env python3
"""Debug script for Dyson device connection."""

import logging
import time
from libdyson import get_device

# Enable DEBUG level logging to see all MQTT activity
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Device credentials
SERIAL = "8HR-US-UCA1194A"
CREDENTIAL = "mUi62la+PLB2YCZo44c7DLCTsonMlV8tOsJqRxPxh19W6G1dVzE9BCSQE+Jmp0ISwxH1Mu1k44TdvAuXAjSuaQ=="
DEVICE_TYPE = "527"  # Pure Hot+Cool
HOST = "192.168.1.102"

def main():
    print(f"\nDevice Type: {DEVICE_TYPE} (Pure Hot+Cool)")
    print(f"Serial: {SERIAL}")
    print(f"Host: {HOST}\n")
    
    device = get_device(SERIAL, CREDENTIAL, DEVICE_TYPE)
    
    if device is None:
        print(f"ERROR: Unknown device type: {DEVICE_TYPE}")
        return
    
    print(f"Expected status topic: {device._status_topic}")
    print(f"Expected command topic: {device._command_topic}\n")
    
    try:
        device.connect(HOST)
        print("\n✓ Connected successfully!")
        
        # Display status
        print(f"\nIs On: {device.is_on}")
        print(f"Speed: {device.speed}")
        print(f"Auto Mode: {device.auto_mode}")
        
        time.sleep(2)
        device.disconnect()
        print("\n✓ Disconnected")
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
