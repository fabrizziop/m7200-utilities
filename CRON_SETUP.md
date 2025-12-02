# Cron Setup for Automatic Reboot

## Quick Test

```bash
cd /path/to/m7200
./reboot_m7200.sh
```

**Expected output:**
```
[2025-12-01 21:28:51] Starting M7200 reboot process...
[2025-12-01 21:28:51] Virtual environment activated
[2025-12-01 21:28:51] M7200 Router Reboot
============================================================
Logging in to router...
Login successful
Sending reboot command...
✅ Reboot command sent successfully!
⚠️  Router is rebooting, it will be offline for ~30-60 seconds
[2025-12-01 21:28:51] SUCCESS: Router reboot command sent successfully
[2025-12-01 21:28:51] Reboot process completed
```

## Cron Setup

```bash
crontab -e
```

Add one of these:

```cron
# Daily at 3 AM
0 3 * * * /path/to/m7200/reboot_m7200.sh >> /path/to/m7200/cron.log 2>&1

# Every Sunday at 2 AM
0 2 * * 0 /path/to/m7200/reboot_m7200.sh >> /path/to/m7200/cron.log 2>&1

# Every 12 hours
0 */12 * * * /path/to/m7200/reboot_m7200.sh >> /path/to/m7200/cron.log 2>&1
```

## Cron Time Format

```
* * * * * command
│ │ │ │ │
│ │ │ │ └─── Day of week (0-7, Sunday = 0 or 7)
│ │ │ └───── Month (1-12)
│ │ └─────── Day of month (1-31)
│ └───────── Hour (0-23)
└─────────── Minute (0-59)
```

## Monitoring

```bash
tail -f reboot.log                    # Script logs
tail -f cron.log                      # Cron output
grep CRON /var/log/syslog | tail -20  # System logs
```

## Exit Codes

The script returns these exit codes:

- **0** - Success, router rebooted
- **1** - Login failed
- **2** - Reboot command failed
- **3** - Other error

## Troubleshooting

```bash
# Check cron service
systemctl status cron

# Make scripts executable
chmod +x reboot_m7200.sh reboot_router_cli.py

# Test manually
./reboot_m7200.sh

# Verify chromedriver
which chromedriver
```

## Log Rotation

Create `/etc/logrotate.d/m7200`:
```
/path/to/m7200/*.log {
    weekly
    rotate 4
    compress
}
```

## Disable Cron

```bash
crontab -e  # Comment out or remove the line
```

## Conditional Reboot

Modify `reboot_router_cli.py` to check signal quality:

```python
lte = controller.get_lte_details()
if int(lte['rsrp']) < -110:
    controller.reboot_router()
```
