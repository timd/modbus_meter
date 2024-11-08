import network
import time
import socket

def connect_wifi():
    # Initialize wireless interface
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    # Connect to your WiFi network - replace with your credentials
    SSID = 'withywindle'
    PASSWORD = 'b0mb4d1lh3yd0ll'
    
    wlan.connect(SSID, PASSWORD)
    
    # Wait for connection with timeout
    max_wait = 10
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        print('Waiting for connection...')
        time.sleep(1)
        
    # Handle connection error
    if wlan.status() != 3:
        raise RuntimeError('Network connection failed')
    else:
        print('Connected')
        status = wlan.ifconfig()
        print('IP Address:', status[0])
        return status[0]  # Return IP address

# Call this before starting the web server
try:
    ip = connect_wifi()
    print(f'Ready! Access your server at: http://{ip}/')
except Exception as e:
    print('Failed to connect:', e)