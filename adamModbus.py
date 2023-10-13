"""
adamModbus

Series of python drivers for ModBus Communication with Advantech ADAM Data Acquisition Modules.
- More Robust and Simple operation than ASCII commands and websockets.
- Simple


See the following classes for specific ADAM controllers:

ADAM-6052 (8DI, 8DO): adam6052ModBus.py
ADAM-6217 (8AI):      adam6052ModBus.py
ADAM-6018+ (8TC):     adam6018ModBus.py


# READ THE DOCS!
https://pypi.org/project/pyModbusTCP/
https://control.com/forums/threads/reading-di-do-status-of-adam-6050.27164/
In directory: adam-user-manuals:
- ADAM-6000_User_Manaul_Ed.12-FINAL.pdf
- ADAM-6200_User_Manual_Ed.5_FINAL.pdf

Example ModBus commands (ADAM-6052 docs)
Example: Force Coil 3 (Address 00003) to ON in an ADAM-6000 module.
01 05 00 03 FF 00

Example: Force Coil DO 0 (Address 00017 (0x11)) to ON in an ADAM-6000 module.
01 05 00 11 FF 00

"""

## Init
from pyModbusTCP.client import ModbusClient
import time

import adam6052ModBus as adamDIO
import adam6217ModBus as adamAI
import adam6018ModBus as adamTC


# Ethernet Delarations
ADAM_6052_IP = "192.168.1.111"
ADAM_6217_IP = "192.168.1.112"
ADAM_6018_IP = "192.168.1.113"


#PORT = 1025    #1024-1029 valid for http
PORT = 502


'''
adam6024 Controller - 12UIO - ModBus

Advantech ADAM 6052 Data Acquisition Module - Universal IO - driver

- 6 Analog Inputs (-10/+10v, 0-20mA)
- 2 Analog Outputs (0-10vDC, 0-20mA)
- 2 Digital Input (Dry Contact, Wet Contact (0-30v)
- 2 Digital Output (Close/Open Contact, 10-30vDC)


# READ THE DOCS!
https://pypi.org/project/pyModbusTCP/
In directory: adam-user-manuals:
- ADAM-6000_User_Manaul_Ed.12-FINAL.pdf
- ADAM-6200_User_Manual_Ed.5_FINAL.pdf
'''




class adam6024ModBus:
    def __init__(self, adam_ip, port = 502):
        print(f'Initializing adam6024 8-DI 8-DO Universal IO ModBus...')
        self._IP = adam_ip
        self.port = port
        self.DO_list = [0x10,0x11,0x12,0x13,0x14,0x15,0x16,0x17]  #DO_0 to DO_7
        self.DO_state = [0,0,0,0,0,0,0,0]   # Dont rely too much on this untill checking added
        self.DI_list = [0x00,0x01,0x02,0x03,0x04,0x05,0x06,0x07]
        self.DI_state = [0,0,0,0,0,0,0,0]
        # Create a Modbus TCP client
        # Module init (TCP always open)
        self.adam6052 = ModbusClient(host=self._IP, port=self.port, unit_id=1, auto_open=True)


    def set_coil(self, DO_number, state):
        no_error = self.adam6052.write_single_coil(self.DO_list[DO_number], state)
        self.DO_state[DO_number] = state
        time.sleep(0.5)
        if (no_error):
            print(f"adam6052: coil DO_{DO_number}: Written to {state}")
            return 0   # return false if complete
        else:
            print(f"adam6052: coil DO_{DO_number}: Unable to write to {state}")
            return 1  # error code can be returned here

    def set_all_coils(self, states):
        no_error = (self.adam6052.write_multiple_coils(self.DO_list[0], states))
        self.DO_state = states
        time.sleep(0.5)
        if (no_error):
            print(f"adam6052: all coils: Written to {states}")
            return 0  # return false if complete
        else:
            print(f"adam6052: all coils: Unable to write to {states}")
            return 1  # error code can be returned here


    def get_input(self, DI_number):
        #print(f"adam6052: Reading Input DI_{DI_number}")
        inputs_list = self.adam6052.read_discrete_inputs(DI_number, 1)
        inputs_list = [int(val) for val in inputs_list]   ## turn bool list into int list
        if inputs_list:
            print(f"DI_{DI_number}: {inputs_list}")
            return inputs_list
        else:
            print("Unable to read inputs :(")
            return "ERROR"

    def get_all_inputs(self):
        #print("adam6052: Reading all Inputs")
        inputs_list = self.adam6052.read_discrete_inputs (0, 8)
        if inputs_list:
            self.DI_state = [int(val) for val in inputs_list]  ## turn bool list into int list
            print(f"DI_0-7: {self.DI_state}")
            return self.DI_state
        else:
            print("Unable to read inputs :(")
            return "ERROR"






def main():
    print("Starting ADAM Modbus control")
    iteration = 0
    adam6052 = adamDIO.adam6052ModBus(ADAM_6052_IP, PORT)
    adam6217 = adamAI.adam6217ModBus(ADAM_6217_IP, PORT)
    adam6018 = adamTC.adam6018ModBus(ADAM_6018_IP, PORT, tc_type="K")
    while (True):
        print(f"{iteration}:", end="\n")
        adam6018.get_all_inputs()
        adam6052.get_all_inputs()
        #print(f"{iteration}:", end=" ")
        adam6217.get_all_inputs()
        time.sleep(2)
        iteration = iteration + 1


    # adam6052_set_coil(0, True)
    # time.sleep(4)
    # adam6052_set_coil(0, False)
    # time.sleep(4)
    # time.sleep(5)
    # adam6052_set_all_coils(DO_state)
    # time.sleep(4)
    # time.sleep(5)
    # adam6052_set_all_coils([0,0,0,0,0,0,0,0])






if __name__ == "__main__":
    main()


