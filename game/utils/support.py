from csv import reader
from os import walk
import pygame


def import_layout(path):
	map_layout = []
	with open(path) as map_object:
		raw_layout = reader(map_object, delimiter=',')
		
		for row in raw_layout:
			map_layout.append(list(row))

		return map_layout


def import_assets(path):
	paths = []
	surfaces = []

	for _, __, images in walk(path):
		for image in images:
			image_path = path + '/' + image
			paths.append(image_path)

	paths.sort()

	for image_path in paths:
		image_surf = pygame.image.load(image_path).convert_alpha()
		surfaces.append(image_surf)

	return surfaces
