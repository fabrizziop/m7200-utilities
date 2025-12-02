# Project Summary

## Structure

```
m7200/
├── m7200_controller.py      # Main controller
├── config.json              # Router config (gitignored)
├── reboot_m7200.sh          # Cron-ready reboot script
├── test_*.py                # Test scripts
├── example.py               # Usage examples
└── docs/                    # Documentation
```

## Features

### ✅ Working
- Login authentication
- Connection status (type, IP, clients, data usage)
- LTE metrics (Band, RSRP, RSRQ, SNR)
- Remote reboot via web interface
- Signal monitoring with CSV logging and PNG graphs
- Cron automation support

## Quick Start

```bash
source venv/bin/activate
python test_all.py          # Test all features
./monitor_signal.sh         # Monitor signal
```

## 💻 Code Example

```python
from m7200_controller import M7200Controller

# Use context manager for automatic cleanup
with M7200Controller() as controller:
    # Login
    controller.login()
    
    # Get all router info
    info = controller.get_all_info()
    
    # Access the data
    print(f"Band: {info['lte_details']['band']}")
    print(f"RSRP: {info['lte_details']['rsrp']} dBm")
    print(f"IP: {info['connection_status']['ipv4_address']}")
```

## Tests

- ✅ Login
- ✅ Connection Status
- ✅ LTE Details
- ✅ Reboot Navigation

## Technology

- Python 3.7+
- Selenium 4.16+
- Chromium with chromium-driver
## Configuration

`config.json`:
```json
{
  "router_ip": "192.168.0.1",
  "username": "admin",
  "password": "your_password",
  "headless": true,
  "timeout": 10
}
```