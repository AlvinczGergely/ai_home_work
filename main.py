import pygame 
import sys 
import random
import neat
import os


def train_ai(self, genome1, genome2, copnfig):
  net1 = neat.nn.FeedForwardNetwork.create(genome1, config)
  net2 = neat.nn.FeedForwardNetwork.create(genome2, config)
  
  run = True
  while run: 
    for event in ptgame.event.get():
      if event.type == pygame.QUIT:
        quit()
      
    output1 = net1.activate((self.left_paddle.y, self.ball.y, abs(self.left_paddle.x - self.ball.x)))
    decision1 = output1.index(max(output1))

    if decision1 == 0:
      pass
    elif decision1 == 1:
      self.game.move_paddle(lest=False, up=True)
    else:
      self.game.move_paddle(lest=True, up=False)

    output2 = net1.activate((self.rigth_paddle.y, self.ball.y, abs(self.rigth_paddle.x - self.ball.x)))
    decision2 = output2.index(max(output2))  

    if decision2 == 0:
      pass
    elif decision2 == 1:
      self.game.move_paddle(lest=True, up=True)
    else:
      self.game.move_paddle(lest=False, up=False)


    game_info = self.game.loop()
    self.game.draw()
    pygame.display.update()
    
    if game_info.left_score >= 1 or game_info.rigth_score >=1 or game_info.left_hits > 50:
      self.calculate_fittnes(genome1, genome2, game_info)
      break

def calculate_fittnes(self, genome1, genom2):
  genome1.fitness += game_info.lef_hits
  genome2.fitness += game_info.rigth_hits
    
 
def eval_genomes(genomes, config):
  width, height = 700, 500
  width = pygame.disyplay.set_mode((width, height))
  
  for i, (genome_id1, genome1) in enumerate(genomes):
    if i == len(genomes) - 1:
      break
    genome1.fittnes = 0
    for genome_id2, genome2 in genomes[i+1:]:         #same genome dos not play egainst itself
      genome2.fittness = 0 if genomes2.fittness == None else genome2.fittness
      game = PongGame(window, width, length)
      game.train_ai(genome1, genome2, config)
  
  
  
def run_neat(config):
  p = neat.Population(config)
  p.add_reporter(neat.StdReporter(True))
  status = neat.StatisticsReporter()
  p.add_reporter(status)
  p.add_reporter(neat.Checkpointer(1))
  
  winner = p.run(eval_genomes, 50)

if __name__== "__main__":
  loca_dir = os.path.dirname(__file__)
  config_path = os.path.join(local_dir, "config.txt")
  
  config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)
  run_neat(config)


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

