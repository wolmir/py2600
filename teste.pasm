label print_data
0x43
0x72
0x69
0x73
0x74
0x69
0x6E
0x61
0x2C
0x20
0x74
0x65
0x20
0x61
0x6D
0x6F
0x21

PUSH 0x00          ;tty_buffer_addr 0x0F[00]
PUSH 0x0F          ;tty_buffer_addr 0x[0F]00
PUSHA (print_data)
CPINC
CPINC
CPINC
CPINC
CPINC
CPINC
CPINC
CPINC
CPINC
CPINC
CPINC
CPINC
CPINC
CPINC
CPINC
CPINC
CP
INT 0x80
END
[print_data]
