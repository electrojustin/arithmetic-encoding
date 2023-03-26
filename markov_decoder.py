from arithmetic_decoder import ArithmeticDecoder
from bit_utils import bits_to_bytes, bytes_to_bits
from header import parse_header
import sys

# Implement an arithmetic decoder that assumes that the probability of the next
# byte is influenced by the previous byte, like a Markov chain. This has good
# performance for some data, like English text files.

input_bytes = []
with open(sys.argv[1], 'rb') as input_file:
  input_bytes = input_file.read()

file_len, input_bytes = parse_header(input_bytes)

probs = []
for i in range(0, 256):
  probs.append([])
  for j in range(0, 256):
    probs[-1].append(0)

ad = ArithmeticDecoder(input_bytes)

prev_byte = 0

output = []
while not ad.IsEOS() and len(output) < file_len:
  byte = ad.DecodeSymbol(probs[prev_byte])

  probs[prev_byte][byte] += 1
  prev_byte = byte

  output.append(byte)

with open(sys.argv[2], 'wb') as output_file:
  output_file.write(bytearray(output))
