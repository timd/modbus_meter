# server.py
import json
import time
import asyncio
from collections import namedtuple
from modbus import process_reading, ModbusError

# Define meter registers
ModbusRegister = namedtuple('ModbusRegister', ['name', 'address', 'registers'])
 
HISTORIC_TOTAL_ACTIVE_ENERGY_IMPORT = ModbusRegister("Historic Total Active Energy Import", 0x0C83, 4)
HISTORIC_TOTAL_ACTIVE_ENERGY_EXPORT = ModbusRegister("Historic Total Active Energy Export", 0x0C87, 4)
NOMINAL_FREQUENCY = ModbusRegister("Nominal Frequency", 0x07E0, 1)
LIVE_TOTAL_ACTIVE_POWER = ModbusRegister("Live total active power", 0x0BF3, 2)
LIVE_ACTIVE_POWER_L1 = ModbusRegister("Live active power Phase L1", 0x0BED, 2)
LIVE_ACTIVE_POWER_L2 = ModbusRegister("Live active power Phase L2", 0x0BEF, 2)
LIVE_ACTIVE_POWER_L3 = ModbusRegister("Live active power Phase L3", 0x0BF1, 2)

async def handle_request(reader, writer):
    try:
        # Get the request
        request_line = await reader.readline()
        path = request_line.decode().split()[1]
        print(f"Received request for: {path}")
        
        # Clear the rest of the request
        while await reader.readline() != b'\r\n':
            pass
        
        # Handle different paths
        if path == '/':
            response = {
                'status': 'success',
                'time': time.time()
            }
            status_code = '200 OK'
            
        elif path == '/frequency':
            try:
                reading = await asyncio.wait_for(process_reading(NOMINAL_FREQUENCY), timeout=5.0)
                response = {
                    'status': 'success',
                    'frequency': reading,
                    'timestamp': time.time()
                }
                status_code = '200 OK'
            except asyncio.TimeoutError:
                response = {
                    'status': 'error',
                    'error': 'Request timed out after 5 seconds',
                    'timestamp': time.time()
                }
                status_code = '503 Service Unavailable'
            except ModbusError as e:
                response = {
                    'status': 'error',
                    'error': 'Modbus communication failed',
                    'detail': str(e),
                    'timestamp': time.time()
                }
                status_code = '503 Service Unavailable'
            except Exception as e:
                response = {
                    'status': 'error',
                    'error': 'Internal server error',
                    'detail': str(e),
                    'timestamp': time.time()
                }
                status_code = '500 Internal Server Error'
                
        elif path == '/import':
            try:
                reading = await asyncio.wait_for(process_reading(HISTORIC_TOTAL_ACTIVE_ENERGY_IMPORT), timeout=5.0)
                response = {
                    'status': 'success',
                    'frequency': reading,
                    'timestamp': time.time()
                }
                status_code = '200 OK'
            except asyncio.TimeoutError:
                response = {
                    'status': 'error',
                    'error': 'Request timed out after 5 seconds',
                    'timestamp': time.time()
                }
                status_code = '503 Service Unavailable'
            except ModbusError as e:
                response = {
                    'status': 'error',
                    'error': 'Modbus communication failed',
                    'detail': str(e),
                    'timestamp': time.time()
                }
                status_code = '503 Service Unavailable'
                
        elif path == '/export':
            try:
                reading = await asyncio.wait_for(process_reading(HISTORIC_TOTAL_ACTIVE_ENERGY_EXPORT), timeout=5.0)
                response = {
                    'status': 'success',
                    'export': reading,
                    'timestamp': time.time()
                }
                status_code = '200 OK'
            except asyncio.TimeoutError:
                response = {
                    'status': 'error',
                    'error': 'Request timed out after 5 seconds',
                    'timestamp': time.time()
                }
                status_code = '503 Service Unavailable'
            except ModbusError as e:
                response = {
                    'status': 'error',
                    'error': 'Modbus communication failed',
                    'detail': str(e),
                    'timestamp': time.time()
                }
                status_code = '503 Service Unavailable'

            except Exception as e:
                response = {
                    'status': 'error',
                    'error': 'Internal server error',
                    'detail': str(e),
                    'timestamp': time.time()
                }
                status_code = '500 Internal Server Error'
        else:
            response = {
                'status': 'error',
                'error': 'Invalid endpoint'
            }
            status_code = '404 Not Found'
            
        # Send response
        response_json = json.dumps(response)
        writer.write(f'HTTP/1.0 {status_code}\r\n'.encode())
        writer.write(b'Content-Type: application/json\r\n')
        writer.write(f'Content-Length: {len(response_json)}\r\n'.encode())
        writer.write(b'\r\n')
        writer.write(response_json.encode())
        await writer.drain()
        print(f"Response sent: {status_code}")
        
    except Exception as e:
        print('Request handling error:', e)
    finally:
        writer.close()
        await writer.wait_closed()
        print("Connection closed")

async def run_server():
    print('Starting server...')
    server = await asyncio.start_server(handle_request, '0.0.0.0', 80)
    print('Server started on port 80')
    while True:
        await asyncio.sleep(1)

def start_server():
    try:
        asyncio.run(run_server())
    except Exception as e:
        print('Server error:', e)