def combine_signed_registers(*registers):
    """
    Combine 1-4 signed 16-bit registers into a single integer value
    First register (registers[0]) = most significant 16 bits
    Last register = least significant 16 bits
    
    Args:
        *registers: Variable number of register values (1-4 registers)
        Either as individual arguments or as a single tuple
        
    Returns:
        int: Combined value from registers
    """
    # Handle case where registers is passed as a tuple
    if len(registers) == 1 and isinstance(registers[0], tuple):
        registers = registers[0]
        
    if not 1 <= len(registers) <= 4:
        raise ValueError("Must provide between 1 and 4 registers")
        
    # Convert negative values to their 16-bit representation
    registers = [reg & 0xFFFF if reg < 0 else reg for reg in registers]
    
    # Calculate total number of bits needed
    total_bits = len(registers) * 16
    
    # Combine registers
    value = 0
    for i, reg in enumerate(registers):
        shift = total_bits - ((i + 1) * 16)  # Calculate shift for each register
        value |= (reg & 0xFFFF) << shift
    
    # If this is a signed value and highest bit is set, make it negative
    if value & (1 << (total_bits - 1)):
        value = value - (1 << total_bits)
        
    return value

def read_modbus_registers(host, starting_address, no_of_registers):
    """
    Read Modbus registers and combine into single decimal value
    
    Args:
        starting_address (int): First register address to read
        no_of_registers (int): Number of registers to read (1-4)
        
    Returns:
        int: Combined decimal value from registers
        or
        str: Error message if reading fails
    """
    try:
        # Read holding registers from the slave device
        values = host.read_holding_registers(
            slave_addr=1, 
            starting_addr=starting_address,
            register_qty=no_of_registers,
            signed=True
        )
        
        # Pass the tuple directly to combine_signed_registers        
        combined = combine_signed_registers(values)
        return combined
        
    except Exception as e:
        return f"Error reading registers: {str(e)}"