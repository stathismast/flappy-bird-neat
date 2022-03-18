import pygame
import os

def load_img(name):
  return pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', name)))