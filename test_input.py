from SpiCmdTestInput import SpiCmdTestInput

test = SpiCmdTestInput()

test.from_json("test.json")
test.to_hex("test.hex", 0xE8001)
test.from_hex("test.hex", 0xE8001)
test.to_json("test_out.json")
print("end")
