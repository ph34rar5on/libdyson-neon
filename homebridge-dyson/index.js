const { PythonShell } = require('python-shell');
const path = require('path');

let Service, Characteristic;

module.exports = (homebridge) => {
  Service = homebridge.hap.Service;
  Characteristic = homebridge.hap.Characteristic;
  homebridge.registerAccessory('homebridge-dyson-neon', 'DysonNeon', DysonAccessory);
};

class DysonAccessory {
  constructor(log, config) {
    this.log = log;
    this.name = config.name || 'Dyson Device';
    this.serial = config.serial;
    this.credential = config.credential;
    this.deviceType = config.deviceType;
    this.host = config.host;
    
    this.pythonScript = path.join(__dirname, 'dyson_bridge.py');
    
    // Services
    this.fanService = new Service.Fanv2(this.name);
    this.informationService = new Service.AccessoryInformation()
      .setCharacteristic(Characteristic.Manufacturer, 'Dyson')
      .setCharacteristic(Characteristic.Model, this.deviceType)
      .setCharacteristic(Characteristic.SerialNumber, this.serial);
    
    // Fan characteristics
    this.fanService
      .getCharacteristic(Characteristic.Active)
      .onGet(this.getActive.bind(this))
      .onSet(this.setActive.bind(this));
    
    this.fanService
      .getCharacteristic(Characteristic.RotationSpeed)
      .onGet(this.getRotationSpeed.bind(this))
      .onSet(this.setRotationSpeed.bind(this));
    
    // Optional: Add oscillation if supported
    this.fanService
      .getCharacteristic(Characteristic.SwingMode)
      .onGet(this.getSwingMode.bind(this))
      .onSet(this.setSwingMode.bind(this));
  }
  
  async runPythonCommand(command, value = null) {
    const options = {
      mode: 'json',
      pythonPath: 'python3',
      args: [
        this.serial,
        this.credential,
        this.deviceType,
        this.host,
        command
      ]
    };
    
    if (value !== null) {
      options.args.push(String(value));
    }
    
    try {
      const results = await PythonShell.run(this.pythonScript, options);
      return results[0];
    } catch (error) {
      this.log.error('Python command error:', error);
      throw error;
    }
  }
  
  async getActive() {
    try {
      const result = await this.runPythonCommand('status');
      return result.is_on ? Characteristic.Active.ACTIVE : Characteristic.Active.INACTIVE;
    } catch (error) {
      this.log.error('Error getting active state:', error);
      return Characteristic.Active.INACTIVE;
    }
  }
  
  async setActive(value) {
    try {
      const command = value === Characteristic.Active.ACTIVE ? 'turn_on' : 'turn_off';
      await this.runPythonCommand(command);
      this.log.info(`Turned ${value === Characteristic.Active.ACTIVE ? 'on' : 'off'}`);
    } catch (error) {
      this.log.error('Error setting active state:', error);
      throw error;
    }
  }
  
  async getRotationSpeed() {
    try {
      const result = await this.runPythonCommand('status');
      // Convert speed (1-10) to percentage (0-100)
      return result.speed ? (result.speed / 10) * 100 : 0;
    } catch (error) {
      this.log.error('Error getting rotation speed:', error);
      return 0;
    }
  }
  
  async setRotationSpeed(value) {
    try {
      // Convert percentage (0-100) to speed (1-10)
      const speed = Math.max(1, Math.round((value / 100) * 10));
      await this.runPythonCommand('set_speed', speed);
      this.log.info(`Set speed to ${speed}`);
    } catch (error) {
      this.log.error('Error setting rotation speed:', error);
      throw error;
    }
  }
  
  async getSwingMode() {
    try {
      const result = await this.runPythonCommand('status');
      return result.oscillation ? 
        Characteristic.SwingMode.SWING_ENABLED : 
        Characteristic.SwingMode.SWING_DISABLED;
    } catch (error) {
      this.log.error('Error getting swing mode:', error);
      return Characteristic.SwingMode.SWING_DISABLED;
    }
  }
  
  async setSwingMode(value) {
    try {
      const command = value === Characteristic.SwingMode.SWING_ENABLED ? 
        'enable_oscillation' : 'disable_oscillation';
      await this.runPythonCommand(command);
      this.log.info(`${value === Characteristic.SwingMode.SWING_ENABLED ? 'Enabled' : 'Disabled'} oscillation`);
    } catch (error) {
      this.log.error('Error setting swing mode:', error);
      throw error;
    }
  }
  
  getServices() {
    return [this.informationService, this.fanService];
  }
}
