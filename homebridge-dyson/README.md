# Homebridge Dyson Neon

Homebridge plugin for Dyson devices using libdyson-neon.

## Installation

1. Install the plugin locally:
```bash
cd homebridge-dyson
npm install
```

2. Link the plugin to Homebridge:
```bash
npm link
```

3. Make sure Python 3 and libdyson-neon are installed:
```bash
cd ..
pip install -e .
```

## Configuration

Add this to your Homebridge `config.json`:

```json
{
  "accessories": [
    {
      "accessory": "DysonNeon",
      "name": "Dyson Pure Hot+Cool",
      "serial": "YOUR_SERIAL",
      "credential": "YOUR_CREDENTIAL",
      "deviceType": "527M",
      "host": "192.168.1.XXX"
    }
  ]
}
```

### Configuration Parameters

- `name`: The name of your device in HomeKit
- `serial`: Your Dyson device serial number
- `credential`: Your Dyson device credential (base64 string)
- `deviceType`: Your device type (e.g., "527M" for Pure Hot+Cool Middle East)
- `host`: IP address of your Dyson device

## Supported Features

- Turn on/off
- Fan speed control (1-10, mapped to 0-100%)
- Oscillation on/off

## Troubleshooting

If the plugin doesn't work:

1. Test the Python bridge directly:
```bash
python dyson_bridge.py "SERIAL" "CREDENTIAL" "DEVICE_TYPE" "HOST" status
```

2. Check Homebridge logs for errors

3. Ensure Python 3 is accessible as `python3` in your PATH
