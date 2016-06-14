import sys
import py2600

code = ''

with open(sys.argv[1], 'r') as source_file:
    code = source_file.read().strip()

bytecode = bytearray()

program = code.split('\n')
ip = 0
data_segs = False
while ip < len(program):
    if not data_segs:
        segs = program[ip].split(' ')
        if segs[0] == 'PUSH':
            bytecode.append(py2600.PUSH)
            bytecode.append(int(segs[1], 16))

        elif segs[0] == 'ADD':
            bytecode.append(py2600.ADD)

        elif segs[0] == 'INC':
            bytecode.append(py2600.INC)

        elif segs[0] == 'DEC':
            bytecode.append(py2600.DEC)

        elif segs[0] == 'CP':
            bytecode.append(py2600.CP)

        elif segs[0] == 'CPINC':
            bytecode.append(py2600.CPINC)

        elif segs[0] == 'INT':
            bytecode.append(py2600.INT)
            bytecode.append(int(segs[1], 16))

        elif segs[0] == 'END':
            bytecode.append(0xFF)
            data_segs = True
            print 'end of program'

    else:
        bytecode.append(int(program[ip], 16))
        print int(program[ip], 16)
    ip += 1

# bytecode.append(0xff)

with open(sys.argv[1].replace('.asm', '.rom'), 'wb') as rom_file:
    rom_file.write(memoryview(bytecode).tobytes())
