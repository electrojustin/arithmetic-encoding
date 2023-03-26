from bit_utils import bits_to_bytes

class ArithmeticEncoder:
  def __init__(self):
    self.num_bits = 32
    self.max_val = (1 << self.num_bits) - 1

    self.output_bits = []
    self.lower_bound = 0
    self.upper_bound = self.max_val
    self.pending = 0

  def OutputBitPlusPending(self, bit):
    self.output_bits.append(bit)
    while self.pending:
      self.output_bits.append(not bit)
      self.pending -= 1


  def UpdateBounds(self, symbol, probs):
    # Move the bounds according to the symbol given and the probability
    # distribution table. This is basically just linear interpolation.
    curr_range = self.upper_bound - self.lower_bound
    self.lower_bound += int(sum(probs[:symbol]) * curr_range)
    self.upper_bound = self.lower_bound + int(probs[symbol] * curr_range)


  def MaybeRenormalize(self):
    while True:
      if self.upper_bound >> (self.num_bits - 1) == self.lower_bound >> (self.num_bits - 1):
        # Shift out the MSB since it's been determined
        self.OutputBitPlusPending(self.lower_bound >> (self.num_bits - 1))

        # Shift in a 0 into |lower_bound|
        self.lower_bound = (self.lower_bound << 1) & self.max_val

        # Shift in a 1 into |upper_bound|
        self.upper_bound = ((self.upper_bound << 1) | 1) & self.max_val
      elif self.lower_bound >> (self.num_bits - 2) >= 0b01 and self.upper_bound >> (self.num_bits - 2) < 0b11:
        # We can't determine the MSB, but we need to shift out info so we don't
        # converge lower and upper too close.
        # We know that the second most significant bit must be the opposite of
        # whatever the most bit is. For example, low will be 0x7FFF... and high
        # will be 0x8000...
        # We can use this information to our advantage. We effectively shift
        # the second most significant bit while preserving the most significant
        # bit, and we increment the variable |pending|. Once we figure out what
        # the most significant bit is through normal bounds updates, we write
        # it out, and then write its complement out as many times as |pending|
        # tells us to. See the OutputBitPlusPending function.
 
        # Increment |pending|.
        self.pending += 1

        # Shift out second most significant bits. Because of the if statement,
        # we already know that |lower_bound| starts with a 0, and |upper_bound|
        # starts with a 1. So we can mask |lower_bound| with 0x7FF... and
        # bitwise or |upper_bound| with 0x800...1.
        self.lower_bound = (self.lower_bound << 1) & (self.max_val >> 1)
        self.upper_bound = ((self.upper_bound << 1) | ((self.max_val >> 1) + 1) | 1) & self.max_val
      else:
        break
   
     
  def EncodeSymbol(self, symbol, probs):
    self.UpdateBounds(symbol, probs)
    self.MaybeRenormalize()

  def Flush(self):
    ret = bits_to_bytes(self.output_bits)
    self.output_bits = []
    self.lower_bound = 0
    self.upper_bound = self.max_val

    return ret
