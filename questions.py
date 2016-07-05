import numpy
import pygame
import pygame.locals
import sys
import time

pygame.mixer.pre_init(size=-8, channels=1)
pygame.init()
pygame.mixer.init()

_display_surf = pygame.display.set_mode((100, 100))

def square_wave(freq, amplitude, duration):
	wavelength = int(round(44100/freq))
	sample_length = int((44100 * duration) / wavelength)
	half_wv = wavelength/2
	snd_buf = numpy.array((([amplitude] * half_wv) + ([-amplitude] * half_wv)) * sample_length, dtype=numpy.int8)
	# print (wavelength, sample_length, len(snd_buf))
	return snd_buf


def triangle_wave(freq, amplitude, duration):
	wavelength = int(round(44100/freq))
	inc = (amplitude * 4.0)/wavelength
	acc = -amplitude
	sample_length = int((44100 * duration) / wavelength)
	raw_buf = []
	for i in range(wavelength/2):
		raw_buf.append(int(acc))
		acc += inc
	return numpy.array((raw_buf + raw_buf[::-1]) * sample_length, dtype=numpy.int8)

pulse_a  = pygame.mixer.Channel(0)
pulse_b  = pygame.mixer.Channel(1)
triangle = pygame.mixer.Channel(2)
noise    = pygame.mixer.Channel(3)


a = triangle_wave(6000, 10, 0.5)
for i in range(10, 10000, 5):
	a = numpy.concatenate((a, triangle_wave(i, 100, 0.05)))
sound = pygame.sndarray.make_sound(a)
pulse_a.play(sound)
# time.sleep(2)
# t = triangle_wave(523.25, 10, 1)
# tsound = pygame.sndarray.make_sound(t)
# triangle.play(tsound)

while True:
	for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                sys.exit()