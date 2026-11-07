"""Drawing ng gallows at ng hangman figure."""

import pygame

from settings import GOLD, PANEL, TEXT


def draw_gallows(surface, rect, wrong):
    pygame.draw.rect(surface, PANEL, rect, border_radius=12)
    ox, oy = rect.x, rect.y

    def p(x, y):
        return (ox + x, oy + y)

    # gallows
    pygame.draw.line(surface, TEXT, p(30, 275), p(230, 275), 5)
    pygame.draw.line(surface, TEXT, p(60, 275), p(60, 30), 5)
    pygame.draw.line(surface, TEXT, p(60, 30), p(160, 30), 5)
    pygame.draw.line(surface, TEXT, p(160, 30), p(160, 60), 4)

    # katawan (isa-isang lalabas bawat mali)
    if wrong >= 1:
        pygame.draw.circle(surface, GOLD, p(160, 85), 25, 4)
    if wrong >= 2:
        pygame.draw.line(surface, GOLD, p(160, 110), p(160, 185), 4)
    if wrong >= 3:
        pygame.draw.line(surface, GOLD, p(160, 125), p(130, 160), 4)
    if wrong >= 4:
        pygame.draw.line(surface, GOLD, p(160, 125), p(190, 160), 4)
    if wrong >= 5:
        pygame.draw.line(surface, GOLD, p(160, 185), p(135, 235), 4)
    if wrong >= 6:
        pygame.draw.line(surface, GOLD, p(160, 185), p(185, 235), 4)
