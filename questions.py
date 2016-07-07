import numpy
import pygame
import pygame.locals
import sys
import time
import random

pygame.mixer.pre_init(size=-8, channels=1)
pygame.init()
pygame.mixer.init()

_display_surf = pygame.display.set_mode((100, 100))

def square_wave(freq, amplitude, duration, duty=0.5):
	wavelength = int(round(44100/freq))
	sample_length = int((44100 * duration) / wavelength)
	half_wv = int(wavelength * duty)
	other_half = wavelength - half_wv
	snd_buf = numpy.array((([amplitude] * half_wv) + ([-amplitude] * other_half)) * sample_length, dtype=numpy.int8)
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


def noise_wave(pulse_width, amplitude, duration):
	pattern = []
	for i in range(int((duration*44100)/pulse_width)):
		pattern += [random.choice([-amplitude, amplitude])] * pulse_width
	# pattern = [random.choice([-amplitude, amplitude]) for _ in range(1000)]
	snd_buf = numpy.array(pattern, dtype=numpy.int8)
	return snd_buf

pulse_a  = pygame.mixer.Channel(0)
pulse_b  = pygame.mixer.Channel(1)
triangle = pygame.mixer.Channel(2)
noise    = pygame.mixer.Channel(3)


a = square_wave(441, 10, 0.5)
a2 = square_wave(441, 10, 0.5, 0.25)
a3 = square_wave(441, 10, 0.5, 0.125)
n = noise_wave(1, 100, 0.01)
for i in range(2, 50):
	b = min(i, 25)
	n = numpy.concatenate((n, noise_wave(b, 100, 0.01)))
for i in range(2, 50, 4):
	n = numpy.concatenate((n, noise_wave(i, 100, 0.01)))
sound = pygame.sndarray.make_sound(a)
sound2 = pygame.sndarray.make_sound(a2)
sound3 = pygame.sndarray.make_sound(a3)
sound4 = pygame.sndarray.make_sound(n)
# pulse_a.play(sound)
# time.sleep(2)
# pulse_a.play(sound2)
# time.sleep(2)
# pulse_a.play(sound3)
# time.sleep(2)
noise.play(sound4)
# t = triangle_wave(523.25, 10, 1)
# tsound = pygame.sndarray.make_sound(t)
# triangle.play(tsound)

while True:
	for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                sys.exit()