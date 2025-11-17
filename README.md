# FH Aachen Game Portal

Game portal written in Python with Pygame for showcasing several turn–based tabletop games that a robot can play with a human opponent. The launcher provides a polished FH Aachen–branded UI that lets you pick between Tic Tac Toe, Othello, and Connect Four, and keeps the window open while embedding each mini game in its own Pygame loop.

## Features
- Modern full-HD launcher with hover states, per-game icons, and “coming soon” placeholders.
- Three playable grid-based games that share one reusable rendering/interaction framework.
- Basic robot/human turn handling with console hooks that can be connected to external hardware.
- Simple asset helper for loading icons and logos from the `assets/` folder.
- Easily extendable: add a new game, icon, and button entry to expose another interaction.

## Repository Layout
- `main.py` – entry point that instantiates the launcher.
- `launcher_menu.py` – UI layout, button handling, and game dispatch.
- `games/` – concrete games plus the shared `BaseGridGame` that renders labeled grids, handles clicks, and exposes helper conversions (pixels↔grid↔algebraic).
- `utils/assets.py` – utilities for locating asset paths inside the repo and loading/scaling images.
- `assets/` – icons and branding images used by the launcher and games.

## Requirements
- Python 3.10+ (tested with CPython, should work on any platform that Pygame supports).
- `pygame>=2.5`.
- A display that can show a 1600×900 window and accepts mouse input.

## Setup
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
pip install --upgrade pip
pip install pygame
```

If you intend to package the dependencies, create a `requirements.txt` with `pygame` so others can `pip install -r requirements.txt`.

## Running the Portal
```bash
python main.py
```

The launcher window opens, showing the list of games. Click a button to start a game. When the game window is closed (via the window close button), the launcher automatically reappears so you can pick another game.

## Game Notes
- **Tic Tac Toe** – Human plays `X`, robot plays `O`. Clicking a free cell places your move; the AI instantly responds with a random legal cell.
- **Othello (Reversi)** – Human plays black (`B`), robot plays white (`W`). Valid moves are indicated by teal dots. The robot chooses moves that flip the most pieces.
- **Connect Four** – Human drops dark discs, robot drops light discs. Click any column to drop a piece to the lowest free row. The AI picks a random valid column.

Each game outputs moves in algebraic notation (e.g., `B3`) to stdout, which you can intercept to drive a robot arm or logging system.

## Customising or Adding Games
1. Create a new class in `games/` that inherits from `BaseGridGame`. Override `draw_game_state` and `handle_player_move`, and add any AI/helper routines you need.
2. Provide an icon (PNG/JPG) in `assets/` sized roughly 80×80 px; larger images can be scaled down by `load_image`.
3. Register the game in `DEFAULT_GAMES` inside `launcher_menu.py` by adding a `GameEntry` with the game name, factory, and icon filename.
4. Optional: set `enabled=False` and a `subtitle="Coming Soon"` to keep placeholders visible without launching unfinished work.

The shared base class gives you:
- Grid rendering with labeled headers and a status bar.
- Coordinate conversions: pixel ↔ (row, col) ↔ algebraic label.
- A consistent 60 FPS loop with `pygame.time.Clock`.

## Assets
All relative paths are resolved against `assets/`. Use `utils.assets.load_image("filename.png", size=(w, h))` to ensure images are loaded with the correct conversion and optional scaling. Store any logos, icons, or additional art here to keep imports tidy and paths predictable.

## Troubleshooting
- **Blank window / missing icons**: ensure the expected image files exist in `assets/` and that the process has permission to read them.
- **Fonts look jagged**: install system fonts or point Pygame to specific `.ttf` files if your OS default is missing; you can replace the `pygame.font.Font(None, size)` calls with explicit font paths.
- **ImportError: No module named pygame**: activate your virtual environment and reinstall `pygame`.

Feel free to adapt the color palette, fonts, and layout to match other branding requirements or to integrate tighter robot communication hooks. Pull requests for new mini games or improved AI opponents are welcome!
