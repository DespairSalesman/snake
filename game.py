import pygame
import sys
import random

pygame.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 920
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

font = pygame.font.Font(None, 36)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Змейка ')


def game_over(score, best_score):
    game_over_text = font.render('Игра окончена', True, WHITE)
    score_text = font.render(f'Счёт: {score}', True, WHITE)
    best_score_text = font.render(f'Рекорд: {best_score}', True, WHITE)
    restart_text = font.render('Нажмите "R" для рестарта', True, WHITE)
    exit_text = font.render('Нажмте "Q" для выхода из игры', True, WHITE)

    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 100,
                                 SCREEN_HEIGHT // 2 - 100))
    screen.blit(score_text, (SCREEN_WIDTH // 2 - 60, SCREEN_HEIGHT // 2 - 50))
    screen.blit(best_score_text, (SCREEN_WIDTH // 2 - 85, SCREEN_HEIGHT // 2 - 10))
    screen.blit(restart_text, (SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 + 30))
    screen.blit(exit_text, (SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 + 70))
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_r:
                    return


def run_game():
    snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
    snake_direction = (0, -1)
    food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
    score = 0
    best_score = load_best_score()

    clock = pygame.time.Clock()

    while True:
        pygame.display.set_caption('Змейка ' + 'Cчёт: ' + str(score))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake_direction != (0, 1):
                    snake_direction = (0, -1)
                elif event.key == pygame.K_DOWN and snake_direction != (0, -1):
                    snake_direction = (0, 1)
                elif event.key == pygame.K_LEFT and snake_direction != (1, 0):
                    snake_direction = (-1, 0)
                elif event.key == pygame.K_RIGHT and snake_direction != (-1, 0):
                    snake_direction = (1, 0)

        new_head = (snake[0][0] + snake_direction[0], snake[0][1] + snake_direction[1])
        snake.insert(0, new_head)

        if snake[0] == food:
            score += 1
            if score > best_score:
                best_score = score
                save_best_score(best_score)
            food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        else:
            snake.pop()

        if (
                snake[0][0] < 0
                or snake[0][0] >= GRID_WIDTH
                or snake[0][1] < 0
                or snake[0][1] >= GRID_HEIGHT
        ):
            game_over(score, best_score)
            return

        if snake[0] in snake[1:]:
            game_over(score, best_score)
            return

        screen.fill(BLACK)

        for segment in snake:
            pygame.draw.rect(
                screen, GREEN, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            )

        pygame.draw.rect(
            screen, WHITE, (food[0] * GRID_SIZE, food[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        )

        pygame.display.update()

        clock.tick(10)


def load_best_score():
    try:
        with open('best_score.txt', 'r') as file:
            best_score = int(file.read())
    except (FileNotFoundError, ValueError):
        best_score = 0
    return best_score


def save_best_score(score):
    with open('best_score.txt', 'w') as file:
        file.write(str(score))


while True:
    run_game()
