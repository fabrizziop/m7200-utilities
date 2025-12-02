# TP-Link M7200 Router Controller

Python-based automation for TP-Link M7200 LTE routers via web interface using Selenium.

> **Note:** This was vibe coded just for fun! 🎉

## Features

- 🔐 Automated login
- 📊 Connection status monitoring
- 📡 LTE signal metrics (Band, RSRP, RSRQ, SNR)
- 🔄 Remote reboot capability
- 📈 Signal monitoring with CSV logging and graphs
- 🤖 Headless browser operation
- ⏰ Cron-ready automation scripts

## Prerequisites

- Python 3.7+
- Chromium and chromium-driver
- Network access to M7200 router

## Installation

```bash
# System dependencies
sudo apt-get update && sudo apt-get install chromium-driver

# Python environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Configuration

Edit `config.json` with your router's details:

```json
{
  "router_ip": "192.168.0.1",
  "username": "admin",
  "password": "your_password_here",
  "headless": true,
  "timeout": 10
}
```

**Configuration Options:**
- `router_ip`: IP address of your M7200 router (default: 192.168.0.1)
- `username`: Admin username (default: admin)
- `password`: Admin password
- `headless`: Run browser in headless mode (true/false)
- `timeout`: Page load timeout in seconds

## Usage

### Quick Start

Run the example script:
```bash
python example.py
```

### Using in Your Own Code

```python
from m7200_controller import M7200Controller

# Use context manager for automatic cleanup
with M7200Controller() as controller:
    # Login
    if controller.login():
        # Get connection status
        status = controller.get_connection_status()
        print(f"Status: {status}")
        
        # Get LTE details
        lte = controller.get_lte_details()
        print(f"LTE Info: {lte}")
        
        # Reboot (use with caution!)
        # controller.reboot_router()
```

### Available Methods

#### `login() -> bool`
Logs into the router's web interface.

```python
controller = M7200Controller()
success = controller.login()
```

#### `get_connection_status() -> dict`
Retrieves current connection status.

```python
status = controller.get_connection_status()
# Returns: {'connectionStatus': '...', 'networkType': '...', ...}
```

#### `get_lte_details() -> dict`
Gets detailed LTE signal information.

```python
lte = controller.get_lte_details()
# Returns: {'band': '...', 'rssi': -70, 'rsrp': -95, 'rsrq': -10, ...}
```

#### `reboot_router() -> bool`
Sends a reboot command to the router.

```python
success = controller.reboot_router()
```

#### `get_all_info() -> dict`
Gets all available information in one call.

```python
info = controller.get_all_info()
# Returns both connection status and LTE details
```

## Signal Monitoring

Monitor LTE signal quality over time with automatic logging and visualization.

### Quick Start

```bash
# Single sample (for cron)
./monitor_signal.sh

# Continuous monitoring (every 5 minutes)
python monitor_signal.py --interval 300
```

### Setup Cron Job

Monitor signal every 15 minutes:
```cron
*/15 * * * * /path/to/m7200/monitor_signal.sh
```

### Output

- **CSV file** - `signal_log.csv` with timestamps and metrics
- **PNG graph** - `signal_graph.png` with RSRP, RSRQ, SNR plots
- **Log file** - `monitor.log` with execution history

See [MONITORING.md](MONITORING.md) for detailed usage.

## Important Notes

### 🔧 Customization Required

The M7200 web interface may vary by firmware version. You'll likely need to:

1. **Inspect the actual web interface** of your router
2. **Update element selectors** in `m7200_controller.py` to match your router's HTML structure
3. **Test the login process** first before using other features

### How to Customize for Your Router

1. **Run in non-headless mode** to see what's happening:
   ```json
   "headless": false
   ```

2. **Use browser DevTools** to inspect the login page:
   - Right-click on username field → Inspect
   - Note the element ID or other selectors
   - Update the `login()` method accordingly

3. **Check JavaScript variables** in the browser console:
   - Open DevTools → Console tab
   - Type variable names like `connectionStatus`, `rssiValue`, etc.
   - Update the JavaScript extraction code in the methods

4. **Find the reboot functionality**:
   - Navigate manually to the reboot page
   - Note the URL and button selectors
   - Update the `reboot_router()` method

## Troubleshooting

### Login Fails
- Verify `router_ip` is correct
- Check username and password
- Run in non-headless mode to see what's happening
- Inspect the actual login form element IDs

### Cannot Get Status/LTE Data
- The JavaScript variable names may differ in your firmware
- Check browser console for actual variable names
- Update the `execute_script()` calls accordingly

### Reboot Doesn't Work
- Navigate manually to find the reboot page
- Update XPath selectors for your specific interface
- Some routers require additional confirmation steps

## Remote Access Setup

To control your router from a remote location:

1. **Set up port forwarding** on your network to access the router's web interface
2. **Use a VPN** to your remote network (recommended for security)
3. **Update the IP address** in config.json to your remote IP or domain
4. **Consider security implications** of exposing your router's web interface

## Security Considerations

⚠️ **Important Security Notes:**
- Store credentials securely (consider using environment variables)
- Use HTTPS if your router supports it
- Don't expose the web interface directly to the internet
- Use VPN for remote access when possible
- Keep your router firmware updated

## Example Output

```
============================================================
TP-Link M7200 Router Controller - Example Usage
============================================================

[1] Logging in to router...
Navigating to http://192.168.0.1...
Entering credentials...
Login successful!
✓ Login successful!

[2] Getting connection status...
Connection Status:
```json
{
  "connection_status": "Connected",
  "network_type": "LTE",
  "band": "3",
  "rsrp": "-97dBm",
  "rsrq": "-15dB",
  "snr": "8.6dB",
  "ipv4_address": "10.x.x.x",
  "ssid": "MyRouter",
  "current_clients": "1",
  "total_used": "6.01 GB"
}

[3] Getting LTE signal details...
LTE Details:
{
  "band": "Band 3 (1800 MHz)",
  "rssi": -68,
  "rsrp": -94,
  "rsrq": -11,
  "sinr": 13,
  "cellId": "12345678",
  "timestamp": 1701432102.456
}
```

## License

This project is provided as-is for educational and personal use.

## Contributing

Feel free to submit issues or pull requests if you've tested this with your M7200 and have improvements!

## Disclaimer

This tool interacts with your router's web interface. Use at your own risk. Always ensure you have physical access to your router in case something goes wrong.
