#!/usr/bin/env python

"""set_config_CH9121.py: Sets the registers of the CH9121 chip to be used as a Ethernet-UART Converter."""
"""It is a part of the Powerswitch-UART here https://hackaday.io/project/189531-powerswitch-uart """

__author__      = "Nikola Trifunovic"
__copyright__ = "Copyright 2023, Powerswitch-UART"
__license__ = "GPL"
__version__ = "0.1"
__status__ = "Develpoment"

import serial
import math
import time
import sys

TCP_SERVER = 0x00
TCP_CLIENT = 0x01
UDP_SERVER = 0x02
UDP_CLIENT = 0x03

UART_PORT = str(sys.argv[1])

ser = serial.Serial(UART_PORT, 9600, timeout=1)  # open serial port

def i_to_b(x: int) -> bytes:
    if x == 0:
        #print("HIER")
        return x.to_bytes(1,'little')
    else:
        return x.to_bytes(math.ceil(x.bit_length()/8), 'little')

    
def send_command(*value):
    command = bytearray()
    command.append(0x57)
    command.append(0xab)

    for val in value:
        command.extend(i_to_b(val))

    print(command)
    
    ser.write(command)     #
    ret = ser.read(1)

    if (ret != b'\xaa'):
        print("Incorrect command or value: "+str(command))
        ser.close()
        exit()

    time.sleep(0.5)

## Reset Module
send_command(0x02)

## Set chip port 1 TCP server
send_command(0x10,TCP_SERVER)

## Set chip IP address
send_command(0x11, 192, 168, 1, 10)

## Set chip mask
send_command(0x12, 255, 255, 255, 0)

## Set chip port 1 book Ground source port
send_command(0x14, 1000)

## Set the destination (target) IP of chip port 1
#send_command(0x15, 192, 168, 1, 100)

## Set chip port 1 destination (target) port
#send_command(0x16, 3000)

## Set the baud rate of port 1 serial port
## Added 0x00; baud value needs 4 bytes
send_command(0x21, 115200,  0x00)

## Turn on/off port 2
send_command(0x39, 0x01)

## Set chip port 2 network mode
send_command(0x40, TCP_SERVER)

## Set chip port 2 local source port
send_command(0x41, 2000)

## Save parameters to EEPROM
send_command(0x0d)

## Execute the configuration command, and Reset CH9121
send_command(0x0e)

## Leave serial port configuration mode
send_command(0x5e)

ser.close()             # close port
