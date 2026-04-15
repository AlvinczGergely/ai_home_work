import pygame 
import sys 
import random
import neat
import os
import matplotlib.pyplot as plt
import pickle


def plot_stats(statistics):
    generation = range(len(statistics.most_fit_genomes))
    best_fitness = [c.fitness for c in statistics.most_fit_genomes]
    avg_fitness = statistics.get_fitness_mean()

    plt.plot(generation, avg_fitness, label="average fitness")
    plt.plot(generation, best_fitness, label="best fitness")
    plt.title("generation learning curve")
    plt.xlabel("generations")
    plt.ylabel("fitness")
    plt.grid()
    plt.legend(loc="best")
    plt.show()

class PongGame:
    def __init__(self, window, width, height):
        self.window = window
        self.width = width
        self.height = height

        self.left_paddle = pygame.Rect(10, height/2 - 70, 10, 140)
        self.right_paddle = pygame.Rect(width - 20, height/2 - 70, 10, 140)
        self.ball = pygame.Rect(width/2 - 15, height/2 - 15, 30, 30)
        
        self.ball_speed_x = 7 * random.choice((1, -1))
        self.ball_speed_y = 7 * random.choice((1, -1))

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
        pygame.draw.rect(self.window, (100, 100, 100), (self.width//2 - 2, 0, 4, self.height))
        pygame.draw.rect(self.window, (200, 200, 200), self.left_paddle)
        pygame.draw.rect(self.window, (200, 200, 200), self.right_paddle)
        pygame.draw.circle(self.window, (200, 200, 200), self.ball.center, 15)
        pygame.display.update()
        
    def test_ai(self, net):
        clock = pygame.time.Clock()
        run = True
        while run:
            clock.tick(60)
            game_info = self.loop()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break

            output = net.activate((self.right_paddle.y, self.ball.y,
              abs(self.right_paddle.x - self.ball.x)))
            decision = output.index(max(output))

            if decision == 1:
                self.move_paddle(left=False, up=True)
            elif decision == 2:
                self.move_paddle(left=False, up=False)

            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                self.move_paddle(left=True, up=True)
            elif keys[pygame.K_s]:
                self.move_paddle(left=True, up=False)

            self.draw(draw_score=True)
            pygame.display.update()



def train_ai(genome, config, window, width, height, difficulty = 1):
  net = neat.nn.FeedForwardNetwork.create(genome, config)
  game = PongGame(window, width, height)
  
  run = True
  while run: 
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        quit()

    srinking_paddle = max(5, int(15 / difficulty))
    distance = min(700, int(350 * difficulty))
      
    if abs(game.ball.x - game.left_paddle.x) < distance:
      if game.left_paddle.centery < game.ball.y - srinking_paddle:
        game.move_paddle(left=True, up=False)
      elif game.left_paddle.centery > game.ball.y + srinking_paddle:
        game.move_paddle(left=True, up=True)

    output = net.activate((game.right_paddle.y, game.ball.y,
      abs(game.right_paddle.x - game.ball.x)))
    decision = output.index(max(output))
    if decision == 1:
      game.move_paddle(left=False, up=True)
    elif decision == 2:
      game.move_paddle(left=False, up=False)

    game_info = game.loop()

    if (game_info.left_score >= 5 or
        game_info.right_score >= 5 or
        game_info.left_hits + game_info.right_hits > 200):
      calculate_fitness(genome, game_info)
      break


def calculate_fitness(genome, game_info):
  genome.fitness += game_info.right_hits * 2
  genome.fitness += game_info.right_score * 10
    
 
def eval_genomes(genomes, config):
  width, height = 700, 500
  window = pygame.display.set_mode((width, height))
  generation = p.generation
  difficulty  = 1.0 + (generation / 50.0)
  
  for genome_id, genome in genomes:
    genome.fitness = 0
    train_ai(genome, config, window, width, height, difficulty)
  
  
  
def run_neat(config):
  global p
  #p = neat.Checkpointer.restore_checkpoint('res/learning_8_check_points/neat-checkpoint-11')
  p = neat.Population(config)
  p.add_reporter(neat.StdOutReporter(True))
  status = neat.StatisticsReporter()
  p.add_reporter(status)
  p.add_reporter(neat.Checkpointer(1))
  
  winner = p.run(eval_genomes, 150)
  with open("best.pickle", "wb") as f:
    pickle.dump(winner, f)
    
  plot_stats(status)
    
    
    
    
def test_ai(config):
  width, height = 700, 500
  window = pygame.display.set_mode((width, height))
  with open("best.pickle", "rb") as f:
    winner = pickle.load(f)
  winner_net = neat.nn.FeedForwardNetwork.create(winner, config) 
    
  width, height = 700, 500
  win = pygame.display.set_mode((width, height))
  pygame.display.set_caption("Pong")
  pong = PongGame(win, width, height)
  pong.test_ai(winner_net)



if __name__== "__main__":
  local_dir = os.path.dirname(__file__)
  config_path = os.path.join(local_dir, "config.txt")
  
  config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)
  run_neat(config)
  test_ai(config)


