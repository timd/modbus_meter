# main.py
import time
import network
from config import WIFI_CONFIG
from server import start_server

# Connect to WiFi
def connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_CONFIG['ssid'], WIFI_CONFIG['password'])
    
    # Wait for connection
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
        print('IP:', status[0])
        return status[0]

# Start everything
try:
    ip = connect()
    start_server()
except Exception as e:
    print('Failed to start:', e)