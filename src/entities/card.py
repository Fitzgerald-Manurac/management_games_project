"""Card para sa Memory Match."""

import pygame

from settings import (BAD, DARK, DEF_COLOR, GOOD, MEMORY_FLIP_MS, MUTED,
                      PANEL, TERM_COLOR, TEXT)
from utils.helpers import draw_wrapped, get_font, wrap_text


class Card:
    def __init__(self, rect, pair_id, kind, text, label=""):
        self.rect = pygame.Rect(rect)
        self.pair_id = pair_id
        self.kind = kind  # "term" o "def"
        self.text = text
        self.label = label
        self.face_up = False
        self.matched = False
        self.wrong = False
        self.anim = 0.0  # 0 = nakataob, 1 = nakaharap

    # ---------- animation ----------

    def update(self, dt):
        target = 1.0 if (self.face_up or self.matched) else 0.0
        if self.anim == target:
            return
        step = dt / max(1, MEMORY_FLIP_MS)
        if target > self.anim:
            self.anim = min(target, self.anim + step)
        else:
            self.anim = max(target, self.anim - step)

    @property
    def showing_front(self):
        return self.anim >= 0.5

    # ---------- drawing ----------

    def fit_font(self, body):
        """Piliin ang pinakamalaking font na kasya pa ang buong text sa card."""
        bold = self.kind == "term"
        sizes = (23, 21, 19, 17) if bold else (17, 16, 15, 14, 13)
        for size in sizes:
            font = get_font(size, bold)
            lines = wrap_text(self.text, font, body.width)
            height = (font.get_linesize() + 4) * len(lines) - 4
            if height <= body.height:
                return font
        return get_font(sizes[-1], bold)

    def colors(self):
        if self.matched:
            return GOOD, TEXT, (214, 245, 216)
        if self.showing_front:
            bg = TERM_COLOR if self.kind == "term" else DEF_COLOR
            return bg, DARK, (BAD if self.wrong else (252, 252, 252))
        return PANEL, MUTED, (62, 84, 106)

    def draw(self, surface):
        # Ang lapad ay lumiliit hanggang sa gitna ng flip para parang bumabaliktad.
        scale = abs(self.anim * 2 - 1)
        width = max(6, int(self.rect.width * scale))
        rect = pygame.Rect(0, 0, width, self.rect.height)
        rect.center = self.rect.center

        bg, fg, border = self.colors()
        pygame.draw.rect(surface, (10, 20, 30), rect.move(0, 5), border_radius=12)
        pygame.draw.rect(surface, bg, rect, border_radius=12)
        pygame.draw.rect(surface, border, rect, 3 if (self.wrong or self.matched) else 2, border_radius=12)

        if width < self.rect.width * 0.8:
            return  # masyadong siksik pa ang card para basahin ang laman

        if self.showing_front:
            tag = "TERM" if self.kind == "term" else "DEFINITION"
            tag_img = get_font(13, True).render(tag, True, fg)
            surface.blit(tag_img, tag_img.get_rect(midtop=(rect.centerx, rect.y + 7)))
            body = pygame.Rect(rect.x + 12, rect.y + 28, rect.width - 24, rect.height - 40)
            draw_wrapped(surface, self.text, self.fit_font(body), fg, body)
            if self.matched:
                check = get_font(15, True).render("OK", True, fg)
                surface.blit(check, check.get_rect(topright=(rect.right - 10, rect.y + 7)))
        else:
            img = get_font(40, True).render("?", True, fg)
            surface.blit(img, img.get_rect(center=rect.center))
            if self.label:
                lab = get_font(15, True).render(self.label, True, (118, 142, 166))
                surface.blit(lab, lab.get_rect(bottomright=(rect.right - 10, rect.bottom - 8)))
