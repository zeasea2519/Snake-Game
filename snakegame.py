import pygame,sys,random
from pygame.math import Vector2

class SNAKE: #creates the snake
    def __init__(self):
        self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]
        self.direction = Vector2(0,0)
        self.new_block = False

    def draw_snake(self):
        for block in self.body:
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos,y_pos,cell_size,cell_size)
            pygame.draw.rect(screen,(0,0,0),block_rect)
            #create a rectangle
            #draw the rectangle

    def move_snake(self):
        if self.new_block == True:
            body_copy = self.body[:]
            body_copy.insert(0,body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False

        else:
            body_copy = self.body[:-1]
            body_copy.insert(0,body_copy[0] + self.direction)
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True

    def reset(self):
        self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]
        self.direction = Vector2(0,0)

class FRUIT: #creates the fruit
    def __init__(self):
        self.x = random.randint(0,cell_number - 1)
        self.y = random.randint(0,cell_number - 1)
        self.pos = Vector2(self.x,self.y)
        #create an x and y position
        #draw a square

    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size),int(self.pos.y * cell_size),cell_size,cell_size)
        pygame.draw.rect(screen,(184,0,104),fruit_rect)
        #create rectangle
        #draw the rectangle

    def randomise(self):
        self.x = random.randint(0,cell_number - 1)
        self.y = random.randint(0,cell_number - 1)
        self.pos = Vector2(self.x,self.y)

class MAIN: #main game logic
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()

    def update(self): #when the game updates, the snake moves
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    def draw_elements(self): #draws elements outside of game loop
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomise() #repositions fruit
            self.snake.add_block() #add another block to snake

        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomise()

    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number: 
            #above code checks if snake is outside of the screen
            self.game_over()

        for block in self.snake.body[1:]: #checks if snake hits itself
            if block == self.snake.body[0]:
                self.game_over()

    def game_over(self):
        self.snake.reset()

    def draw_score(self):
        score_text = str(len(self.snake.body) - 3)
        score_surface = game_font.render(score_text,True,(0,0,0))
        score_x = int(cell_size * cell_number - 60)
        score_y = int(cell_size * cell_number - 40)
        score_rect = score_surface.get_rect(center = (score_x,score_y))
        screen.blit(score_surface,score_rect)

pygame.init()
cell_size = 40
cell_number = 20
screen = pygame.display.set_mode((cell_number * cell_size,cell_number * cell_size))
clock = pygame.time.Clock()
game_font = pygame.font.Font(None,35)

main_game = MAIN()

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE,150)

while True: #game loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #exit game mechanic
            pygame.quit()
            sys.exit()

        if event.type == SCREEN_UPDATE:
            main_game.update()

        if event.type == pygame.KEYDOWN: #moving snake using arrow keys
            if event.key == pygame.K_UP:
                if main_game.snake.direction.y != 1: #snake cannot reverse on itself
                    main_game.snake.direction = Vector2(0,-1)

            if event.key == pygame.K_DOWN:
                if main_game.snake.direction.y != -1: #snake cannot reverse on itself
                    main_game.snake.direction = Vector2(0,1)

            if event.key == pygame.K_LEFT:
                if main_game.snake.direction.x != 1: #snake cannot reverse on itself
                    main_game.snake.direction = Vector2(-1,0)

            if event.key == pygame.K_RIGHT:
                if main_game.snake.direction.x != -1: #snake cannot reverse on itself
                    main_game.snake.direction = Vector2(1,0)

    screen.fill((102,161,255))
    main_game.draw_elements()
    pygame.display.update()
    clock.tick(60)
