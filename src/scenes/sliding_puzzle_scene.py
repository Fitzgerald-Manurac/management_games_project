"""Game 4: Sliding Puzzle linked to lesson concepts."""

import random

import pygame

from entities.button import Button
from scenes.base_scene import Scene
from settings import (ACCENT, BG, DARK, GOLD, HEIGHT, MUTED, PANEL,
                      SLIDING_ANIM_MS, SLIDING_BASE_POINTS,
                      SLIDING_BONUS_POINTS, SLIDING_PAR_MOVES,
                      SLIDING_SHUFFLE_MOVES, TEXT, WIDTH)
from utils.data import LESSON_NAMES, MANAGEMENT_SEQUENCE
from utils.helpers import draw_text, draw_wrapped, get_font

TILE_SIZE = 150
TILE_GAP = 14
GRID_X = 48
GRID_Y = 170
GRID_SPAN = TILE_SIZE * 3 + TILE_GAP * 2
PANEL_RECT = pygame.Rect(556, 170, 404, 478)
PLACED_COLOR = (72, 172, 124)


class SlidingPuzzleScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.size = 3
        self.board = list(range(1, self.size * self.size)) + [0]
        self.goal_terms = list(MANAGEMENT_SEQUENCE)
        self.tile_labels = {}
        self.moves = 0
        self.elapsed_ms = 0
        self.solved = False
        self.auto_solved = False
        self.last_points = 0
        self.best_moves = None
        self.anim = None
        self.tile_rects = self._build_rects()
        self.lesson_name = LESSON_NAMES.get(self.game.lesson, "All Lessons (1-4)") if self.game.lesson is not None else "All Lessons (1-4)"

        self.back_btn = Button((WIDTH - 130, 18, 110, 44), "Back", lambda: game.change_scene("menu"), bg=PANEL, fg=TEXT, size=18)
        self.restart_btn = Button((WIDTH - 250, 18, 110, 44), "Shuffle", self.new_puzzle, bg=GOLD, size=18)
        self.auto_btn = Button((WIDTH - 380, 18, 120, 44), "Auto Solve", self.auto_solve, bg=(96, 112, 128), fg=TEXT, size=16)
        self.new_puzzle()

    # ---------- geometry ----------

    def _build_rects(self):
        rects = []
        for idx in range(self.size * self.size):
            row, col = divmod(idx, self.size)
            rects.append(pygame.Rect(GRID_X + col * (TILE_SIZE + TILE_GAP),
                                     GRID_Y + row * (TILE_SIZE + TILE_GAP),
                                     TILE_SIZE, TILE_SIZE))
        return rects

    # ---------- board logic ----------

    def _lesson_terms(self):
        return list(MANAGEMENT_SEQUENCE)

    def _solved_board(self):
        return list(range(1, self.size * self.size)) + [0]

    def _empty_index(self):
        return self.board.index(0)

    def is_solved(self):
        return self.board == self._solved_board()

    def placed_count(self):
        """Ilang tile ang nasa tamang posisyon na."""
        return sum(1 for idx, value in enumerate(self.board) if value and value == idx + 1)

    def is_placed(self, index):
        return bool(self.board[index]) and self.board[index] == index + 1

    def can_move(self, row_or_index, col=None):
        if col is None:
            index = row_or_index
            row, col = divmod(index, self.size)
        else:
            row, col = row_or_index, col

        empty_row, empty_col = divmod(self._empty_index(), self.size)
        return abs(row - empty_row) + abs(col - empty_col) == 1

    def _neighbors(self, index):
        row, col = divmod(index, self.size)
        result = []
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nr, nc = row + dr, col + dc
            if 0 <= nr < self.size and 0 <= nc < self.size:
                result.append(nr * self.size + nc)
        return result

    def award(self):
        """Puntos sa pag-solve: base + bonus kapag kakaunti ang moves."""
        points = SLIDING_BASE_POINTS
        if self.moves <= SLIDING_PAR_MOVES:
            points += SLIDING_BONUS_POINTS
        elif self.moves <= SLIDING_PAR_MOVES * 2:
            points += SLIDING_BONUS_POINTS // 3
        self.last_points = points
        self.game.add_score(points)
        return points

    def move_tile(self, index):
        if self.solved or self.board[index] == 0 or not self.can_move(index):
            return False

        empty_index = self._empty_index()
        self.board[empty_index], self.board[index] = self.board[index], self.board[empty_index]
        self.moves += 1
        self.game.sound.play_click()

        src = self.tile_rects[index]
        dst = self.tile_rects[empty_index]
        self.anim = {"index": empty_index, "dx": src.x - dst.x, "dy": src.y - dst.y, "left": SLIDING_ANIM_MS}

        if self.is_solved():
            self.solved = True
            self.auto_solved = False
            if self.best_moves is None or self.moves < self.best_moves:
                self.best_moves = self.moves
            self.award()
            self.game.sound.play_win()

        return True

    def move_from_direction(self, key):
        """Arrow keys: ang tile na katabi ng gap ang gumagalaw papunta sa gap."""
        empty = self._empty_index()
        row, col = divmod(empty, self.size)
        target = None
        if key in (pygame.K_UP, pygame.K_w) and row < self.size - 1:
            target = empty + self.size
        elif key in (pygame.K_DOWN, pygame.K_s) and row > 0:
            target = empty - self.size
        elif key in (pygame.K_LEFT, pygame.K_a) and col < self.size - 1:
            target = empty + 1
        elif key in (pygame.K_RIGHT, pygame.K_d) and col > 0:
            target = empty - 1
        if target is None:
            return False
        return self.move_tile(target)

    def new_puzzle(self):
        terms = self._lesson_terms()
        self.goal_terms = terms
        self.tile_labels = {i: term for i, term in enumerate(terms, start=1)}

        board = self._solved_board()
        blank = board.index(0)
        previous = None
        for _ in range(SLIDING_SHUFFLE_MOVES):
            options = [i for i in self._neighbors(blank) if i != previous]
            if not options:
                options = self._neighbors(blank)
            swap = random.choice(options)
            board[blank], board[swap] = board[swap], board[blank]
            previous, blank = blank, swap

        self.board = board
        if self.is_solved():
            self.board[0], self.board[1] = self.board[1], self.board[0]

        self.moves = 0
        self.elapsed_ms = 0
        self.solved = False
        self.auto_solved = False
        self.last_points = 0
        self.anim = None

    def auto_solve(self):
        if self.solved:
            return
        self.board = self._solved_board()
        self.moves = 0
        self.solved = True
        self.auto_solved = True
        self.last_points = 0
        self.anim = None
        self.game.sound.play_win()

    # ---------- loop ----------

    def handle_event(self, event):
        if self.back_btn.handle_event(event) or self.restart_btn.handle_event(event) or self.auto_btn.handle_event(event):
            return

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.change_scene("menu")
            elif event.key == pygame.K_r:
                self.new_puzzle()
                self.game.sound.play_click()
            else:
                self.move_from_direction(event.key)
            return

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for idx, rect in enumerate(self.tile_rects):
                if rect.collidepoint(event.pos):
                    if self.board[idx] != 0:
                        self.move_tile(idx)
                    break

    def update(self, dt):
        if not self.solved and self.moves > 0:
            self.elapsed_ms += dt
        if self.anim is not None:
            self.anim["left"] -= dt
            if self.anim["left"] <= 0:
                self.anim = None

    # ---------- drawing ----------

    def time_text(self):
        total = self.elapsed_ms // 1000
        return f"{total // 60:01d}:{total % 60:02d}"

    def _tile_offset(self, index):
        if self.anim is None or self.anim["index"] != index:
            return 0, 0
        t = max(0.0, self.anim["left"] / SLIDING_ANIM_MS)
        return round(self.anim["dx"] * t), round(self.anim["dy"] * t)

    def _draw_goal_panel(self, surface):
        pygame.draw.rect(surface, PANEL, PANEL_RECT, border_radius=14)
        draw_text(surface, "Correct lesson order", get_font(20, True), ACCENT,
                  (PANEL_RECT.x + 18, PANEL_RECT.y + 14))
        draw_text(surface, f"In place: {self.placed_count()}/{len(self.goal_terms)}", get_font(17, True), GOLD,
                  (PANEL_RECT.right - 18, PANEL_RECT.y + 17), "topright")

        row_h = 50
        top = PANEL_RECT.y + 52
        for i, term in enumerate(self.goal_terms):
            value = i + 1
            row = pygame.Rect(PANEL_RECT.x + 14, top + i * row_h, PANEL_RECT.w - 28, row_h - 6)
            done = self.board[value - 1] == value if value - 1 < len(self.board) else False
            pygame.draw.rect(surface, (32, 48, 64) if not done else (34, 70, 58), row, border_radius=8)
            badge = pygame.Rect(row.x + 8, row.centery - 13, 26, 26)
            pygame.draw.rect(surface, PLACED_COLOR if done else ACCENT, badge, border_radius=13)
            draw_text(surface, str(value), get_font(16, True), DARK, badge.center, "center")
            draw_text(surface, term, get_font(18, True), TEXT if done else MUTED,
                      (badge.right + 12, row.centery), "midleft")
            if done:
                draw_text(surface, "OK", get_font(15, True), PLACED_COLOR,
                          (row.right - 12, row.centery), "midright")

    def _draw_overlay(self, surface, title, lines, color):
        panel = pygame.Rect(0, 0, GRID_SPAN - 8, 170)
        panel.center = (GRID_X + GRID_SPAN // 2, GRID_Y + GRID_SPAN // 2)
        overlay = pygame.Surface(panel.size, pygame.SRCALPHA)
        overlay.fill((14, 28, 40, 232))
        surface.blit(overlay, panel)
        pygame.draw.rect(surface, color, panel, 3, border_radius=12)
        draw_text(surface, title, get_font(34, True), color, (panel.centerx, panel.y + 34), "center")
        for i, line in enumerate(lines):
            draw_text(surface, line, get_font(19), TEXT, (panel.centerx, panel.y + 84 + i * 30), "center")

    def draw(self, surface):
        surface.fill(BG)

        draw_text(surface, "Sliding Puzzle", get_font(34, True), ACCENT, (30, 14))
        draw_text(surface, f"Lesson: {self.lesson_name}  -  arrange the concepts in the correct lesson order",
                  get_font(17), MUTED, (30, 54))

        hud = f"Moves: {self.moves}    Time: {self.time_text()}    Score: {self.game.total_score}"
        if self.best_moves is not None:
            hud += f"    Best: {self.best_moves} moves"
        draw_text(surface, hud, get_font(21, True), GOLD, (30, 86))

        self.back_btn.draw(surface)
        self.restart_btn.draw(surface)
        self.auto_btn.draw(surface)

        self._draw_goal_panel(surface)

        for idx, value in enumerate(self.board):
            if value:
                continue
            rect = self.tile_rects[idx]
            pygame.draw.rect(surface, (15, 30, 42), rect, border_radius=18)
            pygame.draw.rect(surface, (28, 46, 62), rect.inflate(-18, -18), border_radius=14)

        for idx, value in enumerate(self.board):
            if not value:
                continue
            rect = self.tile_rects[idx]
            dx, dy = self._tile_offset(idx)
            rect = rect.move(dx, dy)

            if self.is_placed(idx):
                fill, fg = PLACED_COLOR, TEXT
            elif self.can_move(idx) and not self.solved:
                fill, fg = GOLD, DARK
            else:
                fill, fg = ACCENT, TEXT

            pygame.draw.rect(surface, (12, 22, 32), rect.move(0, 8), border_radius=18)
            pygame.draw.rect(surface, fill, rect, border_radius=18)

            badge = pygame.Rect(rect.x + 10, rect.y + 10, 26, 26)
            pygame.draw.rect(surface, (14, 28, 40), badge, border_radius=13)
            draw_text(surface, str(value), get_font(15, True), GOLD, badge.center, "center")

            label = self.tile_labels.get(value, "")
            draw_wrapped(surface, label, get_font(18 if len(label) > 10 else 23, True), fg,
                         rect.inflate(-20, -18), align="center", valign="middle")

        draw_text(surface, "Click a tile beside the gap or use the arrow keys.  R = shuffle, Esc = back.",
                  get_font(16), MUTED, (GRID_X, HEIGHT - 34))

        if self.auto_solved:
            self._draw_overlay(surface, "Auto Solved!",
                               ["No score added for using the shortcut.",
                                "Press Shuffle (or R) to try it yourself."], GOLD)
        elif self.solved:
            lines = [f"Moves: {self.moves}    Time: {self.time_text()}",
                     f"+{self.last_points} points" + (f"  (bonus for {self.moves} moves!)" if self.last_points > SLIDING_BASE_POINTS else "")]
            self._draw_overlay(surface, "Lesson Puzzle Solved!", lines, ACCENT)
