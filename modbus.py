# modbus.py
import time
from machine import Pin, UART
from umodbus.serial import Serial as ModbusRTUMaster
from modbus_utils import combine_signed_registers, read_modbus_registers
import asyncio

# Define comms params
RTU_PINS = (Pin(0), Pin(1))
BAUD_RATE = 9600
DATA_BITS = 8
STOP_BITS = 1
PARITY = None
UART_ID = 0
CTRL_PIN = None

# Create a single host instance to be reused
host = ModbusRTUMaster(
    baudrate=BAUD_RATE,
    data_bits=DATA_BITS,
    stop_bits=STOP_BITS,
    parity=PARITY,
    pins=RTU_PINS,
    ctrl_pin=CTRL_PIN,
    uart_id=UART_ID
)

class ModbusError(Exception):
    """Custom exception for Modbus errors"""
    pass

async def process_reading(reading):
    try:
        # Give other tasks a chance to run before starting Modbus communication
        await asyncio.sleep(0)
        
        # Perform the Modbus read
        result = read_modbus_registers(
            host,
            starting_address=reading.address,
            no_of_registers=reading.registers
        )
        
        # Give other tasks a chance to run after Modbus communication
        await asyncio.sleep(0)
        
        if isinstance(result, int):
            print(f"{reading.name} - Address: {reading.address} Result: {result}")
            return result
        else:
            print(f"Modbus read failed: {result}")
            raise ModbusError(f"No response from Modbus device")
            
    except Exception as e:
        print(f"Modbus error: {e}")
        raise ModbusError(str(e))

def cleanup():
    host.close()