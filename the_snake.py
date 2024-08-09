from random import choice

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
POSSIBLE_X = tuple(range(0, SCREEN_WIDTH, GRID_SIZE))
POSSIBLE_Y = tuple(range(0, SCREEN_HEIGHT, GRID_SIZE))

# Стартовая позиция змейки
SNAKE_START_POSITION = (SCREEN_WIDTH // 2 - GRID_SIZE, SCREEN_HEIGHT // 2 - GRID_SIZE)

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 5

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject():
    """Class describes game objects"""

    def __init__(self) -> None:
        self.body_color = (0, 0, 0)
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))

    def draw(self) -> None:
        """This method over written in child objects"""
        pass


class Apple(GameObject):
    """Class describes apple (game object)"""

    def __init__(self) -> None:
        self.body_color = APPLE_COLOR
        self.position = (0, 0)

    def draw(self) -> None:
        """It draws apple on the game field"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def randomize_position(self) -> None:
        """Select random coordinate an apple"""
        x_coordinate = choice(POSSIBLE_X)
        y_coordinate = choice(POSSIBLE_Y)
        self.position = (x_coordinate, y_coordinate)


class Snake(GameObject):
    """Class describes Snake (game object)"""

    def __init__(self) -> None:
        self.body_color = SNAKE_COLOR
        self.positions = [SNAKE_START_POSITION]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    @property
    def length(self) -> int:
        """Snake length"""
        return len(self.positions)

    @property
    def next_move(self):
        """Calculating next move"""
        index_x = (self.positions[0][0] // 20 + self.direction[0]) % GRID_WIDTH
        index_y = ((self.positions[0][1] // 20 + self.direction[1])
                   % GRID_HEIGHT)
        next_move = (POSSIBLE_X[index_x],
                     POSSIBLE_Y[index_y])
        print(next_move)

    def update_direction(self):
        """Updating snake direction"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Snake movement"""
        pass

    def reset(self):
        """Reset snake"""
        self.body_color = SNAKE_COLOR
        self.positions = [SNAKE_START_POSITION]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def draw(self) -> None:
        """Drawing snake"""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


# Функция обработки действий пользователя
def handle_keys(game_object):
    """Fuction to process user inputs"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def is_apple_eaten(apple, snake):
    """Will snake eat apple on the next move"""
    return snake.next_move == apple.position


def is_game_over(snake, apple):
    """Will snake byte itself"""
    if snake.next_move in snake.positions[:-1]:
        snake.reset()


def main():
    """Main function"""
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    apple = Apple()
    apple.randomize_position()
    apple.draw()
    snake = Snake()
    snake.draw()
    while True:
        clock.tick(SPEED)

        handle_keys(snake)
        pygame.display.update()


if __name__ == '__main__':
    main()
