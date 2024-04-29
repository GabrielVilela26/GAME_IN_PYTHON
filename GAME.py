import pygame
from pygame.math import Vector2
import random
import sys
import os

pygame.init()

# Cores
BROWN = (191, 166, 110)
DARK_BROWN = (64, 55, 37)

cell_size = 20
number_of_cells = 30

pygame.font.init()
orbitron_font = pygame.font.Font("Orbitron-VariableFont_wght.ttf", 15)

class Comida:
    def __init__(self, cobra_body):
        self.position = self.generate_random_pos(cobra_body)

    def draw(self):
        comida_rect = pygame.Rect(self.position.x * cell_size, self.position.y * cell_size, cell_size, cell_size)
        resized_comida_surface = pygame.transform.scale(comida_surface, (cell_size, cell_size))
        screen.blit(resized_comida_surface, comida_rect)

    def generate_random_cell(self):
        x = random.randint(0, number_of_cells - 1)
        y = random.randint(0, number_of_cells - 1)
        return Vector2(x, y)

    def generate_random_pos(self, cobra_body):
        position = self.generate_random_cell()

        while (
            position in cobra_body
            or position.x <= 1
            or position.x >= number_of_cells - 2
            or position.y <= 1
            or position.y >= number_of_cells - 2
        ):
            position = self.generate_random_cell()
        return position

class Cobra:
    def __init__(self):
        self.body = [Vector2(3, 9), Vector2(2, 9), Vector2(1, 9)]
        self.direction = Vector2(0, 0)
        self.add_segment = False
        self.score = 0
        self.snake_speed = 200

    def draw(self):
        for i, segment in enumerate(self.body):
            segment_rect = pygame.Rect(segment.x * cell_size, segment.y * cell_size, cell_size, cell_size)

            if i == 0:
                pygame.draw.rect(screen, DARK_BROWN, segment_rect, 0, 5)
            else:
                pygame.draw.rect(screen, DARK_BROWN, segment_rect, 5, 5)

    def update(self):
        new_head = self.body[0] + self.direction

        if new_head.x < 0:
            new_head.x = number_of_cells - 1
        elif new_head.x >= number_of_cells:
            new_head.x = 0
        if new_head.y < 0:
            new_head.y = number_of_cells - 1
        elif new_head.y >= number_of_cells:
            new_head.y = 0

        if new_head in self.body:
            game.game_over = True

        self.body.insert(0, new_head)
        if self.add_segment:
            self.add_segment = False
        else:
            self.body = self.body[:-1]

    def increase_snake_speed(self):
        if self.snake_speed >= 45:
            self.snake_speed -= 2
        else:
            self.snake_speed == 45
        pygame.time.set_timer(COBRA_UPDATE, self.snake_speed)

