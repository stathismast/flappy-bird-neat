from re import S
from classes import load_img, Bird, Pipe, Base, Background
import pygame
import neat
import os

# bird.y, bird.vel, pipe.y, pipe.top, pipe.bottom

pygame.font.init()

WIN_WIDTH = 576
WIN_HEIGHT = 932
STAT_FONT = pygame.font.SysFont('Helvetica', 50)

score = 0
generation = 0

def draw(win, birds, pipes, base, bg):
  bg.draw(win)
  for pipe in pipes:
    pipe.draw(win)
  base.draw(win)
  for bird in birds:
    bird.draw(win)
  text = STAT_FONT.render('Generation: ' + str(generation), 1, (255,255,255))
  win.blit(text, (10, 10))

  pygame.display.update()

def move(birds, pipes, base, bg, nets, ge):
  bg.move()
  for bird in birds:
    bird.move()
  for pipe in pipes:
    pipe.move()
  base.move()

def check_collisions(birds, pipes, nets, ge):
  for pipe in pipes:
    for i,bird in enumerate(birds):
      if pipe.collide(bird):
        birds.pop(i)
        nets.pop(i)
        ge.pop(i)

def check_oob(birds, nets, ge):
  for i,bird in enumerate(birds):
    if bird.y > WIN_HEIGHT - 200 or bird.y < 0:
      birds.pop(i)
      nets.pop(i)
      ge.pop(i)

def find_closest_pipe(bird, pipes):
  closest = None
  for pipe in pipes:
    if bird.x < pipe.x + 100:
      if closest is None or abs(bird.x - pipe.x) < abs(bird.x - closest.x):
        closest = pipe
  return closest

def get_nn_output(birds, pipes, nets, ge):
  for i,bird in enumerate(birds):
    ge[i].fitness += 0.1
    next = find_closest_pipe(bird, pipes)
    output = nets[i].activate((bird.y, bird.vel, abs(bird.y - next.height), abs(bird.y - next.bottom), abs(bird.x - next.x)))
    if output[0] > 0.5:
      bird.jump()

def initialize_neat(genomes, config):
  birds = []
  nets = []
  ge = []
  for _,g in genomes:
    nets.append(neat.nn.FeedForwardNetwork.create(g, config))
    birds.append(Bird(200,200))
    g.fitness = 0
    ge.append(g)
  return birds, nets, ge

def check_exit():
  for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        quit()

def fitness(genomes, config):
  global generation
  generation += 1
  birds, nets, ge = initialize_neat(genomes, config)

  pipes = [Pipe(600),Pipe(1000),Pipe(1400)]
  base = Base(WIN_HEIGHT - 150)
  bg = Background()
  win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
  clock = pygame.time.Clock()

  while True:
    clock.tick(45)
    check_exit()
    check_collisions(birds, pipes, nets, ge)
    check_oob(birds, nets, ge)
    get_nn_output(birds, pipes, nets, ge)
    move(birds, pipes, base, bg, nets, ge)
    draw(win, birds, pipes, base, bg)
    if len(birds) == 0:
      break

if __name__ == "__main__":
  local_dir = os.path.dirname(__file__)
  config_path = os.path.join(local_dir, 'neat-config.txt')
  config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)

  p = neat.Population(config)
  p.add_reporter(neat.StdOutReporter(True))
  stats = neat.StatisticsReporter()
  p.add_reporter(stats)

  winner = p.run(fitness,50)
  print('\nBest genome:\n{!s}'.format(winner))

# def old_main():
#   bird = Bird(200, 200)
#   pipes = [Pipe(600),Pipe(1000),Pipe(1400)]
#   base = Base(WIN_HEIGHT - 150)
#   bg = Background()
#   win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
#   clock = pygame.time.Clock()

#   run = True
#   while run:
#     clock.tick(45)
#     for event in pygame.event.get():
#       if event.type == pygame.KEYDOWN:
#         bird.jump()
#       if event.type == pygame.QUIT:
#         run = False
#     move(bird, pipes, base, bg)
#     draw(win, bird, pipes, base, bg)

#   pygame.quit()
#   quit()