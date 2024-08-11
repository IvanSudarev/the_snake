from random import choice, randint
from typing import Optional
import pygame as pg

# Constants for the game field and greed.
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Snake initial position.
SNAKE_START_POSITION = (SCREEN_WIDTH // 2 - GRID_SIZE,
                        SCREEN_HEIGHT // 2 - GRID_SIZE)

# Possible movements.
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

NEXT_MOVE = {
    (LEFT, pg.K_UP): UP,
    (RIGHT, pg.K_UP): UP,
    (UP, pg.K_LEFT): LEFT,
    (DOWN, pg.K_LEFT): LEFT,
    (LEFT, pg.K_DOWN): DOWN,
    (RIGHT, pg.K_DOWN): DOWN,
    (UP, pg.K_RIGHT): RIGHT,
    (DOWN, pg.K_RIGHT): RIGHT,
}

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

    def __init__(self, body_color: tuple = BOARD_BACKGROUND_COLOR) -> None:
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

    def __init__(self, body_color: tuple = APPLE_COLOR,
                 snake_positions: list = [SNAKE_START_POSITION]) -> None:
        super().__init__(body_color)
        self.randomize_position(snake_positions)

    def randomize_position(self, snake_positions: list) -> None:
        """Set apple on a random position on the field."""
        while True:
            x_coordinate = randint(0, GRID_WIDTH - 1) * GRID_SIZE
            y_coordinate = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            self.position = (x_coordinate, y_coordinate)
            if self.position not in snake_positions:
                break

    def draw(self) -> None:
        """Draws apple on the game field."""
        self.draw_cell(self.position, self.body_color)


class Snake(GameObject):
    """Class describes Snake (game object)."""

    def __init__(self, body_color: tuple = SNAKE_COLOR) -> None:
        super().__init__(body_color)
        self.reset()
        self.direction = RIGHT
        self.speed = 10

    def reset(self) -> None:
        """The snake is dead long live the snake."""
        self.positions = [SNAKE_START_POSITION]
        self.direction = choice(list(NEXT_MOVE.values()))
        self.last: Optional[tuple] = None
        self.length = 1

    @property
    def get_head_position(self) -> tuple:
        """Snake head position. I don't use it, so I guess I can remove it."""
        return self.positions[0]

    def move(self, apple_position) -> None:
        """Snake makes a move."""
        # Calculating next snake movement.
        next_x, next_y = self.get_head_position
        next_x += self.direction[0] * GRID_SIZE
        next_y += self.direction[1] * GRID_SIZE
        if next_x > SCREEN_WIDTH - GRID_SIZE:
            next_x = 0
        elif next_x < 0:
            next_x = SCREEN_WIDTH - GRID_SIZE
        if next_y > SCREEN_HEIGHT - GRID_SIZE:
            next_y = 0
        elif next_y < 0:
            next_y = SCREEN_HEIGHT - GRID_SIZE

        # Did snake bite itself?
        if (next_x, next_y) in self.positions[:-1]:
            rect = (pg.Rect((0, 0), (SCREEN_WIDTH, SCREEN_HEIGHT)))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, rect)
            self.reset()
        else:
            # Snake move on one the next cell.
            self.positions.insert(0, (next_x, next_y))
            # Checking out will the snake eat an apple.
            if (next_x, next_y) == apple_position:
                self.last = None
            else:
                self.last = self.positions.pop(-1)

    def draw(self) -> None:
        """Drawing snake"""
        # Draw the head.
        self.draw_cell(self.get_head_position, self.body_color)

        # Remove the tail (the last segment).
        if self.last:
            self.draw_cell(self.last, BOARD_BACKGROUND_COLOR, False)

    def update_direction(self):
        """I don't need it"""
        pass


def handle_keys(game_object) -> None:
    """Fuction to process user inputs."""
    for event in pg.event.get():
        if event.type == pg.QUIT or event.type == pg.KEYDOWN \
                and event.key == pg.K_ESCAPE:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            # Change game speed.
            if 48 <= event.key <= 57:
                game_object.speed = (1 + event.key - 48) * 4
            # Change direction.
            if (game_object.direction, event.key) in NEXT_MOVE:
                game_object.direction = NEXT_MOVE[(game_object.direction,
                                                   event.key)]


def main():
    """Main function."""
    pg.init()
    snake = Snake(SNAKE_COLOR)
    apple = Apple(APPLE_COLOR, snake.positions)
    while True:
        handle_keys(snake)
        snake.move(apple.position)
        if snake.length < len(snake.positions):
            apple.randomize_position(snake.positions)
            snake.length += 1
        snake.draw()
        apple.draw()
        pg.display.update()
        clock.tick(snake.speed)


if __name__ == '__main__':
    main()
