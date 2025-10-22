#!/usr/bin/env python3
"""Bridge script for Homebridge to control Dyson devices."""

import sys
import json
import logging
from pathlib import Path

# Add parent directory to path to import libdyson
sys.path.insert(0, str(Path(__file__).parent.parent))

from libdyson import get_device

# Suppress logs unless error
logging.basicConfig(level=logging.ERROR)


def main():
    if len(sys.argv) < 6:
        print(json.dumps({"error": "Usage: dyson_bridge.py <serial> <credential> <device_type> <host> <command> [value]"}))
        sys.exit(1)
    
    serial = sys.argv[1]
    credential = sys.argv[2]
    device_type = sys.argv[3]
    host = sys.argv[4]
    command = sys.argv[5]
    value = sys.argv[6] if len(sys.argv) > 6 else None
    
    try:
        device = get_device(serial, credential, device_type)
        if device is None:
            print(json.dumps({"error": f"Unknown device type: {device_type}"}))
            sys.exit(1)
        
        device.connect(host)
        
        result = {}
        
        if command == "status":
            result = {
                "is_on": device.is_on if hasattr(device, 'is_on') else False,
                "speed": device.speed if hasattr(device, 'speed') else None,
                "auto_mode": device.auto_mode if hasattr(device, 'auto_mode') else False,
                "oscillation": device.oscillation if hasattr(device, 'oscillation') else False,
                "night_mode": device.night_mode if hasattr(device, 'night_mode') else False,
            }
            
            # Add temperature data if available
            if hasattr(device, 'temperature') and device.temperature:
                result["temperature"] = device.temperature - 273.15  # Convert K to C
            if hasattr(device, 'humidity'):
                result["humidity"] = device.humidity
                
        elif command == "turn_on":
            device.turn_on()
            result = {"success": True, "action": "turned_on"}
            
        elif command == "turn_off":
            device.turn_off()
            result = {"success": True, "action": "turned_off"}
            
        elif command == "set_speed":
            if value is None:
                raise ValueError("Speed value required")
            speed = int(value)
            if speed < 1 or speed > 10:
                raise ValueError("Speed must be between 1 and 10")
            device.set_speed(speed)
            result = {"success": True, "action": "set_speed", "speed": speed}
            
        elif command == "enable_oscillation":
            device.enable_oscillation()
            result = {"success": True, "action": "oscillation_enabled"}
            
        elif command == "disable_oscillation":
            device.disable_oscillation()
            result = {"success": True, "action": "oscillation_disabled"}
            
        elif command == "enable_auto_mode":
            device.enable_auto_mode()
            result = {"success": True, "action": "auto_mode_enabled"}
            
        elif command == "disable_auto_mode":
            device.disable_auto_mode()
            result = {"success": True, "action": "auto_mode_disabled"}
            
        elif command == "enable_night_mode":
            device.enable_night_mode()
            result = {"success": True, "action": "night_mode_enabled"}
            
        elif command == "disable_night_mode":
            device.disable_night_mode()
            result = {"success": True, "action": "night_mode_disabled"}
            
        elif command == "set_heat_target":
            if value is None:
                raise ValueError("Temperature value required")
            temp_kelvin = int(value)
            device.set_heat_target(temp_kelvin)
            result = {"success": True, "action": "heat_target_set", "temperature_k": temp_kelvin}
            
        else:
            result = {"error": f"Unknown command: {command}"}
        
        device.disconnect()
        print(json.dumps(result))
        
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)


if __name__ == "__main__":
    main()
