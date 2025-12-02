#!/usr/bin/env python3
"""
Inspect the Shutdown page more thoroughly
"""

from m7200_controller import M7200Controller
from selenium.webdriver.common.by import By
import time


def inspect_shutdown_page():
    print("=" * 70)
    print("Inspecting Shutdown Page Elements")
    print("=" * 70)
    
    controller = M7200Controller()
    controller.headless = False
    
    try:
        if not controller.login():
            return
        
        print("✅ Logged in")
        
        # Navigate directly to shutdown page URL if we can find it
        print("\nNavigating to: Advanced -> Device -> Shutdown")
        
        # Click Advanced
        advanced = controller.driver.find_element(By.LINK_TEXT, "Advanced")
        advanced.click()
        time.sleep(1)
        
        # Click Device
        device = controller.driver.find_element(By.LINK_TEXT, "Device")
        device.click()
        time.sleep(1)
        
        # Click Shutdown
        shutdown = controller.driver.find_element(By.LINK_TEXT, "Shutdown")
        shutdown.click()
        time.sleep(2)
        
        print(f"\n✅ On page: {controller.driver.current_url}")
        
        # Get all interactive elements
        print("\n[ALL BUTTONS]")
        buttons = controller.driver.find_elements(By.TAG_NAME, "button")
        for i, btn in enumerate(buttons):
            print(f"  Button {i+1}: ID='{btn.get_attribute('id')}', "
                  f"Text='{btn.text}', Class='{btn.get_attribute('class')}'")
        
        print("\n[ALL INPUTS]")
        inputs = controller.driver.find_elements(By.TAG_NAME, "input")
        for i, inp in enumerate(inputs):
            inp_type = inp.get_attribute("type")
            inp_id = inp.get_attribute("id")
            inp_value = inp.get_attribute("value")
            inp_class = inp.get_attribute("class")
            if inp_type in ["button", "submit"]:
                print(f"  Input {i+1}: Type='{inp_type}', ID='{inp_id}', "
                      f"Value='{inp_value}', Class='{inp_class}'")
        
        print("\n[PAGE CONTENT WITH ID 'shutdown' or 'reboot']")
        all_elements = controller.driver.find_elements(By.XPATH, "//*[contains(@id, 'shutdown') or contains(@id, 'reboot') or contains(@id, 'Shutdown') or contains(@id, 'Reboot')]")
        for elem in all_elements:
            print(f"  Tag: {elem.tag_name}, ID: {elem.get_attribute('id')}, "
                  f"Text: {elem.text[:50]}")
        
        print("\n[PAGE TEXT]")
        page_content = controller.driver.find_element(By.TAG_NAME, "body").text
        lines = [line.strip() for line in page_content.split('\n') if line.strip()]
        for line in lines[20:40]:  # Print middle section
            print(f"  {line}")
        
        print("\n" + "=" * 70)
        print("Keeping browser open - inspect with F12")
        print("=" * 70)
        time.sleep(60)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        controller.close()


if __name__ == "__main__":
    inspect_shutdown_page()
