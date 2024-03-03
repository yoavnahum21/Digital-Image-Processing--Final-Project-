import serial


def init_port():
    port = serial.Serial(
        port='COM6',  # Adjust this to match your serial port
        baudrate=115200,  # Set the baudrate according to your device
        timeout=0.1  # Set timeout as needed
    )
    return port


def Set_package_and_transmit(message, port):
    encoded_message = message.encode('utf-8')
    port.write(encoded_message)


def Received_package():
    pass

