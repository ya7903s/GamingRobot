import pygame

class BaseGridGame:
    def __init__(self, rows, cols, cell_size=150, header_size=50):
        # --- Core Grid Parameters ---
        self.ROWS = rows
        self.COLS = cols
        self.CELL_SIZE = cell_size
        self.HEADER_SIZE = header_size

        # --- Derived Sizes ---
        self.BOARD_WIDTH = self.CELL_SIZE * self.COLS
        self.BOARD_HEIGHT = self.CELL_SIZE * self.ROWS
        self.STATUS_HEIGHT = 70 # Space for messages at the bottom

        self.WIDTH = self.BOARD_WIDTH + self.HEADER_SIZE
        self.HEIGHT = self.BOARD_HEIGHT + self.HEADER_SIZE + self.STATUS_HEIGHT

        # --- Pygame Initialization ---
        pygame.init()
        self.SCREEN = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        
        # --- Colors (Professional) ---
        self.COLOR_BG = (0, 166, 160) # FH Turquoise
        self.COLOR_LINE = (0, 0, 0)
        self.COLOR_HEADER_BG = (40, 40, 40)
        self.COLOR_HEADER_TEXT = (255, 255, 255)
        self.COLOR_STATUS_TEXT = (40, 40, 40)

        # --- Fonts ---
        self.FONT_HEADER = pygame.font.Font(None, 40)
        self.FONT_STATUS = pygame.font.Font(None, 45)

        self.clock = pygame.time.Clock()

    def draw_grid_and_headers(self):
        # Full background
        self.SCREEN.fill(self.COLOR_BG)

        # Header backgrounds (top and left)
        pygame.draw.rect(self.SCREEN, self.COLOR_HEADER_BG, (0, 0, self.WIDTH, self.HEADER_SIZE))
        pygame.draw.rect(self.SCREEN, self.COLOR_HEADER_BG, (0, 0, self.HEADER_SIZE, self.HEIGHT))
        
        # Status area background
        status_rect = (0, self.HEIGHT - self.STATUS_HEIGHT, self.WIDTH, self.STATUS_HEIGHT)
        pygame.draw.rect(self.SCREEN, self.COLOR_BG, status_rect) # Turquoise

        # Letters (Column Headers: A, B, C...)
        for c in range(self.COLS):
            text = self.FONT_HEADER.render(chr(ord('A') + c), True, self.COLOR_HEADER_TEXT)
            x_pos = self.HEADER_SIZE + c * self.CELL_SIZE + self.CELL_SIZE // 2
            text_rect = text.get_rect(center=(x_pos, self.HEADER_SIZE // 2))
            self.SCREEN.blit(text, text_rect)

        # Numbers (Row Headers: 1, 2, 3...)
        for r in range(self.ROWS):
            text = self.FONT_HEADER.render(str(r + 1), True, self.COLOR_HEADER_TEXT)
            y_pos = self.HEADER_SIZE + r * self.CELL_SIZE + self.CELL_SIZE // 2
            text_rect = text.get_rect(center=(self.HEADER_SIZE // 2, y_pos))
            self.SCREEN.blit(text, text_rect)

        # Draw grid lines
        grid_start_x, grid_start_y = self.HEADER_SIZE, self.HEADER_SIZE
        # Horizontal lines
        for r in range(self.ROWS + 1):
            y = grid_start_y + r * self.CELL_SIZE
            pygame.draw.line(self.SCREEN, self.COLOR_LINE, (grid_start_x, y), (self.WIDTH, y), 3)
        # Vertical lines
        for c in range(self.COLS + 1):
            x = grid_start_x + c * self.CELL_SIZE
            pygame.draw.line(self.SCREEN, self.COLOR_LINE, (x, grid_start_y), (x, self.HEIGHT - self.STATUS_HEIGHT), 3)

    def _pixel_to_coord(self, x, y):
        """ Converts pixels (x, y) to grid coordinates (row, col) """
        # Check if the click is inside the grid (not in the header)
        if x < self.HEADER_SIZE or y < self.HEADER_SIZE or y > (self.HEIGHT - self.STATUS_HEIGHT):
            return None, None

        # Calculate grid position
        row = (y - self.HEADER_SIZE) // self.CELL_SIZE
        col = (x - self.HEADER_SIZE) // self.CELL_SIZE

        # Ensure coordinates are within the valid range
        if 0 <= row < self.ROWS and 0 <= col < self.COLS:
            return row, col
        
        return None, None

    def _coord_to_algebraic(self, row, col):
        """ Converts grid coordinates (row, col) to 'A1', 'B2' etc. """
        if row is None or col is None:
            return None
        col_letter = chr(ord('A') + col)
        row_number = str(row + 1)
        return f"{col_letter}{row_number}"

    def draw_status_message(self, message):
        """ Draws a message in the bottom status area """
        text = self.FONT_STATUS.render(message, True, self.COLOR_STATUS_TEXT)
        text_rect = text.get_rect(center=(self.WIDTH // 2, self.HEIGHT - self.STATUS_HEIGHT // 2))
        self.SCREEN.blit(text, text_rect)

    # --- Methods that MUST be overridden by child classes (e.g., TicTacToe) ---

    def draw_game_state(self):
        """ *MUST BE OVERRIDDEN* Draws the specific game state (X, O, etc.) """
        raise NotImplementedError("This method must be implemented by the child class.")

    def handle_player_move(self, algebraic_coord, row, col):
        """ *MUST BE OVERRIDDEN* Processes the player's click """
        raise NotImplementedError("This method must be implemented by the child class.")

    # --- Main Game Loop ---

    def run_game(self):
        running = True
        while running:
            # Event handling
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    running = False # Only quits this game, returns to the launcher
                
                if e.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    row, col = self._pixel_to_coord(x, y)
                    
                    if row is not None:
                        algebraic_coord = self._coord_to_algebraic(row, col)
                        # Calls the specific logic of the child game
                        self.handle_player_move(algebraic_coord, row, col)

            # Drawing
            self.draw_grid_and_headers()
            self.draw_game_state() # Calls the specific drawing method of the child game
            
            pygame.display.flip()
            self.clock.tick(60)