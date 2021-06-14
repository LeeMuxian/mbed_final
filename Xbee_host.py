import serial
import time
import sys,tty,termios

# XBee setting
serdev = '/dev/ttyUSB0'
s = serial.Serial(serdev, 9600, timeout=3)

print('Start Communication, sending RPC')
send = 'start'
s.write("/xbee_start/run\n".encode())
while send!='stop':
    #print('Sent RPC')
    send = s.readline()
    print(send)
    if (send == b'circle'):
        # send to remote
        s.write("/circle/run\n".encode())
    elif (send == b'parking'):
        # send to remote
        s.write("/parking/run 5 5 west\n".encode())


s.close()