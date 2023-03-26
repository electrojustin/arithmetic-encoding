from arithmetic_encoder import ArithmeticEncoder
from header import generate_header
import sys

# Implement an arithmetic encoder that assumes that the probability of the next
# byte is influenced by the previous byte, like a Markov chain. This has good
# performance for some data, like English text files.

input_bytes = []
with open(sys.argv[1], 'rb') as input_file:
  input_bytes = input_file.read()

probs = []
for i in range(0, 256):
  probs.append([])
  for j in range(0, 256):
    probs[-1].append(0)

ae = ArithmeticEncoder()

prev_byte = 0

for byte in input_bytes:
  ae.EncodeSymbol(byte, probs[prev_byte])

  probs[prev_byte][byte] += 1
  prev_byte = byte

ae.EncodeSymbol(255, probs[prev_byte])

with open(sys.argv[2], 'wb') as output_file:
  data = generate_header(len(input_bytes))
  data = data + ae.Flush()
  output_file.write(bytearray(data))
