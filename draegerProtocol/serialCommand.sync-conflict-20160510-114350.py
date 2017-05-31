#!/usr/bin/python
import time
import serial
import signal
import sys
from threading import Thread, Event, current_thread

# Kill threads nicely on interrupt
class ThreadHandler:
    threads = []
    initialized = False

    @staticmethod
    def initialize():
        signal.signal(signal.SIGTERM, ThreadHandler.sig_handler)
        signal.signal(signal.SIGINT, ThreadHandler.sig_handler)
        ThreadHandler.initialized = True

    @staticmethod
    def add_thread(thread):
        if current_thread().name != 'MainThread':
            raise InvalidOperationException("InterruptableThread objects may only be started from the Main thread.")

        if not ThreadHandler.initialized:
            ThreadHandler.initialize()

        ThreadHandler.threads.append(thread)

    @staticmethod
    def sig_handler(signum, frame):
        for thread in ThreadHandler.threads:
            thread.stop()

# Threads which can be killed nicely
class InterruptableThread:
    def __init__(self, target=None, args=None):
        self.stop_requested = Event()
        self.t = Thread(target=target, args=[self]+args) if target else Thread(target=self.run)

    def run(self):
        pass

    def start(self):
        ThreadHandler.add_thread(self)
        self.t.start()

    def stop(self):
        self.stop_requested.set()

    def is_stop_requested(self):
        return self.stop_requested.is_set()

    def join(self):
        try:
            while self.t.is_alive():
                self.t.join(timeout=1)
        except (KeyboardInterrupt, SystemExit):
            self.stop_requested.set()
            self.t.join()

        sys.stdout.write("join completed\n")
        sys.stdout.flush()

def main():
    # Define serial port
    ser = serial.Serial(
            port='/dev/ttyUSB0',
            baudrate=9600)

    # Command codes
    ESC = 0x1B
    ICC = 0x51
    CONFIG_DATA_RESPONSE = 0x4A
    REQUEST_DATA = 0x24
    PAW = 0x00
    Q = 0x01
    V = 0x03
    CHKSUM=(ESC + CONFIG_DATA_RESPONSE + REQUEST_DATA + PAW + Q + V)
    CR=0x0D

    # Command to send
    # Use 'x' instead of 'X' for lowercase output
    COMMAND='{:02X}'.format(ESC)\
            + '{:02X}'.format(CONFIG_DATA_RESPONSE)\
            + '{:02X}'.format(REQUEST_DATA)\
            + '{:02X}'.format(PAW)\
            + '{:02X}'.format(Q)\
            + '{:02X}'.format(V)\
            + '{:02X}'.format(CHKSUM)\
            + '{:02X}'.format(CR)

    # Write command to serial port
    def writeCommand(self, serial, command):
        while(not self.is_stop_requested()):
            print "Sending: ", command
            serial.write(command)
            time.sleep(2)

    # Read serial port
    # Assuming nothing returned between requests
    # may need to add handler if idle char used
    def readSerial(serial):
        msg_array = []
        while(1):
			#print("reading")
            # This will block until a char is received
            char = serial.read(2).encode('utf-8')
            # Case char was start bit
            if char == '01':
                msg_array = []
                msg_array.append(char)
            # Case char was end bit
            elif char == '0D':
                msg_array.append(char)
                print "Received: ", msg_array
            else:
				msg_array.append(char)

			# This may need to be reduced or set to pass
			# if missing parts of received message
            time.sleep(0.01)

    # Connect to serial port
    connected = False
    while not connected:
        ser.flushInput()
        ser.flushOutput()
        connected = True

    # Start threads - Writer in foreground, Reader in background
    writer = InterruptableThread(target=writeCommand, args=[ser,COMMAND])
    reader = Thread(target=readSerial, args=(ser,))
    reader.daemon = True
    writer.start()
    reader.start()

    # Program will run until ctl-c pressed
    while(not writer.is_stop_requested()):
        time.sleep(5)

    # Kill daemon thread and close serial port
    reader.join(0.1)
    ser.close()

if __name__ == '__main__':
    main()
