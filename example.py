#!/usr/bin/env python3
"""
Example usage script for M7200 Router Controller

This script demonstrates how to use the M7200Controller to:
- Login to the router
- Get connection status
- Get LTE signal details
- Reboot the router
"""

import json
from m7200_controller import M7200Controller


def main():
    """Main function demonstrating controller usage."""
    
    print("=" * 60)
    print("TP-Link M7200 Router Controller - Example Usage")
    print("=" * 60)
    print()
    
    # Use context manager to ensure proper cleanup
    with M7200Controller() as controller:
        
        # 1. Login to the router
        print("\n[1] Logging in to router...")
        if not controller.login():
            print("❌ Login failed! Check your credentials and router IP.")
            return
        
        print("✓ Login successful!")
        
        # 2. Get connection status
        print("\n[2] Getting connection status...")
        status = controller.get_connection_status()
        print("\nConnection Status:")
        print(json.dumps(status, indent=2))
        
        # 3. Get LTE details
        print("\n[3] Getting LTE signal details...")
        lte_details = controller.get_lte_details()
        print("\nLTE Details:")
        print(json.dumps(lte_details, indent=2))
        
        # 4. Get all info at once
        print("\n[4] Getting all information...")
        all_info = controller.get_all_info()
        print("\nAll Router Info:")
        print(json.dumps(all_info, indent=2))
        
        # 5. Reboot option (commented out for safety)
        print("\n[5] Reboot option (disabled by default for safety)...")
        print("To test reboot, run: python test_reboot.py")
        print()
        print("Or uncomment the lines below to enable reboot in this script:")
        
        # Uncomment to actually reboot:
        # print("\n⚠️  WARNING: This will reboot the router!")
        # response = input('Do you want to reboot the router? (type YES to confirm): ')
        # if response == 'YES':
        #     if controller.reboot_router():
        #         print('✅ Reboot command sent!')
        #     else:
        #         print('❌ Reboot failed!')
    
    print("\n" + "=" * 60)
    print("Example completed. Browser closed.")
    print("=" * 60)


if __name__ == "__main__":
    main()
