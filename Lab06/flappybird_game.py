import pygame
import random
import sys
import os

# Constants
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SKY_BLUE = (135, 206, 235)
YELLOW = (255, 255, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BROWN = (139, 69, 19)
DARK_BROWN = (101, 67, 33)

# Game Physics
GRAVITY = 0.25
FLAP_STRENGTH = -6.5
PIPE_SPEED = 3
PIPE_FREQUENCY = 1500  # milliseconds
GAP_SIZE_DEFAULT = 150
HIGHSCORE_FILE = "highscore.txt"

class Bird:
    def __init__(self):
        self.width = 30
        self.height = 30
        self.x = 50
        self.y = WINDOW_HEIGHT // 2
        self.velocity = 0
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def flap(self):
        self.velocity = FLAP_STRENGTH

    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity
        self.rect.y = int(self.y)

    def draw(self, screen):
        # Draw bird (yellow circle)
        pygame.draw.circle(screen, YELLOW, (int(self.x + self.width // 2), int(self.y + self.height // 2)), self.width // 2)
        # Draw eye (small black circle)
        eye_x = int(self.x + self.width * 0.7)
        eye_y = int(self.y + self.height * 0.3)
        pygame.draw.circle(screen, BLACK, (eye_x, eye_y), 3)

class Pipe:
    def __init__(self, x, color=GREEN, gap_size=150, outline_color=BLACK):
        self.x = x
        self.width = 70
        self.color = color
        self.outline_color = outline_color
        self.gap_size = gap_size
        self.gap_y = random.randint(100, WINDOW_HEIGHT - 100 - self.gap_size)
        self.top_rect = pygame.Rect(self.x, 0, self.width, self.gap_y)
        self.bottom_rect = pygame.Rect(self.x, self.gap_y + self.gap_size, self.width, WINDOW_HEIGHT - (self.gap_y + self.gap_size))
        self.passed = False

    def update(self):
        self.x -= PIPE_SPEED
        self.top_rect.x = int(self.x)
        self.bottom_rect.x = int(self.x)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.top_rect)
        pygame.draw.rect(screen, self.color, self.bottom_rect)
        # Add a border to pipes
        pygame.draw.rect(screen, self.outline_color, self.top_rect, 2)
        pygame.draw.rect(screen, self.outline_color, self.bottom_rect, 2)

class FlappyBirdGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Flappy Bird Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 32)
        self.bold_font = pygame.font.SysFont("Arial", 32, bold=True)
        self.large_font = pygame.font.SysFont("Arial", 48, bold=True)
        
        # Difficulty Buttons
        button_width = 150
        button_height = 50
        center_x = WINDOW_WIDTH // 2 - button_width // 2
        self.easy_rect = pygame.Rect(center_x, 250, button_width, button_height)
        self.medium_rect = pygame.Rect(center_x, 320, button_width, button_height)
        self.hard_rect = pygame.Rect(center_x, 390, button_width, button_height)
        
        # Back Button
        self.back_rect = pygame.Rect(center_x, 500, button_width, button_height)

        self.high_score = self.load_high_score()
        self.current_gap_size = GAP_SIZE_DEFAULT
        self.current_outline_color = BLACK
        self.reset_game()
        self.in_menu = True
        self.game_started = False
        self.paused = False

    def load_high_score(self):
        if os.path.exists(HIGHSCORE_FILE):
            try:
                with open(HIGHSCORE_FILE, "r") as f:
                    return int(f.read())
            except:
                return 0
        return 0

    def save_high_score(self):
        with open(HIGHSCORE_FILE, "w") as f:
            f.write(str(self.high_score))

    def reset_game(self):
        self.bird = Bird()
        self.pipes = []
        self.score = 0
        self.pipes_spawned = 0
        self.game_over = False
        self.last_pipe_time = pygame.time.get_ticks()
        self.game_started = False
        self.paused = False
        self.new_high_score_achieved = False
        self.high_score_message_timer = 0

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if self.in_menu:
                    if self.easy_rect.collidepoint(mouse_pos):
                        self.current_gap_size = 180
                        self.current_outline_color = BLACK
                        self.in_menu = False
                    elif self.medium_rect.collidepoint(mouse_pos):
                        self.current_gap_size = 150
                        self.current_outline_color = YELLOW
                        self.in_menu = False
                    elif self.hard_rect.collidepoint(mouse_pos):
                        self.current_gap_size = 120
                        self.current_outline_color = RED
                        self.in_menu = False
                elif not self.game_started and not self.game_over:
                    if self.back_rect.collidepoint(mouse_pos):
                        self.in_menu = True
                        self.reset_game()

            if event.type == pygame.KEYDOWN:
                if not self.in_menu:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                        if not self.game_started:
                            self.game_started = True
                        if not self.game_over and not self.paused:
                            self.bird.flap()
                    
                    if event.key == pygame.K_p:
                        if not self.game_over and self.game_started:
                            self.paused = not self.paused
                    
                    if event.key == pygame.K_r:
                        self.reset_game()

    def update(self):
        if self.in_menu or not self.game_started or self.game_over or self.paused:
            return

        # Update bird
        self.bird.update()

        # Check collisions with ground and ceiling
        if self.bird.rect.top < 0 or self.bird.rect.bottom > WINDOW_HEIGHT - 50:
            self.game_over = True

        # Generate pipes
        current_time = pygame.time.get_ticks()
        if current_time - self.last_pipe_time > PIPE_FREQUENCY:
            self.pipes_spawned += 1
            color = BLUE if self.pipes_spawned % 10 == 0 else GREEN
            self.pipes.append(Pipe(WINDOW_WIDTH, color, self.current_gap_size, self.current_outline_color))
            self.last_pipe_time = current_time

        # Update pipes
        for pipe in self.pipes[:]:
            pipe.update()
            
            # Check collisions with pipes
            if self.bird.rect.colliderect(pipe.top_rect) or self.bird.rect.colliderect(pipe.bottom_rect):
                self.game_over = True

            # Scoring
            if not pipe.passed and pipe.x + pipe.width < self.bird.x:
                pipe.passed = True
                self.score += 1
                
                # Check for new high score
                if self.score > self.high_score:
                    if not self.new_high_score_achieved:
                        self.new_high_score_achieved = True
                        self.high_score_message_timer = 120 # Show for 2 seconds at 60 FPS
                    self.high_score = self.score
                    self.save_high_score()
            
            # Remove off-screen pipes
            if pipe.x + pipe.width < 0:
                self.pipes.remove(pipe)

        # Update high score message timer
        if self.high_score_message_timer > 0:
            self.high_score_message_timer -= 1

    def draw(self):
        # Background
        self.screen.fill(SKY_BLUE)

        if self.in_menu:
            # Draw Title
            title_surface = self.large_font.render("Flappy Bird Python", True, WHITE)
            title_rect = title_surface.get_rect(center=(WINDOW_WIDTH // 2, 150))
            self.screen.blit(title_surface, title_rect)
            
            # Get mouse position for hover effect
            mouse_pos = pygame.mouse.get_pos()
            
            # Draw Buttons
            for rect, text in [(self.easy_rect, "Easy"), (self.medium_rect, "Medium"), (self.hard_rect, "Hard")]:
                # Gray out if hovering
                color = (200, 200, 200) if rect.collidepoint(mouse_pos) else WHITE
                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, BLACK, rect, 2)
                text_surf = self.font.render(text, True, BLACK)
                text_rect = text_surf.get_rect(center=rect.center)
                self.screen.blit(text_surf, text_rect)
            
            pygame.display.flip()
            return

        # Draw pipes
        for pipe in self.pipes:
            pipe.draw(self.screen)

        # Ground
        pygame.draw.rect(self.screen, BROWN, (0, WINDOW_HEIGHT - 50, WINDOW_WIDTH, 50))
        pygame.draw.rect(self.screen, GREEN, (0, WINDOW_HEIGHT - 50, WINDOW_WIDTH, 10))

        # Draw bird
        self.bird.draw(self.screen)

        # Draw score
        score_surface = self.font.render(f"Score: {self.score}", True, WHITE)
        score_rect = score_surface.get_rect(center=(WINDOW_WIDTH // 2, 40))
        self.screen.blit(score_surface, score_rect)

        # Draw high score
        high_score_surface = self.font.render(f"High Score: {self.high_score}", True, WHITE)
        high_score_rect = high_score_surface.get_rect(center=(WINDOW_WIDTH // 2, 75))
        self.screen.blit(high_score_surface, high_score_rect)

        # New High Score Notification (Temporary)
        if self.high_score_message_timer > 0:
            new_record_surface = self.bold_font.render("New High Score!", True, YELLOW)
            new_record_rect = new_record_surface.get_rect(center=(WINDOW_WIDTH // 2, 110))
            self.screen.blit(new_record_surface, new_record_rect)

        # UI Messages
        if not self.game_started and not self.game_over:
            start_surface = self.font.render("Press SPACE to Start", True, WHITE)
            start_rect = start_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            self.screen.blit(start_surface, start_rect)
            
            # Draw Back Button
            mouse_pos = pygame.mouse.get_pos()
            color = (200, 200, 200) if self.back_rect.collidepoint(mouse_pos) else WHITE
            pygame.draw.rect(self.screen, color, self.back_rect)
            pygame.draw.rect(self.screen, BLACK, self.back_rect, 2)
            back_text = self.font.render("Back", True, BLACK)
            back_text_rect = back_text.get_rect(center=self.back_rect.center)
            self.screen.blit(back_text, back_text_rect)
        
        if self.game_over:
            # Semi-transparent overlay for game over
            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            self.screen.blit(overlay, (0, 0))

            # New High Score banner on Game Over
            if self.new_high_score_achieved:
                banner_surface = self.bold_font.render("NEW HIGH SCORE!", True, YELLOW)
                banner_rect = banner_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 100))
                self.screen.blit(banner_surface, banner_rect)

            over_surface = self.large_font.render("GAME OVER", True, WHITE)
            over_rect = over_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 30))
            self.screen.blit(over_surface, over_rect)

            final_score_surface = self.font.render(f"Score: {self.score}", True, WHITE)
            final_score_rect = final_score_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 20))
            self.screen.blit(final_score_surface, final_score_rect)

            final_high_surface = self.font.render(f"High Score: {self.high_score}", True, WHITE)
            final_high_rect = final_high_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 60))
            self.screen.blit(final_high_surface, final_high_rect)

            restart_surface = self.font.render("Press 'R' to Restart", True, WHITE)
            restart_rect = restart_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 110))
            self.screen.blit(restart_surface, restart_rect)

        if self.paused:
            pause_surface = self.large_font.render("PAUSED", True, WHITE)
            pause_rect = pause_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            self.screen.blit(pause_surface, pause_rect)

        pygame.display.flip()

    def run(self):
        while True:
            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = FlappyBirdGame()
    game.run()
