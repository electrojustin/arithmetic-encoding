from arithmetic_decoder import ArithmeticDecoder
from bit_utils import bits_to_bytes, bytes_to_bits
from header import parse_header
import sys

# Implement an arithmetic decoder that assumes that bytes are distributed
# independently and randomly.

input_bytes = []
with open(sys.argv[1], 'rb') as input_file:
  input_bytes = input_file.read()

file_len, input_bytes = parse_header(input_bytes)

probs = []
for i in range(0, 256):
  probs.append(0)

ad = ArithmeticDecoder(input_bytes)

output = []
while not ad.IsEOS() and len(output) < file_len:
  byte = ad.DecodeSymbol(probs)

  probs[byte] += 1

  output.append(byte)

with open(sys.argv[2], 'wb') as output_file:
  output_file.write(bytearray(output))
