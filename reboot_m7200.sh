#!/bin/bash
#
# M7200 Router Reboot Script
# 
# This script automatically reboots the TP-Link M7200 router.
# Suitable for use with cron for scheduled reboots.
#
# Usage:
#   ./reboot_m7200.sh
#
# Cron example (reboot daily at 3 AM):
#   0 3 * * * /path/to/m7200/reboot_m7200.sh >> /var/log/m7200_reboot.log 2>&1
#

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Configuration
VENV_PATH="${SCRIPT_DIR}/venv"
PYTHON_SCRIPT="${SCRIPT_DIR}/reboot_router_cli.py"
LOG_FILE="${SCRIPT_DIR}/reboot.log"

# Timestamp for logging
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

# Function to log messages
log_message() {
    echo "[${TIMESTAMP}] $1" | tee -a "${LOG_FILE}"
}

# Check if virtual environment exists
if [ ! -d "${VENV_PATH}" ]; then
    log_message "ERROR: Virtual environment not found at ${VENV_PATH}"
    exit 1
fi

# Check if Python script exists
if [ ! -f "${PYTHON_SCRIPT}" ]; then
    log_message "ERROR: Python script not found at ${PYTHON_SCRIPT}"
    exit 1
fi

log_message "Starting M7200 reboot process..."

# Activate virtual environment and run the reboot script
source "${VENV_PATH}/bin/activate"

if [ $? -ne 0 ]; then
    log_message "ERROR: Failed to activate virtual environment"
    exit 1
fi

log_message "Virtual environment activated"

# Run the Python reboot script
python "${PYTHON_SCRIPT}"
EXIT_CODE=$?

# Deactivate virtual environment
deactivate

if [ ${EXIT_CODE} -eq 0 ]; then
    log_message "SUCCESS: Router reboot command sent successfully"
    log_message "Router should be back online in approximately 60 seconds"
else
    log_message "ERROR: Router reboot failed with exit code ${EXIT_CODE}"
    exit ${EXIT_CODE}
fi

log_message "Reboot process completed"
exit 0
