import pygame
from .image_loader import load_img

BIRD_IMGS = [load_img('bird1.png'),load_img('bird2.png'),load_img('bird3.png')]

class Bird:
  IMGS = BIRD_IMGS
  MAX_ROTATION = 25
  ROT_VEL = 10
  ANIMATION_TIME = 5
  TERMINAL_VEL = 14

  def __init__(self, x, y):
    self.x = x
    self.y = y
    self.tilt = 0
    self.tick_count = 0
    self.vel = 0
    self.height = self.y
    self.img_count = 0
    self.img = self.IMGS[0]

  def jump(self):
    self.vel = -8.5
    self.tick_count = 0
    self.height = self.y

  def move(self):
    self.tick_count += 1

    d = self.vel * self.tick_count + 0.9*self.tick_count**2 #displacement
    if d > self.TERMINAL_VEL:
      d = self.TERMINAL_VEL

    if d < 0:
      d -= 1

    self.y = self.y + d

    if d < 0 or self.y < self.height-50:
      if self.tilt < self.MAX_ROTATION:
        self.tilt = self.MAX_ROTATION
    else:
      if self.tilt > -70:
        self.tilt -= self.ROT_VEL

  def draw(self, win):
    self.img_count += 1

    if self.img_count < self.ANIMATION_TIME:
      self.img = self.IMGS[0]
    elif self.img_count < self.ANIMATION_TIME * 2:
      self.img = self.IMGS[1]
    elif self.img_count < self.ANIMATION_TIME * 3:
      self.img = self.IMGS[2]
    elif self.img_count < self.ANIMATION_TIME * 4:
      self.img = self.IMGS[1]
    else:
      self.img = self.IMGS[0]
      self.img_count = 0

    if self.tilt <= -60:
      self.img = self.IMGS[1]
      self.img_count = self.ANIMATION_TIME * 2

    rotated_image = pygame.transform.rotate(self.img, self.tilt)
    new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft = (self.x, self.y)).center)
    win.blit(rotated_image, new_rect.topleft)

  def get_mask(self):
    return pygame.mask.from_surface(self.img)