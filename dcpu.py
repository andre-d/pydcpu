# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


class DCPU_OpCodes:
    """
        Defines the opcode contstants from the dcpu spec
    """
    
    NOP = 0  
    RES = 0  # -RESERVED- (This implementation treats as NOP)
    SET = 1  # Sets value of b to a
    ADD = 2  # Adds b to a, sets O
    SUB = 3  # Subtracts b from a, sets O
    MUL = 4  # Multiplies a by b, sets O
    DIV = 5  # Divides a by b, sets O
    MOD = 6  # Remainder of a over b
    SHL = 7  # Shifts a left b places, sets O
    SHR = 8  # Shifts a right b places, sets O
    AND = 9  # Binary and of a and b
    BOR = 10 # Binary or of a and b
    XOR = 11 # Binary xor of a and b
    IFE = 12 # Skips one instruction if a!=b
    IFN = 13 # Skips one instruction if a==b
    IFG = 14 # Skips one instruction if a<=b
    IFB = 15 # Skips one instruction if (a&b)==0

class DCPU_Values:
    """
        Defines various constants from the dcpu spec
    """
    
    # Various Value Codes (Parenthesis = memory lookup of value)
    REG = range(0,8)                   # Register value - register values
    REG_MEM = range(8,16)              # (Register value) - value at address in registries
    MEM_OFFSET_REG = range(16,24)      # (Next word of ram + register value) - memory address offset by register value
    POP = 24                           # Value at stack address, then increases stack counter
    PEEK = 25                          # Value at stack address
    PUSH = 26                          # Decreases stack address, then value at stack address
    SP = 27                            # Current stack pointer value - current stack address
    PC = 28                            # Program counter - current program counter
    O = 29                             # Overflow - current value of the overflow
    MEM = 30                           # (Next word of ram) - memory address
    MEM_LIT = 31                       # Next word of ram - literal, does nothing on assign
    NUM_LIT = range(32,64)             # Literal value 0-31 - literal, does nothing on assign
    
    
    # opcodes------|bbbbbbaaaaaaoooo
    _OP_PORTION = 0b0000000000001111
    _AV_PORTION = 0b0000001111110000
    _BV_PORTION = 0b1111110000000000
    # Bit positions for the above
    _OP_POSITION = 0
    _AV_POSITION = 4
    _BV_POSITION = 10
    
    
    # 8 registers (A, B, C, X, Y, Z, I, J)
    _NUM_REGISTERS = 8 
    
    REGISTER_NAMES = ['SP', 'PC', 'O']
    SPECIAL_REGISTERS = list(REGISTER_NAMES)
    REGISTER_NAMES += [chr(ord('A') + i) for i in range(_NUM_REGISTERS)]
    
    # All values are 16 bit unsigned
    _MAX_VAL = 0xFFFF

