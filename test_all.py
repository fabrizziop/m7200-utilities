#!/usr/bin/env python3
"""
Comprehensive test of all M7200 controller features
"""

from m7200_controller import M7200Controller
import json

def test_all_features():
    print("=" * 70)
    print("M7200 Router Controller - Full Feature Test")
    print("=" * 70)
    
    with M7200Controller() as controller:
        # Test 1: Login
        print("\n[TEST 1] Login")
        print("-" * 70)
        if not controller.login():
            print("❌ Login failed - cannot continue")
            return
        print("✅ Login successful")
        
        # Test 2: Get Connection Status
        print("\n[TEST 2] Connection Status")
        print("-" * 70)
        status = controller.get_connection_status()
        print(json.dumps(status, indent=2))
        
        # Test 3: Get LTE Details
        print("\n[TEST 3] LTE Signal Details")
        print("-" * 70)
        lte_details = controller.get_lte_details()
        print(json.dumps(lte_details, indent=2))
        
        # Test 4: Get All Info
        print("\n[TEST 4] All Router Info")
        print("-" * 70)
        all_info = controller.get_all_info()
        print(json.dumps(all_info, indent=2))
        
        # Summary
        print("\n" + "=" * 70)
        print("SUMMARY")
        print("=" * 70)
        
        if "error" not in status:
            print(f"✅ Connection Status: Retrieved successfully")
        else:
            print(f"❌ Connection Status: {status.get('error')}")
            
        if "error" not in lte_details:
            print(f"✅ LTE Details: Retrieved successfully")
            if 'band' in lte_details:
                print(f"   - Band: {lte_details['band']}")
            if 'rsrp' in lte_details:
                print(f"   - RSRP: {lte_details['rsrp']}")
            if 'rsrq' in lte_details:
                print(f"   - RSRQ: {lte_details['rsrq']}")
            if 'snr' in lte_details:
                print(f"   - SNR: {lte_details['snr']}")
        else:
            print(f"❌ LTE Details: {lte_details.get('error')}")
        
        print("\n" + "=" * 70)
        print("All tests complete!")
        print("=" * 70)

if __name__ == "__main__":
    test_all_features()
