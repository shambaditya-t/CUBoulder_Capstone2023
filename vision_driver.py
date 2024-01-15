"""
This is a driver script to run a CLI which will allow us to test the integration
of the vision system and the moving gantry.
"""

import io
import serial
from serial.tools import list_ports


class Gantry():
    def __init__(self, serial_port: serial.Serial):
        self.s = io.TextIOWrapper(io.BufferedRWPair(serial_port, serial_port))

    def write_cmd(self, cmd: str):
        self.s.write(f'{cmd}\n')

    def home(self, axis='all'):
        if axis == 'all':
            self.write_cmd('home all')
        elif axis == 'x':
            self.write_cmd('home x')
        elif axis == 'y':
            self.write_cmd('home y')
        elif axis == 'z':
            self.write_cmd('home z')
        else:
            raise ValueError('Invalid axis')
        print(self.s.readline())


if __name__ == "__main__":
    # Initialize the COM port
    print("Please choose a COM port from the following list (e.g. COM6)")
    print('\n'.join([', '.join([d.name, d.manufacturer or '', d.product or '']) for d in list_ports.comports()]))
    # print(list_ports.join(', '))
    gantry = None
    while True:
        try:
            print('> ', end='')
            com = input()
            ser = serial.Serial(com)
            gantry = Gantry(ser)
            break
        except serial.SerialException:
            print("Invalid selection")
            continue

    # run a repl cli
    while True:
        print('> ', end='')
        cmd = input()
        cmd = cmd.lower()

        if "exit" == cmd:
            exit(0)
        elif "help" == cmd:
            print("home, vision, exit")
        elif "home" == cmd:
            print("TODO: home")
            gantry.write_cmd("home all")
        elif "vision" == cmd:
            print("TODO: vision")
            gantry.write_cmd("testing 1234")
        else:
            print("Invalid Command. Type 'help' for a list of available commands.")
