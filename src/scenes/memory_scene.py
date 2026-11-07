"""Game 1: Memory Match (term <-> definition)."""

import random

import pygame

from entities.button import Button
from entities.card import Card
from scenes.base_scene import Scene
from settings import (ACCENT, BAD, BG, DARK, GOLD, GOOD, MEMORY_COLS,
                      MEMORY_HINT_MS, MEMORY_HINTS, MEMORY_MATCH_POINTS,
                      MEMORY_MISMATCH_DELAY, MEMORY_PAIRS_PER_ROUND,
                      MEMORY_PERFECT_BONUS, MEMORY_PREVIEW_MS,
                      MEMORY_STREAK_BONUS, MEMORY_STREAK_MAX, MUTED, PANEL,
                      TEXT, WIDTH)
from utils.data import MEMORY_PAIRS, filter_by_lesson
from utils.helpers import draw_text, get_font

CARD_W, CARD_H, GAP = 220, 126, 14
GRID_Y = 132
PERFECT_MOVES = MEMORY_PAIRS_PER_ROUND + MEMORY_PAIRS_PER_ROUND // 2


class MemoryScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.back_btn = Button((WIDTH - 130, 18, 110, 44), "Back", lambda: game.change_scene("menu"), bg=PANEL, fg=TEXT, size=20)
        self.restart_btn = Button((WIDTH - 255, 18, 115, 44), "Restart", self.new_round, bg=GOLD, size=20)
        self.hint_btn = Button((WIDTH - 385, 18, 120, 44), "Hint", self.use_hint, bg=ACCENT, fg=DARK, size=20)
        self.best_moves = None
        self.new_round()

    # ---------- round setup ----------

    def new_round(self):
        pool = filter_by_lesson(MEMORY_PAIRS, self.game.lesson)
        if len(pool) < MEMORY_PAIRS_PER_ROUND:
            pool = list(MEMORY_PAIRS)
        count = min(MEMORY_PAIRS_PER_ROUND, len(pool))
        chosen = random.sample(pool, count)
        self.pair_count = count

        data = []
        for i, (term, definition, _lesson) in enumerate(chosen):
            data.append((i, "term", term))
            data.append((i, "def", definition))
        random.shuffle(data)

        grid_w = MEMORY_COLS * CARD_W + (MEMORY_COLS - 1) * GAP
        start_x = (WIDTH - grid_w) // 2
        self.cards = []
        for idx, (pair_id, kind, text) in enumerate(data):
            col, row = idx % MEMORY_COLS, idx // MEMORY_COLS
            rect = (start_x + col * (CARD_W + GAP), GRID_Y + row * (CARD_H + GAP), CARD_W, CARD_H)
            self.cards.append(Card(rect, pair_id, kind, text, label=str(idx + 1)))

        self.open_cards = []
        self.hint_cards = []
        self.lock_timer = 0
        self.hint_timer = 0
        self.preview_timer = MEMORY_PREVIEW_MS
        self.hints_left = MEMORY_HINTS
        self.moves = 0
        self.elapsed = 0
        self.score = 0
        self.streak = 0
        self.best_streak = 0
        self.last_points = 0
        self.won = False
        self.message = "Study the board before it flips over."
        self.message_color = MUTED
        for card in self.cards:
            card.face_up = True
            card.anim = 1.0

    # ---------- gameplay ----------

    @property
    def busy(self):
        """Hindi tumatanggap ng bagong flip habang may preview, hint o mismatch."""
        return self.preview_timer > 0 or self.lock_timer > 0 or self.hint_timer > 0

    def flip(self, card):
        if self.won or self.busy or card.matched or card.face_up:
            return
        card.face_up = True
        self.open_cards.append(card)
        if len(self.open_cards) < 2:
            return

        self.moves += 1
        a, b = self.open_cards
        if a.pair_id == b.pair_id:
            self.on_match(a, b)
        else:
            self.on_mismatch(a, b)

    def on_match(self, a, b):
        a.matched = b.matched = True
        self.open_cards = []
        self.streak += 1
        self.best_streak = max(self.best_streak, self.streak)
        bonus = MEMORY_STREAK_BONUS * min(self.streak - 1, MEMORY_STREAK_MAX)
        points = MEMORY_MATCH_POINTS + bonus
        self.award(points)
        if bonus:
            self.set_message(f"Matched! +{points} (streak x{self.streak})", GOOD)
        else:
            self.set_message(f"Matched! +{points}", GOOD)
        self.game.sound.play_correct()
        if all(c.matched for c in self.cards):
            self.finish_round()

    def on_mismatch(self, a, b):
        a.wrong = b.wrong = True
        self.lock_timer = MEMORY_MISMATCH_DELAY
        self.streak = 0
        self.set_message("Not a pair - read both cards again.", BAD)
        self.game.sound.play_error()

    def finish_round(self):
        self.won = True
        if self.best_moves is None or self.moves < self.best_moves:
            self.best_moves = self.moves
        if self.moves <= PERFECT_MOVES:
            self.award(MEMORY_PERFECT_BONUS)
            self.set_message(f"Round clear! Efficiency bonus +{MEMORY_PERFECT_BONUS}", GOLD)
        else:
            self.set_message("Round clear!", GOLD)
        self.game.sound.play_win()

    def award(self, points):
        self.score += points
        self.last_points = points
        self.game.add_score(points)
        return points

    def set_message(self, text, color):
        self.message = text
        self.message_color = color

    def use_hint(self):
        if self.won or self.busy or self.hints_left <= 0:
            return
        remaining = sorted({c.pair_id for c in self.cards if not c.matched})
        if not remaining:
            return
        for card in self.open_cards:
            card.face_up = False
        self.open_cards = []
        pair_id = random.choice(remaining)
        self.hint_cards = [c for c in self.cards if c.pair_id == pair_id]
        for card in self.hint_cards:
            card.face_up = True
        self.hint_timer = MEMORY_HINT_MS
        self.hints_left -= 1
        self.streak = 0
        self.set_message("Hint shown - the streak bonus resets.", MUTED)
        self.game.sound.play_click()

    def pairs_found(self):
        return sum(1 for c in self.cards if c.matched) // 2

    # ---------- loop ----------

    def handle_event(self, event):
        if self.back_btn.handle_event(event) or self.restart_btn.handle_event(event):
            return
        if self.hint_btn.handle_event(event):
            return
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                self.new_round()
            elif event.key == pygame.K_h:
                self.use_hint()
            elif event.key == pygame.K_ESCAPE:
                self.game.change_scene("menu")
            return
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for card in self.cards:
                if card.rect.collidepoint(event.pos):
                    self.flip(card)
                    break

    def update(self, dt):
        if not self.won and self.preview_timer <= 0:
            self.elapsed += dt

        if self.preview_timer > 0:
            self.preview_timer -= dt
            if self.preview_timer <= 0:
                self.preview_timer = 0
                for card in self.cards:
                    card.face_up = False
                self.set_message(f"Find the {self.pair_count} term and definition pairs.", MUTED)

        if self.lock_timer > 0:
            self.lock_timer -= dt
            if self.lock_timer <= 0:
                self.lock_timer = 0
                for card in self.open_cards:
                    card.face_up = False
                    card.wrong = False
                self.open_cards = []

        if self.hint_timer > 0:
            self.hint_timer -= dt
            if self.hint_timer <= 0:
                self.hint_timer = 0
                for card in self.hint_cards:
                    if not card.matched:
                        card.face_up = False
                self.hint_cards = []

        for card in self.cards:
            card.update(dt)

        self.hint_btn.enabled = not self.won and self.hints_left > 0

    # ---------- drawing ----------

    def draw(self, surface):
        surface.fill(BG)
        draw_text(surface, "Memory Match", get_font(32, True), ACCENT, (30, 12))
        draw_text(surface, "Match each TERM (blue) with its DEFINITION (yellow).", get_font(17), TEXT, (32, 52))

        message = self.message
        if self.preview_timer > 0:
            seconds = int((self.preview_timer + 999) // 1000)
            message = f"Study the board - hiding in {seconds}s"
        draw_text(surface, message, get_font(19, True), self.message_color, (32, 78))

        self.draw_progress(surface, pygame.Rect(32, 108, 520, 12))

        hud = f"Moves: {self.moves}    Pairs: {self.pairs_found()}/{self.pair_count}    Time: {self.elapsed // 1000}s"
        draw_text(surface, hud, get_font(19, True), GOLD, (WIDTH - 20, 70), "topright")
        extra = f"Round: {self.score}    Streak: {self.streak}    Hints: {self.hints_left}"
        if self.best_moves is not None:
            extra += f"    Best: {self.best_moves}"
        draw_text(surface, extra, get_font(18), MUTED, (WIDTH - 20, 96), "topright")

        for card in self.cards:
            card.draw(surface)
        self.hint_btn.draw(surface)
        self.back_btn.draw(surface)
        self.restart_btn.draw(surface)

        draw_text(surface, "Keys: H = hint, R = new round, Esc = back to menu", get_font(15), MUTED, (WIDTH // 2, 700), "center")

        if self.won:
            self.draw_win(surface)

    def draw_progress(self, surface, rect):
        pygame.draw.rect(surface, PANEL, rect, border_radius=6)
        done = self.pairs_found() / max(1, self.pair_count)
        if done > 0:
            filled = pygame.Rect(rect.x, rect.y, max(6, int(rect.width * done)), rect.height)
            pygame.draw.rect(surface, GOOD, filled, border_radius=6)
        pygame.draw.rect(surface, (62, 84, 106), rect, 2, border_radius=6)

    def draw_win(self, surface):
        overlay = pygame.Surface((600, 200), pygame.SRCALPHA)
        overlay.fill((16, 32, 46, 238))
        rect = overlay.get_rect(center=(WIDTH // 2, 360))
        surface.blit(overlay, rect)
        pygame.draw.rect(surface, ACCENT, rect, 3, border_radius=8)
        draw_text(surface, "All Pairs Matched!", get_font(38, True), GOLD, (rect.centerx, rect.y + 42), "center")
        stats = f"Moves: {self.moves}   Time: {self.elapsed // 1000}s   Best streak: x{self.best_streak}"
        draw_text(surface, stats, get_font(22), TEXT, (rect.centerx, rect.y + 96), "center")
        draw_text(surface, f"Round score: {self.score}", get_font(22, True), GOOD, (rect.centerx, rect.y + 132), "center")
        draw_text(surface, "Press Restart or R to play again", get_font(17), MUTED, (rect.centerx, rect.y + 170), "center")
