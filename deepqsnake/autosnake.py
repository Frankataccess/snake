import pygame,sys,random
from pygame.math import Vector2

frame_iteration = 0
# Define the Snake class
class SNAKE_AI:
    def __init__(self):
        # Initialize snake attributes
        self.body = [Vector2(5,10), Vector2(4,10), Vector2(3,10)]
        self.direction = Vector2(0,0)
        self.new_block = False

        # Load snake graphics for different directions
        self.head_up = pygame.image.load('snake/graphics/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('snake/graphics/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('snake/graphics/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('snake/graphics/head_left.png').convert_alpha()

        # Similar graphics for tail and body in different configurations
        self.tail_up = pygame.image.load('snake/graphics/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('snake/graphics/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('snake/graphics/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('snake/graphics/tail_left.png').convert_alpha()

        self.body_vertical = pygame.image.load('snake/graphics/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('snake/graphics/body_horizontal.png').convert_alpha()

        self.body_tr = pygame.image.load('snake/graphics/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('snake/graphics/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('snake/graphics/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('snake/graphics/body_bl.png').convert_alpha()

        # Load the crunch sound
        self.crunch_sound = pygame.mixer.Sound('snake/sound/crunch.wav')

    # Draw the snake on the screen
    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()

        for index, block in enumerate(self.body):
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)

            if index == 0:
                screen.blit(self.head, block_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail, block_rect)
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical, block_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal, block_rect)
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_tl, block_rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl, block_rect)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr, block_rect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br, block_rect)

    # Update the head graphics based on the direction
    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1, 0):
            self.head = self.head_left
        elif head_relation == Vector2(-1, 0):
            self.head = self.head_right
        elif head_relation == Vector2(0, 1):
            self.head = self.head_up
        elif head_relation == Vector2(0, -1):
            self.head = self.head_down

    # Update the tail graphics based on the direction
    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1, 0):
            self.tail = self.tail_left
        elif tail_relation == Vector2(-1, 0):
            self.tail = self.tail_right
        elif tail_relation == Vector2(0, 1):
            self.tail = self.tail_up
        elif tail_relation == Vector2(0, -1):
            self.tail = self.tail_down

    # Move the snake on the screen
    def move_snake(self):
        if self.new_block == True:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    # Add a new block to the snake
    def add_block(self):
        self.new_block = True

    # Play the crunch sound
    def play_crunch_sound(self):
        self.crunch_sound.play()

    # Reset the snake to its initial state
    def reset(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)
        self.score = 0
        self.frame_iteration = 0

# Define the Fruit class
class FRUIT:
    def __init__(self):
        self.randomize()

    # Draw the fruit on the screen
    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        screen.blit(apple, fruit_rect)

    # Randomize the position of the fruit
    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)

# Define the Main class
class MAIN:
    def __init__(self):
        self.snake = SNAKE_AI()
        self.fruit = FRUIT()

    # Update the game state
    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    # Draw game elements on the screen
    def draw_elements(self):
        self.draw_grass()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()

    # Check for collisions with the fruit
    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()
            self.snake.play_crunch_sound()

        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()

    # Check for game over conditions
    def check_fail(self):
        reward = 0
        # Check if the snake is out of bounds or if the frame iteration exceeds a threshold
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number or self.frame_iteration > 100*len(self.snake):
            self.game_over()
            reward = -10
            # Return the reward, game_over status, and the current score
            return reward, self.game_over, self.score

        # Check if the snake collides with itself or if the frame iteration exceeds a threshold
        for block in self.snake.body[1:] or self.frame_iteration > 100*len(self.snake):
            if block == self.snake.body[0]:
                self.game_over()
                reward = -10
                # Return the reward, game_over status, and the current score
                return reward, self.game_over, self.score

    # Game over function
    def game_over(self):
        self.snake.reset()

    # Draw the grass background
    def draw_grass(self):
        grass_color = (167, 209, 61)
        for row in range(cell_number):
            if row % 2 == 0:
                for col in range(cell_number):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)
            else:
                for col in range(cell_number):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)

    # Draw the score on the screen
    def draw_score(self):
        score_text = str(len(self.snake.body) - 3)
        score_surface = game_font.render(score_text, True, (56, 74, 12))
        score_x = int(cell_size * cell_number - 60)
        score_y = int(cell_size * cell_number - 40)
        score_rect = score_surface.get_rect(center=(score_x, score_y))
        apple_rect = apple.get_rect(midright=(score_rect.left, score_rect.centery))
        bg_rect = pygame.Rect(apple_rect.left, apple_rect.top, apple_rect.width + score_rect.width + 6,
                              apple_rect.height)

        pygame.draw.rect(screen, (167, 209, 61), bg_rect)
        screen.blit(score_surface, score_rect)
        screen.blit(apple, apple_rect)
        pygame.draw.rect(screen, (56, 74, 12), bg_rect, 2)


# reset
# reward
# play(action -> direction)
# game_iteration
# is_collision

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
cell_size = 40
cell_number = 20
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
clock = pygame.time.Clock()
apple = pygame.image.load('snake/graphics/apple.png').convert_alpha()
game_font = pygame.font.Font('snake/font/PoetsenOne-Regular.ttf', 25)

SCREEN_UPDATE = pygame.USEREVENT
#speed
pygame.time.set_timer(SCREEN_UPDATE, 100)

main_game = MAIN()

while True:
   frame_iteration += 1
    # 1. collect user input
   for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()


   screen.fill((175, 215, 70))
   main_game.draw_elements()
   pygame.display.update()
   clock.tick(60)