#!/usr/bin/env python3
"""
Inspect the status page after login to find LTE data elements
"""

from m7200_controller import M7200Controller
import time
import json

def inspect_status_page():
    print("=" * 60)
    print("M7200 Status Page Inspector")
    print("=" * 60)
    
    controller = M7200Controller()
    controller.headless = False  # Show browser
    
    try:
        if not controller.login():
            print("❌ Login failed!")
            return
        
        print("\n✅ Logged in! Now on status page.")
        print(f"URL: {controller.driver.current_url}")
        
        time.sleep(2)
        
        # Get page text
        from selenium.webdriver.common.by import By
        page_text = controller.driver.find_element(By.TAG_NAME, "body").text
        print("\n[PAGE TEXT]")
        print(page_text[:1000])
        
        # Check for JavaScript variables with LTE info
        print("\n[CHECKING JAVASCRIPT VARIABLES]")
        js_vars_to_check = [
            'connectionStatus', 'networkType', 'signalStrength', 'signalLevel',
            'rssi', 'rsrp', 'rsrq', 'sinr', 'rsrpValue', 'rsrqValue', 'sinrValue',
            'band', 'bandInfo', 'cellId', 'pci', 'operator', 'operatorName',
            'wanStatus', 'networkInfo', 'lteInfo', 'statusData'
        ]
        
        for var in js_vars_to_check:
            try:
                result = controller.driver.execute_script(
                    f"return typeof {var} !== 'undefined' ? {var} : null;"
                )
                if result is not None:
                    print(f"  ✓ {var} = {result}")
            except Exception as e:
                pass
        
        # Try to extract from global objects
        print("\n[CHECKING WINDOW OBJECTS]")
        try:
            window_keys = controller.driver.execute_script("""
                var keys = [];
                for (var key in window) {
                    if (key.toLowerCase().includes('status') || 
                        key.toLowerCase().includes('lte') ||
                        key.toLowerCase().includes('signal') ||
                        key.toLowerCase().includes('network')) {
                        keys.push(key);
                    }
                }
                return keys.slice(0, 20);
            """)
            for key in window_keys:
                print(f"  Found: {key}")
        except Exception as e:
            print(f"  Error: {e}")
        
        # Look for specific elements
        print("\n[LOOKING FOR STATUS ELEMENTS]")
        try:
            elements = controller.driver.find_elements(By.CSS_SELECTOR, '[id*="status"], [id*="signal"], [class*="status"], [class*="signal"]')
            for elem in elements[:15]:
                elem_id = elem.get_attribute("id")
                elem_class = elem.get_attribute("class")
                elem_text = elem.text[:50] if elem.text else ""
                if elem_id or elem_text:
                    print(f"  ID: {elem_id}, Class: {elem_class}, Text: {elem_text}")
        except Exception as e:
            print(f"  Error: {e}")
        
        print("\n" + "=" * 60)
        print("Browser will stay open for 30 seconds.")
        print("Use DevTools (F12) to inspect further.")
        print("=" * 60)
        time.sleep(30)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        controller.close()

if __name__ == "__main__":
    inspect_status_page()
