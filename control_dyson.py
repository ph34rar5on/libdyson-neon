#!/usr/bin/env python3
"""Control script for Dyson device."""

import logging
import time
from libdyson import get_device

# Configure logging to see what's happening
logging.basicConfig(level=logging.INFO)

# Device credentials - REPLACE THESE WITH YOUR VALUES
SERIAL = "8HR-US-UCA1194A"  # e.g., "JH1-US-HBB1111A"
CREDENTIAL = "mUi62la+PLB2YCZo44c7DLCTsonMlV8tOsJqRxPxh19W6G1dVzE9BCSQE+Jmp0ISwxH1Mu1k44TdvAuXAjSuaQ=="  # Long base64 string
DEVICE_TYPE = "527M"  # Pure Hot+Cool Middle East variant
HOST = "192.168.1.102"  # Your device's IP address

def main():
    print("Creating device...")
    device = get_device(SERIAL, CREDENTIAL, DEVICE_TYPE)
    
    if device is None:
        print(f"Unknown device type: {DEVICE_TYPE}")
        print("Check libdyson/const.py for valid DEVICE_TYPE_* constants")
        return
    
    print(f"Connecting to {HOST}...")
    try:
        device.connect(HOST)
        print("Connected successfully!")
        
        # Display current status
        print("\n=== Current Status ===")
        print(f"Device Type: {device.device_type}")
        print(f"Is On: {device.is_on if hasattr(device, 'is_on') else 'N/A'}")
        
        # For fan devices
        if hasattr(device, 'speed'):
            print(f"Speed: {device.speed}")
            print(f"Auto Mode: {device.auto_mode}")
            print(f"Oscillation: {device.oscillation}")
            print(f"Night Mode: {device.night_mode}")
        
        # Display environmental data if available
        if hasattr(device, 'temperature'):
            print(f"\n=== Environmental Data ===")
            temp_k = device.temperature
            temp_c = temp_k - 273.15 if temp_k else None
            print(f"Temperature: {temp_c:.1f}°C" if temp_c else "Temperature: N/A")
            print(f"Humidity: {device.humidity}%" if device.humidity else "Humidity: N/A")
            
            if hasattr(device, 'particulate_matter_2_5'):
                print(f"PM2.5: {device.particulate_matter_2_5} µg/m³")
            if hasattr(device, 'particulate_matter_10'):
                print(f"PM10: {device.particulate_matter_10} µg/m³")
        
        # Example commands (uncomment to use)
        print("\n=== Example Commands (currently commented out) ===")
        
        #Turn on the device
        #device.turn_on()
        #print("Turned on")
        
        #Set speed to 5
        #device.set_speed(5)
        #print("Set speed to 5")
        
        #Enable auto mode
        #device.enable_auto_mode()
        #print("Enabled auto mode")
        
        #Disable auto mode
        device.disable_auto_mode()
        print("Disabled auto mode")
        
        #Enable oscillation
        #device.enable_oscillation()
        #print("Enabled oscillation")
        
        #Disable oscillation
        #device.disable_oscillation()
        #print("Disabled oscillation")
        
        #Turn off the device
        #device.turn_off()
        #print("Turned off")
         
        #Enable night mode
        #device.enable_night_mode()
        #print("Enabled night mode")
        
        #Disable night mode
        #device.disable_night_mode()
        #print("Disabled night mode")
        
        #Heat target
        #device.set_heat_target(300)
        #print("Set heat to 80 degrees")
        
        print("\nKeeping connection open for 5 seconds...")
        time.sleep(5)
        
        device.disconnect()
        print("Disconnected")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
