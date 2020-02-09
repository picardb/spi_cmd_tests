import json
from intelhex import IntelHex


class SpiCmdTestInput:

    def __init__(self, filename = ""):
        self.__cycles_number = 1
        self.__commands = {}
        self.__CMD_ID = {
            "StartApplication": 0x10,
            "GotoSleep": 0x11,
            "StartAdvertising": 0x12
        }
        self.__RSP_ID = {
            "StartApplicationRsp": 0x90,
            "StartAdvertisingRsp": 0x92,
            "UnavailableCmd": 0xFF
        }

    def __str__(self):
        return "CyclesNumber = " + str(self.__cycles_number)

    def __cmd_to_hex(self, cmd, intel_hex, address):
        # Command data
        cmd_name = cmd.get("cmd_name")
        cmd_id = self.__CMD_ID.get(cmd_name)
        if cmd_id is None:
            cmd_id = int(cmd_name, 16)
        cmd_payload = cmd.get("cmd_payload")
        if cmd_payload is not None:
            cmd_len = len(cmd_payload)
        else:
            cmd_len = 0

        # Expected response data
        expected_rsp = cmd.get("expected_rsp")
        if expected_rsp:
            rsp_name = cmd.get("rsp_name")
            rsp_id = self.__RSP_ID.get(rsp_name)
            if rsp_id is None:
                rsp_id = int(rsp_name, 16)
            rsp_payload = cmd.get("rsp_payload")
            if rsp_payload is not None:
                rsp_len = len(rsp_payload)
            else:
                rsp_len = 0
        else:
            rsp_len = 0

        # Write command to HEX
        intel_hex[address] = cmd_id                 # ID
        intel_hex[address + 1] = cmd_len            # Length
        address += 2
        if cmd_payload is not None:
            for byte in cmd_payload:                # Payload
                intel_hex[address] = int(byte, 16)
                address += 1
        for i in range(0, 116 - cmd_len):           # Padding
            intel_hex[address] = 0xFF
            address += 1

        # Write expected response to hex
        if expected_rsp:
            intel_hex[address] = 1                  # Expected
            intel_hex[address + 1] = rsp_id         # ID
            intel_hex[address + 2] = rsp_len        # Length
            address += 2
            if rsp_payload is not None:
                for byte in rsp_payload:            # Payload
                    intel_hex[address] = int(byte, 16)
                    address += 1
        else:
            intel_hex[address] = 0                  # Expected
            intel_hex[address + 1] = 0xFF           # ID
            intel_hex[address + 2] = 0xFF           # Length
            address += 3
        for i in range(0, 119 - rsp_len):           # Padding
            intel_hex[address] = 0xFF
            address += 1

        return address

    def from_json(self, filename):
        with open(filename, "r") as in_file:
            in_data = json.load(in_file)
            self.__cycles_number = in_data.get("cycles_number", 1)
            self.__commands = in_data.get("commands")

    def to_hex(self, filename, offset):
        ih = IntelHex()

        # Cycles and command numbers
        ih[offset] = self.__cycles_number // 256
        ih[offset + 1] = self.__cycles_number % 256
        ih[offset + 2] = self.cmd_number()
        offset += 3

        # Commands
        for cmd in self.__commands:
            offset = self.__cmd_to_hex(cmd, ih, offset)

        ih.write_hex_file(filename)

    def cmd_number(self):
        return len(self.__commands)
