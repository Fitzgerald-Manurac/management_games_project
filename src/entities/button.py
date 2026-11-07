"""Simpleng clickable button."""

import pygame

from settings import ACCENT, DARK, GOLD
from utils.helpers import get_font, mouse_pos


class Button:
    def __init__(self, rect, text, callback, bg=ACCENT, fg=DARK, size=22, hover=GOLD, icon=None):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.callback = callback
        self.bg = bg
        self.fg = fg
        self.size = size
        self.hover_color = hover
        self.enabled = True
        self.icon = icon  # callable(surface, rect) - opsyonal na logo sa kaliwa

    def handle_event(self, event):
        """Return True kapag na-click ang button."""
        if (
            self.enabled
            and event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos)
        ):
            self.callback()
            return True
        return False

    def draw(self, surface):
        hovering = self.enabled and self.rect.collidepoint(mouse_pos())
        color = self.hover_color if hovering else self.bg
        shade = self.rect.move(0, 6)
        pygame.draw.rect(surface, (10, 20, 30), shade, border_radius=10)
        draw_rect = self.rect.copy()
        if hovering:
            draw_rect = self.rect.move(0, -2)
        pygame.draw.rect(surface, color, draw_rect, border_radius=10)
        img = get_font(self.size, True).render(self.text, True, self.fg)
        if self.icon is None:
            surface.blit(img, img.get_rect(center=draw_rect.center))
            return
        box = min(draw_rect.h - 12, draw_rect.w // 4)
        icon_rect = pygame.Rect(0, 0, box, box)
        icon_rect.midleft = (draw_rect.x + 10, draw_rect.centery)
        self.icon(surface, icon_rect)
        text_area = draw_rect.copy()
        text_area.x = icon_rect.right
        text_area.w = draw_rect.right - icon_rect.right - 10
        surface.blit(img, img.get_rect(center=text_area.center))
