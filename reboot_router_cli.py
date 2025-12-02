#!/usr/bin/env python3
"""
CLI script to reboot the M7200 router without interactive prompts.
Designed for use with cron jobs and automation.

Exit codes:
  0 - Success
  1 - Login failed
  2 - Reboot command failed
  3 - Other error
"""

import sys
import os
from datetime import datetime

# Add the script directory to Python path
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

from m7200_controller import M7200Controller


def main():
    """Main function to reboot the router."""
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] M7200 Router Reboot")
    print("=" * 60)
    
    try:
        with M7200Controller() as controller:
            # Login
            print("Logging in to router...")
            if not controller.login():
                print("ERROR: Login failed")
                return 1
            
            print("Login successful")
            
            # Reboot
            print("Sending reboot command...")
            if not controller.reboot_router():
                print("ERROR: Reboot command failed")
                return 2
            
            print("SUCCESS: Router is rebooting")
            return 0
            
    except Exception as e:
        print(f"ERROR: Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 3


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
