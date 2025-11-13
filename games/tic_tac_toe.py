import pygame
import random
from .base_game import BaseGridGame # Imports our new base class

# TicTacToeGame NOW INHERITS from BaseGridGame
class TicTacToeGame(BaseGridGame):
    
    def __init__(self):
        # --- 1. Call the constructor of the base class ---
        # We define that Tic Tac Toe is 3x3 and has larger cells
        super().__init__(rows=3, cols=3, cell_size=180, header_size=50)

        # --- 2. Tic Tac Toe specific settings ---
        pygame.display.set_caption("Tic Tac Toe (Modular Grid)")
        
        # Load the icon (path is relative to main.py)
        try:
            icon = pygame.image.load("assets/icon_tictactoe.png")
            pygame.display.set_icon(icon)
        except Exception as e:
            print(f"Icon 'assets/icon_tictactoe.png' not found: {e}")

        # Specific colors for X and O
        self.PLAYER_X_COLOR = (70, 70, 70)   # Dark Gray for X
        self.PLAYER_O_COLOR = (150, 150, 150) # Light Gray for O
        
        # Specific fonts
        self.FONT_CELL = pygame.font.Font(None, 170) 

        # --- 3. Tic Tac Toe game logic ---
        self.BOARD = [[None]*3 for _ in range(3)] # Internal 3x3 board
        self.CURRENT_PLAYER = "X"
        self.GAME_OVER = False
        self.WINNER = None

    def _draw_piece(self, piece, r, c):
        """ Helper function: Draws an X or O in the cell (r, c) """
        color = self.PLAYER_X_COLOR if piece == "X" else self.PLAYER_O_COLOR
        text = self.FONT_CELL.render(piece, True, color)
        
        # Calculate the pixel position of the cell (accounting for the header)
        x_center = self.HEADER_SIZE + c * self.CELL_SIZE + self.CELL_SIZE // 2
        y_center = self.HEADER_SIZE + r * self.CELL_SIZE + self.CELL_SIZE // 2
        
        text_rect = text.get_rect(center=(x_center, y_center))
        self.SCREEN.blit(text, text_rect)

    # --- 4. Override Base Class Methods ---

    def draw_game_state(self):
        """ 
        This method IS OVERRIDDEN.
        It draws the specific game state for Tic Tac Toe.
        """
        # Draw all 'X' and 'O' on the board
        for r in range(self.ROWS):
            for c in range(self.COLS):
                if self.BOARD[r][c]:
                    self._draw_piece(self.BOARD[r][c], r, c)

        # Draw the status message (e.g., "X wins!")
        message = ""
        if self.GAME_OVER:
            if self.WINNER:
                message = f"{self.WINNER} wins!"
            elif not any(None in row for row in self.BOARD):
                message = "It's a draw!"
        
        if message:
            # --- KORRIGIERTE ZEILE ---
            self.draw_status_message(message) # Calls the function from the base class

    def handle_player_move(self, algebraic_coord, row, col):
        """ 
        This method IS OVERRIDDEN.
        It processes the Tic Tac Toe logic.
        """
        if self.GAME_OVER or self.CURRENT_PLAYER == "O":
            return # Game over or AI's turn

        if self.BOARD[row][col] is None:
            # --- ROBOT COMMUNICATION (Example) ---
            print(f"[PLAYER] Moving to: {algebraic_coord} (Grid: {row}, {col})")
            
            self.BOARD[row][col] = "X"
            if self.check_winner("X"):
                self.GAME_OVER = True
                self.WINNER = "X"
            elif not any(None in row for row in self.BOARD):
                self.GAME_OVER = True
            else:
                self.CURRENT_PLAYER = "O"
                self.ai_move() # AI's turn immediately

    # --- 5. Tic Tac Toe specific helper functions ---

    def ai_move(self):
        if self.GAME_OVER:
            return

        empty = [(r, c) for r in range(3) for c in range(3) if self.BOARD[r][c] is None]
        if empty:
            r, c = random.choice(empty)
            
            # --- ROBOT COMMUNICATION (Example) ---
            algebraic_coord = self._coord_to_algebraic(r, c) # Uses the function from the base class
            print(f"[ROBOT] Moving to: {algebraic_coord} (Grid: {r}, {c})")

            self.BOARD[r][c] = "O"
            if self.check_winner("O"):
                self.GAME_OVER = True
                self.WINNER = "O"
            elif not any(None in row for row in self.BOARD):
                self.GAME_OVER = True
            else:
                self.CURRENT_PLAYER = "X"

    def check_winner(self, player):
        for row in self.BOARD:
            if all(cell == player for cell in row): return True
        for c in range(3):
            if all(self.BOARD[r][c] == player for r in range(3)): return True
        if all(self.BOARD[i][i] == player for i in range(3)): return True
        if all(self.BOARD[i][2-i] == player for i in range(3)): return True
        return False

    # The 'run_game' method is now completely inherited from BaseGridGame!
    # We don't need to define it here anymore.