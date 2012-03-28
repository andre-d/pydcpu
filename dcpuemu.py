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

"""
    An implementation of dcpu spec from Mojang/Notch
    Implements: Spec version 3
    (http://notch.tumblr.com/post/20056289891/start-classified-transmission)
    
    Should run in any version of python 2 or 3
    
    Implementation notes:
        - If a value overflows it will zero any bits past the max value (16bits)
        - RESERVED is treated as NOP (No state change except PC)
        - Values codes which involve "next word of ram" increase the program counter
            (otherwise they are useless and when it goes to exec the next instruction it'd be that data)
            - NOTCH: What does "next word of ram" mean?  I assume you mean program counter.
        - Program counter is increased after instruction has executed
            - NOTCH: If you could clarify when that happens that would be great.
        - Overflow value is 0 when no overflow, 1 when overflow
"""

import array
from dcpu import DCPU_Values, DCPU_OpCodes

class DCPUEmu_Options:
    """
        Options which could possibly be changed as needed
    """
    
    # Size of CPU memory
    _MEMORY_SIZE = 0x10000
    
    # Default value for memory
    _MEM_DEFAULT = 0
    
    # Default value for registers
    _REG_DEFAULT = 0
    
    # Default Program Counter value
    _PC_DEFAULT = 0
    
    # Default Stack Pointer value
    _SP_DEFAULT = 0


