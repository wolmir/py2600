import sys
import time
import pygame

# pygame.init()
from pygame.locals import *

# Organisation

MEM_SIZE = 8192
STACK_SIZE = 256

# ISA
NOP     = 0x00
LOAD    = 0x01
STORE   = 0x02
INC     = 0x03
INCM    = 0x15
DEC     = 0x04
ADD     = 0x05
SUB     = 0x06
MUL     = 0X07
DIV     = 0X08
PUSH    = 0x09
IFCMPEQ = 0x0A
IFCMPLT = 0x14
CP      = 0x0B
CPIP    = 0x0C
CPINC   = 0x0D
INT     = 0x0E
PUSHA   = 0x0F
BRK     = 0x10
CPV     = 0x11 # Video Buffer ops
CPIPV   = 0x12 # Video Buffer ops
CPINCV  = 0x13 # Video Buffer ops
END     = 0xFF

memory = bytearray(MEM_SIZE)
stack  = bytearray()

# def tty_print():
#     txt = map(lambda x: chr(x), memory[3840:])
#     print ''.join(txt)

it = []
# it.append((0x80, tty_print))


# ///////////////////////////// Graphics Display Config /////////////////////////
WIDTH  = 800
HEIGHT = 800

TIA_WIDTH  = 160
TIA_HEIGHT = 192

GFX_ADDR = 0x1DFF

pal = []
pal.append(0x000000)
pal.append(0x404040)
pal.append(0x6c6c6c)
pal.append(0x909090)
pal.append(0xb0b0b0)
pal.append(0xc8c8c8)
pal.append(0xdcdcdc)
pal.append(0xececec)
pal.append(0x444400)
pal.append(0x646410)
pal.append(0x848424)
pal.append(0xa0a034)
pal.append(0xb8b840)
pal.append(0xd0d050)
pal.append(0xe8e85c)
pal.append(0xfcfc68)
pal.append(0x702800)
pal.append(0x844414)
pal.append(0x985c28)
pal.append(0xac783c)
pal.append(0xbc8c4c)
pal.append(0xcca05c)
pal.append(0xdcb468)
pal.append(0xecc878)
pal.append(0x841800)
pal.append(0x983418)
pal.append(0xac5030)
pal.append(0xc06848)
pal.append(0xd0805c)
pal.append(0xe09470)
pal.append(0xeca880)
pal.append(0xfcbc94)
pal.append(0x880000)
pal.append(0x9c2020)
pal.append(0xb03c3c)
pal.append(0xc05858)
pal.append(0xd07070)
pal.append(0xe08888)
pal.append(0xeca0a0)
pal.append(0xfcb4b4)
pal.append(0x78005c)
pal.append(0x8c2074)
pal.append(0xa03c88)
pal.append(0xb0589c)
pal.append(0xc070b0)
pal.append(0xd084c0)
pal.append(0xdc9cd0)
pal.append(0xecb0e0)
pal.append(0x480078)
pal.append(0x602090)
pal.append(0x783ca4)
pal.append(0x8c58b8)
pal.append(0xa070cc)
pal.append(0xb484dc)
pal.append(0xc49cec)
pal.append(0xd4b0fc)
pal.append(0x140084)
pal.append(0x302098)
pal.append(0x4c3cac)
pal.append(0x6858c0)
pal.append(0x7c70d0)
pal.append(0x9488e0)
pal.append(0xa8a0ec)
pal.append(0xbcb4fc)
pal.append(0x000088)
pal.append(0x1c209c)
pal.append(0x3840b0)
pal.append(0x505cc0)
pal.append(0x6874d0)
pal.append(0x7c8ce0)
pal.append(0x90a4ec)
pal.append(0xa4b8fc)
pal.append(0x00187c)
pal.append(0x1c3890)
pal.append(0x3854a8)
pal.append(0x5070bc)
pal.append(0x6888cc)
pal.append(0x7c9cdc)
pal.append(0x90b4ec)
pal.append(0xa4c8fc)
pal.append(0x002c5c)
pal.append(0x1c4c78)
pal.append(0x386890)
pal.append(0x5084ac)
pal.append(0x689cc0)
pal.append(0x7cb4d4)
pal.append(0x90cce8)
pal.append(0xa4e0fc)
pal.append(0x003c2c)
pal.append(0x1c5c48)
pal.append(0x387c64)
pal.append(0x509c80)
pal.append(0x68b494)
pal.append(0x7cd0ac)
pal.append(0x90e4c0)
pal.append(0xa4fcd4)
pal.append(0x003c00)
pal.append(0x205c20)
pal.append(0x407c40)
pal.append(0x5c9c5c)
pal.append(0x74b474)
pal.append(0x8cd08c)
pal.append(0xa4e4a4)
pal.append(0xb8fcb8)
pal.append(0x143800)
pal.append(0x345c1c)
pal.append(0x507c38)
pal.append(0x6c9850)
pal.append(0x84b468)
pal.append(0x9ccc7c)
pal.append(0xb4e490)
pal.append(0xc8fca4)
pal.append(0x2c3000)
pal.append(0x4c501c)
pal.append(0x687034)
pal.append(0x848c4c)
pal.append(0x9ca864)
pal.append(0xb4c078)
pal.append(0xccd488)
pal.append(0xe0ec9c)
pal.append(0x442800)
pal.append(0x644818)
pal.append(0x846830)
pal.append(0xa08444)
pal.append(0xb89c58)
pal.append(0xd0b46c)
pal.append(0xe8cc7c)
pal.append(0xfce08c)


