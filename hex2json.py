from SpiCmdTestInput import SpiCmdTestInput
import sys
import os

in_filename = sys.argv[1]
print("Input file: " + in_filename)
out_filename = os.path.splitext(sys.argv[1])[0] + ".json"
print("Output file: " + out_filename)

input = SpiCmdTestInput()
input.from_hex(in_filename, 0xE8001)
input.to_json(out_filename)