# Reboot Implementation

## Method

Navigates: Advanced → Device → Shutdown → Reboot → Confirm

Downtime: ~30-60 seconds

## Testing

```bash
python test_reboot_dry_run.py  # Safe navigation test
python test_reboot.py          # Actual reboot (needs YES)
./reboot_m7200.sh              # Cron-ready script
```

## Usage

```python
from m7200_controller import M7200Controller

with M7200Controller() as controller:
    controller.login()
    controller.reboot_router()
```

## Features

- Connection monitoring (status, IPs, clients, data)
- LTE metrics (Band, RSRP, RSRQ, SNR)
- Remote reboot with confirmation
- Cron automation support

## Automation Examples

```python
# Scheduled reboot (use with cron)
controller.login()
controller.reboot_router()

# Signal-based reboot
lte = controller.get_lte_details()
if int(lte['rsrp']) < -110:
    controller.reboot_router()
```
