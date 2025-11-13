import pygame
import random
from .base_game import BaseGridGame # Imports our base class

# ConnectFourGame INHERITS from BaseGridGame
class ConnectFourGame(BaseGridGame):
    
    def __init__(self):
        # --- 1. Call the constructor of the base class ---
        # Connect Four is 6 rows high, 7 columns wide
        super().__init__(rows=6, cols=7, cell_size=100, header_size=50)

        # --- 2. Connect Four specific settings ---
        pygame.display.set_caption("Connect Four (Modular Grid)")
        
        # (Optional: Load an icon if you have one)
        try:
            icon = pygame.image.load("assets/icon_connectfour.png")
            pygame.display.set_icon(icon)
        except Exception as e:
            print(f"Icon 'assets/icon_connectfour.png' not found: {e}")

        # Player Definitions
        self.PLAYER_1 = 'P1' # Human
        self.PLAYER_2 = 'P2' # Robot
        
        # Specific colors (matching your gray theme)
        self.PLAYER_1_COLOR = (70, 70, 70)   # Dark Gray (like X)
        self.PLAYER_2_COLOR = (150, 150, 150) # Light Gray (like O)

        # --- 3. Connect Four game logic ---
        self.BOARD = [[None]*self.COLS for _ in range(self.ROWS)]
        self.CURRENT_PLAYER = self.PLAYER_1
        self.GAME_OVER = False
        self.WINNER = None
        self.STATUS_MESSAGE = "Player 1's turn"

    # --- 5. Specific helper functions ---

    def _is_valid_location(self, col):
        """ Checks if the top cell in the column is free """
        return self.BOARD[0][col] is None

    def _get_next_open_row(self, col):
        """ Finds the lowest free row in a column """
        for r in range(self.ROWS - 1, -1, -1): # From bottom to top
            if self.BOARD[r][col] is None:
                return r
        return -1 # Should not happen if _is_valid_location is used

    def _is_board_full(self):
        """ Checks if the entire board is full """
        for c in range(self.COLS):
            if self._is_valid_location(c):
                return False
        return True

    def check_winner(self, piece):
        """ Checks all 4-in-a-row conditions """
        # Check horizontal
        for c in range(self.COLS - 3):
            for r in range(self.ROWS):
                if all(self.BOARD[r][c+i] == piece for i in range(4)):
                    return True
        # Check vertical
        for c in range(self.COLS):
            for r in range(self.ROWS - 3):
                if all(self.BOARD[r+i][c] == piece for i in range(4)):
                    return True
        # Check positive diagonal (/)
        for c in range(self.COLS - 3):
            for r in range(3, self.ROWS): # Start from row 3 (index) upwards
                if all(self.BOARD[r-i][c+i] == piece for i in range(4)):
                    return True
        # Check negative diagonal (\)
        for c in range(self.COLS - 3):
            for r in range(self.ROWS - 3):
                if all(self.BOARD[r+i][c+i] == piece for i in range(4)):
                    return True
        return False

    def ai_move(self):
        """ Simple AI: Chooses a random valid column """
        if self.GAME_OVER or self.CURRENT_PLAYER != self.PLAYER_2:
            return

        # Find all columns that are not full
        valid_cols = [c for c in range(self.COLS) if self._is_valid_location(c)]
        
        if not valid_cols:
            return # No move possible

        col = random.choice(valid_cols)
        row = self._get_next_open_row(col)
        
        # Make the move
        self.BOARD[row][col] = self.PLAYER_2
        
        algebraic = self._coord_to_algebraic(row, col)
        print(f"[ROBOT] moves to Column {chr(ord('A') + col)} (drops to {algebraic})")

        # Check & switch player
        if self.check_winner(self.PLAYER_2):
            self.GAME_OVER = True
            self.WINNER = self.PLAYER_2
            self.STATUS_MESSAGE = "Robot wins!"
        elif self._is_board_full():
            self.GAME_OVER = True
            self.STATUS_MESSAGE = "It's a draw!"
        else:
            self.CURRENT_PLAYER = self.PLAYER_1
            self.STATUS_MESSAGE = "Player 1's turn"

    # --- 4. Override Base Class Methods ---

    def draw_game_state(self):
        """ Draws the game pieces (circles) """
        
        PIECE_RADIUS = self.CELL_SIZE // 2 - 10 # Radius of the pieces

        for r in range(self.ROWS):
            for c in range(self.COLS):
                # Calculate the pixel position of the cell center
                x_center = self.HEADER_SIZE + c * self.CELL_SIZE + self.CELL_SIZE // 2
                y_center = self.HEADER_SIZE + r * self.CELL_SIZE + self.CELL_SIZE // 2

                piece = self.BOARD[r][c]
                
                # Draw the piece
                if piece == self.PLAYER_1:
                    pygame.draw.circle(self.SCREEN, self.PLAYER_1_COLOR, (x_center, y_center), PIECE_RADIUS)
                elif piece == self.PLAYER_2:
                    pygame.draw.circle(self.SCREEN, self.PLAYER_2_COLOR, (x_center, y_center), PIECE_RADIUS)
        
        # Draw the status message
        self.draw_status_message(self.STATUS_MESSAGE)

    def handle_player_move(self, algebraic_coord, row, col):
        """ 
        Processes the player's click (P1).
        NOTE: 'row' is ignored, only 'col' is important!
        """
        if self.GAME_OVER or self.CURRENT_PLAYER != self.PLAYER_1:
            return # Game over or Robot's turn

        if self._is_valid_location(col):
            # Find the actual row where the piece will land
            drop_row = self._get_next_open_row(col)
            
            # Make the move
            self.BOARD[drop_row][col] = self.PLAYER_1
            
            # Robot-friendly output
            real_algebraic = self._coord_to_algebraic(drop_row, col)
            print(f"[PLAYER] moves to Column {chr(ord('A') + col)} (drops to {real_algebraic})")

            # Check & switch player
            if self.check_winner(self.PLAYER_1):
                self.GAME_OVER = True
                self.WINNER = self.PLAYER_1
                self.STATUS_MESSAGE = "Player 1 wins!"
            elif self._is_board_full():
                self.GAME_OVER = True
                self.STATUS_MESSAGE = "It's a draw!"
            else:
                self.CURRENT_PLAYER = self.PLAYER_2
                self.STATUS_MESSAGE = "Robot's turn..."
                self.ai_move()
        
        else:
            self.STATUS_MESSAGE = "Column is full! Try another."
            print(f"Invalid move: Column {col} is full.")