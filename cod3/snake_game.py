import pygame
from pygame.locals import * #importing certain global variables that we'll use
import time
import random

SIZE = 38
BACKGROUND_COLOUR = 129, 36, 166
TEXT_COLOUR = 19, 2, 33

class Apple:
    def __init__(self, parent_screen):
        self.image = pygame.image.load("resources/apple.jpg").convert()
        self.parent_screen = parent_screen
        self.x = 569
        self.y = 379

    def draw(self):
        self.parent_screen.blit(self.image,(self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(0,24)*SIZE
        self.y = random.randint(0,19)*SIZE

class Snake:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("resources/block.jpg").convert()
        self.direction = 'down'

        self.length = 1
        self.x = [SIZE]
        self.y = [SIZE]

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'
    
    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def walk(self):
        #update body
        for i in range(self.length-1,0,-1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        if self.direction == 'up':
            self.y[0] -= SIZE
        if self.direction == 'down':
            self.y[0] += SIZE
        if self.direction == 'right':
            self.x[0] += SIZE
        if self.direction == 'left':
            self.x[0] -= SIZE

        self.draw()

    def draw(self):
        self.parent_screen.fill(BACKGROUND_COLOUR)

        for i in range(self.length):
            self.parent_screen.blit(self.image,(self.x[i], self.y[i]))

        pygame.display.flip()

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake Game")

        pygame.mixer.init() #sound module is initialized
        self.play_background_music()

        self.surface = pygame.display.set_mode((1138, 758))
          #pygame.display.set_mode => this function will create (initialize) a display surface
        self.snake = Snake(self.surface)  
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

    def reset(self):
        self.snake = Snake(self.surface)
        self.apple = Apple(self.surface)

    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True
        return False

    def play_sound(self, sound):
        sound = pygame.mixer.Sound(f"resources/{sound}.mp3")
        pygame.mixer.Sound.play(sound)

    def play_background_music(self):
        pygame.mixer.music.load("resources/bgm_music.mp3")
        pygame.mixer.music.play()

    def play(self):
        self.snake.walk()
        self.apple.draw()
        self.display_Score()
        pygame.display.flip()

        # snake eating the apple
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.play_sound("ding")
            self.snake.increase_length()
            self.apple.move()

        # snake colliding with itself
        for i in range(2, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound("crash")
                raise "Collision Occured"
            
        # snake colliding with the border
        if not (0 <= self.snake.x[0] <= 1138 and 0 <= self.snake.y[0] <= 758):
            self.play_sound("crash")
            raise "Collision Occured"

    def display_Score(self):
        font = pygame.font.SysFont('mono bold.ttf', 30)
        score = font.render(f"SCORE: {self.snake.length}", True, (TEXT_COLOUR))#score text
        self.surface.blit(score, (830, 20))#use the blit function when have to show smt on the surface

    def show_game_over(self):
        self.surface.fill(BACKGROUND_COLOUR)
        self.play_sound("gameover")
        font = pygame.font.SysFont('mono bold.ttf', 30)
        line1 = font.render(f"GAME OVER! YOUR SCORE IS {self.snake.length}", True, (TEXT_COLOUR))
        self.surface.blit(line1, (200,300))
        line2 = font.render("TO PLAY AGAIN PRESS ENTER, TO EXIT PRESS ESC . . .", True, (TEXT_COLOUR))
        self.surface.blit(line2,(200,350))

        pygame.display.flip()

        pygame.mixer.music.pause()

    def run(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                
                    if event.key == K_RETURN:
                        pygame.mixer.music.play()
                        pause = False

                    if not pause:
                        if event.key == K_UP:
                            self.snake.move_up()

                        if event.key == K_DOWN:
                            self.snake.move_down()

                        if event.key == K_LEFT:
                            self.snake.move_left()
                            
                        if event.key == K_RIGHT:
                            self.snake.move_right()

                elif event.type == QUIT:
                    running = False

            try:

                if not pause:
                    self.play()

            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()
            
            time.sleep(0.1)


# Initializing the module
if __name__ == "__main__":
    game = Game()
    game.run()


    