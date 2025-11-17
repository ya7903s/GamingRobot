from pathlib import Path
from typing import Optional, Tuple

import pygame

# Absolute path to the repository root (one level above this utils package)
BASE_DIR = Path(__file__).resolve().parents[1]
ASSETS_DIR = BASE_DIR / "assets"


def resource_path(*parts: str) -> Path:
    """
    Returns an absolute path inside the repository. Useful when pygame
    requires explicit filesystem locations (e.g. for images/icons).
    """
    return BASE_DIR.joinpath(*parts)


def load_image(
    relative_path: str,
    *,
    size: Optional[Tuple[int, int]] = None,
    convert_alpha: bool = True,
) -> pygame.Surface:
    """
    Loads an image from the assets folder, optionally scales it and applies
    the correct conversion for fast blitting.
    """
    image_path = ASSETS_DIR / relative_path
    image = pygame.image.load(str(image_path))
    image = image.convert_alpha() if convert_alpha else image.convert()

    if size is not None:
        image = pygame.transform.smoothscale(image, size)
    return image


__all__ = ["ASSETS_DIR", "BASE_DIR", "load_image", "resource_path"]
