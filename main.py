import pygame, sys

# setup fo the basic game needs
pygame.init()
clock = pygame.time.Clock()

# main window settings
screen_width = 1280
screen_height = 960
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('BasePongGame')

# Game elements geometry
ball = pygame.Rect(screen_width/2 - 15, screen_height/2 - 15, 30, 30)
player = pygame.Rect(screen_width - 20, screen_height/2 - 70, 10, 140)
opponent = pygame.Rect(10, screen_height/2 - 70, 10, 140)


# colors
bg_color = pygame.Color('grey12')
ligth_grey = (200, 200, 200)

# server loop
while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      sys.exit()


  # Visualise the elements
  pygame.draw.rect(screen, ligth_grey, player)
  pygame.draw.rect(screen, ligth_grey, opponent)
  pygame.draw.rect(screen, ligth_grey, ball)

  # loop update    
  pygame.display.flip()
  clock.tick(60)
