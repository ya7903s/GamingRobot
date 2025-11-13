import pygame
import sys
from games.tic_tac_toe import TicTacToeGame
from games.othello import OthelloGame 
from games.connect_four import ConnectFourGame # <-- 1. IMPORT ADDED

class GameLauncher:
    def __init__(self):
        pygame.init()
        self.WIDTH, self.HEIGHT = 1600, 900
        self.SCREEN = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("FH Aachen Game Portal")

        # FH Aachen brand colors
        self.FH_TURQUOISE = (0, 166, 160)
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.DARK_GRAY = (40, 40, 40)
        self.LIGHT_GRAY = (230, 230, 230)
        self.BUTTON_COLOR = (0, 130, 125)
        self.BUTTON_HOVER = (0, 190, 180)
        self.DISABLED_COLOR = (150, 150, 150)

        self.FONT_TITLE = pygame.font.Font(None, 88)
        self.FONT_SUB = pygame.font.Font(None, 42)
        self.FONT_BUTTON = pygame.font.Font(None, 48)
        self.FONT_SMALL = pygame.font.Font(None, 28)

        # Game buttons in grid layout
        button_width = 420
        button_height = 160
        spacing_x = 80
        spacing_y = 60
        start_x = (self.WIDTH - (button_width * 3 + spacing_x * 2)) // 2
        start_y = 320

        self.game_buttons = []
        
        # --- 2. GAMES LIST UPDATED ---
        games = [
            {"name": "Tic Tac Toe", "enabled": True, "icon": "assets/icon_tictactoe.png"},
            {"name": "Othello", "enabled": True, "icon": "assets/icon_othello.png"},
            {"name": "Connect Four", "enabled": True, "icon": "assets/icon_connectfour.png"}, # <-- ADDED
            {"name": "Game 4", "enabled": False, "icon": None},
            {"name": "Game 5", "enabled": False, "icon": None},
        ]

        # Create button layout (2 rows: 3 on top, 2 on bottom)
        for i, game in enumerate(games):
            if i < 3:  # First row
                x = start_x + (button_width + spacing_x) * i
                y = start_y
            else:  # Second row (centered)
                # This logic centers the 2 buttons on the second row
                row2_width = button_width * 2 + spacing_x
                row2_start_x = (self.WIDTH - row2_width) // 2
                x = row2_start_x + (button_width + spacing_x) * (i - 3)
                y = start_y + button_height + spacing_y

            rect = pygame.Rect(x, y, button_width, button_height)
            
            # Load icon if available
            icon = None
            if game["icon"]:
                try:
                    icon = pygame.image.load(game["icon"]).convert_alpha()
                    icon = pygame.transform.scale(icon, (80, 80))
                except Exception as e:
                    print(f"Could not load icon for {game['name']}: {e}")

            self.game_buttons.append({
                "rect": rect,
                "name": game["name"],
                "enabled": game["enabled"],
                "icon": icon
            })

        # Load FH Aachen logo
        try:
            self.logo = pygame.image.load("assets/logo.jpg").convert()
            self.logo = pygame.transform.scale(self.logo, (400, 150))
        except Exception as e:
            print(f"Could not load logo: {e}")
            self.logo = None

        self.clock = pygame.time.Clock()
        self.hovered_button = None

    def draw_ui(self):
        self.SCREEN.fill(self.FH_TURQUOISE)

        # Title
        title = self.FONT_TITLE.render("FH Aachen Game Portal", True, self.BLACK)
        self.SCREEN.blit(title, (self.WIDTH//2 - title.get_width()//2, 80))

        # Subtitle with robot arm info
        subtitle = self.FONT_SUB.render("Robot Interactive Games", True, self.DARK_GRAY)
        self.SCREEN.blit(subtitle, (self.WIDTH//2 - subtitle.get_width()//2, 180))

        # Instruction text
        instruction = self.FONT_SMALL.render("Select a game to play with the robot", True, self.DARK_GRAY)
        self.SCREEN.blit(instruction, (self.WIDTH//2 - instruction.get_width()//2, 240))

        # Draw game buttons
        for i, button in enumerate(self.game_buttons):
            rect = button["rect"]
            is_hovered = self.hovered_button == i
            
            # Shadow effect
            shadow_rect = pygame.Rect(rect.x + 6, rect.y + 6, rect.width, rect.height)
            pygame.draw.rect(self.SCREEN, self.DARK_GRAY, shadow_rect, border_radius=15)
            
            # Button background
            if button["enabled"]:
                color = self.BUTTON_HOVER if is_hovered else self.BUTTON_COLOR
            else:
                color = self.DISABLED_COLOR
            
            pygame.draw.rect(self.SCREEN, color, rect, border_radius=15)
            
            # Border highlight on hover
            if is_hovered and button["enabled"]:
                pygame.draw.rect(self.SCREEN, self.WHITE, rect, 4, border_radius=15)
            
            # Icon
            if button["icon"]:
                icon_x = rect.x + 30
                icon_y = rect.centery - 40
                self.SCREEN.blit(button["icon"], (icon_x, icon_y))
                text_x_offset = 130
            else:
                text_x_offset = 30
            
            # Game name
            text_color = self.WHITE if button["enabled"] else self.LIGHT_GRAY
            text = self.FONT_BUTTON.render(button["name"], True, text_color)
            text_x = rect.x + text_x_offset
            text_y = rect.centery - text.get_height()//2
            self.SCREEN.blit(text, (text_x, text_y))
            
            # "Coming Soon" label for disabled games
            if not button["enabled"]:
                small_font = pygame.font.Font(None, 26)
                coming_soon = small_font.render("Coming Soon", True, self.LIGHT_GRAY)
                cs_x = rect.x + text_x_offset
                cs_y = rect.centery + 20
                self.SCREEN.blit(coming_soon, (cs_x, cs_y))

        # FH logo at bottom right
        if self.logo:
            self.SCREEN.blit(self.logo, (self.WIDTH - 430, self.HEIGHT - 170))

        # Footer info
        footer_font = pygame.font.Font(None, 24)
        footer = footer_font.render("Powered by FH Aachen @2025", True, self.DARK_GRAY)
        self.SCREEN.blit(footer, (30, self.HEIGHT - 30))

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            mx, my = pygame.mouse.get_pos()
            
            # Check which button is hovered
            self.hovered_button = None
            for i, button in enumerate(self.game_buttons):
                if button["rect"].collidepoint(mx, my) and button["enabled"]:
                    self.hovered_button = i
                    break
            
            self.draw_ui()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Check button clicks
                    for i, button in enumerate(self.game_buttons):
                        if button["rect"].collidepoint(mx, my) and button["enabled"]:
                            if button["name"] == "Tic Tac Toe":
                                print("Starting Tic Tac Toe...")
                                game = TicTacToeGame()
                                game.run_game()
                                # Return to launcher after game
                                self.SCREEN = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
                                pygame.display.set_caption("FH Aachen Game Portal")
                            
                            elif button["name"] == "Othello":
                                print("Starting Othello...")
                                game = OthelloGame()
                                game.run_game()
                                # Return to launcher after game
                                self.SCREEN = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
                                pygame.display.set_caption("FH Aachen Game Portal")

                            # --- 3. ELIF FOR CONNECT FOUR ADDED ---
                            elif button["name"] == "Connect Four":
                                print("Starting Connect Four...")
                                game = ConnectFourGame()
                                game.run_game()
                                # Return to launcher after game
                                self.SCREEN = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
                                pygame.display.set_caption("FH Aachen Game Portal")

            self.clock.tick(60)