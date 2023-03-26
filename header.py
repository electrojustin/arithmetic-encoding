def generate_header(file_len):
  # Magic identifier
  ret = [0x4D, 0x41, 0x4B, 0x34]
  # Big endian file len
  for i in range(0, 32, 8):
    ret.append((file_len >> (24 - i)) & 0xFF)

  return ret

def parse_header(data):
  if data[0] != 0x4D or data[1] != 0x41 or data[2] != 0x4B or data[3] != 0x34:
    print('Invalid file!')
    return None

  file_len = 0
  for i in range(0, 4):
    file_len <<= 8
    file_len |= data[4+i]

  return (file_len, data[8:])
