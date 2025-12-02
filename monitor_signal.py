#!/usr/bin/env python3
"""
M7200 Signal Monitor

Periodically logs LTE signal statistics to CSV and generates visualizations.
Can be run continuously or as a single sample via cron.

Usage:
    # Single sample (for cron)
    python monitor_signal.py

    # Continuous monitoring with custom interval
    python monitor_signal.py --interval 300

    # Daemon mode (runs in background)
    python monitor_signal.py --daemon --interval 600
"""

import sys
import os
import time
import csv
import argparse
from datetime import datetime
from pathlib import Path

# Add script directory to path
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

from m7200_controller import M7200Controller

try:
    import matplotlib
    matplotlib.use('Agg')  # Non-interactive backend
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False
    print("WARNING: matplotlib not installed. PNG generation disabled.")
    print("Install with: pip install matplotlib")


class SignalMonitor:
    """Monitor and log M7200 LTE signal statistics."""
    
    def __init__(self, csv_file="signal_log.csv", png_file="signal_graph.png"):
        self.csv_file = Path(script_dir) / csv_file
        self.png_file = Path(script_dir) / png_file
        self.fieldnames = ['timestamp', 'datetime', 'band', 'rsrp', 'rsrq', 'snr', 
                          'connection_status', 'network_type']
    
    def ensure_csv_exists(self):
        """Create CSV file with headers if it doesn't exist."""
        if not self.csv_file.exists():
            with open(self.csv_file, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=self.fieldnames)
                writer.writeheader()
            print(f"Created new CSV file: {self.csv_file}")
    
    def log_sample(self):
        """Collect and log a single signal sample."""
        timestamp = time.time()
        dt = datetime.fromtimestamp(timestamp)
        
        print(f"\n[{dt.strftime('%Y-%m-%d %H:%M:%S')}] Collecting signal data...")
        
        try:
            with M7200Controller() as controller:
                # Login
                if not controller.login():
                    print("ERROR: Login failed")
                    return False
                
                # Get LTE details
                lte = controller.get_lte_details()
                status = controller.get_connection_status()
                
                if 'error' in lte or 'error' in status:
                    print("ERROR: Failed to retrieve data")
                    return False
                
                # Prepare data row
                data = {
                    'timestamp': timestamp,
                    'datetime': dt.strftime('%Y-%m-%d %H:%M:%S'),
                    'band': lte.get('band', 'N/A'),
                    'rsrp': lte.get('rsrp', 'N/A'),
                    'rsrq': lte.get('rsrq', 'N/A'),
                    'snr': lte.get('snr', 'N/A'),
                    'connection_status': status.get('connection_status', 'N/A'),
                    'network_type': status.get('network_type', 'N/A')
                }
                
                # Write to CSV
                self.ensure_csv_exists()
                with open(self.csv_file, 'a', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=self.fieldnames)
                    writer.writerow(data)
                
                print(f"✓ Logged: Band={data['band']}, RSRP={data['rsrp']}, "
                      f"RSRQ={data['rsrq']}, SNR={data['snr']}")
                
                return True
                
        except Exception as e:
            print(f"ERROR: {e}")
            return False
    
    def generate_graph(self):
        """Generate PNG graph from CSV data."""
        if not HAS_MATPLOTLIB:
            print("Skipping graph generation (matplotlib not available)")
            return False
        
        if not self.csv_file.exists():
            print("No data to graph yet")
            return False
        
        # LTE Band to Frequency mapping (approximate center frequencies in MHz)
        band_frequencies = {
            '1': 2140, '2': 1930, '3': 1805, '4': 2132, '5': 869,
            '7': 2620, '8': 925, '12': 737, '13': 746, '17': 734,
            '20': 791, '28': 758, '38': 2595, '40': 2350, '41': 2496
        }
        
        print(f"\nGenerating graph: {self.png_file}")
        
        try:
            # Read CSV data
            timestamps = []
            rsrp_values = []
            rsrq_values = []
            snr_values = []
            band_values = []
            
            with open(self.csv_file, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        ts = float(row['timestamp'])
                        timestamps.append(datetime.fromtimestamp(ts))
                        
                        # Convert signal values to floats
                        rsrp = float(row['rsrp']) if row['rsrp'] != 'N/A' else None
                        rsrq = float(row['rsrq']) if row['rsrq'] != 'N/A' else None
                        snr = float(row['snr']) if row['snr'] != 'N/A' else None
                        
                        # Get band and map to frequency
                        band = str(row['band']) if row['band'] != 'N/A' else None
                        freq = band_frequencies.get(band, None) if band else None
                        
                        rsrp_values.append(rsrp)
                        rsrq_values.append(rsrq)
                        snr_values.append(snr)
                        band_values.append(freq)
                    except (ValueError, KeyError):
                        continue
            
            if not timestamps:
                print("No valid data points to graph")
                return False
            
            # Create figure with subplots
            fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(12, 13))
            fig.suptitle('M7200 LTE Signal Statistics', fontsize=16, fontweight='bold')
            
            # Plot RSRP
            ax1.plot(timestamps, rsrp_values, 'b-', linewidth=2, label='RSRP')
            ax1.set_ylabel('RSRP (dBm)', fontsize=12)
            ax1.set_title('Reference Signal Received Power')
            ax1.grid(True, alpha=0.3)
            ax1.axhline(y=-80, color='g', linestyle='--', alpha=0.5, label='Good (-80)')
            ax1.axhline(y=-100, color='orange', linestyle='--', alpha=0.5, label='Fair (-100)')
            ax1.axhline(y=-110, color='r', linestyle='--', alpha=0.5, label='Poor (-110)')
            ax1.legend(loc='best')
            
            # Plot RSRQ
            ax2.plot(timestamps, rsrq_values, 'g-', linewidth=2, label='RSRQ')
            ax2.set_ylabel('RSRQ (dB)', fontsize=12)
            ax2.set_title('Reference Signal Received Quality')
            ax2.grid(True, alpha=0.3)
            ax2.axhline(y=-10, color='g', linestyle='--', alpha=0.5, label='Good (-10)')
            ax2.axhline(y=-15, color='orange', linestyle='--', alpha=0.5, label='Fair (-15)')
            ax2.axhline(y=-20, color='r', linestyle='--', alpha=0.5, label='Poor (-20)')
            ax2.legend(loc='best')
            
            # Plot SNR
            ax3.plot(timestamps, snr_values, 'r-', linewidth=2, label='SNR')
            ax3.set_ylabel('SNR (dB)', fontsize=12)
            ax3.set_title('Signal-to-Noise Ratio')
            ax3.grid(True, alpha=0.3)
            ax3.axhline(y=20, color='g', linestyle='--', alpha=0.5, label='Good (20)')
            ax3.axhline(y=13, color='orange', linestyle='--', alpha=0.5, label='Fair (13)')
            ax3.axhline(y=0, color='r', linestyle='--', alpha=0.5, label='Poor (0)')
            ax3.legend(loc='best')
            
            # Plot LTE Band (Frequency)
            ax4.plot(timestamps, band_values, 'purple', linewidth=2, marker='o', markersize=6, label='Frequency')
            ax4.set_ylabel('Frequency (MHz)', fontsize=12)
            ax4.set_xlabel('Time', fontsize=12)
            ax4.set_title('LTE Band Frequency')
            ax4.grid(True, alpha=0.3)
            ax4.legend(loc='best')
            
            # Add band labels as secondary y-axis
            if any(band_values):
                # Get unique frequencies and their corresponding bands
                unique_freqs = sorted(set(f for f in band_values if f is not None))
                if unique_freqs:
                    freq_to_band = {v: k for k, v in band_frequencies.items()}
                    band_labels = [f"Band {freq_to_band.get(f, '?')}" for f in unique_freqs]
                    ax4_right = ax4.twinx()
                    ax4_right.set_ylabel('LTE Band', fontsize=12)
                    ax4_right.set_ylim(ax4.get_ylim())
                    ax4_right.set_yticks(unique_freqs)
                    ax4_right.set_yticklabels(band_labels)
            
            # Format x-axis for all subplots
            for ax in [ax1, ax2, ax3, ax4]:
                ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
                ax.xaxis.set_major_locator(mdates.AutoDateLocator())
                plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
            
            # Adjust layout and save
            plt.tight_layout()
            
            # Delete old graph if exists
            if self.png_file.exists():
                self.png_file.unlink()
            
            plt.savefig(self.png_file, dpi=100, bbox_inches='tight')
            plt.close()
            
            print(f"✓ Graph saved: {self.png_file}")
            print(f"  Data points: {len(timestamps)}")
            
            return True
            
        except Exception as e:
            print(f"ERROR generating graph: {e}")
            import traceback
            traceback.print_exc()
            return False


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description='Monitor M7200 LTE signal statistics',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Single sample (for cron)
  python monitor_signal.py
  
  # Continuous monitoring every 5 minutes
  python monitor_signal.py --interval 300
  
  # Run in background every 10 minutes
  python monitor_signal.py --daemon --interval 600
        """
    )
    
    parser.add_argument('--interval', type=int, default=0,
                       help='Monitoring interval in seconds (0 = single sample)')
    parser.add_argument('--daemon', action='store_true',
                       help='Run as daemon (background process)')
    parser.add_argument('--csv', default='signal_log.csv',
                       help='CSV output file (default: signal_log.csv)')
    parser.add_argument('--png', default='signal_graph.png',
                       help='PNG output file (default: signal_graph.png)')
    parser.add_argument('--no-graph', action='store_true',
                       help='Skip graph generation')
    
    args = parser.parse_args()
    
    # Create monitor instance
    monitor = SignalMonitor(csv_file=args.csv, png_file=args.png)
    
    print("=" * 60)
    print("M7200 Signal Monitor")
    print("=" * 60)
    print(f"CSV file: {monitor.csv_file}")
    print(f"PNG file: {monitor.png_file}")
    
    if args.interval > 0:
        print(f"Interval: {args.interval} seconds ({args.interval/60:.1f} minutes)")
        print(f"Mode: {'Daemon' if args.daemon else 'Foreground'}")
    else:
        print("Mode: Single sample")
    print("=" * 60)
    
    # Daemon mode
    if args.daemon and args.interval > 0:
        try:
            import daemon
            with daemon.DaemonContext():
                continuous_monitoring(monitor, args.interval, args.no_graph)
        except ImportError:
            print("ERROR: python-daemon not installed")
            print("Install with: pip install python-daemon")
            print("Running in foreground instead...")
            continuous_monitoring(monitor, args.interval, args.no_graph)
    
    # Continuous monitoring
    elif args.interval > 0:
        continuous_monitoring(monitor, args.interval, args.no_graph)
    
    # Single sample
    else:
        success = monitor.log_sample()
        if success and not args.no_graph:
            monitor.generate_graph()
        
        sys.exit(0 if success else 1)


def continuous_monitoring(monitor, interval, no_graph):
    """Run continuous monitoring loop."""
    print("\nStarting continuous monitoring...")
    print("Press Ctrl+C to stop\n")
    
    try:
        while True:
            success = monitor.log_sample()
            
            if success and not no_graph:
                monitor.generate_graph()
            
            print(f"\nNext sample in {interval} seconds...")
            time.sleep(interval)
            
    except KeyboardInterrupt:
        print("\n\nMonitoring stopped by user")
        sys.exit(0)


if __name__ == "__main__":
    main()
