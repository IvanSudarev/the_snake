from random import randint

import pygame as pg

# Constants for the game field and greed.
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
POSSIBLE_X = tuple(range(0, SCREEN_WIDTH, GRID_SIZE))
POSSIBLE_Y = tuple(range(0, SCREEN_HEIGHT, GRID_SIZE))

# Snake initial position.
SNAKE_START_POSITION = (SCREEN_WIDTH // 2 - GRID_SIZE,
                        SCREEN_HEIGHT // 2 - GRID_SIZE)

# Possible movements.
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Background color.
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Color of cell borders.
BORDER_COLOR = (93, 216, 228)

# Apple color.
APPLE_COLOR = (255, 0, 0)

# Snake color.
SNAKE_COLOR = (0, 255, 0)

# Game window settings.
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Game window title.
pg.display.set_caption('Snake | Conrols: movement ↑, ↓, ←, →; speed 0, ..., 9')

# Clock settings.
clock = pg.time.Clock()


class GameObject():
    """Class describes game objects."""

    def __init__(self, body_color: tuple) -> None:
        self.body_color = body_color
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))

    def draw(self) -> None:
        """This method over written in child objects."""
        NotImplementedError

    def draw_cell(self, position, background_color,
                  draw_border: bool = True) -> None:
        """Draws one cell on the game field"""
        rect = (pg.Rect(position, (GRID_SIZE, GRID_SIZE)))
        pg.draw.rect(screen, background_color, rect)
        if draw_border:
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Class describes apple (game object)."""

    def __init__(self, body_color: tuple, snake_positions: list) -> None:
        super().__init__(body_color)
        self.randomize_position(snake_positions)

    def randomize_position(self, snake_positions: list) -> None:
        """Set apple on a random position on the field."""
        while True:
            x_coordinate = (randint(0, SCREEN_WIDTH // GRID_SIZE - 1)
                            * GRID_SIZE)
            y_coordinate = (randint(0, SCREEN_HEIGHT // GRID_SIZE - 1)
                            * GRID_SIZE)
            self.position = (x_coordinate, y_coordinate)
            if self.position not in snake_positions:
                break

    def draw(self) -> None:
        """Draws apple on the game field."""
        self.draw_cell(self.position, self.body_color)


class Snake(GameObject):
    """Class describes Snake (game object)."""

    def __init__(self, body_color: tuple) -> None:
        super().__init__(body_color)
        self.positions: list = [SNAKE_START_POSITION]
        self.direction = RIGHT
        self.speed = 10
        self.next_direction = None
        self.last = None

    @property
    def length(self) -> int:
        """Snake length. I don't use it, so I guess I can remove it."""
        return len(self.positions)

    @property
    def get_head_position(self) -> tuple:
        """Snake head position. I don't use it, so I guess I can remove it."""
        return self.positions[0]

    @property
    def next_move(self) -> tuple[int, int]:
        """Calculation of the nex movement of the snake."""
        index_x = (self.positions[0][0] // 20 + self.direction[0]) % GRID_WIDTH
        index_y = ((self.positions[0][1] // 20 + self.direction[1])
                   % GRID_HEIGHT)
        next_move = (POSSIBLE_X[index_x],
                     POSSIBLE_Y[index_y])
        return next_move

    def update_direction(self) -> None:
        """Updating snake movement direction."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self, apple_eaten) -> None:
        """Snake makes a move."""
        self.positions.insert(0, self.next_move)
        if not apple_eaten:
            self.last = self.positions.pop(-1)
        else:
            self.last = None

    def reset(self) -> None:
        """The snake is dead long live the snake."""
        self.body_color = SNAKE_COLOR
        self.positions = [SNAKE_START_POSITION]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def draw(self) -> None:
        """Drawing snake"""
        for position in self.positions[:-1]:
            self.draw_cell(position, self.body_color)

        # Draw the head.
        head_rect = pg.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, head_rect)
        pg.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Remove the tail (the last segment).
        if self.last:
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


def handle_keys(game_object) -> None:
    """Fuction to process user inputs."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT
            elif 48 <= event.key <= 57:
                game_object.speed = (1 + event.key - 48) * 4
            game_object.update_direction()


def is_apple_eaten(apple, snake) -> bool:
    """Will snake eat apple on the next move?"""
    return snake.next_move == apple.position


def is_game_over(snake) -> None:
    """Will snake byte itself? If yes - reset the field, reset the snake."""
    if snake.next_move in snake.positions[:-1]:
        rect = (pg.Rect((0, 0), (SCREEN_WIDTH, SCREEN_HEIGHT)))
        pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, rect)
        snake.reset()


def main():
    """Main function."""
    pg.init()
    snake = Snake(SNAKE_COLOR)
    snake.draw()
    apple = Apple(APPLE_COLOR, snake.positions)
    apple.randomize_position(snake.positions)
    apple.draw()
    while True:
        handle_keys(snake)
        apple_eaten = is_apple_eaten(apple, snake)
        snake.move(apple_eaten)
        is_game_over(snake)
        if apple_eaten:
            apple.randomize_position(snake.positions)
        snake.draw()
        apple.draw()
        pg.display.update()
        clock.tick(snake.speed)


if __name__ == '__main__':
    main()