class DCPU(DCPU_Values, DCPU_OpCodes, DCPUEmu_Options):
    """
        Implements dcpu version 3
    """
    
    # 16bit unsigned is 'H'
    _MEM_TYPESTR = 'H'
    
    def _buffer(self, size, default, typestr=_MEM_TYPESTR):
        """
            Creates a buffer with a size (of typestr values),
                and a default value
        """
        return array.array(typestr, [default] * size)
    
    def _init_cpu(self, size, num_registers):
        """
            Inits memory, registers, program counter, stack pointer,
                and overflow flag
        """
        self.memory = self._buffer(size, self._MEM_DEFAULT)
        self.registers = [self._REG_DEFAULT] * self._NUM_REGISTERS
        self.pc = self._PC_DEFAULT
        self.sp = self._SP_DEFAULT
        self.o = False
    
    def _has_overflown(self, val):
        """
            Checks to see if a number is within the constraints of 
                an unsigned 16bit (or _MAX_VAL) value.
        """
        return (val < 0 or val > self._MAX_VAL)
    
    def _overflown(self, val, setO=True):
        """
            Set the overflow flag if val is or is not overflown and setO is True
                Returns val modified to reflect a value within a valid range
        """
        self.o = self._has_overflown(val)
        return val & self._MAX_VAL
    
    def _tick(self, op, a, b):
        """
            Handle opcodes with an a and b value.
            
            Returns None if no modifcation should be made to a
            Otherwise, returns an int which should be stored in a
        """
        if op == self.NOP:
            return
        elif op == self.SET:
            b = a
        elif op == self.ADD:
            a += b
        elif op == self.SUB:
            a -= b
        elif op == self.MUL:
            a *= b
        elif op == self.DIV:
            a /= b
        elif op == self.MOD:
            a %= b
        elif op == self.SHL:
            a <<= b
        elif op == self.SHR:
            a >>= b
        else:
            if op == self.AND:
                a &= b
            elif op == self.BOR:
                a |= b
            elif op == self.XOR:
                a ^= b
            else:
                if op == self.IFE:
                    if a != b:
                        self._incPC()
                elif op == IFN:
                    if a == b:
                        self._incPC()
                elif op == IFG:
                    if a <= b:
                        self._incPC()
                elif op == IFB:
                    if not (a or b):
                        self._incPC()
                else:
                    self._abort("UNKNOWN OPCODE %d" % op)
                return
            return a
        return self._overflown(a, setO=True)
    
    def _abort(self, message):
        print(self.__dict__)
        raise Exception(message)
    
    def _setval(self, vc, f=None):
        """
            Given a value code, store f in the associated location
                If f is None, returns the value at the location and sets nothing
                If f is not None, the return value is undefined
        """
        
        if vc in self.REG:
            # The value of a register
            if f is None:
                return self.registers[vc]
            else:
                self.registers[vc] = f
        elif vc in self.REG_MEM:
            # The value of memory addressed at a register
            vc -= self.REG_MEM[0]
            if f is None:
                return self.memory[self.registers[reg]]
            else:
                self.memory[self.registers[reg]] = f
        elif vc in self.MEM_OFFSET_REG:
            # The value of memory at an offset+value at a register
            vc -= self.MEM_OFFSET_REG[0]
            self._incPC()
            next_mem = self.memory[self.pc]
            reg = self.registers[vc]
            vc = self._overflown(reg + next_mem)
            if f is None:
                return self.memory[vc]
            else:
                self.memory[vc] = f
        elif vc == self.POP:
            # The value at the stack (and pop)
            if f is None:
                vc = self.memory[self.sp]
            else:
                self.memory[self.sp] = f
            self._incSP()
            return vc
        elif vc == self.PEEK:
            # The value at the stack
            if f is None:
                return self.memory[self.sp]
            else:
                self.memory[self.sp] = f
        elif vc == self.PUSH:
            # The value at the stack (and push)
            self._decSP()
            if f is None:
                return self.memory[self.sp]
            else:
                self.memory[self.sp] = f
        elif vc == self.SP:
            # The value of the stack pointer
            if f is None:
                return self.sp
            else:
                self.sp = f
        elif vc == self.PC:
            # The value of the program counter
            if f is None:
                return self.pc
            else:
                self.pc = f
        elif vc == self.O:
            # The value of the overflow 
            if f is None:
                return int(self.o)
            else:
                self.o = bool(f)
        elif vc == self.MEM:
            # The value of the memoery at the address stored in the memory at PC+1
            self._incPC()
            vc = self.memory[self.pc]
            if f is None:
                return self.memory[vc]
            else:
                self.memory[vc] = f
        elif vc == self.MEM_LIT:
            # The value stored memory at PC+1
            if f is not None:
                return
            self._incPC()
            return self.memory[self.pc]
        elif vc in NUM_LIT:
            # A single value (0-31)
            if f is not None:
                return
            return vc - NUM_LIT[0]
        else:
            self._abort("UNKNOWN VALUE CODE %d" % vc)
    
    def _getval(self, vc):
        """
            Returns a value from an associated location based on a value code
        """
        return self._setval(vc, None)
    
    def _incPC(self):
        """
            Increases and overflows the program counter
        """
        self.pc = self._overflown(self.pc+1)
    
    def _incSP(self):
        """
            Increases and overflows the stack pointer
        """
        self.sp = self._overflown(self.sp+1)
    
    def _decSP(self):
        """
            Decreases and overflows the stack pointer
        """
        self.sp = self._overflown(self.sp-1)
    
    def tick(self):
        """
            Tick the CPU ahead one instruction 
        """
        # Get the current instruction from memory at the program counter
        v = int(self.memory[self.pc])
        # Isolate the opcode
        op = v & self._OP_PORTION
        # Isolate the A value portion
        a = v & self._AV_PORTION
        # Isolate the B value portion
        b = v & self._BV_PORTION
        # Get the actual value of A
        aval = self._getval(a)
        # Get the actual value of B
        bval = self._getval(b)
        # Tick the cpu with those values and opcode
        fval = self._tick(op, aval, bval)
        # If the value of a should be modified
        if fval is not None:
            fval = self._overflown(int(fval), setO=True)
            self._setval(a, fval)
        # Increase the program counter
        self._incPC()
    
    def __init__(self):
        """
            Inits cpu registers and memory
        """
        self._init_cpu(self._MEMORY_SIZE, self._NUM_REGISTERS)

if __name__ == "__main__":
    import time
    _CPU_MHZ = 100
    cpus = [DCPU() for i in range(500)]
    i = 0
    time_total = 0.0
    while(True):
        start = time.time()
        for d in cpus:
            d.tick()
        dt = time.time() - start
        time_total += dt
        t = (1.0/float(_CPU_MHZ)) - dt
        i += 1
        if not i % 100:
            print("Took %fseconds total, with an average of %fseconds" % (time_total, time_total/i))
            i = 0
            time_total = 0
        if t >= 0.001:
            time.sleep(t)
