"""Game 2: Word Scramble."""

import random

import pygame

from entities.button import Button
from scenes.base_scene import Scene
from settings import (ACCENT, BAD, BG, GOLD, GOOD, MUTED, PANEL, SCRAMBLE_CORRECT_POINTS,
                      SCRAMBLE_HINT_POINTS, SCRAMBLE_ROUNDS, TEXT, WIDTH)
from utils.data import WORDS, filter_by_lesson
from utils.helpers import draw_text, draw_wrapped, get_font, scramble_phrase

INPUT_RECT = pygame.Rect(200, 380, 600, 64)


class ScrambleScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        cx = WIDTH // 2
        self.back_btn = Button((WIDTH - 130, 18, 110, 44), "Back", lambda: game.change_scene("menu"), bg=PANEL, fg=TEXT, size=20)
        self.restart_btn = Button((WIDTH - 255, 18, 115, 44), "Restart", self.start, bg=GOLD, size=20)
        self.submit_btn = Button((cx - 190, 470, 190, 52), "Submit", self.check, size=22)
        self.skip_btn = Button((cx + 20, 470, 190, 52), "Skip", self.skip, bg=PANEL, fg=TEXT, size=22)
        self.buttons = [self.back_btn, self.restart_btn, self.submit_btn, self.skip_btn]
        self.start()

    # ---------- game flow ----------
    def start(self):
        pool = filter_by_lesson(WORDS, self.game.lesson)
        random.shuffle(pool)
        self.queue = pool[:SCRAMBLE_ROUNDS]
        self.index = -1
        self.score = 0
        self.correct = 0
        self.finished = False
        self.advance_timer = 0
        self.next_word()

    def next_word(self):
        self.index += 1
        if self.index >= len(self.queue):
            self.finished = True
            return
        self.answer, self.hint, _lesson = self.queue[self.index]
        self.scrambled = scramble_phrase(self.answer)
        self.input_text = ""
        self.feedback = ""
        self.feedback_color = TEXT
        self.points = SCRAMBLE_CORRECT_POINTS
        self.advance_timer = 0

    def locked(self):
        return self.finished or self.advance_timer > 0

    def check(self):
        guess = " ".join(self.input_text.upper().split())
        if self.locked() or not guess:
            return
        if guess == self.answer:
            self.correct += 1
            self.game.add_score(self.points)
            self.game.sound.play_correct()
            self.feedback = f"Correct! +{self.points} points"
            self.feedback_color = GOOD
            self.advance_timer = 900
        else:
            self.feedback = "Wrong, try again!"
            self.feedback_color = BAD
            self.game.sound.play_error()

    def skip(self):
        if self.locked():
            return
        self.feedback = f"Answer: {self.answer}"
        self.feedback_color = GOLD
        self.advance_timer = 1600

    # ---------- loop ----------
    def handle_event(self, event):
        for btn in self.buttons:
            if btn.handle_event(event):
                return
        if event.type == pygame.KEYDOWN and not self.locked():
            if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                self.check()
            elif event.key == pygame.K_BACKSPACE:
                self.input_text = self.input_text[:-1]
            elif event.unicode and (event.unicode.isalpha() or event.unicode == " ") and len(self.input_text) < 30:
                self.input_text += event.unicode

    def update(self, dt):
        if self.advance_timer > 0:
            self.advance_timer -= dt
            if self.advance_timer <= 0:
                self.advance_timer = 0
                self.next_word()

    def draw(self, surface):
        surface.fill(BG)
        draw_text(surface, "Word Scramble", get_font(34, True), ACCENT, (30, 14))
        for btn in self.buttons:
            btn.draw(surface)

        if self.finished:
            draw_text(surface, "GAME OVER!", get_font(56, True), GOLD, (WIDTH // 2, 230), "center")
            draw_text(surface, f"Correct answers: {self.correct}/{len(self.queue)}", get_font(34, True), TEXT, (WIDTH // 2, 320), "center")
            draw_text(surface, f"Total score: {self.game.total_score}", get_font(26, True), GOLD, (WIDTH // 2, 370), "center")
            draw_text(surface, "Press Restart to play again", get_font(20), MUTED, (WIDTH // 2, 430), "center")
            return

        status = f"Word {self.index + 1}/{len(self.queue)}    Correct: {self.correct}    Score: {self.game.total_score}"
        draw_text(surface, status, get_font(22, True), GOLD, (WIDTH // 2, 100), "center")

        draw_wrapped(surface, self.scrambled, get_font(48, True), TEXT, pygame.Rect(60, 150, WIDTH - 120, 90))
        draw_wrapped(surface, "Hint: " + self.hint, get_font(21), MUTED, pygame.Rect(180, 245, WIDTH - 360, 80))

        pygame.draw.rect(surface, TEXT, INPUT_RECT, border_radius=10)
        shown = self.input_text.upper()
        if (pygame.time.get_ticks() // 500) % 2 == 0 and not self.locked():
            shown += "|"
        draw_text(surface, shown, get_font(30, True), (16, 32, 46), INPUT_RECT.center, "center")

        draw_wrapped(surface, self.feedback, get_font(26, True), self.feedback_color, pygame.Rect(100, 545, WIDTH - 200, 80))
