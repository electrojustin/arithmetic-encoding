from arithmetic_encoder import ArithmeticEncoder
from header import generate_header
import sys

# Implement an arithmetic encoder that assumes that bytes are distributed
# independently and randomly.

input_bytes = []
with open(sys.argv[1], 'rb') as input_file:
  input_bytes = input_file.read()

probs = []
for i in range(0, 256):
  probs.append(0)

ae = ArithmeticEncoder()

for byte in input_bytes:
  ae.EncodeSymbol(byte, probs)

  probs[byte] += 1

ae.EncodeSymbol(255, probs)

with open(sys.argv[2], 'wb') as output_file:
  data = generate_header(len(input_bytes))
  data = data + ae.Flush()
  output_file.write(bytearray(data))
