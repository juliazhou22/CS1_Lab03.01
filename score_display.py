import pygame


class HighScoreScreen:
    """Screen for displaying and entering high scores"""

    def __init__(self, screen, high_score_manager):
        """Initialize the high score screen

        Args:
            screen: Pygame display surface
            high_score_manager: HighScoreManager instance
        """
        self.screen = screen
        self.high_score_manager = high_score_manager
        self.font_large = pygame.font.SysFont('Arial', 48)
        self.font_medium = pygame.font.SysFont('Arial', 36)
        self.font_small = pygame.font.SysFont('Arial', 24)

        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.IKEA_BLUE = (12, 110, 183)
        self.IKEA_YELLOW = (255, 215, 0)

        # Name entry variables
        self.entering_name = False
        self.player_name = ""
        self.current_score = 0
        self.name_entered = False
        self.cursor_visible = True
        self.cursor_timer = 0

    def show_high_scores(self):
        """Display the high scores screen

        Returns:
            bool: True if user wants to return to main menu, False otherwise
        """
        clock = pygame.time.Clock()
        done = False

        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False  # Exit game

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                        done = True  # Return to main menu

            # Draw high scores screen
            self.screen.fill(self.IKEA_BLUE)

            # Title
            title = self.font_large.render("HIGH SCORES", True, self.IKEA_YELLOW)
            title_rect = title.get_rect(center=(self.screen.get_width() // 2, 80))
            self.screen.blit(title, title_rect)

            # Scores
            scores = self.high_score_manager.get_scores()
            if scores:
                for i, (name, score) in enumerate(scores):
                    # Rank
                    rank_text = self.font_small.render(f"{i + 1}.", True, self.WHITE)
                    self.screen.blit(rank_text, (250, 150 + i * 40))

                    # Name
                    name_text = self.font_small.render(name, True, self.WHITE)
                    self.screen.blit(name_text, (300, 150 + i * 40))

                    # Score
                    score_text = self.font_small.render(str(score), True, self.WHITE)
                    self.screen.blit(score_text, (500, 150 + i * 40))
            else:
                no_scores = self.font_medium.render("No high scores yet!", True, self.WHITE)
                no_scores_rect = no_scores.get_rect(center=(self.screen.get_width() // 2, 250))
                self.screen.blit(no_scores, no_scores_rect)

            # Instructions
            instructions = self.font_small.render("Press ENTER or ESC to return", True, self.WHITE)
            instructions_rect = instructions.get_rect(center=(self.screen.get_width() // 2, 550))
            self.screen.blit(instructions, instructions_rect)

            pygame.display.flip()
            clock.tick(60)

        return True  # Return to main menu

    def show_name_entry(self, score):
        """Show screen for entering player name when achieving a high score

        Args:
            score (int): Player's score

        Returns:
            str: Player's name
        """
        self.entering_name = True
        self.player_name = ""
        self.current_score = score
        self.name_entered = False
        self.cursor_visible = True
        self.cursor_timer = 0

        clock = pygame.time.Clock()

        while self.entering_name:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # If player quits, save with default name
                    self.player_name = "Player" if not self.player_name else self.player_name
                    self.entering_name = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        # Finish name entry if name is not empty
                        if self.player_name:
                            self.name_entered = True
                            self.entering_name = False
                    elif event.key == pygame.K_BACKSPACE:
                        # Remove last character
                        self.player_name = self.player_name[:-1]
                    elif event.key == pygame.K_ESCAPE:
                        # Cancel and use default name
                        self.player_name = "Player"
                        self.entering_name = False
                    else:
                        # Add character (limit to 12 characters)
                        if len(self.player_name) < 12 and event.unicode.isprintable():
                            self.player_name += event.unicode

            # Draw name entry screen
            self.screen.fill(self.IKEA_BLUE)

            # Title
            title = self.font_large.render("HIGH SCORE!", True, self.IKEA_YELLOW)
            title_rect = title.get_rect(center=(self.screen.get_width() // 2, 100))
            self.screen.blit(title, title_rect)

            # Score display
            score_text = self.font_medium.render(f"Your score: {self.current_score}", True, self.WHITE)
            score_rect = score_text.get_rect(center=(self.screen.get_width() // 2, 180))
            self.screen.blit(score_text, score_rect)

            # Name entry prompt
            prompt = self.font_medium.render("Enter your name:", True, self.WHITE)
            prompt_rect = prompt.get_rect(center=(self.screen.get_width() // 2, 250))
            self.screen.blit(prompt, prompt_rect)

            # Name entry box
            pygame.draw.rect(self.screen, self.WHITE, (250, 300, 300, 50), 2)

            # Entered name
            name_text = self.font_medium.render(self.player_name, True, self.WHITE)
            name_rect = name_text.get_rect(midleft=(260, 325))
            self.screen.blit(name_text, name_rect)

            # Blinking cursor
            self.cursor_timer += 1
            if self.cursor_timer >= 30:
                self.cursor_visible = not self.cursor_visible
                self.cursor_timer = 0

            if self.cursor_visible:
                cursor_x = 260 + name_rect.width + 2
                pygame.draw.line(self.screen, self.WHITE, (cursor_x, 310), (cursor_x, 340), 2)

            # Instructions
            instructions = self.font_small.render("Press ENTER when done", True, self.WHITE)
            instructions_rect = instructions.get_rect(center=(self.screen.get_width() // 2, 380))
            self.screen.blit(instructions, instructions_rect)

            pygame.display.flip()
            clock.tick(60)

        # If player didn't enter a name, use default
        if not self.player_name:
            self.player_name = "Player"

        return self.player_name