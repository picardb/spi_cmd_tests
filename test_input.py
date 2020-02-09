from SpiCmdTestInput import SpiCmdTestInput

test = SpiCmdTestInput()

test.from_json("test.json")
test.to_hex("test.hex", 0xE8001)

