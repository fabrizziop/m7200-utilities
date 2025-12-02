# M7200 Router Controller - Installation Guide

## Quick Fix for ChromeDriver Error

The error you encountered is from webdriver-manager. The updated code now uses Selenium's built-in driver management (available in Selenium 4.6+).

### Option 1: Install System ChromeDriver (Recommended)

```bash
# For Debian/Ubuntu
sudo apt-get update
sudo apt-get install chromium-driver
```

### Option 2: Use Selenium's Built-in Management (Already Configured)

The code now automatically uses Selenium's built-in driver manager, which handles ChromeDriver installation automatically. Just run:

```bash
source venv/bin/activate
python inspect_router.py
```

### Option 3: Manual ChromeDriver Installation

If automatic methods fail:

1. **Check your Chrome/Chromium version:**
   ```bash
   chromium-browser --version
   # or
   google-chrome --version
   ```

2. **Download matching ChromeDriver:**
   - Visit: https://googlechromelabs.github.io/chrome-for-testing/
   - Download the version matching your Chrome version
   - Extract it to `/usr/local/bin/` or your project directory

3. **Make it executable:**
   ```bash
   chmod +x chromedriver
   sudo mv chromedriver /usr/local/bin/
   ```

### Troubleshooting

If you still get errors:

1. **Verify chromium-driver is installed:**
   ```bash
   which chromedriver
   chromedriver --version
   ```
   If not found, install it:
   ```bash
   sudo apt-get install chromium-driver
   ```

2. **Clear Selenium cache:**
   ```bash
   rm -rf ~/.cache/selenium
   ```

3. **Reinstall Python dependencies:**
   ```bash
   pip install --upgrade selenium
   ```

## Running the Scripts

```bash
# Activate venv
source venv/bin/activate

# Run inspector (non-headless to see what's happening)
python inspect_router.py

# Run example
python example.py
```
