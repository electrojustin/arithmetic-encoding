from bit_utils import bytes_to_bits

class ArithmeticDecoder:
  def __init__(self, input_bytes):     
    self.num_bits = 32
    self.max_val = (1 << self.num_bits) - 1

    self.lower_bound = 0
    self.upper_bound = self.max_val
    self.stream_done = False

    self.curr_val = 0
    for i in range(0, self.num_bits, 8):
      self.curr_val <<= 8
      self.curr_val |= input_bytes[int(i/8)]
    self.input_bits = bytes_to_bits(input_bytes[int(self.num_bits/8):])
    self.input_idx = 0


  def UpdateBounds(self, symbol, probs):
    # Move the bounds according to the symbol given and the probability
    # distribution table. This is basically just linear interpolation.
    curr_range = self.upper_bound - self.lower_bound
    self.lower_bound += int(sum(probs[:symbol]) * curr_range)
    self.upper_bound = self.lower_bound + int(probs[symbol] * curr_range)

    if self.curr_val > self.upper_bound or self.curr_val < self.lower_bound:
      print('Error! invalid bounds')
      self.stream_done = True


  def MaybeRenormalize(self):
    while True:
      if self.upper_bound >> (self.num_bits - 1) == self.lower_bound >> (self.num_bits - 1):
        # Shift out the MSB since it's been determined

        # Shift in a 0 into |lower_bound|
        self.lower_bound = (self.lower_bound << 1) & self.max_val

        # Shift in a 1 into |upper_bound|
        self.upper_bound = ((self.upper_bound << 1) | 1) & self.max_val

        # Shift in a 0 into |curr_val|. This is temporary, we will bitwise or
        # it with the next bit in the input stream.
        self.curr_val = (self.curr_val << 1) & self.max_val
      elif self.lower_bound >> (self.num_bits - 2) >= 0b01 and self.upper_bound >> (self.num_bits - 2) < 0b11:
        # We can't determine the MSB, but we need to shift out info so we don't
        # converge lower and upper too close.
        # We know that the second most significant bit must be the opposite of
        # whatever the most bit is. For example, low will be 0x7FFF... and high
        # will be 0x8000...
        # We can use this information to our advantage. We effectively shift
        # the second most significant bit while preserving the most significant
        # bit, and then continue the computation as normal.

        # Shift out second most significant bits. Because of the if statement,
        # we already know that |lower_bound| starts with a 0, and |upper_bound|
        # starts with a 1. So we can mask |lower_bound| with 0x7FF... and
        # bitwise or |upper_bound| with 0x800...1.
        self.lower_bound = (self.lower_bound << 1) & (self.max_val >> 1)
        self.upper_bound = ((self.upper_bound << 1) | ((self.max_val >> 1) + 1) | 1) & self.max_val

        # We don't directly know the second most significant bit of |curr_val|
        # so we use a little trick. We know the second most significant bit
        # of |curr_val| must be the opposite of the most significant bit,
        # because |curr_val| is bounded by |lower_bound| and |upper_bound|
        # based on the core logic of the algorithm. So, we flip the second
        # most significant bit of |curr_val| and shift it into the most
        # significant bit position.
        self.curr_val ^= 1 << (self.num_bits - 2)
        self.curr_val = (self.curr_val << 1) & self.max_val
      else:
        break
      
      # Read in a new bit from the input stream, if we haven't consumed the
      # entire stream already.
      if self.input_idx >= len(self.input_bits):
        self.stream_done = True
        return
      self.curr_val |= self.input_bits[self.input_idx]
      self.input_idx += 1


  def IsEOS(self):
    return self.stream_done      


  def DecodeSymbol(self, probs):
    curr_range = self.upper_bound - self.lower_bound
    symbol = 0
    while self.lower_bound + int(sum(probs[:symbol+1]) * curr_range) <= self.curr_val:
      symbol += 1

    self.UpdateBounds(symbol, probs)
    self.MaybeRenormalize()

    return symbol
