from arithmetic_decoder import ArithmeticDecoder
from bit_utils import bits_to_bytes, bytes_to_bits
import sys

# Implement an arithmetic decoder that assumes that the probability of the next
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

# Probability normalization logic that makes sure every outcome has a
# 1/65536 chance of happening. I was worried that numbers which are "too small"
# will result in floating point issues.
def normalize_probs(probs):
  ret = probs.copy()
  total = sum(ret)
  if total >= 2**16:
    ret = list(map(lambda x: x*(2**16)/total, ret))
  ret = list(map(lambda x: x if x else 1, ret))
  total = sum(ret)
  ret = list(map(lambda x: x / total, ret))

  return ret

ad = ArithmeticDecoder(input_bytes)

prev_byte = 0

output = []
while not ad.IsEOS():
  normalized_probs = normalize_probs(probs[prev_byte])

  byte = ad.DecodeSymbol(normalized_probs)

  probs[prev_byte][byte] += 1
  prev_byte = byte
  output.append(byte)

with open(sys.argv[2], 'wb') as output_file:
  output_file.write(bytearray(output))
