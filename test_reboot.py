#!/usr/bin/env python3
"""
Test the reboot functionality (with safety confirmation)
"""

from m7200_controller import M7200Controller
import time


def test_reboot():
    print("=" * 70)
    print("M7200 Router Reboot Test")
    print("=" * 70)
    print()
    print("⚠️  WARNING: This will reboot your router!")
    print("⚠️  The router will be offline for approximately 30-60 seconds.")
    print("⚠️  Any active connections will be dropped.")
    print()
    
    response = input("Are you SURE you want to reboot the router? (type 'YES' to confirm): ")
    
    if response != "YES":
        print("\n❌ Reboot cancelled.")
        return
    
    print("\n" + "=" * 70)
    print("Proceeding with reboot...")
    print("=" * 70)
    
    with M7200Controller() as controller:
        # Login
        print("\n[1] Logging in...")
        if not controller.login():
            print("❌ Login failed")
            return
        print("✅ Login successful")
        
        # Reboot
        print("\n[2] Sending reboot command...")
        if controller.reboot_router():
            print("\n" + "=" * 70)
            print("✅ SUCCESS! Reboot command sent to router")
            print("=" * 70)
            print()
            print("The router is now rebooting...")
            print("Expected downtime: 30-60 seconds")
            print()
            print("You can monitor the connection by pinging the router:")
            print(f"  ping {controller.router_ip}")
        else:
            print("\n" + "=" * 70)
            print("❌ FAILED! Could not send reboot command")
            print("=" * 70)


if __name__ == "__main__":
    test_reboot()
