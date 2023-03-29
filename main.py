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
    responsePort = serial.Serial('/dev/ttyUSB0')
    requestPort = serial.Serial('/dev/ttyUSB1')
    while True:
        responsePort.timeout = None
        requestPort.timeout = None

        if responsePort.in_waiting == 0 and requestPort.in_waiting == 0:
            sleep(0.5)
            continue

        if requestPort.in_waiting > 0:
            readPort(requestPort, '>')
        else:
            readPort(responsePort, '<')


if __name__ == '__main__':
    sniffSerial()