class Game: 
    def __init__(self):
        self.cobra = Cobra()
        self.comida = Comida(self.cobra.body)
        self.game_over = False
        self.game_started = False
        self.game_paused = False

        self.snake_speed = 200 
        self.highscore = self.load_highscore()

        self.game_over_font = pygame.font.Font("Orbitron-VariableFont_wght.ttf", 40)
        self.restart_font = pygame.font.Font("Orbitron-VariableFont_wght.ttf", 20)
        self.start_font = pygame.font.Font("Orbitron-VariableFont_wght.ttf", 20)
        self.pause_font = pygame.font.Font("Orbitron-VariableFont_wght.ttf", 40)
        self.pause_font1 = pygame.font.Font("Orbitron-VariableFont_wght.ttf", 20)
        self.highscore_font = pygame.font.Font("Orbitron-VariableFont_wght.ttf", 20)
        self.score_font = pygame.font.Font("Orbitron-VariableFont_wght.ttf", 20)

    def restart_game(self):
        self.cobra = Cobra()
        self.comida = Comida(self.cobra.body)
        self.game_over = False
        self.game_started = False
        self.game_paused = False
        pygame.time.set_timer(COBRA_UPDATE, self.snake_speed)

    def draw(self):
        if not self.game_over:
            self.comida.draw()
            self.cobra.draw()

        if not self.game_started:
            scaled_inicio_surface = pygame.transform.scale(inicio_surface, (cell_size * 9, cell_size * 6))
            screen.blit(scaled_inicio_surface, (210, 240))
            
            scaled_pause_surface = pygame.transform.scale(pause_surface, (cell_size * 4, cell_size * 4))
            screen.blit(scaled_pause_surface, (280, 400))

            start_text = self.start_font.render("Aperte as teclas de movimento para mover a cobra", True, DARK_BROWN)
            start_rect = start_text.get_rect(center=(cell_size * 15, cell_size * 11))
            screen.blit(start_text, start_rect)
            
            pause_text = self.pause_font1.render("Aperte (P) para pausar", True, DARK_BROWN)
            pause_rect = pause_text.get_rect(center=(cell_size * 7, cell_size * 22))
            screen.blit(pause_text, pause_rect)
            

        if self.game_over:
            game_over_text = self.game_over_font.render("Game Over", True, DARK_BROWN)
            game_over_rect = game_over_text.get_rect(center=(cell_size * 15, cell_size * 10))
            screen.blit(game_over_text, game_over_rect)

            # Verifica se a pontuação é maior que o recorde
            if self.cobra.score > self.highscore:
                self.highscore = self.cobra.score
                new_highscore_text = self.highscore_font.render("Novo Recorde!", True, DARK_BROWN)
                new_highscore_rect = new_highscore_text.get_rect(center=(cell_size * 15, cell_size * 13))
                screen.blit(new_highscore_text, new_highscore_rect)
                self.save_highscore()
                
            score_text = self.score_font.render("Pontuação: {}".format(self.cobra.score), True, DARK_BROWN)
            score_rect = score_text.get_rect(center=(cell_size * 15, cell_size * 20))
            screen.blit(score_text, score_rect)

            restart_text = self.restart_font.render("Pressione a tecla de Espaço para reiniciar", True, DARK_BROWN)
            restart_rect = restart_text.get_rect(center=(cell_size * 15, cell_size * 13))

            scaled_restart_surface = pygame.transform.scale(restart_surface, (cell_size * 16, cell_size * 4))
            screen.blit(scaled_restart_surface, (140, 280))

            screen.blit(restart_text, restart_rect)

        if self.game_paused:
            pause_text = self.pause_font.render("JOGO PAUSADO", True, DARK_BROWN)
            pause_rect = pause_text.get_rect(center=(cell_size * 14, cell_size * 3))
            pause_text1 = self.pause_font1.render("Aperte (P) para continuar", True, DARK_BROWN)
            pause_rect1 = pause_text1.get_rect(center=(cell_size * 10, cell_size * 14))
            pause_text2 = self.pause_font1.render("Aperte (R) para reiniciar", True, DARK_BROWN)
            pause_rect2 = pause_text2.get_rect(center=(cell_size * 10, cell_size * 19))
            screen.blit(pause_text, pause_rect)
            screen.blit(pause_text1, pause_rect1)
            screen.blit(pause_text2, pause_rect2)

            scaled_pause_surface = pygame.transform.scale(pause_surface, (cell_size * 4, cell_size * 4))
            screen.blit(scaled_pause_surface, (290, 230))
            
            scaled_reset_surface = pygame.transform.scale(reset_surface, (cell_size * 4, cell_size * 4))
            screen.blit(scaled_reset_surface, (290, 320))

        score_text = orbitron_font.render("Pts.: {}".format(self.cobra.score), True, DARK_BROWN)
        screen.blit(score_text, (10, 5))

        highscore_text = orbitron_font.render("Recorde: {}".format(self.highscore), True, DARK_BROWN)
        screen.blit(highscore_text, (cell_size * number_of_cells - 130, 5))

    def update(self):
        if not self.game_over and self.game_started and not self.game_paused:
            self.cobra.update()
            self.checar_colisao_comida()

    def checar_colisao_comida(self):
        if self.cobra.body[0] == self.comida.position:
            self.comida.position = self.comida.generate_random_pos(self.cobra.body)
            self.cobra.add_segment = True
            self.cobra.score += 1
            self.cobra.increase_snake_speed()

    def save_highscore(self):
        with open("recorde.txt", "w") as file:
            file.write(str(self.highscore))

    def load_highscore(self):
        if os.path.exists("recorde.txt"):
            with open("recorde.txt", "r") as file:
                highscore = file.read()
                if highscore:
                    return int(highscore)
        return 0

screen = pygame.display.set_mode((cell_size * number_of_cells, cell_size * number_of_cells))
pygame.display.set_caption("Retro Snake")
clock = pygame.time.Clock()
game = Game()


comida_surface = pygame.image.load("apple.png")
inicio_surface = pygame.image.load("vectors.png")
pause_surface = pygame.image.load("p.png")
restart_surface = pygame.image.load("space.png")
reset_surface = pygame.image.load("r.png")

COBRA_UPDATE = pygame.USEREVENT
pygame.time.set_timer(COBRA_UPDATE, game.snake_speed)

while True:
    for event in pygame.event.get():
        if event.type == COBRA_UPDATE:
            game.update()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if not game.game_started:
                game.game_started = True

            if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_RIGHT, pygame.K_LEFT, pygame.K_SPACE]:
                if event.key == pygame.K_UP and game.cobra.direction != Vector2(0, 1):
                    game.cobra.direction = Vector2(0, -1)

                elif event.key == pygame.K_DOWN and game.cobra.direction != Vector2(0, -1):
                    game.cobra.direction = Vector2(0, 1)

                elif event.key == pygame.K_RIGHT and game.cobra.direction != Vector2(-1, 0):
                    game.cobra.direction = Vector2(1, 0)

                elif event.key == pygame.K_LEFT and game.cobra.direction != Vector2(1, 0):
                    game.cobra.direction = Vector2(-1, 0)

                elif event.key == pygame.K_SPACE and game.game_over:
                    game.restart_game()

            elif event.key == pygame.K_r and game.game_paused:
                game.restart_game()

            elif event.key == pygame.K_p:
                game.game_paused = not game.game_paused

    screen.fill(BROWN)

    border_rect = pygame.Rect(0, 0, cell_size * number_of_cells, cell_size * number_of_cells)
    pygame.draw.rect(screen, BROWN, border_rect)
    pygame.draw.rect(screen, DARK_BROWN, border_rect, 5, border_radius=10)

    game.draw()

    pygame.display.update()
    clock.tick(60)
