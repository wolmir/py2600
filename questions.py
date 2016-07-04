import numpy
import pygame
import pygame.locals
import sys

pygame.mixer.pre_init(size=-8, channels=1)
pygame.init()
pygame.mixer.init()

_display_surf = pygame.display.set_mode((100, 100))

def square_wave(freq, amplitude, duration):
	wavelength = int(round(44100/freq))
	sample_length = int((44100 * duration) / wavelength)
	print sample_length
	half_wv = wavelength/2
	return numpy.array((([amplitude] * half_wv) + ([-amplitude] * half_wv)) * sample_length, dtype=numpy.int8)

# a = numpy.zeros(44100, numpy.int8)
# amplitude = 120
# square_cycle = ([amplitude] * 30) + ([-amplitude] * 30)
# for i in range(44100/len(square_cycle)):
# 	a[i*len(square_cycle):(i+1)*len(square_cycle)] = square_cycle
a = square_wave(441, 100, 0.05)
a = numpy.concatenate((a, square_wave(261.63, 100, 0.05)))
sound = pygame.sndarray.make_sound(a)
# sound.play(loops=-1)
sound.play()

while True:
	for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                sys.exit()