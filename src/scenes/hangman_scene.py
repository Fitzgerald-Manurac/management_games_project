"""Game 3: Hangman."""

import random

import pygame

from entities.button import Button
from entities.hangman_figure import draw_gallows
from scenes.base_scene import Scene
from settings import (ACCENT, BAD, BG, DARK, GOLD, GOOD, HANGMAN_MAX_WRONG,
                      MUTED, PANEL, TEXT, WIDTH)
from utils.data import WORDS, filter_by_lesson
from utils.helpers import draw_text, draw_wrapped, get_font

LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
GALLOWS_RECT = pygame.Rect(30, 130, 260, 300)
WORD_AREA = pygame.Rect(330, 140, 640, 170)
SLOT_W, SLOT_GAP, LINE_H = 28, 4, 58


class HangmanScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.wins = 0
        self.losses = 0
        self.deck = []

        self.back_btn = Button((WIDTH - 130, 18, 110, 44), "Back", lambda: game.change_scene("menu"), bg=PANEL, fg=TEXT, size=20)
        self.next_btn = Button((WIDTH - 290, 18, 145, 44), "Next Word", self.new_word, bg=GOLD, size=20)

        self.keys = {}
        key_w, key_h, gap = 58, 52, 8
        start_x = (WIDTH - (13 * key_w + 12 * gap)) // 2
        for i, ch in enumerate(LETTERS):
            rect = (start_x + (i % 13) * (key_w + gap), 535 + (i // 13) * (key_h + gap), key_w, key_h)
            self.keys[ch] = Button(rect, ch, lambda c=ch: self.guess(c), size=22)

        self.new_word()

    # ---------- game flow ----------
    def new_word(self):
        if not self.deck:
            self.deck = filter_by_lesson(WORDS, self.game.lesson)
            random.shuffle(self.deck)
        self.answer, self.hint, _lesson = self.deck.pop()
        self.guessed = set()
        self.wrong = 0
        self.over = False
        self.lost = False
        for btn in self.keys.values():
            btn.enabled = True
            btn.bg = ACCENT

    def guess(self, ch):
        if self.over or ch in self.guessed or ch not in self.keys:
            return
        self.guessed.add(ch)
        btn = self.keys[ch]
        btn.enabled = False
        if ch in self.answer:
            btn.bg = GOOD
            self.game.sound.play_correct()
        else:
            btn.bg = BAD
            self.wrong += 1
            self.game.sound.play_error()
        self.check_end()

    def check_end(self):
        letters = {c for c in self.answer if c != " "}
        if letters <= self.guessed:
            self.over = True
            self.wins += 1
            self.game.add_score(15)
            self.game.sound.play_win()
        elif self.wrong >= HANGMAN_MAX_WRONG:
            self.over = True
            self.lost = True
            self.losses += 1
            self.game.sound.play_lose()
        if self.over:
            for btn in self.keys.values():
                btn.enabled = False

    # ---------- loop ----------
    def handle_event(self, event):
        if self.back_btn.handle_event(event) or self.next_btn.handle_event(event):
            return
        for btn in self.keys.values():
            if btn.handle_event(event):
                return
        if event.type == pygame.KEYDOWN and event.unicode and event.unicode.isalpha():
            self.guess(event.unicode.upper())

    def draw_word(self, surface):
        x, y = WORD_AREA.x, WORD_AREA.y
        font = get_font(32, True)
        for word in self.answer.split(" "):
            word_w = len(word) * (SLOT_W + SLOT_GAP)
            if x != WORD_AREA.x and x + word_w > WORD_AREA.right:
                x = WORD_AREA.x
                y += LINE_H
            for ch in word:
                if ch in self.guessed:
                    img = font.render(ch, True, TEXT)
                    surface.blit(img, img.get_rect(centerx=x + SLOT_W // 2, y=y))
                elif self.lost:
                    img = font.render(ch, True, GOLD)
                    surface.blit(img, img.get_rect(centerx=x + SLOT_W // 2, y=y))
                pygame.draw.line(surface, MUTED, (x, y + 44), (x + SLOT_W, y + 44), 3)
                x += SLOT_W + SLOT_GAP
            x += SLOT_W  # space sa pagitan ng salita

    def draw(self, surface):
        surface.fill(BG)
        draw_text(surface, "Hangman", get_font(34, True), ACCENT, (30, 14))
        draw_text(surface, f"Wins: {self.wins}    Losses: {self.losses}    Score: {self.game.total_score}", get_font(22, True), GOLD, (30, 78))
        self.back_btn.draw(surface)
        self.next_btn.draw(surface)

        draw_gallows(surface, GALLOWS_RECT, self.wrong)
        self.draw_word(surface)

        draw_wrapped(surface, "Hint: " + self.hint, get_font(20), MUTED, pygame.Rect(330, 330, 640, 70), align="left", valign="top")

        wrong_letters = " ".join(sorted(c for c in self.guessed if c not in self.answer))
        draw_text(surface, f"Lives: {HANGMAN_MAX_WRONG - self.wrong}/{HANGMAN_MAX_WRONG}    Wrong: {wrong_letters}", get_font(22, True), BAD, (330, 410))

        if self.over:
            if self.lost:
                draw_text(surface, f"You lost! The answer was: {self.answer}", get_font(24, True), BAD, (330, 450))
            else:
                draw_text(surface, "You won! Press Next Word.", get_font(24, True), GOOD, (330, 450))

        for btn in self.keys.values():
            btn.draw(surface)
