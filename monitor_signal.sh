#!/bin/bash
#
# M7200 Signal Monitor Script
# 
# Logs LTE signal statistics and generates visualization graph.
# Suitable for use with cron for periodic monitoring.
#
# Usage:
#   ./monitor_signal.sh
#
# Cron example (monitor every 5 minutes):
#   */5 * * * * /path/to/m7200/monitor_signal.sh >> /var/log/m7200_monitor.log 2>&1
#

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Configuration
VENV_PATH="${SCRIPT_DIR}/venv"
PYTHON_SCRIPT="${SCRIPT_DIR}/monitor_signal.py"
LOG_FILE="${SCRIPT_DIR}/monitor.log"

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

log_message "Starting signal monitoring..."

# Activate virtual environment and run the monitor script
source "${VENV_PATH}/bin/activate"

if [ $? -ne 0 ]; then
    log_message "ERROR: Failed to activate virtual environment"
    exit 1
fi

# Run the Python monitor script
python "${PYTHON_SCRIPT}"
EXIT_CODE=$?

# Deactivate virtual environment
deactivate

if [ ${EXIT_CODE} -eq 0 ]; then
    log_message "SUCCESS: Signal data logged and graph updated"
else
    log_message "ERROR: Signal monitoring failed with exit code ${EXIT_CODE}"
    exit ${EXIT_CODE}
fi

exit 0
