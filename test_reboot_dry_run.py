#!/usr/bin/env python3
"""
Verify reboot navigation works (stops before actually rebooting)
"""

from m7200_controller import M7200Controller
from selenium.webdriver.common.by import By
import time


def test_reboot_navigation():
    print("=" * 70)
    print("Testing Reboot Navigation (Dry Run - Won't Actually Reboot)")
    print("=" * 70)
    
    controller = M7200Controller()
    
    try:
        # Login
        print("\n[1] Logging in...")
        if not controller.login():
            print("❌ Login failed")
            return False
        print("✅ Login successful")
        
        # Navigate to reboot page
        print("\n[2] Navigating to reboot page...")
        
        try:
            # Click Advanced
            print("  - Clicking Advanced...")
            advanced = controller.driver.find_element(By.LINK_TEXT, "Advanced")
            advanced.click()
            time.sleep(1)
            print("    ✓ Advanced menu opened")
            
            # Click Device
            print("  - Clicking Device...")
            device = controller.driver.find_element(By.LINK_TEXT, "Device")
            device.click()
            time.sleep(1)
            print("    ✓ Device submenu opened")
            
            # Click Shutdown
            print("  - Clicking Shutdown...")
            shutdown = controller.driver.find_element(By.LINK_TEXT, "Shutdown")
            shutdown.click()
            time.sleep(2)
            print("    ✓ Shutdown page loaded")
            
            # Verify reboot button exists
            print("\n[3] Verifying reboot button...")
            reboot_btn = controller.driver.find_element(By.ID, "rebootBtn")
            print(f"    ✓ Reboot button found: Text='{reboot_btn.text}'")
            
            # Verify confirm button exists
            print("\n[4] Verifying confirmation button...")
            confirm_btn = controller.driver.find_element(By.ID, "shutdownOK")
            print(f"    ✓ Confirm button found: ID='shutdownOK'")
            
            print("\n" + "=" * 70)
            print("✅ SUCCESS! Reboot Navigation Test Passed")
            print("=" * 70)
            print()
            print("All elements found:")
            print("  ✓ Advanced menu")
            print("  ✓ Device submenu")
            print("  ✓ Shutdown page")
            print("  ✓ Reboot button")
            print("  ✓ Confirmation button")
            print()
            print("The reboot_router() method is ready to use!")
            print("Run test_reboot.py to actually reboot the router.")
            return True
            
        except Exception as e:
            print(f"\n❌ Navigation failed: {e}")
            return False
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        controller.close()


if __name__ == "__main__":
    success = test_reboot_navigation()
    exit(0 if success else 1)
