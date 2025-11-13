import pygame
import random
from .base_game import BaseGridGame # Importiert unsere Basis-Klasse

# OthelloGame ERBT von BaseGridGame
class OthelloGame(BaseGridGame):
    
    def __init__(self):
        # --- 1. Rufe den Konstruktor der Basis-Klasse auf ---
        # Othello ist 8x8. Wir machen die Zellen kleiner.
        super().__init__(rows=8, cols=8, cell_size=80, header_size=50)

        # --- 2. Othello spezifische Einstellungen ---
        pygame.display.set_caption("Othello (Reversi)")
        
        # (Optional: Lade ein Icon, wenn du eines hast)
        try:
            icon = pygame.image.load("assets/icon_othello.png")
            pygame.display.set_icon(icon)
        except Exception as e:
            print(f"Icon not found: {e}")

        # Spieler-Definitionen
        self.PLAYER_B = 'B' # Human (Black)
        self.PLAYER_W = 'W' # Robot (White)
        
        # Spezifische Farben
        self.COLOR_B = (30, 30, 30)   # Dunkles Grau (Schwarz)
        self.COLOR_W = (230, 230, 230) # Helles Grau (Weiß)
        self.COLOR_HINT = (0, 100, 95) # Dunkles Türkis für Zug-Hinweise

        # --- 3. Othello Spiel-Logik ---
        self.BOARD = [[None]*8 for _ in range(8)] # Internes 8x8 Board
        self.setup_start_board()

        self.CURRENT_PLAYER = self.PLAYER_B # Spieler B (Schwarz) beginnt
        self.GAME_OVER = False
        self.WINNER = None
        self.STATUS_MESSAGE = "Player B's turn"
        
        # Wichtig für Othello: Liste der gültigen Züge
        self.VALID_MOVES = []
        self.update_valid_moves() # Finde die ersten Züge

    def setup_start_board(self):
        """ Platziert die 4 Start-Steine in der Mitte """
        self.BOARD[3][3] = self.PLAYER_W
        self.BOARD[3][4] = self.PLAYER_B
        self.BOARD[4][3] = self.PLAYER_B
        self.BOARD[4][4] = self.PLAYER_W

    def _is_on_board(self, r, c):
        """ Prüft, ob eine Koordinate (r, c) auf dem Spielfeld ist """
        return 0 <= r < self.ROWS and 0 <= c < self.COLS

    def _get_pieces_to_flip(self, r, c):
        """ 
        Findet alle Steine, die umgedreht würden, wenn der aktuelle
        Spieler auf (r, c) setzt. Gibt eine leere Liste zurück,
        wenn der Zug ungültig ist.
        """
        if self.BOARD[r][c] is not None or not self._is_on_board(r, c):
            return [] # Feld ist besetzt oder außerhalb

        opponent = self.PLAYER_W if self.CURRENT_PLAYER == self.PLAYER_B else self.PLAYER_B
        
        # Alle 8 Richtungen (N, S, O, W, NO, NW, SO, SW)
        directions = [[0, 1], [1, 0], [0, -1], [-1, 0], 
                      [1, 1], [1, -1], [-1, 1], [-1, -1]]
        
        all_flips = []

        for dr, dc in directions:
            current_flips = []
            cr, cc = r + dr, c + dc # Aktuelle Position

            while self._is_on_board(cr, cc):
                if self.BOARD[cr][cc] == opponent:
                    # Gültiger Gegner-Stein, füge ihn zur temporären Flip-Liste hinzu
                    current_flips.append((cr, cc))
                elif self.BOARD[cr][cc] == self.CURRENT_PLAYER:
                    # Wir haben einen eigenen Stein gefunden, der die Linie schließt
                    if current_flips: # Nur wenn wir vorher Gegner-Steine gefunden haben
                        all_flips.extend(current_flips)
                    break # Diese Richtung ist fertig
                else:
                    # Leeres Feld gefunden, diese Richtung ist ungültig
                    break 
                
                # Gehe einen Schritt weiter in diese Richtung
                cr, cc = cr + dr, cc + dc
        
        return all_flips # Gibt alle Steine zurück, die umgedreht werden

    def update_valid_moves(self):
        """ Aktualisiert die self.VALID_MOVES Liste für den aktuellen Spieler """
        self.VALID_MOVES = []
        for r in range(self.ROWS):
            for c in range(self.COLS):
                if self.BOARD[r][c] is None:
                    if self._get_pieces_to_flip(r, c):
                        self.VALID_MOVES.append((r, c))

    def _end_game(self):
        """ Zählt die Steine und ermittelt den Gewinner """
        self.GAME_OVER = True
        score_b = 0
        score_w = 0
        for r in range(self.ROWS):
            for c in range(self.COLS):
                if self.BOARD[r][c] == self.PLAYER_B:
                    score_b += 1
                elif self.BOARD[r][c] == self.PLAYER_W:
                    score_w += 1
        
        if score_b > score_w:
            self.WINNER = self.PLAYER_B
            self.STATUS_MESSAGE = f"Game Over! Player B wins: {score_b} to {score_w}"
        elif score_w > score_b:
            self.WINNER = self.PLAYER_W
            self.STATUS_MESSAGE = f"Game Over! Robot W wins: {score_w} to {score_b}"
        else:
            self.WINNER = "Draw"
            self.STATUS_MESSAGE = f"Game Over! It's a draw: {score_b} to {score_b}"
        print(self.STATUS_MESSAGE)

    def switch_player(self):
        """ Wechselt den Spieler und prüft auf Zug-Überspringungen / Spiel-Ende """
        self.CURRENT_PLAYER = self.PLAYER_W if self.CURRENT_PLAYER == self.PLAYER_B else self.PLAYER_B
        self.update_valid_moves()

        if not self.VALID_MOVES:
            # Der neue Spieler kann nicht ziehen.
            if self.GAME_OVER: return # Spiel wurde bereits beendet

            print(f"No valid moves for {self.CURRENT_PLAYER}. Skipping turn.")
            self.STATUS_MESSAGE = f"No moves for {self.CURRENT_PLAYER}. Turn skipped."
            
            # Wechsle zurück zum *vorherigen* Spieler, um zu sehen, ob ER ziehen kann
            self.CURRENT_PLAYER = self.PLAYER_W if self.CURRENT_PLAYER == self.PLAYER_B else self.PLAYER_B
            self.update_valid_moves()

            if not self.VALID_MOVES:
                # Keiner kann ziehen. Spiel ist vorbei.
                self._end_game()
            else:
                # Der andere Spieler kann ziehen (z.B. Spieler B kann nicht, Roboter W nicht, Spieler B wieder)
                if self.CURRENT_PLAYER == self.PLAYER_B:
                    self.STATUS_MESSAGE = "Robot had no moves. Player B's turn."
                    # Warten auf Spieler-Input
                else:
                    self.STATUS_MESSAGE = "Player had no moves. Robot's turn."
                    self.ai_move() # KI ist wieder dran
        else:
            # Normaler Zug
            if self.CURRENT_PLAYER == self.PLAYER_B:
                self.STATUS_MESSAGE = "Player B's turn"
            else:
                self.STATUS_MESSAGE = "Robot's turn..."
                self.ai_move() # Rufe die KI auf

    # --- 4. Überschreiben der Basis-Klassen-Methoden ---

    def draw_game_state(self):
        """ 
        Zeichnet den Othello-Spielstand (Steine und Hinweise).
        """
        cell_radius = self.CELL_SIZE // 2 - 8 # Radius der Steine

        for r in range(self.ROWS):
            for c in range(self.COLS):
                # Berechne die Pixel-Position der Zelle
                x_center = self.HEADER_SIZE + c * self.CELL_SIZE + self.CELL_SIZE // 2
                y_center = self.HEADER_SIZE + r * self.CELL_SIZE + self.CELL_SIZE // 2

                # 1. Zeichne die Steine
                piece = self.BOARD[r][c]
                if piece == self.PLAYER_B:
                    pygame.draw.circle(self.SCREEN, self.COLOR_B, (x_center, y_center), cell_radius)
                elif piece == self.PLAYER_W:
                    pygame.draw.circle(self.SCREEN, self.COLOR_W, (x_center, y_center), cell_radius)
                
                # 2. Zeichne Hinweise für den Spieler (nur wenn er dran ist)
                if self.CURRENT_PLAYER == self.PLAYER_B and (r, c) in self.VALID_MOVES:
                    pygame.draw.circle(self.SCREEN, self.COLOR_HINT, (x_center, y_center), cell_radius // 4)
        
        # 3. Zeichne die Status-Nachricht
        self.draw_status_message(self.STATUS_MESSAGE)

    def handle_player_move(self, algebraic_coord, row, col):
        """ 
        Verarbeitet den Klick des Spielers (Spieler B).
        """
        if self.GAME_OVER or self.CURRENT_PLAYER != self.PLAYER_B:
            return # Spiel vorbei oder Roboter ist dran

        if (row, col) not in self.VALID_MOVES:
            self.STATUS_MESSAGE = "Invalid move! Try again."
            print(f"Invalid move: {algebraic_coord}")
            return
        
        # Gültiger Zug
        pieces_to_flip = self._get_pieces_to_flip(row, col)
        
        # 1. Setze den neuen Stein
        self.BOARD[row][col] = self.PLAYER_B
        
        # 2. Drehe die Gegner-Steine um
        for (r_flip, c_flip) in pieces_to_flip:
            self.BOARD[r_flip][c_flip] = self.PLAYER_B

        print(f"[PLAYER] moves to {algebraic_coord}, flips {len(pieces_to_flip)} pieces.")

        # 3. Wechsle zum Roboter
        self.switch_player()

    # --- 5. Othello spezifische KI-Logik ---

    def ai_move(self):
        """ Die Logik für den Roboter-Zug (Spieler W) """
        if self.GAME_OVER or self.CURRENT_PLAYER != self.PLAYER_W:
            return
        
        if not self.VALID_MOVES:
             # Sollte nicht passieren, da switch_player dies abfängt, aber sicher ist sicher
            print("[ROBOT] AI has no moves, but was asked to move.")
            return

        # KI-Strategie: Wähle den Zug, der die meisten Steine umdreht.
        # (Das ist eine einfache "gierige" Strategie)
        best_move = None
        max_flips = -1

        # Gehe alle gültigen Züge durch und bewerte sie
        for (r, c) in self.VALID_MOVES:
            num_flips = len(self._get_pieces_to_flip(r, c))
            if num_flips > max_flips:
                max_flips = num_flips
                best_move = (r, c)
        
        # Wähle den besten Zug (oder einen zufälligen der besten, wenn es mehrere gibt)
        if best_move is None:
            best_move = random.choice(self.VALID_MOVES) # Fallback

        (r, c) = best_move
        pieces_to_flip = self._get_pieces_to_flip(r, c)
        
        # 1. Setze den KI-Stein
        self.BOARD[r][c] = self.PLAYER_W
        
        # 2. Drehe die Gegner-Steine um
        for (r_flip, c_flip) in pieces_to_flip:
            self.BOARD[r_flip][c_flip] = self.PLAYER_W

        algebraic = self._coord_to_algebraic(r, c)
        print(f"[ROBOT] moves to {algebraic}, flips {len(pieces_to_flip)} pieces.")

        # 3. Wechsle zurück zum Spieler
        self.switch_player()