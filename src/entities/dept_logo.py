"""Sariling vector logo (badge) para sa bawat departamento.

Walang image files na kailangan - iginuguhit lahat gamit ang pygame.draw,
kaya gumagana ito kahit naka-bundle sa exe.
"""

import math

import pygame

GLYPH = (255, 255, 255)

DEPT_COLORS = {
    "Sales and Marketing": (235, 145, 60),
    "Finance": (46, 160, 110),
    "Operations": (70, 130, 200),
    "Human Resources": (168, 110, 205),
    "Information Technology": (38, 122, 150),
}

FALLBACK_COLOR = (96, 110, 130)


def _point(rect, fx, fy):
    return (rect.x + rect.w * fx, rect.y + rect.h * fy)


def _rect(rect, fx, fy, fw, fh):
    return pygame.Rect(
        round(rect.x + rect.w * fx),
        round(rect.y + rect.h * fy),
        max(1, round(rect.w * fw)),
        max(1, round(rect.h * fh)),
    )


def _megaphone(surface, rect, color):
    """Sales and Marketing: megaphone na may sound waves."""
    pygame.draw.polygon(surface, GLYPH, [
        _point(rect, 0.26, 0.42),
        _point(rect, 0.56, 0.24),
        _point(rect, 0.56, 0.76),
        _point(rect, 0.26, 0.58),
    ])
    pygame.draw.rect(surface, GLYPH, _rect(rect, 0.30, 0.56, 0.10, 0.22), border_radius=2)
    for i, fy in enumerate((0.38, 0.50, 0.62)):
        x1 = 0.64
        x2 = 0.76 if i % 2 == 0 else 0.82
        pygame.draw.line(surface, GLYPH, _point(rect, x1, fy), _point(rect, x2, fy),
                         max(2, rect.w // 16))


def _coins(surface, rect, color):
    """Finance: salansan ng barya."""
    for fy in (0.52, 0.26):
        coin = _rect(rect, 0.22, fy, 0.56, 0.24)
        pygame.draw.ellipse(surface, GLYPH, coin)
        pygame.draw.ellipse(surface, color, coin.inflate(-max(4, rect.w // 5), -max(4, rect.h // 8)))


def _gear(surface, rect, color):
    """Operations: gear/cog."""
    cx, cy = rect.center
    outer = rect.w * 0.40
    inner = rect.w * 0.29
    teeth = 8
    points = []
    for i in range(teeth * 2):
        radius = outer if i % 2 == 0 else inner
        angle = math.pi * i / teeth
        points.append((cx + radius * math.cos(angle), cy + radius * math.sin(angle)))
    pygame.draw.polygon(surface, GLYPH, points)
    pygame.draw.circle(surface, color, (cx, cy), max(2, int(rect.w * 0.13)))


def _person(surface, rect, color):
    """Human Resources: tao (bust)."""
    pygame.draw.circle(surface, GLYPH, _point(rect, 0.5, 0.34), max(2, int(rect.w * 0.15)))
    pygame.draw.rect(surface, GLYPH, _rect(rect, 0.24, 0.54, 0.52, 0.30),
                     border_radius=max(3, rect.w // 4))


def _laptop(surface, rect, color):
    """Information Technology: laptop."""
    screen = _rect(rect, 0.24, 0.26, 0.52, 0.36)
    pygame.draw.rect(surface, GLYPH, screen, border_radius=3)
    pygame.draw.rect(surface, color, screen.inflate(-max(4, rect.w // 8), -max(4, rect.w // 8)))
    pygame.draw.rect(surface, GLYPH, _rect(rect, 0.14, 0.66, 0.72, 0.10), border_radius=3)


DEPT_SHAPES = {
    "Sales and Marketing": _megaphone,
    "Finance": _coins,
    "Operations": _gear,
    "Human Resources": _person,
    "Information Technology": _laptop,
}


def draw_dept_logo(surface, dept, rect):
    """Iguhit ang logo ng `dept` sa loob ng square na `rect`."""
    rect = pygame.Rect(rect)
    color = DEPT_COLORS.get(dept, FALLBACK_COLOR)
    radius = min(rect.w, rect.h) // 2
    pygame.draw.circle(surface, (12, 24, 34), rect.center, radius)
    pygame.draw.circle(surface, color, rect.center, max(1, radius - 2))
    shape = DEPT_SHAPES.get(dept)
    if shape is not None:
        shape(surface, rect, color)
