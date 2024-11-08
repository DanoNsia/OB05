import pygame
import sys
import random


pygame.init()


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)


SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Flappy Bird')

# Параметры игры
GRAVITY = 0.5
FLAP_STRENGTH = -10
PIPE_WIDTH = 70
PIPE_HEIGHT = random.randint(150, 450)
GAP = 200
SPEED = 3

# Загрузка изображений
bird_img = pygame.Surface((30, 30), pygame.SRCALPHA)
pygame.draw.circle(bird_img, BLUE, (15, 15), 15)

# Загрузка музыки
pygame.mixer.music.load('music/0acc5912d33cb02.mp3')  # Замените 'your_music_file.mp3' на путь к вашему музыкальному файлу
pygame.mixer.music.play(-1)  # -1 означает, что музыка будет зацикливаться
pygame.mixer.music.set_volume(0.2)

# Шрифт для отображения счета
font = pygame.font.SysFont(None, 36)

def draw_pipes(pipes):
    for pipe in pipes:
        pygame.draw.rect(screen, BLACK, pipe)

def main():
    clock = pygame.time.Clock()
    bird = pygame.Rect(100, SCREEN_HEIGHT // 2, 30, 30)
    bird_velocity = 0
    pipes = []
    score = 0
    passed_pipe = False

    # Создание начальных труб
    for i in range(2):
        x = SCREEN_WIDTH + i * (PIPE_WIDTH + 200)
        pipes.append(pygame.Rect(x, 0, PIPE_WIDTH, PIPE_HEIGHT))
        pipes.append(pygame.Rect(x, PIPE_HEIGHT + GAP, PIPE_WIDTH, SCREEN_HEIGHT - PIPE_HEIGHT - GAP))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird_velocity = FLAP_STRENGTH

        # Обновление состояния птицы
        bird_velocity += GRAVITY
        bird.y += int(bird_velocity)

        # Обновление состояния труб
        for pipe in pipes:
            pipe.x -= SPEED

        # Удаление труб, которые вышли за экран, и добавление новых
        if pipes[0].x < -PIPE_WIDTH:
            pipes.pop(0)
            pipes.pop(0)
            new_pipe_height = random.randint(150, 450)
            pipes.append(pygame.Rect(SCREEN_WIDTH, 0, PIPE_WIDTH, new_pipe_height))
            pipes.append(
                pygame.Rect(SCREEN_WIDTH, new_pipe_height + GAP, PIPE_WIDTH, SCREEN_HEIGHT - new_pipe_height - GAP))
            passed_pipe = False

            # Проверка прохождения трубы для увеличения счета
        if pipes[0].x + PIPE_WIDTH < bird.x and not passed_pipe:
            score += 1
            passed_pipe = True

            # Проверка столкновений
        if bird.y > SCREEN_HEIGHT or bird.y < 0 or any(pipe.colliderect(bird) for pipe in pipes):
            print("Game Over. Your score:", score)
            pygame.quit()
            sys.exit()

            # Отрисовка игры
        screen.fill(WHITE)
        screen.blit(bird_img, bird)
        draw_pipes(pipes)

        # Отображение счета
        score_text = font.render(f'Score: {score}', True, BLACK)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()

        # Контроль частоты кадров
        clock.tick(60)


if __name__ == "__main__":
    main()
