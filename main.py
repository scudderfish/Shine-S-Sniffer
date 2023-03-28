import serial
import itertools
from time import sleep
import datetime

def readPort(ser, leader):
    bytebuffer = bytearray()
    count = 0
    byte = ser.read()
    while len(byte) > 0:
        count = count + len(byte)
        bytebuffer = bytearray(itertools.chain(bytebuffer, byte))
        map(bytebuffer.extend, byte)
        ser.timeout = 0.2
        byte = ser.read()
    bytesAsHex = bytebuffer.hex(" ")
    print(f'{datetime.datetime.now()} {leader} {bytesAsHex}')


def sniffSerial():
    ser1 = serial.Serial('/dev/ttyUSB0')
    ser2 = serial.Serial('/dev/ttyUSB1')
    while True:
        ser1.timeout = None
        ser2.timeout = None

        if ser1.in_waiting == 0 and ser2.in_waiting == 0:
            sleep(0.5)
            continue

        if ser1.in_waiting > 0:
            readPort(ser1, '>')
        else:
            readPort(ser2, '<')


if __name__ == '__main__':
    sniffSerial()
