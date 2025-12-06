"""
TP-Link M7200 Router Controller

This module provides a Python interface to control and monitor a TP-Link M7200 LTE router
via its web interface using Selenium WebDriver.
"""

import json
import time
import os
import subprocess
import re
from typing import Dict, Optional, Any, Type
import types
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


class M7200Controller:
    """Controller class for TP-Link M7200 router operations."""

    def __init__(self, config_path: str = "config.json"):
        """
        Initialize the M7200 controller.

        Args:
            config_path: Path to the configuration JSON file
        """
        with open(config_path, "r") as f:
            self.config = json.load(f)

        self.router_ip = self.config.get("router_ip", "192.168.0.1")
        self.username = self.config.get("username", "admin")
        self.password = self.config.get("password", "admin")
        self.headless = self.config.get("headless", True)
        self.timeout = self.config.get("timeout", 10)
        self.driver: Optional[webdriver.Chrome] = None
        self.base_url = f"http://{self.router_ip}"

    def _get_chromedriver_path(self) -> Optional[str]:
        """Find or use system chromedriver."""
        # Try to find chromedriver in PATH
        try:
            result = subprocess.run(
                ["which", "chromedriver"], capture_output=True, text=True, check=True
            )
            chromedriver_path = result.stdout.strip()
            if chromedriver_path and os.path.isfile(chromedriver_path):
                return chromedriver_path
        except (subprocess.CalledProcessError, FileNotFoundError):
            pass

        # If not found, let Selenium use default
        return None

    def _init_driver(self) -> None:
        """Initialize the Selenium WebDriver."""
        if self.driver is not None:
            return

        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument("--headless=new") # pyright: ignore[reportUnknownMemberType]
            chrome_options.add_argument("--no-sandbox") # pyright: ignore[reportUnknownMemberType]
            chrome_options.add_argument("--disable-dev-shm-usage") # pyright: ignore[reportUnknownMemberType]

        chrome_options.add_argument("--disable-gpu") # pyright: ignore[reportUnknownMemberType]
        chrome_options.add_argument("--window-size=1920,1080") # pyright: ignore[reportUnknownMemberType]
        chrome_options.add_argument("--disable-blink-features=AutomationControlled") # pyright: ignore[reportUnknownMemberType]

        # Try to use system chromedriver or let Selenium find it
        chromedriver_path = self._get_chromedriver_path()

        try:
            if chromedriver_path:
                service = Service(chromedriver_path)
                self.driver = webdriver.Chrome(service=service, options=chrome_options)
            else:
                # Let Selenium use its built-in driver management
                self.driver = webdriver.Chrome(options=chrome_options)
        except Exception as e:
            print(f"Chrome initialization error: {e}")
            print("Trying alternative approach...")
            # Fallback: try without explicit service
            self.driver = webdriver.Chrome(options=chrome_options)

        assert self.driver is not None, "Failed to initialize Chrome driver"
        self.driver.set_page_load_timeout(self.timeout)

    def login(self) -> bool:
        """
        Log into the router's web interface.

        Returns:
            bool: True if login successful, False otherwise
        """
        try:
            self._init_driver()
            assert self.driver is not None, "Driver not initialized"
            print(f"Navigating to {self.base_url}...")
            self.driver.get(self.base_url)

            # Wait for login page to load
            wait = WebDriverWait(self.driver, self.timeout)

            # M7200 uses password-only login (no username field visible)
            try:
                # Wait for password field to be clickable (not just present)
                print("Waiting for page to load...")
                password_field = wait.until(
                    EC.element_to_be_clickable((By.ID, "password"))
                )

                # Additional wait for any JavaScript initialization
                time.sleep(2)

                print("Entering password...")
                password_field.clear()
                password_field.send_keys(self.password) # pyright: ignore[reportUnknownMemberType]

                # Find and click login button - also wait for it to be clickable
                login_button = wait.until(
                    EC.element_to_be_clickable((By.ID, "loginBtn"))
                )
                login_button.click()

                # Wait for dashboard to load
                time.sleep(3)

                # Check if login was successful by verifying we're not on login page
                current_url = self.driver.current_url
                page_text = self.driver.find_element(By.TAG_NAME, "body").text

                if (
                    "login" not in current_url.lower()
                    and "password" not in page_text.lower()
                ):
                    print("Login successful!")
                    return True
                else:
                    print("Login may have failed - still on login page")
                    return False

            except Exception as e:
                print(f"Login error: {e}")
                # Try to capture more info
                try:
                    page_source = self.driver.page_source[:500]
                    print(f"Page source preview: {page_source}")
                except Exception:
                    pass
                return False

        except Exception as e:
            print(f"Login error: {e}")
            return False

    def get_connection_status(self) -> Dict[str, Any]:
        """
        Get the current connection status.

        Returns:
            dict: Connection status information including network type, IP addresses
        """
        try:
            if self.driver is None:
                if not self.login():
                    return {"error": "Failed to login"}

            assert self.driver is not None, "Driver not initialized"
            print("Fetching connection status...")

            # Make sure we're on the status page
            if "#Status" not in self.driver.current_url:
                self.driver.get(f"{self.base_url}/settings.html#Status")
                time.sleep(2)

            status_data = {}

            try:
                # Extract data from HTML elements by ID
                element_ids = {
                    "connectionStatus": "Connection Status",
                    "networkType": "Network Type",
                }

                for elem_id, label in element_ids.items():
                    try:
                        element = self.driver.find_element(By.ID, elem_id)
                        value = element.text.strip()
                        status_data[label.lower().replace(" ", "_")] = value
                    except Exception:
                        pass

                # Get full status page text and parse it
                page_text = self.driver.find_element(By.ID, "statusContent").text

                # Parse key-value pairs from the text
                for line in page_text.split("\n"):
                    if ":" in line:
                        key, value = line.split(":", 1)
                        key = key.strip().lower().replace(" ", "_")
                        value = value.strip()
                        status_data[key] = value

            except Exception as e:
                print(f"Status extraction error: {e}")

            status_data["timestamp"] = time.time()
            return status_data  # pyright: ignore[reportUnknownVariableType]

        except Exception as e:
            return {"error": str(e)}

    def get_lte_details(self) -> Dict[str, Any]:
        """
        Get detailed LTE signal information.

        Returns:
            dict: LTE signal details including band, RSRP, RSRQ, SNR, etc.
        """
        try:
            if self.driver is None:
                if not self.login():
                    return {"error": "Failed to login"}

            assert self.driver is not None, "Driver not initialized"
            print("Fetching LTE details...")

            # Make sure we're on the status page which has LTE info
            if "#Status" not in self.driver.current_url:
                self.driver.get(f"{self.base_url}/settings.html#Status")
                time.sleep(2)

            lte_data = {}

            try:
                # M7200 has LTE data in HTML elements with specific IDs
                lte_element_ids = {
                    "band": "Band",
                    "rsrp": "RSRP",
                    "rsrq": "RSRQ",
                    "rssi": "RSSI",  # Might not be visible but check
                    "snr": "SNR",
                }

                for key, elem_id in lte_element_ids.items():
                    try:
                        element = self.driver.find_element(By.ID, elem_id)
                        value = element.text.strip()
                        lte_data[key] = value
                    except Exception:
                        # Element might not exist
                        pass

                # Also extract from the page text as fallback
                try:
                    status_content = self.driver.find_element(
                        By.ID, "statusContent"
                    ).text

                    # Parse signal metrics from text
                    patterns = {
                        "band": r"Band:\s*(\d+)",
                        "rsrp": r"RSRP:\s*(-?\d+(?:\.\d+)?)\s*dBm",
                        "rsrq": r"RSRQ:\s*(-?\d+(?:\.\d+)?)\s*dB",
                        "snr": r"SNR:\s*(-?\d+(?:\.\d+)?)\s*dB",
                        "network_type": r"Network Type:\s*(\w+)",
                    }

                    for key, pattern in patterns.items():
                        match = re.search(pattern, status_content)
                        if match:
                            lte_data[key] = match.group(1)

                except Exception as parse_error:
                    print(f"Text parsing error: {parse_error}")

            except Exception as e:
                print(f"LTE extraction error: {e}")

            lte_data["timestamp"] = time.time()
            return lte_data  # pyright: ignore[reportUnknownVariableType]

        except Exception as e:
            return {"error": str(e)}

    def reboot_router(self) -> bool:
        """
        Reboot the router.

        Navigates to Advanced -> Device -> Shutdown and clicks the Reboot button.

        Returns:
            bool: True if reboot command sent successfully
        """
        try:
            if self.driver is None:
                if not self.login():
                    return False

            assert self.driver is not None, "Driver not initialized"
            print("Initiating router reboot...")

            try:
                # Navigate to: Advanced -> Device -> Shutdown

                # Step 1: Click Advanced menu
                print("  Navigating to Advanced menu...")
                advanced = self.driver.find_element(By.LINK_TEXT, "Advanced")
                advanced.click()
                time.sleep(1)

                # Step 2: Click Device submenu
                print("  Opening Device submenu...")
                device = self.driver.find_element(By.LINK_TEXT, "Device")
                device.click()
                time.sleep(1)

                # Step 3: Click Shutdown
                print("  Navigating to Shutdown page...")
                shutdown = self.driver.find_element(By.LINK_TEXT, "Shutdown")
                shutdown.click()
                time.sleep(2)

                # Step 4: Click Reboot button (it's a span element)
                print("  Clicking Reboot button...")
                reboot_btn = self.driver.find_element(By.ID, "rebootBtn")
                reboot_btn.click()
                time.sleep(1)

                # Step 5: Confirm reboot in popup (click OK button)
                print("  Confirming reboot...")
                try:
                    confirm_btn = self.driver.find_element(By.ID, "shutdownOK")
                    confirm_btn.click()
                    print("✅ Reboot command sent successfully!")
                    print(
                        "⚠️  Router is rebooting, it will be offline for ~30-60 seconds"
                    )
                    return True
                except Exception as confirm_error:
                    print(f"  Warning: Could not click confirm button: {confirm_error}")
                    # Button might have different ID or timing issue
                    return False

            except Exception as nav_error:
                print(f"❌ Navigation error: {nav_error}")
                print("Could not navigate to reboot page")
                return False

        except Exception as e:
            print(f"❌ Reboot error: {e}")
            return False

    def get_all_info(self) -> Dict[str, Any]:
        """
        Get all available information from the router.

        Returns:
            dict: Combined connection status and LTE details
        """
        return {
            "connection_status": self.get_connection_status(),
            "lte_details": self.get_lte_details(),
        }

    def close(self) -> None:
        """Close the browser and clean up resources."""
        if self.driver:
            print("Closing browser...")
            self.driver.quit()
            self.driver = None

    def __enter__(self) -> 'M7200Controller':
        """Context manager entry."""
        return self

    def __exit__(self, exc_type: Optional[Type[BaseException]], exc_val: Optional[BaseException], exc_tb: Optional[types.TracebackType]) -> None:
        """Context manager exit."""
        self.close()
