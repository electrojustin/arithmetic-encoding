def bytes_to_bits(bytestream):
  bits = []
  
  for byte in bytestream:
    for i in range(0, 8):
      bits.append((byte >> (7 - i)) & 0x1)

  return bits

def bits_to_bytes(bitstream):
  bytestream = []
  
  while len(bitstream) % 8:
    bitstream.append(0)

  for i in range(0, len(bitstream), 8):
    byte = 0
    for j in range(0, 8):
      byte <<= 1
      byte |= bitstream[i + j]
    bytestream.append(byte)

  return bytestream
