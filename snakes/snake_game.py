import pygame
import random
import os
import sys
from pygame import mixer

# Initialize Pygame and mixer
pygame.init()
mixer.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 200, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)
PURPLE = (128, 0, 128)

# Game states
MENU = 'menu'
PLAYING = 'playing'
GAME_OVER = 'game_over'

class SnakeGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Modern Snake Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.load_assets()
        self.reset_game()

    def load_assets(self):
        # Create sounds directory if it doesn't exist
        if not os.path.exists('sounds'):
            os.makedirs('sounds')
        
        # Initialize sound effects
        self.eat_sound = mixer.Sound('sounds/eat.wav') if os.path.exists('sounds/eat.wav') else None
        self.crash_sound = mixer.Sound('sounds/crash.wav') if os.path.exists('sounds/crash.wav') else None

    def reset_game(self):
        self.snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0)
        self.score = 0
        self.game_state = MENU
        self.speed = 10
        self.obstacles = []
        self.badges = set()
        self.last_obstacle_score = 0
        self.generate_obstacles()
        self.food = self.spawn_food()  # Moved after obstacles initialization

    def generate_obstacles(self):
        # Clear existing obstacles when generating new ones
        self.obstacles = []
        
        # Add obstacles based on score milestones
        num_obstacles = 0
        if self.score >= 10:
            num_obstacles = 3
        if self.score >= 20:
            num_obstacles = 6
        if self.score >= 30:
            num_obstacles = 9
        if self.score >= 40:
            num_obstacles = 12

        # Generate new obstacles
        for _ in range(num_obstacles):
            while True:
                obstacle = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
                if (obstacle not in self.snake and 
                    obstacle not in self.obstacles and 
                    obstacle != self.food):
                    self.obstacles.append(obstacle)
                    break

    def check_badge(self):
        if self.score >= 50 and "MASTER" not in self.badges:
            self.badges.add("MASTER")
            return True
        return False

    def spawn_food(self):
        while True:
            food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if (food not in self.snake and 
                food not in self.obstacles):
                return food

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if self.game_state == MENU:
                    if event.key == pygame.K_SPACE:
                        self.game_state = PLAYING
                elif self.game_state == PLAYING:
                    if event.key == pygame.K_UP and self.direction != (0, 1):
                        self.direction = (0, -1)
                    elif event.key == pygame.K_DOWN and self.direction != (0, -1):
                        self.direction = (0, 1)
                    elif event.key == pygame.K_LEFT and self.direction != (1, 0):
                        self.direction = (-1, 0)
                    elif event.key == pygame.K_RIGHT and self.direction != (-1, 0):
                        self.direction = (1, 0)
                elif self.game_state == GAME_OVER:
                    if event.key == pygame.K_SPACE:
                        self.reset_game()
        return True

    def update(self):
        if self.game_state != PLAYING:
            return

        # Move snake
        new_head = (
            (self.snake[0][0] + self.direction[0]) % GRID_WIDTH,
            (self.snake[0][1] + self.direction[1]) % GRID_HEIGHT
        )

        # Check collision with obstacles
        if new_head in self.obstacles:
            self.game_state = GAME_OVER
            if self.crash_sound:
                self.crash_sound.play()
            return

        # Check collision with self
        if new_head in self.snake:
            self.game_state = GAME_OVER
            if self.crash_sound:
                self.crash_sound.play()
            return

        self.snake.insert(0, new_head)

        # Check food collision
        if new_head == self.food:
            if self.eat_sound:
                self.eat_sound.play()
            self.score += 1
            
            # Check for new obstacles based on score milestones
            if (self.score in [10, 20, 30, 40] and 
                self.score != self.last_obstacle_score):
                self.last_obstacle_score = self.score
                self.generate_obstacles()
            
            # Check for badge achievement
            self.check_badge()
            
            self.food = self.spawn_food()
            self.speed = min(20, 10 + self.score // 5)
        else:
            self.snake.pop()

    def draw(self):
        self.screen.fill(BLACK)

        if self.game_state == MENU:
            self.draw_menu()
        elif self.game_state == PLAYING:
            self.draw_game()
        elif self.game_state == GAME_OVER:
            self.draw_game_over()

        pygame.display.flip()

    def draw_menu(self):
        title = self.font.render("SNAKE GAME", True, GREEN)
        start_text = self.font.render("Press SPACE to Start", True, WHITE)
        instruction_text = self.font.render("Collect food and avoid obstacles!", True, YELLOW)
        
        self.screen.blit(title, (WINDOW_WIDTH // 2 - title.get_width() // 2, WINDOW_HEIGHT // 4))
        self.screen.blit(start_text, (WINDOW_WIDTH // 2 - start_text.get_width() // 2, WINDOW_HEIGHT // 2))
        self.screen.blit(instruction_text, 
                        (WINDOW_WIDTH // 2 - instruction_text.get_width() // 2, 
                         WINDOW_HEIGHT * 3 // 4))

    def draw_game(self):
        # Draw obstacles
        for obstacle in self.obstacles:
            pygame.draw.rect(self.screen, GRAY, (
                obstacle[0] * GRID_SIZE,
                obstacle[1] * GRID_SIZE,
                GRID_SIZE - 1,
                GRID_SIZE - 1
            ))

        # Draw snake
        for i, segment in enumerate(self.snake):
            color = GREEN if i == 0 else DARK_GREEN
            pygame.draw.rect(self.screen, color, (
                segment[0] * GRID_SIZE,
                segment[1] * GRID_SIZE,
                GRID_SIZE - 1,
                GRID_SIZE - 1
            ))

        # Draw food
        pygame.draw.rect(self.screen, RED, (
            self.food[0] * GRID_SIZE,
            self.food[1] * GRID_SIZE,
            GRID_SIZE - 1,
            GRID_SIZE - 1
        ))

        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))

        # Draw badges
        if "MASTER" in self.badges:
            badge_text = self.font.render("🏆 MASTER SNAKE!", True, PURPLE)
            self.screen.blit(badge_text, (WINDOW_WIDTH - badge_text.get_width() - 10, 10))

    def draw_game_over(self):
        game_over_text = self.font.render("GAME OVER", True, RED)
        score_text = self.font.render(f"Final Score: {self.score}", True, WHITE)
        restart_text = self.font.render("Press SPACE to Restart", True, WHITE)
        
        self.screen.blit(game_over_text, (WINDOW_WIDTH // 2 - game_over_text.get_width() // 2, WINDOW_HEIGHT // 3))
        self.screen.blit(score_text, (WINDOW_WIDTH // 2 - score_text.get_width() // 2, WINDOW_HEIGHT // 2))
        self.screen.blit(restart_text, (WINDOW_WIDTH // 2 - restart_text.get_width() // 2, WINDOW_HEIGHT * 2 // 3))

        # Draw badges earned
        if "MASTER" in self.badges:
            badge_text = self.font.render("🏆 MASTER SNAKE ACHIEVED!", True, PURPLE)
            self.screen.blit(badge_text, 
                           (WINDOW_WIDTH // 2 - badge_text.get_width() // 2, 
                            WINDOW_HEIGHT * 3 // 4))

    def run(self):
        running = True
        while running:
            running = self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(self.speed)

if __name__ == "__main__":
    game = SnakeGame()
    game.run()
    pygame.quit()
    sys.exit()