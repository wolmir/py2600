import sys
import pygame

from pygame.locals import *

# Organisation

MEM_SIZE = 4096
STACK_SIZE = 256

# ISA
LOAD    = 0x01
STORE   = 0x02
INC     = 0x03
DEC     = 0x04
ADD     = 0x05
SUB     = 0x06
MUL     = 0X07
DIV     = 0X08
PUSH    = 0x09
IFCMPEQ = 0x0A
CP      = 0x0B
CPIP    = 0x0C
CPINC   = 0x0D
INT     = 0x0E
PUSHA   = 0x0F
BRK     = 0x10
END     = 0xFF

memory = bytearray(MEM_SIZE)
stack  = bytearray()

def tty_print():
    txt = map(lambda x: chr(x), memory[3840:])
    print ''.join(txt)

it = []
it.append((0x80, tty_print))

debug_msg = False

def run():
    ip = 0
    while memory[ip] != END:
        if debug_msg:
            for e in stack:
                print e
            print '---------------'
        op = memory[ip]
        if op == PUSH:
            if debug_msg:
                print 'push: ' + str(memory[ip + 1])
            stack.append(memory[ip + 1])
            ip += 1
        elif op == PUSHA:
            if debug_msg:
                print 'push_addr: ' + str(memory[ip + 1]) + ' ' + str(memory[ip + 2])
            stack.append(memory[ip + 1])
            stack.append(memory[ip + 2])
            ip += 2
        elif op == LOAD:
            addr = (stack.pop() << n) | stack.pop()
            stack.append(memory[addr])
        elif op == STORE:
            addr = (stack.pop() << n) | stack.pop()
            memory[addr] = stack.pop()
        elif op == INC:
            opr = stack.pop()
            opr += 1
            opr = min(255, opr)
            stack.append(opr)
        elif op == DEC:
            opr = stack.pop()
            opr -= 1
            opr = max(0, opr)
            stack.append(opr)
        elif op == ADD:
            s1 = stack.pop()
            s2 = stack.pop()
            stack.append(min(255, s1 + s2))
        elif op == SUB:
            s1 = stack.pop()
            s2 = stack.pop()
            stack.append(max(0, s1 - s2))
        elif op == MUL:
            m1 = stack.pop()
            m2 = stack.pop()
            stack.append(min(255, m1 * m2))
        elif op == DIV:
            d1 = stack.pop()
            d2 = stack.pop()
            stack.append(m1 / m2)
        elif op == IFCMPEQ:
            if stack.pop() == stack.pop():
                ip += memory[ip + 1]
            else:
                ip += 1
        elif op == CP:
            src = (stack.pop() << 8) | stack.pop()
            dest = (stack.pop() << 8) | stack.pop()
            if debug_msg:
                print 'copy: ' + str(src) + ' -> ' + str(dest)
                print 'copy: ' + str(memory[src]) + ' -> ' + str(memory[dest])
                print memory[src - 1]
            memory[dest] = memory[src]
        elif op == CPIP:
            src = (stack[-1] << 8) | stack[-2]
            dest = (stack[-3] << 8) | stack[-4]
            memory[dest] = memory[src]
        elif op == CPINC:
            src  = (stack.pop() << 8) | stack.pop()
            dest = (stack.pop() << 8) | stack.pop()
            if debug_msg:
                print 'copy_inc: ' + str(src) + ' -> ' + str(dest)
                print 'copy_inc: ' + str(memory[src]) + ' -> ' + str(memory[dest])
            memory[dest] = memory[src]
            src  += 1
            dest += 1
            stack.append(dest & 0x00FF)
            stack.append((dest & 0xFF00) >> 8)
            stack.append(src & 0x00FF)
            stack.append(src & 0xFF00)
        elif op == INT:
            ic = memory[ip + 1]
            if debug_msg:
                print 'interrupt: ' + str(ic)
            cb = None
            for ih in it:
                if ih[0] == ic:
                    cb = ih[1]
            cb()
            ip += 1
        ip += 1

    if debug_msg:
        for e in stack:
            print e
        print ''
        raw_input()


# ///////////////////////////// Graphics Display Config /////////////////////////
WIDTH  = 800
HEIGHT = 800

TIA_WIDTH  = 160
TIA_HEIGHT = 192

pygame.init()

# ///////////////////////////// Graphics Display Config /////////////////////////

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "Usage: py2600 rom_file"
        sys.exit()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Py2600')

    tia = pygame.Surface((TIA_WIDTH, TIA_HEIGHT)).convert()

    with open(sys.argv[1], 'rb') as rom_file:
        program = bytearray(rom_file.read(MEM_SIZE))
        memory[0:len(program)] = program
        run()
