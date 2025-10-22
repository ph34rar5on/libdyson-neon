#!/usr/bin/env node
/**
 * Test script to verify the Dyson Homebridge plugin works
 * Run with: node test_plugin.js
 */

const { PythonShell } = require('python-shell');
const path = require('path');

// REPLACE THESE WITH YOUR DEVICE DETAILS
const SERIAL = "8HR-US-UCA1194A";
const CREDENTIAL = "mUi62la+PLB2YCZo44c7DLCTsonMlV8tOsJqRxPxh19W6G1dVzE9BCSQE+Jmp0ISwxH1Mu1k44TdvAuXAjSuaQ==";
const DEVICE_TYPE = "527M";
const HOST = "192.168.1.102";

async function testPythonBridge() {
  console.log("Testing Python bridge...");
  
  const pythonScript = path.join(__dirname, 'dyson_bridge.py');
  console.log("Python script path:", pythonScript);
  
  const options = {
    mode: 'json',
    pythonPath: 'python3',
    args: [SERIAL, CREDENTIAL, DEVICE_TYPE, HOST, 'status']
  };
  
  try {
    console.log("\nRunning command: status");
    const results = await PythonShell.run(pythonScript, options);
    console.log("Success! Device status:");
    console.log(JSON.stringify(results[0], null, 2));
    
    console.log("\n✅ Python bridge is working correctly!");
    console.log("\nNext steps:");
    console.log("1. Make sure your Homebridge config.json includes:");
    console.log(JSON.stringify({
      "accessory": "DysonNeon",
      "name": "Dyson Pure Hot+Cool",
      "serial": SERIAL,
      "credential": CREDENTIAL,
      "deviceType": DEVICE_TYPE,
      "host": HOST
    }, null, 2));
    console.log("\n2. Restart Homebridge");
    console.log("3. Check Homebridge logs for any errors");
    
  } catch (error) {
    console.error("❌ Error:", error);
    console.log("\nTroubleshooting:");
    console.log("- Check if python3 is in PATH");
    console.log("- Verify libdyson is installed: pip3 show libdyson-neon");
    console.log("- Try running the bridge directly:");
    console.log(`  python3 ${pythonScript} "${SERIAL}" "${CREDENTIAL}" "${DEVICE_TYPE}" "${HOST}" status`);
  }
}

testPythonBridge();
