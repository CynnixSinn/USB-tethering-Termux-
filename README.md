# USB-Tethering-Termux-
Works entirely within Termux No root required Real-time network monitoring Automatic port selection Easy to use interface  Important Notes for Termux Usage:  Keep Termux running in the background Make sure Termux has network access Accept any permission requests Keep screen on while sharing.


This version is specifically designed for Termux. Here's what you need to do:

1. **Initial Setup:**
First, install Termux from Play Store and then install required packages:
```bash
pkg update
pkg install python
pkg install termux-api
pkg install termux-tools
```

2. **Install Termux:API app:**
- Install "Termux:API" app from Play Store
- This allows the script to access network functions

3. **Save and Run:**
```bash
# Create a directory for the script
mkdir ~/connection_share

# Create the script
nano ~/connection_share/share.py
# (Paste the code in the python script file)

# Make it executable
chmod +x ~/connection_share/share.py

# Run it
python ~/connection_share/share.py
```

Key Features:
1. Works entirely within Termux
2. No root required
3. Real-time network monitoring
4. Automatic port selection
5. Easy to use interface

Important Notes for Termux Usage:
1. Keep Termux running in the background
2. Make sure Termux has network access
3. Accept any permission requests
4. Keep screen on while sharing

To Use:
1. Run the script in Termux
2. Note the IP address and port shown
3. Enter that address in your computer's browser
4. Connection will be established

Troubleshooting:
- If you get permission errors:
  ```bash
  termux-setup-storage
  termux-wifi-enable
  ```
- If connection fails:
  ```bash
  termux-reload-settings
  ```