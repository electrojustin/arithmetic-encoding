from arithmetic_encoder import ArithmeticEncoder
import sys

# Implement an arithmetic encoder that assumes that bytes are distributed
# independently and randomly.

input_bytes = []
with open(sys.argv[1], 'rb') as input_file:
  input_bytes = input_file.read()

probs = []
for i in range(0, 256):
  probs.append(0)

# Probability normalization logic that makes sure every outcome has at least a
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

ae = ArithmeticEncoder()

for byte in input_bytes:
  normalized_probs = normalize_probs(probs)

  ae.EncodeSymbol(byte, normalized_probs)

  probs[byte] += 1

with open(sys.argv[2], 'wb') as output_file:
  output_file.write(bytearray(ae.Flush()))
