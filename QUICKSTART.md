# Quick Start Guide

## Setup

```bash
sudo apt-get install chromium-driver
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 📊 What You Can Do

### 1. Get Connection Status
```python
from m7200_controller import M7200Controller

with M7200Controller() as controller:
    controller.login()
    status = controller.get_connection_status()
    print(f"Connection: {status['connection_status']}")
    print(f"Network: {status['network_type']}")
    print(f"IP: {status['ipv4_address']}")
```

### 2. Get LTE Signal Details
```python
lte = controller.get_lte_details()
print(f"Band: {lte['band']}")
print(f"RSRP: {lte['rsrp']} dBm")
print(f"RSRQ: {lte['rsrq']} dB")
print(f"SNR: {lte['snr']} dB")
```

### 3. Get Everything at Once
```python
all_info = controller.get_all_info()
```

## Usage

```bash
source venv/bin/activate
python test_all.py        # Test all features
python example.py         # Usage examples
./reboot_m7200.sh         # Reboot router
./monitor_signal.sh       # Log signal stats + graph
```

## 📡 Data Retrieved

The controller successfully retrieves:

**Connection Info:**
- Connection Status (Connected/Disconnected)
- Network Type (LTE/3G/etc)
- IPv4 and IPv6 addresses
- WiFi SSID and security status
- Current connected clients

**LTE Signal Metrics:**
- Band number
- RSRP (Reference Signal Received Power)
- RSRQ (Reference Signal Received Quality)
- SNR (Signal-to-Noise Ratio)

**Data Usage:**
- Total data used
- Daily data used
- Upstream/downstream rates

## 🔄 Rebooting the Router

To add reboot functionality, run the inspector script:
```bash
python find_reboot.py
```

This will help you locate the reboot button in the web interface. Once found, update the `reboot_router()` method in `m7200_controller.py` with the correct selectors.

## 🛠️ Troubleshooting

**If login fails:**
- Verify the password in `config.json`
- Check that the router IP is correct (for example: 192.168.0.1)
- Make sure you can access the router's web interface in a regular browser

**If data extraction fails:**
- The router firmware may have changed
- Run `inspect_status.py` to see the current page structure
- Update element selectors in the controller if needed

## 📝 Configuration

Edit `config.json`:
```json
{
  "router_ip": "192.168.0.1",
  "username": "admin",
  "password": "your_password",
  "headless": true,
  "timeout": 10
}
```

- Set `"headless": false` to see the browser while debugging
- Increase `timeout` if you have a slow connection

## 🔒 Security Notes

- The `config.json` file contains your router password
- It's included in `.gitignore` to prevent accidental commits
- For production use, consider using environment variables

## 📦 Dependencies

All dependencies are in the virtual environment:
- Selenium 4.16+ (with built-in ChromeDriver management)
- Python 3.7+

## 🎯 Example Output

```json
{
  "connection_status": "Connected",
  "network_type": "LTE",
  "band": "3",
  "rsrp": "-97dBm",
  "rsrq": "-15dB",
  "snr": "8.6dB",
  "ipv4_address": "203.0.113.10",
  "ipv6_address": "2001:db8::10",
  "ssid": "MyRouter",
  "current_clients": "1",
  "total_used": "6.01 GB",
  "upstream_rate": "1.2 KB/s",
  "downstream_rate": "1.26 KB/s"
}
```

## 🤖 Automation Ideas

You can use this controller to:
- Monitor signal strength over time
- Auto-reboot when connection degrades
- Log data usage for billing purposes
- Send alerts when clients connect
- Create a dashboard with real-time metrics

## 📚 API Reference

### M7200Controller

**Methods:**
- `login()` → bool - Authenticate with the router
- `get_connection_status()` → dict - Get connection and network info
- `get_lte_details()` → dict - Get LTE signal metrics
- `get_all_info()` → dict - Get everything combined
- `reboot_router()` → bool - Reboot the device (needs implementation)
- `close()` - Clean up browser resources

**Context Manager:**
```python
with M7200Controller() as controller:
    # Automatically closes browser when done
    controller.login()
    ...
```

## 💡 Next Steps

1. ✅ Basic login and data retrieval - **DONE**
2. 🔄 Implement reboot functionality (use `find_reboot.py`)
3. 📊 Build a monitoring dashboard
4. 🔔 Add alerting for signal degradation
5. 📈 Log historical data for analysis

Enjoy your automated M7200 controller! 🎉
