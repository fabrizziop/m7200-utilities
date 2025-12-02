#!/usr/bin/env python3
"""
Inspector script to help identify the correct element selectors for your M7200 router.

Run this script in non-headless mode to see and interact with your router's interface,
then check the console output to find the correct element IDs and JavaScript variables.
"""

from m7200_controller import M7200Controller
from selenium.webdriver.common.by import By
import time


def inspect_router():
    """Inspect the router's web interface to find correct selectors."""
    
    print("=" * 60)
    print("M7200 Router Inspector")
    print("=" * 60)
    print("\nThis script will help you identify the correct element selectors")
    print("for your router's web interface.\n")
    
    # Create controller with non-headless mode
    controller = M7200Controller()
    controller.headless = False  # Override to show browser
    
    try:
        controller._init_driver()
        print(f"Opening {controller.base_url}...")
        controller.driver.get(controller.base_url)
        
        print("\n✓ Browser opened. Now inspect the page:")
        print("  1. Look at the browser window that just opened")
        print("  2. Right-click on elements and select 'Inspect'")
        print("  3. Note the element IDs, names, or other selectors")
        print("\nWaiting 30 seconds for you to inspect...")
        time.sleep(5)
        
        # Try to get page source
        print("\n" + "=" * 60)
        print("PAGE TITLE:", controller.driver.title)
        print("=" * 60)
        
        # List all input fields
        print("\n[INPUT FIELDS FOUND]")
        inputs = controller.driver.find_elements(By.TAG_NAME, "input")
        for i, inp in enumerate(inputs[:10]):  # Show first 10
            try:
                input_id = inp.get_attribute("id")
                input_name = inp.get_attribute("name")
                input_type = inp.get_attribute("type")
                print(f"  Input {i+1}: ID='{input_id}', Name='{input_name}', Type='{input_type}'")
            except:
                pass
        
        # List all buttons
        print("\n[BUTTONS FOUND]")
        buttons = controller.driver.find_elements(By.TAG_NAME, "button")
        for i, btn in enumerate(buttons[:10]):
            try:
                btn_id = btn.get_attribute("id")
                btn_text = btn.text
                print(f"  Button {i+1}: ID='{btn_id}', Text='{btn_text}'")
            except:
                pass
        
        # Try to extract JavaScript variables
        print("\n[CHECKING JAVASCRIPT VARIABLES]")
        js_vars = [
            "userName", "password", "connectionStatus", "networkType",
            "rssiValue", "rsrpValue", "rsrqValue", "sinrValue", 
            "bandInfo", "cellId", "operatorName"
        ]
        
        for var in js_vars:
            try:
                value = controller.driver.execute_script(f"return typeof {var} !== 'undefined' ? {var} : 'undefined';")
                if value != 'undefined':
                    print(f"  ✓ {var} = {value}")
            except:
                pass
        
        print("\n" + "=" * 60)
        print("Keeping browser open for 60 more seconds...")
        print("Use this time to manually navigate and inspect pages.")
        print("=" * 60)
        time.sleep(60)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
    finally:
        print("\nClosing browser...")
        controller.close()


if __name__ == "__main__":
    inspect_router()
