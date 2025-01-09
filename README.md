# WAN Listener for Internet Connection Monitoring

This project implements a listener on the WAN port using the `pfSense REST API` to monitor internet connectivity. If the internet connection is down, the script will attempt to reset the connection by disabling and re-enabling the WAN port.

## Prerequisites

- **pfSense REST API**: This script uses the `pfSense REST API` provided by [jaredhendrickson13/pfsense-api](https://github.com/jaredhendrickson13/pfsense-api).
- **Linux Machine**: The service is designed to run on a Linux machine. This guide assumes you're using Ubuntu.

## Installation Instructions

### 1. Clone the Repository
Clone the repository to your Ubuntu machine:
```bash
git clone https://github.com/david1x/pfsense_wan_reset.git
```

### 2. Set Up a Virtual Environment
Navigate to the repository directory and create a Python virtual environment:
```bash
cd pfsense_wan_reset
python3 -m venv venv
```
Activate the virtual environment and install any required dependencies (if applicable):
```bash
source venv/bin/activate
pip3 install -r requirements.txt
```

### 3. Make the Script Executable
Ensure the main script (`main.py`) is executable:
```bash
chmod +x /path/to/repo/main.py
```

### 4. Create a Systemd Service
To run the script as a background service, create a new systemd service file:
```bash
sudo nano /etc/systemd/system/wan_listener.service
```

Add the following content, making the necessary adjustments:
```ini
[Unit]
Description=WAN Listener for Internet Connection Monitoring
After=network.target

[Service]
ExecStart=/path/to/repo/venv/bin/python3 /path/to/repo/main.py
Restart=always
RestartSec=5
User=your_user
Group=your_group
StandardOutput=syslog
StandardError=syslog
SyslogIdentifier=wan_listener

[Install]
WantedBy=multi-user.target
```
Replace `/path/to/repo` with the actual path to the cloned repository and adjust `User` and `Group` as needed.

### 5. Enable and Start the Service
Reload systemd to recognize the new service and enable it to start on boot:
```bash
sudo systemctl daemon-reload
sudo systemctl enable wan_listener.service
sudo systemctl start wan_listener.service
```

### 6. Verify the Service
Check the status of the service to ensure it is running:
```bash
sudo systemctl status wan_listener.service
```

To view the service logs:
```bash
sudo journalctl -u wan_listener.service
```

## Notes
- This script assumes the `pfSense REST API` is properly configured and accessible.
- Adjust the `RestartSec` value in the service file if you want to change the delay between restarts.

## License
This project is licensed under the [MIT License](LICENSE).

For more information, refer to the original `pfSense REST API` documentation: [jaredhendrickson13/pfsense-api](https://github.com/jaredhendrickson13/pfsense-api).

