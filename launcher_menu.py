from dataclasses import dataclass
from typing import Callable, List, Optional, Sequence, Tuple

import pygame
import sys

from games.connect_four import ConnectFourGame
from games.othello import OthelloGame
from games.tic_tac_toe import TicTacToeGame
from utils.assets import load_image


@dataclass(frozen=True)
class GameEntry:
    name: str
    factory: Optional[Callable[[], object]]
    icon: Optional[str] = None
    enabled: bool = True
    subtitle: Optional[str] = None


@dataclass
class Button:
    entry: GameEntry
    rect: pygame.Rect
    icon_surface: Optional[pygame.Surface]


DEFAULT_GAMES: Tuple[GameEntry, ...] = (
    GameEntry("Tic Tac Toe", TicTacToeGame, "icon_tictactoe.png"),
    GameEntry("Othello", OthelloGame, "icon_othello.png"),
    GameEntry("Connect Four", ConnectFourGame, "icon_connectfour.png"),
    GameEntry("Game 4", None, enabled=False, subtitle="Coming Soon"),
    GameEntry("Game 5", None, enabled=False, subtitle="Coming Soon"),
)


class GameLauncher:
    WIDTH, HEIGHT = 1600, 900

    BUTTON_WIDTH = 420
    BUTTON_HEIGHT = 160
    BUTTON_SPACING_X = 80
    BUTTON_SPACING_Y = 60
    BUTTON_TOP = 320
    BUTTON_COLUMNS = 3

    def __init__(self, games: Sequence[GameEntry] | None = None):
        pygame.init()

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
        self.DISABLED_COLOR = (140, 140, 140)

        # Fonts
        self.FONT_TITLE = pygame.font.Font(None, 88)
        self.FONT_SUBTITLE = pygame.font.Font(None, 42)
        self.FONT_BUTTON = pygame.font.Font(None, 48)
        self.FONT_SMALL = pygame.font.Font(None, 28)
        self.FONT_COMING_SOON = pygame.font.Font(None, 26)
        self.FONT_FOOTER = pygame.font.Font(None, 24)

        # Static text surfaces so we do not recreate them every frame
        self.TEXT_SURFACES = {
            "title": self.FONT_TITLE.render("FH Aachen Game Portal", True, self.BLACK),
            "subtitle": self.FONT_SUBTITLE.render("Robot Interactive Games", True, self.DARK_GRAY),
            "instruction": self.FONT_SMALL.render("Select a game to play with the robot", True, self.DARK_GRAY),
            "coming_soon": self.FONT_COMING_SOON.render("Coming Soon", True, self.LIGHT_GRAY),
            "footer": self.FONT_FOOTER.render("Powered by FH Aachen @2025", True, self.DARK_GRAY),
        }

        self.games: Sequence[GameEntry] = games if games is not None else DEFAULT_GAMES
        self.buttons: List[Button] = self._build_buttons()
        self.logo = self._load_logo()

        self.clock = pygame.time.Clock()
        self.hovered_button: Optional[int] = None

    def _load_logo(self) -> Optional[pygame.Surface]:
        try:
            return load_image("logo.jpg", size=(400, 150), convert_alpha=False)
        except Exception as exc:
            print(f"Could not load logo: {exc}")
            return None

    def _compute_button_position(self, index: int) -> Tuple[int, int]:
        row = index // self.BUTTON_COLUMNS
        col = index % self.BUTTON_COLUMNS

        buttons_remaining = len(self.games) - row * self.BUTTON_COLUMNS
        buttons_in_row = min(self.BUTTON_COLUMNS, buttons_remaining)

        row_width = (
            buttons_in_row * self.BUTTON_WIDTH
            + max(0, buttons_in_row - 1) * self.BUTTON_SPACING_X
        )
        row_start_x = (self.WIDTH - row_width) // 2

        x = row_start_x + col * (self.BUTTON_WIDTH + self.BUTTON_SPACING_X)
        y = self.BUTTON_TOP + row * (self.BUTTON_HEIGHT + self.BUTTON_SPACING_Y)
        return x, y

    def _build_buttons(self) -> List[Button]:
        buttons: List[Button] = []
        for idx, entry in enumerate(self.games):
            x, y = self._compute_button_position(idx)
            rect = pygame.Rect(x, y, self.BUTTON_WIDTH, self.BUTTON_HEIGHT)

            icon_surface = None
            if entry.icon:
                try:
                    icon_surface = load_image(entry.icon, size=(80, 80))
                except Exception as exc:
                    print(f"Could not load icon for {entry.name}: {exc}")

            buttons.append(Button(entry=entry, rect=rect, icon_surface=icon_surface))
        return buttons

    def _reset_display(self) -> None:
        """Re-create the launcher window after closing a mini game."""
        self.SCREEN = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("FH Aachen Game Portal")

    def _launch_game(self, entry: GameEntry) -> None:
        if not entry.enabled or entry.factory is None:
            return

        print(f"Starting {entry.name}...")
        game_instance = entry.factory()
        game_instance.run_game()
        self._reset_display()

    def _handle_click(self, position: Tuple[int, int]) -> None:
        for idx, button in enumerate(self.buttons):
            if button.rect.collidepoint(position) and button.entry.enabled:
                self._launch_game(button.entry)
                self.hovered_button = idx
                break

    def draw_ui(self) -> None:
        self.SCREEN.fill(self.FH_TURQUOISE)

        title_rect = self.TEXT_SURFACES["title"].get_rect(center=(self.WIDTH // 2, 120))
        subtitle_rect = self.TEXT_SURFACES["subtitle"].get_rect(center=(self.WIDTH // 2, 200))
        instruction_rect = self.TEXT_SURFACES["instruction"].get_rect(center=(self.WIDTH // 2, 250))

        self.SCREEN.blit(self.TEXT_SURFACES["title"], title_rect)
        self.SCREEN.blit(self.TEXT_SURFACES["subtitle"], subtitle_rect)
        self.SCREEN.blit(self.TEXT_SURFACES["instruction"], instruction_rect)

        for idx, button in enumerate(self.buttons):
            rect = button.rect
            entry = button.entry
            is_hovered = self.hovered_button == idx

            shadow_rect = pygame.Rect(rect.x + 6, rect.y + 6, rect.width, rect.height)
            pygame.draw.rect(self.SCREEN, self.DARK_GRAY, shadow_rect, border_radius=15)

            color = self.BUTTON_COLOR if entry.enabled else self.DISABLED_COLOR
            if entry.enabled and is_hovered:
                color = self.BUTTON_HOVER

            pygame.draw.rect(self.SCREEN, color, rect, border_radius=15)

            if entry.enabled and is_hovered:
                pygame.draw.rect(self.SCREEN, self.WHITE, rect, width=4, border_radius=15)

            text_color = self.WHITE if entry.enabled else self.LIGHT_GRAY
            label_surface = self.FONT_BUTTON.render(entry.name, True, text_color)

            text_x_offset = 30
            if button.icon_surface:
                icon_pos = (rect.x + 30, rect.centery - 40)
                self.SCREEN.blit(button.icon_surface, icon_pos)
                text_x_offset = 130

            text_x = rect.x + text_x_offset
            text_y = rect.centery - label_surface.get_height() // 2
            self.SCREEN.blit(label_surface, (text_x, text_y))

            if not entry.enabled and entry.subtitle:
                subtitle_surface = self.FONT_COMING_SOON.render(entry.subtitle, True, self.LIGHT_GRAY)
                subtitle_y = text_y + label_surface.get_height()
                self.SCREEN.blit(subtitle_surface, (text_x, subtitle_y))

        if self.logo:
            self.SCREEN.blit(self.logo, (self.WIDTH - 430, self.HEIGHT - 170))

        footer_pos = (30, self.HEIGHT - 40)
        self.SCREEN.blit(self.TEXT_SURFACES["footer"], footer_pos)

        pygame.display.flip()

    def run(self) -> None:
        running = True
        while running:
            mouse_pos = pygame.mouse.get_pos()
            self.hovered_button = None
            for idx, button in enumerate(self.buttons):
                if button.rect.collidepoint(mouse_pos) and button.entry.enabled:
                    self.hovered_button = idx
                    break

            self.draw_ui()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self._handle_click(event.pos)

            self.clock.tick(60)
