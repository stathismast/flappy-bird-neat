import pygame
import random
from .image_loader import load_img

PIPE_IMG = load_img('pipe.png')

class Pipe:
  VEL = 5
  WIDTH = PIPE_IMG.get_width()

  def __init__(self, x):
    self.x = x
    self.height = 0

    self.top = 0
    self.bottom = 0
    self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True)
    self.PIPE_BOTTOM = PIPE_IMG

    self.set_height()

  def set_height(self):
    self.passed = False
    self.gap = 250 + random.randrange(-30, 50)
    self.height = random.randrange(150, 450)
    self.top = self.height - self.PIPE_TOP.get_height()
    self.bottom = self.height + self.gap

  def move(self):
    self.x -= self.VEL
    if self.x + self.WIDTH < 1:
      self.x = 1100
      self.set_height()

  def draw(self, win):
    win.blit(self.PIPE_TOP, (self.x, self.top))
    win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

  def collide(self, bird):
    bird_mask = bird.get_mask()
    top_mask = pygame.mask.from_surface(self.PIPE_TOP)
    bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

    top_offset = (self.x - bird.x, self.top - round(bird.y))
    bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

    t_point = bird_mask.overlap(top_mask, top_offset)
    b_point = bird_mask.overlap(bottom_mask, bottom_offset)

    if t_point or b_point:
      return True
    return False