pygame.init()

screen = None
tia = None
tia_buffer = [[0x00 for _ in range(0, TIA_HEIGHT)] for _ in range(0, TIA_WIDTH)]

def configure_gfx():
    global screen, tia
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Py2600')
    tia = pygame.Surface((TIA_WIDTH, TIA_HEIGHT)).convert()
    print(tia.get_locked())

def blit_array():
    _buffer = pygame.surfarray.array2d(tia)
    _buffer[:] = tia_buffer[:]
    pygame.surfarray.blit_array(tia, _buffer)

def gfx_blit():
    global tia
    blit_array()
    # pygame.surfarray.blit_array(tia, tia_buffer)
    # blit_array()
    screen.blit(pygame.transform.scale(tia, (WIDTH, HEIGHT)), (0,0))
    pygame.display.update()
    # for i in range(TIA_HEIGHT):
    #     tia_buffer[i][:] = map(lambda x: pal[x], memory[GFX_ADDR:])

it.append((0x42, gfx_blit))

# ///////////////////////////// End of Graphics Display Config /////////////////////////

debug_msg = False

def print_stack():
    print('->'.join(stack))
    print('')

def run():
    ip = 0
    print("running")
    while memory[ip] != END:
        # print ip
        op = memory[ip]
        if op == PUSH:
            if debug_msg:
                print('push: ' + hex(memory[ip + 1]) + ' (' + str(memory[ip + 1]) + ')')
            stack.append(memory[ip + 1])
            ip += 1
        elif op == PUSHA:
            if debug_msg:
                print('push_addr: ' + hex((memory[ip + 2] << 8) | memory[ip + 1]) + ' (' + str((memory[ip + 2] << 8) | memory[ip + 1]) + ')')
            stack.append(memory[ip + 1])
            stack.append(memory[ip + 2])
            ip += 2
        elif op == LOAD:
            addr = (stack.pop() << 8) | stack.pop()
            stack.append(memory[addr])
            if debug_msg:
                print('load ' + str(memory[addr]) + ' from ' + hex(addr) + '(' + str(addr) + ')')
        elif op == STORE:
            addr = (stack.pop() << 8) | stack.pop()
            value = stack.pop()
            memory[addr] = value
            if debug_msg:
                print('store ' + hex(value) + ' (' + str(value) + ') -> ' + hex(addr) + '(' + str(addr) + ')')
        elif op == INC:
            stack[-1] = min(0xFF, stack[-1] + 1)
        elif op == INCM:
            addr = (stack[-1] << 8) | stack[-2]
            memory[addr] = min(0xFF, memory[addr] + 1)
            if debug_msg:
                print('incm at ' + hex(addr) + ' to ' + str(memory[addr]))
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
                ip = ((memory[ip + 1] << 8) | memory[ip + 2])
            else:
                ip += 2
        elif op == IFCMPLT:
            v1 = stack.pop()
            v2 = stack.pop()
            if v2 < v1:
                if debug_msg:
                    print('ifcmplt ' + str(v2) + ' < ' + str(v1))
                ip = max((memory[ip + 2] << 8) | memory[ip + 1], 0)
                ip -= 1
                if debug_msg:
                    print('\tjump to ' + hex(ip) + ' (' + str(ip) + ')')
            else:
                if debug_msg:
                    print('ifcmplt ' + str(v2) + ' >= ' + str(v1))
                ip += 2

        elif op == CP:
            src = (stack.pop() << 8) | stack.pop()
            dest = (stack.pop() << 8) | stack.pop()
            if debug_msg:
                print('copy: ' + str(src) + ' -> ' + str(dest))
                print('copy: ' + str(memory[src]) + ' -> ' + str(memory[dest]))
                print(memory[src - 1])
            memory[dest] = memory[src]
        elif op == CPIP:
            src = (stack[-1] << 8) | stack[-2]
            dest = (stack[-3] << 8) | stack[-4]
            memory[dest] = memory[src]
        elif op == CPINC:
            src  = (stack.pop() << 8) | stack.pop()
            dest = (stack.pop() << 8) | stack.pop()
            if debug_msg:
                print('copy_inc: ' + str(src) + ' -> ' + str(dest))
                print('copy_inc: ' + str(memory[src]) + ' -> ' + str(memory[dest]))
            memory[dest] = memory[src]
            src  += 1
            dest += 1
            stack.append(dest & 0x00FF)
            stack.append((dest & 0xFF00) >> 8)
            stack.append(src & 0x00FF)
            stack.append(src & 0xFF00)

        elif op == CPV:
            src = (stack.pop() << 8) | stack.pop()
            destx = stack.pop()
            desty = stack.pop()
            if debug_msg:
                print('copyv: ' + str(src) + ' -> ' + str((destx, desty)))
                # print 'copyv: ' + str(memory[src]) + ' -> ' + str(memory[dest])
                print(memory[src - 1])
            tia_buffer[destx][desty] = pal[memory[src]]
        elif op == CPIPV:
            src = (stack[-1] << 8) | stack[-2]
            destx = stack[-3]
            desty = stack[-4]
            tia_buffer[destx][desty] = pal[memory[src]]
        elif op == CPINCV:
            src  = (stack.pop() << 8) | stack.pop()
            destx = stack.pop()
            desty = stack.pop()
            if debug_msg:
                print('copy_incv: ' + hex(src) + '(' + hex(pal[memory[src]]) + ')' + ' -> ' + str((destx, desty)))
                # print 'copy_inc: ' + str(memory[src]) + ' -> ' + str(memory[dest])
            tia_buffer[destx][desty] = pal[memory[src]]
            src  += 1
            destx += 1
            if destx >= 160:
                destx = 0
                desty += 1
            stack.append(desty)
            stack.append(destx)
            stack.append(src & 0x00FF)
            stack.append(src & 0xFF00)

        elif op == INT:
            ic = memory[ip + 1]
            if debug_msg:
                print('interrupt: ' + str(ic))
            cb = None
            for ih in it:
                if ih[0] == ic:
                    cb = ih[1]
            if cb:
                cb()
            ip += 1
        elif op == NOP:
            if debug_msg:
                print('nop')

        ip += 1
        if debug_msg:
            print('\nStack:')
            for e in reversed(stack):
                print(hex(e) + ' == ' + str(e))
            print('---------------')
            input()

    print("done")
    # if debug_msg:
    #     print_stack()



if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: py2600 rom_file")
        sys.exit()

    with open(sys.argv[1], 'rb') as rom_file:
        program = bytearray(rom_file.read(MEM_SIZE))
        memory[0:len(program)] = program
        configure_gfx()
        run()
        input()

