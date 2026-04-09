import pygame 
import sys 
import random
import neat
import os


class PongGame:
    def __init__(self, window, width, height):
        self.window = window
        self.width = width
        self.height = height

        self.left_paddle = pygame.Rect(10, height/2 - 70, 10, 140)
        self.right_paddle = pygame.Rect(width - 20, height/2 - 70, 10, 140)
        self.ball = pygame.Rect(width/2 - 15, height/2 - 15, 30, 30)
        
        self.left_score = 0
        self.right_score = 0
        self.left_hits = 0
        self.right_hits = 0

    def move_paddle(self, left=True, up=True):
        if left:
            if up and self.left_paddle.top > 0:
                self.left_paddle.y -= 7
            elif not up and self.left_paddle.bottom < self.height:
                self.left_paddle.y += 7
        else:
            if up and self.right_paddle.top > 0:
                self.right_paddle.y -= 7
            elif not up and self.right_paddle.bottom < self.height:
                self.right_paddle.y += 7

    def loop(self):
        self._move_ball()
        self._handle_collision()
        return self
    
    def _move_ball(self):
        self.ball.x += self.ball_speed_x
        self.ball.y += self.ball_speed_y
        if self.ball.top <= 0 or self.ball.bottom >= self.height:
            self.ball_speed_y *= -1
        if self.ball.left <= 0:
            self.right_score += 1
            self.reset_ball()
        elif self.ball.right >= self.width:
            self.left_score += 1
            self.reset_ball()


    def _handle_collision(self):
        if self.ball.colliderect(self.left_paddle) or self.ball.colliderect(self.right_paddle):
            self.ball_speed_x *= -1
            if self.ball.colliderect(self.left_paddle): self.left_hits += 1
            else: self.right_hits += 1
    
    def reset_ball(self):
        self.ball.center = (self.width/2, self.height/2)
        self.ball_speed_x *= -1

    def draw(self, draw_score=True):
        self.window.fill((30, 30, 30))
        pygame.draw.rect(self.window, (200, 200, 200), self.left_paddle)
        pygame.draw.rect(self.window, (200, 200, 200), self.right_paddle)
        pygame.draw.circle(self.window, (200, 200, 200), self.ball.center, 15)
        pygame.display.update()



def train_ai(genome1, genome2, config, window, width, height):
  net1 = neat.nn.FeedForwardNetwork.create(genome1, config)
  net2 = neat.nn.FeedForwardNetwork.create(genome2, config)
  game = PongGame(window, width, height)
  
  run = True
  while run: 
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        quit()
      
    output1 = net1.activate((game.left_paddle.y, game.ball.y, abs(game.left_paddle.x - game.ball.x)))
    decision1 = output1.index(max(output1))

    if decision1 == 0:
      pass
    elif decision1 == 1:
      game.move_paddle(left=False, up=True)
    else:
      game.move_paddle(left=True, up=False)

    output2 = net1.activate((game.right_paddle.y, game.ball.y, abs(game.right_paddle.x - game.ball.x)))
    decision2 = output2.index(max(output2))  

    if decision2 == 0:
      pass
    elif decision2 == 1:
      game.move_paddle(left=True, up=True)
    else:
      game.move_paddle(left=False, up=False)


    game_info = game.loop()
    game.draw()
    pygame.display.update()
    
    if game_info.left_score >= 1 or game_info.right_score >=1 or game_info.left_hits > 50:
      calculate_fitness(genome1, genome2, game_info)
      break

def calculate_fitness(game_info, genome1, genome2):
  genome1.fitness += game_info.left_hits
  genome2.fitness += game_info.right_hits
    
 
def eval_genomes(genomes, config):
  width, height = 700, 500
  window = pygame.display.set_mode((width, height))
  
  for i, (genome_id1, genome1) in enumerate(genomes):
    if i == len(genomes) - 1:
      break
    genome1.fittnes = 0
    for genome_id2, genome2 in genomes[i+1:]:         #same genome dos not play egainst itself
      genome2.fitness = 0 if genome2.fitness == None else genome2.fitness
      train_ai(genome1, genome2, config, window, width, height)
  
  
  
def run_neat(config):
  p = neat.Population(config)
  p.add_reporter(neat.StdOutReporter(True))
  status = neat.StatisticsReporter()
  p.add_reporter(status)
  p.add_reporter(neat.Checkpointer(1))
  
  winner = p.run(eval_genomes, 50)

if __name__== "__main__":
  local_dir = os.path.dirname(__file__)
  config_path = os.path.join(local_dir, "config.txt")
  
  config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)
  run_neat(config)


