import pygame 
import sys 
import random
import neat

def eval_genomes(genomes, config):
    nets = []
    ge = []
    paddles = []
    balls = []    # -->minden ai sajat labdaval tanuljon
    """
    for -> evoluciok kezelese

    todo:
      - halozatok letrehozasa
      - fitnes kalkulalas
      - kornyezet reremtes minden egyes ai-nak
    """


def ball_animation():
    global ball_speed_x, ball_speed_y, player_score, opponent_score, score_time

    if not score_time:
      ball.x += ball_speed_x
      ball.y += ball_speed_y

    if ball.top <= 0 or ball.bottom >= screen_height:
        ball_speed_y *= -1

    if ball.left <= 0:
      player_score += 1
      score_time = pygame.time.get_ticks()

    if ball.right >= screen_width:
      opponent_score += 1
      score_time = pygame.time.get_ticks()

    if ball.colliderect(player) and ball_speed_x > 0: 
      if abs(ball.right - player.left) < 10:
        ball_speed_x *= -1
      elif abs(ball.bottom - player.top) < 10 and ball_speed_y > 10:
        ball_speed_y *= 1
      elif abs(ball.top - player.bottom) < 10 and ball_speed_y < 0:
        ball_speed_y *= 1        

    if ball.colliderect(opponent) and ball_speed_x < 0:
      if abs(ball.left - opponent.right) < 10:
        ball_speed_x *= -1
      elif abs(ball.bottom - opponent.top) < 10 and ball_speed_y > 10:
        ball_speed_y *= 1
      elif abs(ball.top - opponent.bottom) < 10 and ball_speed_y < 0:
        ball_speed_y *= 1  

def player_animation():
  player.y += player_speed
  if player.top <= 0:
    player.top = 0
  if player.bottom >= screen_height:
    player.bottom = screen_height

def opponent_animation():
  if opponent.top < ball.y:
    opponent.top += opponent_speed
  if opponent.bottom > ball.y:
      opponent.bottom -= opponent_speed
  if opponent.top <= 0:
    opponent.top = 0
  if opponent.bottom >= screen_height:
    opponent.bottom = screen_height

def ball_restart():
    global ball_speed_x, ball_speed_y, score_time

    current_time = pygame.time.get_ticks()
    ball.center = (screen_width / 2, screen_height / 2)

    # Countdown logic --remove for teaching
    if current_time - score_time < 700:
        number_three = game_font.render("3", False, ligth_grey)
        screen.blit(number_three, (screen_width / 2 - 10, screen_height / 2 + 20))
    elif 700 < current_time - score_time < 1400:
        number_two = game_font.render("2", False, ligth_grey)
        screen.blit(number_two, (screen_width / 2 - 10, screen_height / 2 + 20))
    elif 1400 < current_time - score_time < 2100:
        number_one = game_font.render("1", False, ligth_grey)
        screen.blit(number_one, (screen_width / 2 - 10, screen_height / 2 + 20))

    if current_time - score_time > 2100:
        ball_speed_y *= random.choice((1, -1))
        ball_speed_x *= random.choice((1, -1))
        score_time = None

pygame.init()
clock = pygame.time.Clock ()

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

# fizik data
ball_speed_x = 7 * random.choice((1, -1))
ball_speed_y = 7 * random.choice((1, -1))
player_speed = 0
opponent_speed = 7

# text variables
player_score = 0
opponent_score = 0
game_font = pygame.font.Font("freesansbold.ttf", 32)

# time managemant
score_time = True

# game loop
while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      sys.exit()
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_UP:
        player_speed -= 7
      if event.key == pygame.K_DOWN:
        player_speed += 7
    if event.type == pygame.KEYUP:
      if event.key == pygame.K_UP:
        player_speed += 7
      if event.key == pygame.K_DOWN:
        player_speed -= 7

  ball_animation()
  player_animation()
  opponent_animation()

  # Visualise the elements
  screen.fill(bg_color)
  pygame.draw.rect(screen, ligth_grey, player)
  pygame.draw.rect(screen, ligth_grey, opponent)
  pygame.draw.circle(screen, ligth_grey, ball.center, ball.width // 2)
  pygame.draw.aaline(screen, ligth_grey, (screen_width/2,0), (screen_width/2,screen_height))

  if score_time:
    ball_restart()

  player_text = game_font.render(f"{player_score}", False, ligth_grey)
  screen.blit(player_text, (660,20))

  opponent_text = game_font.render(f"{opponent_score}", False, ligth_grey)
  screen.blit(opponent_text, (600,20))

  # loop update    
  pygame.display.flip()
  clock.tick(60)
