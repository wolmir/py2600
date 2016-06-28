label game_loop
PUSHA   0x1FFF         ; Gamepad addr
LOAD
PUSH    0x08            ; Right arrow
IFCMPEQ (update_line)

label draw_line
PUSHA   (liney)
LOAD
PUSHA   (linex)
LOAD
PUSHA   (line_color)
CPV
INT     0x42
JMP     (game_loop)

label update_line
PUSHA (linex)
INCM
JMP (draw_line)

label linex
0x00

label liney
0x2A

label line_color
0x0D

[game_loop]
[draw_line]
[update_line]
[linex]
[liney]
[line_color]
