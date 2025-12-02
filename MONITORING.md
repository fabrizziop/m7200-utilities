# Signal Monitoring

## Overview

Monitor LTE signal statistics over time with automatic CSV logging and graph generation.

## Quick Start

```bash
# Single sample
./monitor_signal.sh

# Or directly with Python
python monitor_signal.py

# Continuous monitoring (every 5 minutes)
python monitor_signal.py --interval 300
```

## Features

- Logs Band, RSRP, RSRQ, SNR to CSV
- Generates PNG graphs with signal thresholds
- Configurable monitoring interval
- Cron-ready bash script
- Old graphs automatically replaced

## Cron Setup

**Every 5 minutes:**
```cron
*/5 * * * * /path/to/m7200/monitor_signal.sh >> /path/to/m7200/monitor.log 2>&1
```

**Every 15 minutes:**
```cron
*/15 * * * * /path/to/m7200/monitor_signal.sh
```

**Hourly:**
```cron
0 * * * * /path/to/m7200/monitor_signal.sh
```

## Output Files

- `signal_log.csv` - Raw data with timestamps
- `signal_graph.png` - Visual representation (auto-updated)
- `monitor.log` - Script execution log

## CSV Format

```csv
timestamp,datetime,band,rsrp,rsrq,snr,connection_status,network_type
1733169980.0,2025-12-02 20:26:20,3,-93,-15,15.4,Connected,LTE
```

## Graph Features

Three subplots showing:
- **RSRP** (Reference Signal Received Power)
- **RSRQ** (Reference Signal Received Quality)  
- **SNR** (Signal-to-Noise Ratio)

Each with quality thresholds (Good/Fair/Poor).

## Command Options

```bash
# Custom interval (seconds)
python monitor_signal.py --interval 600

# Custom output files
python monitor_signal.py --csv my_data.csv --png my_graph.png

# Skip graph generation
python monitor_signal.py --no-graph

# View help
python monitor_signal.py --help
```

## Continuous Monitoring

Run in foreground:
```bash
python monitor_signal.py --interval 300
```

Stop with `Ctrl+C`.

## Data Analysis

View recent samples:
```bash
tail -20 signal_log.csv
```

Count samples:
```bash
wc -l signal_log.csv
```

Filter by poor signal:
```bash
awk -F',' '$4 < -100 {print $2, $4}' signal_log.csv
```

## Troubleshooting

**No graph generated:**
```bash
pip install matplotlib
```

**Permission denied:**
```bash
chmod +x monitor_signal.sh monitor_signal.py
```

**View logs:**
```bash
tail -f monitor.log
```
