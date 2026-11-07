"""Mga helper function para sa text at scramble."""

import random
from functools import lru_cache

import pygame

from settings import FONT_NAMES


@lru_cache(maxsize=None)
def get_font(size, bold=False):
    return pygame.font.SysFont(FONT_NAMES, size, bold=bold)


_mouse_transform = None


def set_mouse_transform(transform):
    """Itakda kung paano iko-convert ang window coords papuntang canvas coords."""
    global _mouse_transform
    _mouse_transform = transform


def mouse_pos():
    """Posisyon ng mouse sa canvas coords (sakto kahit naka-fullscreen o naka-resize)."""
    pos = pygame.mouse.get_pos()
    return _mouse_transform(pos) if _mouse_transform else pos


def wrap_text(text, font, max_width):
    """Hatiin ang text sa maraming lines para kumasya sa max_width."""
    lines = []
    current = ""
    for word in text.split(" "):
        test = word if not current else current + " " + word
        if font.size(test)[0] <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_text(surface, text, font, color, pos, anchor="topleft"):
    img = font.render(text, True, color)
    rect = img.get_rect(**{anchor: pos})
    surface.blit(img, rect)
    return rect


def draw_wrapped(surface, text, font, color, rect, align="center", valign="middle", spacing=4):
    """Mag-draw ng wrapped text sa loob ng rect."""
    lines = wrap_text(text, font, rect.width)
    line_h = font.get_linesize() + spacing
    total = line_h * len(lines) - spacing
    y = rect.y if valign == "top" else rect.y + (rect.height - total) // 2
    for line in lines:
        img = font.render(line, True, color)
        if align == "center":
            r = img.get_rect(centerx=rect.centerx, y=y)
        else:
            r = img.get_rect(x=rect.x, y=y)
        surface.blit(img, r)
        y += line_h


def scramble_phrase(answer):
    """I-scramble ang bawat salita (hindi ginagalaw ang spaces)."""

    def scramble_word(word):
        if len(word) < 4 or len(set(word)) == 1:
            return word
        letters = list(word)
        for _ in range(20):
            random.shuffle(letters)
            if "".join(letters) != word:
                break
        return "".join(letters)

    return " ".join(scramble_word(w) for w in answer.split(" "))
