#!/usr/bin/env python3
"""
Navigate to Advanced -> Device -> Shutdown to find the Reboot button
"""

from m7200_controller import M7200Controller
from selenium.webdriver.common.by import By
import time


def find_reboot():
    print("=" * 70)
    print("Finding Reboot Button: Advanced -> Device -> Shutdown")
    print("=" * 70)
    
    controller = M7200Controller()
    controller.headless = False  # Show browser
    
    try:
        if not controller.login():
            print("❌ Login failed")
            return
        
        print("\n✅ Logged in!")
        time.sleep(2)
        
        # Step 1: Click Advanced menu
        print("\n[Step 1] Clicking 'Advanced' menu...")
        try:
            # Try multiple ways to find Advanced
            advanced = None
            try:
                advanced = controller.driver.find_element(By.LINK_TEXT, "Advanced")
            except:
                advanced = controller.driver.find_element(By.PARTIAL_LINK_TEXT, "Advanced")
            
            advanced.click()
            time.sleep(2)
            print("✅ Clicked Advanced")
        except Exception as e:
            print(f"❌ Error: {e}")
            return
        
        # Step 2: Look for Device submenu and click it
        print("\n[Step 2] Looking for 'Device' submenu...")
        try:
            # Get all visible links
            links = controller.driver.find_elements(By.TAG_NAME, "a")
            device_link = None
            
            print("  Available menu items:")
            for link in links:
                text = link.text.strip()
                if text and len(text) < 50 and len(text) > 2:
                    print(f"    - {text}")
                    if "device" in text.lower():
                        device_link = link
                        print(f"      ⭐ Found Device link!")
            
            if device_link:
                device_link.click()
                time.sleep(2)
                print("\n✅ Clicked Device")
            else:
                print("\n❌ 'Device' menu not found. Looking for alternatives...")
                # Maybe it's under a different name
                for link in links:
                    text = link.text.strip()
                    if "system" in text.lower() or "manage" in text.lower():
                        print(f"  Found alternative: {text}")
                return
                
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
            return
        
        # Step 3: Look for Shutdown option
        print("\n[Step 3] Looking for 'Shutdown' option...")
        try:
            links = controller.driver.find_elements(By.TAG_NAME, "a")
            shutdown_link = None
            
            print("  Available Device submenu items:")
            for link in links:
                text = link.text.strip()
                if text and len(text) < 50:
                    if "shutdown" in text.lower() or "reboot" in text.lower() or "restart" in text.lower():
                        print(f"    ⭐ {text}")
                        shutdown_link = link
                    elif text and len(text) > 2:
                        print(f"    - {text}")
            
            if shutdown_link:
                shutdown_link.click()
                time.sleep(2)
                print("\n✅ Navigated to Shutdown page")
            else:
                print("\n❌ Shutdown option not found")
                return
                
        except Exception as e:
            print(f"❌ Error: {e}")
            return
        
        # Step 4: Find the Reboot button
        print("\n[Step 4] Looking for Reboot button...")
        try:
            buttons = controller.driver.find_elements(By.TAG_NAME, "button")
            inputs = controller.driver.find_elements(By.CSS_SELECTOR, "input[type='button'], input[type='submit']")
            
            print("  Buttons found:")
            for btn in buttons + inputs:
                btn_id = btn.get_attribute("id") or ""
                btn_text = btn.text.strip()
                btn_value = btn.get_attribute("value") or ""
                btn_class = btn.get_attribute("class") or ""
                
                display_text = btn_text or btn_value
                if display_text:
                    is_reboot = "reboot" in display_text.lower() or "restart" in display_text.lower()
                    marker = "⭐⭐⭐" if is_reboot else "   "
                    print(f"  {marker} ID='{btn_id}', Text='{display_text}', Class='{btn_class}'")
                    
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("\n" + "=" * 70)
        print("Browser staying open for 30 seconds for manual inspection...")
        print("Press Ctrl+C to close early")
        print("=" * 70)
        time.sleep(30)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        controller.close()

if __name__ == "__main__":
    find_reboot()
