
def set_equipment_linux():

    pass

def set_equipment_windows():
    """
    Function to discover the COM which is connected the device, once it's discover, it will
    write it down inside the config_file, generating a new one with the name
    'config_file_generated.yaml'

    Params:
    -----------

    Returns: True/False Depending if the creation of the file was sucessfull
    """
    # import the libraries to discover bluetooth and ports
    from bluetooth import discover_devices
    import serial.tools.list_ports
    import yaml

    # fixed Name of the device
    fixed_names = "MindWave Mobile"
    # Port to be discovered
    COM_port = None

    # Extract the Bluetooth devices saved and connected
    nearby_devices = discover_devices(lookup_names=True)
    # extract the COM ports
    comPorts = serial.tools.list_ports.comports()

    # Run over the devices
    for addr, name in nearby_devices:
        # Match with the comPorts
        for COM, des, port_addr in comPorts:
            # Remove the : form the addres in order to match it
            if addr.replace(":", "") in port_addr and fixed_names == name:
                COM_port = COM
                break

    # check if we have discovered the COM_port
    if COM_port is None: return False

    # return the successful
    return COM_port
